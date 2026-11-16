"""The C++ client library, driven by rtma_test_client (test_client.cpp).

Most tests run it against both managers. A few run it against FakeManager, a
scripted stand-in, for what a real manager doesn't do on demand, such as
sending another module's ACK first. pyrtma's client is the reference.
"""

from __future__ import annotations

import os
import socket
import struct
import subprocess
import threading
import time

import pytest

from conftest import CLIENT_BIN, free_port
from rtma_raw import (
    HEADER,
    MT_ACKNOWLEDGE,
    MT_HELLO,
    MT_MODULE_READY,
    Header,
    Hello,
    RawClient,
)

MT_TEST_REQUEST = 1001
MT_TEST_REPLY = 1002
HID_ALL_HOSTS = 0x7FFF
HASH_MODULE_READY = 0xFD0E0311
RTMA_MAX_DATA_BYTES = 1024 * 1024


@pytest.fixture(autouse=True)
def _need_client():
    if not CLIENT_BIN.exists():
        pytest.skip(
            f"rtma_test_client not found at {CLIENT_BIN}; set RTMA_TEST_CLIENT_BIN"
        )


def parse(lines: list[str]) -> dict[str, str]:
    """Collect key=value items, and lines without one, such as ``sent``, as keys."""
    out = {}
    for line in lines:
        if "=" not in line and line.strip():
            out.setdefault(line.strip(), "")
        for item in line.split():
            key, sep, value = item.partition("=")
            if sep:
                out.setdefault(key, value)
        if line.startswith("error="):
            out["error"] = line[len("error=") :]
    return out


def run(
    port: int, scenario: str, mod_id: int, *args, timeout: float = 30
) -> dict[str, str]:
    """Run a scenario to the end and parse its output."""
    proc = subprocess.run(
        [str(CLIENT_BIN), f"127.0.0.1:{port}", scenario, str(mod_id), *map(str, args)],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return parse(proc.stdout.splitlines())


class Running:
    """A scenario that runs until its stdin is closed."""

    def __init__(self, port: int, scenario: str, mod_id: int, *args):
        self.proc = subprocess.Popen(
            [
                str(CLIENT_BIN),
                f"127.0.0.1:{port}",
                scenario,
                str(mod_id),
                *map(str, args),
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        self.lines: list[str] = []

    def wait_for(self, prefix: str, timeout: float = 10) -> dict[str, str]:
        """Read output until a line starts with ``prefix``."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            line = self.proc.stdout.readline()
            if not line:
                break
            self.lines.append(line.rstrip())
            if line.startswith(prefix):
                return parse(self.lines)
        raise AssertionError(f"no {prefix!r} line: {self.lines}")

    def finish(self) -> dict[str, str]:
        out, _ = self.proc.communicate(timeout=10)
        self.lines += out.splitlines()
        return parse(self.lines)

    def kill(self):
        if self.proc.poll() is None:
            self.proc.kill()
            self.proc.wait()


@pytest.fixture
def running():
    procs: list[Running] = []

    def start(*args) -> Running:
        procs.append(Running(*args))
        return procs[-1]

    yield start
    for p in procs:
        p.kill()


# Against both managers ---------------------------------------------------


def test_connects_with_a_dynamic_id(manager, running):
    client = running(manager.port, "connect", 0)
    out = client.wait_for("pid=")
    assert int(out["module_id"]) >= 10000
    assert client.finish().get("error") is None


def test_exchanges_messages(manager):
    peer = RawClient.connect(manager.port, 20)
    peer.subscribe(MT_TEST_REPLY)
    client = subprocess.Popen(
        [str(CLIENT_BIN), f"127.0.0.1:{manager.port}", "echo", "30", "1"],
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        assert client.stdout.readline().startswith("connect_seconds=")
        assert client.stdout.readline().strip() == "module_id=30"
        assert client.stdout.readline().strip() == "ready"
        # The client doesn't wait for its SUBSCRIBE's ACK; give the manager a
        # moment to process it.
        time.sleep(0.2)
        payload = bytes(range(16))
        peer.send(MT_TEST_REQUEST, payload, msg_count=55)
        reply = peer.wait_for(MT_TEST_REPLY, 5)
        out, _ = client.communicate(timeout=10)
    finally:
        client.kill()
    recv = parse([line for line in out.splitlines() if line.startswith("recv ")])
    assert recv["msg_count"] == "55"
    assert recv["src_mod_id"] == "20"
    assert recv["num_data_bytes"] == "16"
    assert reply is not None
    assert reply.header.src_mod_id == 30
    assert reply.header.dest_mod_id == 20
    assert reply.payload == payload


@pytest.mark.parametrize("mod_id", [0, 31])
def test_connects_again_after_disconnecting(manager, mod_id):
    out = run(manager.port, "connect_twice", mod_id)
    assert "error" not in out
    assert "reconnected" in out


def test_reconnects_after_disconnecting(manager):
    for _ in range(2):
        out = run(manager.port, "send", 31, 8, 0, 0)
        assert out["module_id"] == "31"
        assert "sent" in out


def test_announces_its_process_id_when_connecting(manager, running):
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_HELLO)
    client = running(manager.port, "connect", 31)
    out = client.wait_for("pid=")
    msg = watcher.wait_for(
        MT_HELLO, where=lambda m: Hello.parse(m.payload).mod_id == 31
    )
    assert msg is not None
    assert Hello.parse(msg.payload).pid == int(out["pid"])


def test_marks_core_messages_with_their_hash(manager, running):
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_MODULE_READY)
    client = running(manager.port, "module_ready", 31)
    client.wait_for("sent")
    msg = watcher.wait_for(MT_MODULE_READY, where=lambda m: m.header.src_mod_id == 31)
    assert msg is not None
    assert msg.header.reserved == HASH_MODULE_READY


def hello_for(watcher: RawClient, mod_id: int) -> Hello:
    msg = watcher.wait_for(
        MT_HELLO, where=lambda m: Hello.parse(m.payload).mod_id == mod_id
    )
    assert msg is not None, f"no HELLO for module {mod_id}"
    return Hello.parse(msg.payload)


def test_announces_its_name_when_connecting(manager, running):
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_HELLO)
    client = running(manager.port, "connect", 31, "cpp-module")
    client.wait_for("pid=")
    assert hello_for(watcher, 31).name == "cpp-module"


def test_setting_the_name_after_connecting_announces_it(manager, running):
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_HELLO)
    client = running(manager.port, "rename", 31, "renamed")
    client.wait_for("renamed")
    assert hello_for(watcher, 31).name == ""
    assert hello_for(watcher, 31).name == "renamed"


def test_a_long_name_is_cut(manager, running):
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_HELLO)
    client = running(manager.port, "connect", 31, "n" * 40)
    client.wait_for("pid=")
    assert hello_for(watcher, 31).name == "n" * 31


def test_pyrtma_accepts_its_core_messages_with_sync_check(manager, running):
    pyrtma = pytest.importorskip("pyrtma")
    import pyrtma.core_defs as cd

    observer = pyrtma.Client(name="observer", definitions=cd)
    observer.connect(f"127.0.0.1:{manager.port}")
    try:
        observer.subscribe([cd.MT_MODULE_READY])
        time.sleep(0.2)
        client = running(manager.port, "module_ready", 31)
        client.wait_for("sent")
        msg = observer.read_message(timeout=5, sync_check=True)
        assert msg is not None
        assert msg.header.src_mod_id == 31
    finally:
        observer.disconnect()


def test_user_messages_have_no_version_by_default(manager):
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_TEST_REQUEST)
    run(manager.port, "send", 31, 8, 0, 0)
    msg = watcher.wait_for(MT_TEST_REQUEST)
    assert msg is not None
    assert msg.header.reserved == 0


def test_user_messages_carry_the_version_given(manager):
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_TEST_REQUEST)
    run(manager.port, "send", 31, 8, 0, 0, "0xfae632b5")
    msg = watcher.wait_for(MT_TEST_REQUEST)
    assert msg is not None
    assert msg.header.reserved == 0xFAE632B5


@pytest.mark.client_gap("dest_host_id ALL_HOSTS is refused")
def test_sends_to_all_hosts(manager):
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_TEST_REQUEST)
    out = run(manager.port, "send", 31, 8, 0, HID_ALL_HOSTS)
    assert "error" not in out
    msg = watcher.wait_for(MT_TEST_REQUEST)
    assert msg is not None
    assert msg.header.dest_host_id == HID_ALL_HOSTS


@pytest.mark.client_gap(
    "an oversized message is sent, and the manager drops the client"
)
def test_refuses_to_send_an_oversized_message(manager):
    out = run(manager.port, "send", 31, RTMA_MAX_DATA_BYTES + 1, 0, 0)
    assert "RTMA_MAX_DATA_BYTES" in out.get("error", "")


# Against FakeManager ----------------------------------------------------


class Peer:
    """The fake manager's end of one client connection."""

    def __init__(self, sock: socket.socket):
        self.sock = sock

    def read(self) -> Header:
        def recv(n: int) -> bytes:
            data = b""
            while len(data) < n:
                chunk = self.sock.recv(n - len(data))
                if not chunk:
                    raise ConnectionError("client closed")
                data += chunk
            return data

        header = Header(*HEADER.unpack(recv(HEADER.size)))
        recv(header.num_data_bytes)
        return header

    def send(
        self, msg_type: int, payload: bytes = b"", *, dest_mod_id: int = 0, size=None
    ):
        n = len(payload) if size is None else size
        header = HEADER.pack(msg_type, 0, 0.0, 0.0, 0, 0, 0, dest_mod_id, n, 0, 0, 0)
        self.sock.sendall(header + payload)


class FakeManager:
    """Accepts one client and runs ``script(peer)`` on its connection."""

    def __init__(self, script):
        self.port = free_port()
        self.listener = socket.socket()
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind(("127.0.0.1", self.port))
        self.listener.listen(1)
        self.error: BaseException | None = None
        self.thread = threading.Thread(target=self._serve, args=(script,), daemon=True)
        self.thread.start()

    def _serve(self, script):
        conn, _ = self.listener.accept()
        try:
            script(Peer(conn))
        except BaseException as e:  # reported by close()
            self.error = e
        finally:
            conn.close()

    def close(self):
        self.thread.join(15)
        self.listener.close()
        if self.error and not isinstance(self.error, ConnectionError):
            raise self.error


@pytest.mark.client_gap("takes the first ACK, even one addressed to another module")
def test_static_id_waits_for_its_own_ack():
    def script(peer: Peer):
        peer.read()  # CONNECT
        # A logger is sent copies of other modules' ACKs.
        peer.send(MT_ACKNOWLEDGE, dest_mod_id=31)
        time.sleep(0.6)
        peer.send(MT_ACKNOWLEDGE, dest_mod_id=30)
        peer.read()  # DISCONNECT

    fake = FakeManager(script)
    out = run(fake.port, "send", 30, 8, 0, 0)
    fake.close()
    assert out["module_id"] == "30"
    assert float(out["connect_seconds"]) >= 0.5


def test_dynamic_id_takes_the_first_ack():
    def script(peer: Peer):
        peer.read()
        peer.send(MT_ACKNOWLEDGE, dest_mod_id=10005)
        peer.read()

    fake = FakeManager(script)
    out = run(fake.port, "send", 0, 8, 0, 0)
    fake.close()
    assert out["module_id"] == "10005"


@pytest.mark.client_gap("waits 1 s for the ACK, where pyrtma's client waits 5 s")
def test_waits_five_seconds_for_the_ack():
    def script(peer: Peer):
        peer.read()
        time.sleep(3)
        peer.send(MT_ACKNOWLEDGE, dest_mod_id=30)
        peer.read()

    fake = FakeManager(script)
    out = run(fake.port, "send", 30, 8, 0, 0)
    fake.close()
    assert "error" not in out
    assert out["module_id"] == "30"


@pytest.mark.client_gap("stays connected after a message it can't read")
def test_disconnects_after_a_message_it_cannot_read():
    def script(peer: Peer):
        peer.read()
        peer.send(MT_ACKNOWLEDGE, dest_mod_id=30)
        # A header announcing more than RTMA_MAX_DATA_BYTES, and no payload.
        peer.send(MT_TEST_REQUEST, size=2 * RTMA_MAX_DATA_BYTES)
        time.sleep(2)

    fake = FakeManager(script)
    out = run(fake.port, "read_once", 30)
    fake.close()
    assert "error" in out
    assert out["connected"] == "0"
