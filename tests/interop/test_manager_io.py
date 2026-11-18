"""How a manager copes with slow and stalled clients.

A manager serves every client from one thread, so one client must not hold
up the others: a client that stops partway through sending a message, a
module that stops reading, and a logger that reads slowly. pyrtma's manager
is the reference.
"""

from __future__ import annotations

import struct
import threading
import time

import pytest

from rtma_raw import (
    ALL_MESSAGE_TYPES,
    HEADER,
    MSG_TYPE,
    MT_ACKNOWLEDGE,
    MT_GOODBYE,
    MT_SUBSCRIBE,
    Hello,
    RawClient,
)

MT_FAILED_MESSAGE = 8
MT_RTMA_LOG_INFO = 44
RTMA_LOG_SIZE = 1936
A, B = 1001, 1002
STALL_TIMEOUT = 5.0  # both managers' default
FAILED_MESSAGE = struct.Struct("=h6xd")  # dest_mod_id, reserved, time_of_failure


def flood(producer: RawClient, msg_type: int, size: int, seconds: float) -> int:
    """Send messages for a while, from a thread, so a stuck manager can't
    stop the test. Returns how many were sent."""
    sent = [0]
    payload = b"\x01" * size
    deadline = time.monotonic() + seconds

    def run():
        try:
            while time.monotonic() < deadline:
                producer.send(msg_type, payload)
                sent[0] += 1
        except OSError:
            pass

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    thread.join(seconds + 5)
    return sent[0]


def stop_reading(client: RawClient) -> None:
    """Make a client's receive buffer small, so it fills soon."""
    import socket

    client.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)


# Stalled senders --------------------------------------------------------


def test_stalled_sender_does_not_hold_up_others(manager):
    consumer = RawClient.connect(manager.port, 20)
    consumer.subscribe(A)
    producer = RawClient.connect(manager.port, 22)
    stalled = RawClient.connect(manager.port, 21)
    stalled.sock.sendall(HEADER.pack(A, 1, 0.0, 0.0, 0, 21, 0, 0, 8, 0, 0, 0)[:20])
    time.sleep(0.2)
    producer.send(A, b"\x02" * 8)
    msg = consumer.wait_for(A, 2.0)
    assert msg is not None
    assert msg.header.src_mod_id == 22


def test_stalled_sender_is_dropped(manager):
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_GOODBYE)
    stalled = RawClient.connect(manager.port, 21)
    stalled.sock.sendall(
        HEADER.pack(A, 1, 0.0, 0.0, 0, 21, 0, 0, 8, 0, 0, 0) + b"\x03" * 4
    )
    start = time.monotonic()
    goodbye = watcher.wait_for(
        MT_GOODBYE,
        STALL_TIMEOUT + 5,
        where=lambda m: Hello.parse(m.payload).mod_id == 21,
    )
    assert goodbye is not None
    assert time.monotonic() - start >= STALL_TIMEOUT - 0.5
    assert stalled.is_closed()


def test_slow_sender_is_not_dropped(manager):
    consumer = RawClient.connect(manager.port, 20)
    consumer.subscribe(A)
    slow = RawClient.connect(manager.port, 21)
    wire = HEADER.pack(A, 1, 0.0, 0.0, 0, 21, 0, 0, 8, 0, 0, 0) + b"\x04" * 8
    for i in range(0, len(wire), 8):
        slow.sock.sendall(wire[i : i + 8])
        time.sleep(0.3)
    msg = consumer.wait_for(A, 2.0)
    assert msg is not None
    assert msg.payload == b"\x04" * 8


# Modules that don't read ------------------------------------------------


def test_module_that_stops_reading_does_not_hold_up_others(manager):
    # The C++ manager used to stop when select() said the connection could take
    # some bytes and the message didn't fit, which depends on the platform and
    # the socket buffers' sizes.
    blocked = RawClient.connect(manager.port, 20)
    stop_reading(blocked)
    blocked.subscribe(A)
    other = RawClient.connect(manager.port, 21)
    other.subscribe(B)
    producer = RawClient.connect(manager.port, 22)
    assert flood(producer, A, 1024 * 1024, 2.0) > 0
    producer.send(B, b"\x05" * 8)
    msg = other.wait_for(B, 5.0)
    assert msg is not None


def test_module_that_stops_reading_gets_failed_messages(manager):
    watcher = RawClient.connect(manager.port, 30)
    watcher.subscribe(MT_FAILED_MESSAGE)
    blocked = RawClient.connect(manager.port, 20)
    stop_reading(blocked)
    blocked.subscribe(A)
    producer = RawClient.connect(manager.port, 22)
    flood(producer, A, 1024 * 1024, 2.0)
    failed = watcher.wait_for(MT_FAILED_MESSAGE, 5.0)
    assert failed is not None
    dest_mod_id, _ = FAILED_MESSAGE.unpack_from(failed.payload)
    assert dest_mod_id == 20
    # The failed message's header is in the report.
    assert struct.unpack_from("=i", failed.payload, FAILED_MESSAGE.size)[0] == A


def test_no_failed_message_for_log_messages(manager):
    watcher = RawClient.connect(manager.port, 30)
    watcher.subscribe(MT_FAILED_MESSAGE, B)
    blocked = RawClient.connect(manager.port, 20)
    stop_reading(blocked)
    blocked.subscribe(MT_RTMA_LOG_INFO)
    producer = RawClient.connect(manager.port, 22)
    assert flood(producer, MT_RTMA_LOG_INFO, RTMA_LOG_SIZE, 2.0) > 0
    # The manager is still serving, and reported nothing.
    producer.send(B, b"\x06" * 8)
    seen = []
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline and B not in seen:
        m = watcher.read(0.5)
        if m is not None:
            seen.append(m.msg_type)
    assert B in seen
    assert MT_FAILED_MESSAGE not in seen


# Loggers -----------------------------------------------------------------


def test_slow_logger_is_sent_every_message(manager):
    # A logger is waited for, so it misses nothing, however slowly it reads.
    logger = RawClient.connect(manager.port, 25, logger=True)
    logger.subscribe(A)
    producer = RawClient.connect(manager.port, 22)
    count = 200
    payload = b"\x07" * (16 * 1024)

    def produce():
        for i in range(count):
            producer.send(A, payload, msg_count=i + 1)

    thread = threading.Thread(target=produce, daemon=True)
    thread.start()
    got = []
    deadline = time.monotonic() + 30
    while len(got) < count and time.monotonic() < deadline:
        m = logger.read(1.0)
        if m is not None and m.msg_type == A:
            got.append(m.header.msg_count)
            time.sleep(0.002)  # slower than the producer
    thread.join(5)
    assert got == list(range(1, count + 1))


def test_every_logger_is_sent_other_modules_acks(manager):
    logger = RawClient.connect(manager.port, 25, logger=True)
    module = RawClient.connect(manager.port, 21)
    logger.collect()
    module.send(MT_SUBSCRIBE, MSG_TYPE.pack(A))
    ack = logger.wait_for(
        MT_ACKNOWLEDGE, 2.0, where=lambda m: m.header.dest_mod_id == 21
    )
    assert ack is not None


# Destinations -------------------------------------------------------------


@pytest.mark.parametrize("dest", [{"dest_mod_id": -5}, {"dest_host_id": 99}])
def test_message_with_invalid_destination_is_not_forwarded(manager, dest):
    logger = RawClient.connect(manager.port, 25, logger=True)
    logger.subscribe(ALL_MESSAGE_TYPES)
    producer = RawClient.connect(manager.port, 22)
    logger.collect()
    producer.send(A, b"\x08" * 8, **dest)
    assert [m.msg_type for m in logger.collect(0.5) if m.msg_type == A] == []


# Options -----------------------------------------------------------------
# Both managers take --stall-timeout, --no-stall-timeout and
# --logger-timeout.


@pytest.fixture
def manager_with(request, manager_kind, tmp_path):
    """Starts a manager of each kind with the given options."""
    from conftest import Manager, _report_logs, _require, free_port

    _require(manager_kind)
    started = []

    def start(*args):
        mm = Manager(manager_kind, free_port(), tmp_path, args)
        started.append(mm)
        return mm

    yield start
    for mm in started:
        _report_logs(request, mm)
        mm.stop()


def test_stall_timeout_option(manager_with):
    manager = manager_with("--stall-timeout", "1")
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_GOODBYE)
    stalled = RawClient.connect(manager.port, 21)
    stalled.sock.sendall(HEADER.pack(A, 1, 0.0, 0.0, 0, 21, 0, 0, 8, 0, 0, 0)[:20])
    start = time.monotonic()
    goodbye = watcher.wait_for(
        MT_GOODBYE, 4.0, where=lambda m: Hello.parse(m.payload).mod_id == 21
    )
    assert goodbye is not None
    assert 0.5 <= time.monotonic() - start < 4.0


def test_logger_timeout_option(manager_with):
    manager = manager_with("--logger-timeout", "1")
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_GOODBYE)
    logger = RawClient.connect(manager.port, 25, logger=True)
    stop_reading(logger)
    logger.subscribe(A)
    producer = RawClient.connect(manager.port, 22)
    flood(producer, A, 1024 * 1024, 4.0)
    goodbye = watcher.wait_for(
        MT_GOODBYE, 5.0, where=lambda m: Hello.parse(m.payload).mod_id == 25
    )
    assert goodbye is not None
    assert manager.accepts_clients()


def test_cpp_manager_usage(tmp_path):
    import subprocess

    from conftest import MM_BIN

    if not MM_BIN.exists():
        pytest.skip(f"C++ MessageManager not found at {MM_BIN}")
    run = lambda *args: subprocess.run(
        [str(MM_BIN), *args], cwd=tmp_path, capture_output=True, text=True, timeout=5
    )
    shown = run("--help")
    assert shown.returncode == 0
    assert "usage: MessageManager [SERVER]" in shown.stdout
    for bad in (
        ["--stall-timeout"],
        ["--logger-timeout", "0"],
        ["--bogus"],
        [":1", ":2"],
    ):
        refused = run(*bad)
        assert refused.returncode == 2, bad
        assert "usage: MessageManager" in refused.stderr
