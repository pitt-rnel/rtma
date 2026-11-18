"""The MATLAB bindings through either manager, run with matlab -batch.

Opt-in, since MATLAB is slow to start: run with --matlab, or
--matlab=PATH_TO_MATLAB. It needs the mex built from this repository
(lang/matlab/make.m), and pyrtma to compile the test definitions.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys
import threading
import time

import pytest

from conftest import REPO
from rtma_raw import MT_HELLO, Hello, RawClient

HERE = pathlib.Path(__file__).resolve().parent
MT_REQUEST = 1001
MT_REPLY = 1002
MT_UNDEFINED = 1500  # not in interop_messages.yaml
PAYLOAD = __import__("struct").Struct("=i3i")


@pytest.fixture
def matlab(request):
    path = request.config.getoption("--matlab")
    if not path:
        pytest.skip("MATLAB tests run only with --matlab")
    return path


@pytest.fixture
def matlab_defs(tmp_path) -> pathlib.Path:
    """interop.defs compiled to a MATLAB definitions function."""
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pyrtma.compile",
            "-i",
            str(HERE / "matlab" / "interop.defs"),
            "--matlab",
            "-o",
            str(tmp_path),
            "-n",
            "interop_defs",
        ],
        check=True,
        capture_output=True,
    )
    return tmp_path / "interop_defs.m"


def request_hash() -> int:
    from pyrtma.parser import Parser

    parser = Parser()
    parser.parse(HERE / "matlab" / "interop.defs")
    return int(parser.message_defs["MATLAB_TEST_REQUEST"].hash[:8], 16)


def test_matlab_module(manager, matlab, matlab_defs, tmp_path):
    peer = RawClient.connect(manager.port, 20)
    peer.subscribe(MT_REQUEST, MT_HELLO)
    out_file = tmp_path / "matlab_client.out"
    command = (
        f"addpath('{(REPO / 'lang' / 'matlab').as_posix()}'); "
        f"addpath('{(HERE / 'matlab').as_posix()}'); "
        f"matlab_client('127.0.0.1:{manager.port}', '{matlab_defs.as_posix()}', "
        f"'{out_file.as_posix()}')"
    )
    proc = subprocess.Popen(
        [matlab, "-batch", command],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    output = []
    reader = threading.Thread(target=lambda: output.extend(proc.stdout), daemon=True)
    reader.start()
    try:
        # MATLAB can take a while to start. Keep the HELLOs that come first.
        hellos = []

        def keep_hellos(m):
            if m.msg_type == MT_HELLO:
                hellos.append(Hello.parse(m.payload))
            return m.msg_type == MT_REQUEST

        request = None
        deadline = time.monotonic() + 120
        while request is None and time.monotonic() < deadline and proc.poll() is None:
            m = peer.read(1.0)
            if m is not None and keep_hellos(m):
                request = m
        assert request is not None, "no MATLAB_TEST_REQUEST:\n" + "".join(output)
        module_id = request.header.src_mod_id
        assert module_id >= 10000
        assert request.header.reserved == request_hash()
        value, *values = PAYLOAD.unpack(request.payload)
        assert (value, values) == (7, [1, 2, 3])

        # A message of a type MATLAB doesn't know, which it should skip, then
        # the reply.
        peer.send(MT_UNDEFINED, b"\0" * 8, dest_mod_id=module_id)
        peer.send(
            MT_REPLY,
            PAYLOAD.pack(value + 1, *[v * 10 for v in values]),
            dest_mod_id=module_id,
        )
        status = proc.wait(120)
        written = out_file.read_text() if out_file.exists() else ""
        assert status == 0, "".join(output) + "\nmatlab_client wrote:\n" + written
    finally:
        if proc.poll() is None:
            proc.kill()
    reader.join(5)

    lines = dict(
        line.split("=", 1) for line in out_file.read_text().splitlines() if "=" in line
    )
    assert "error" not in lines, lines["error"]
    assert int(lines["module_id"]) == module_id
    assert lines["reply_type"] == "MATLAB_TEST_REPLY"
    assert lines["reply_value"] == "8"
    assert lines["reply_values"] == "[10 20 30]"
    assert lines["warning_id"] == "ReadMessage:UnknownMessageType"
    assert "disconnected" in out_file.read_text()
    names = {h.name for h in hellos if h.mod_id == module_id}
    assert "matlab-client" in names, hellos
