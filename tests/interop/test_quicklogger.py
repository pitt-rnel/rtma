"""The C++ QuickLogger through either manager, read back by pyrtma."""

from __future__ import annotations

import struct

import pytest

from rtma_raw import HEADER, Header, RawClient

pytest.importorskip("pyrtma")

MID_QUICKLOGGER = 5
MT_LM_EXIT = 55
MT_SAVE_MESSAGE_LOG = 56
MT_MESSAGE_LOG_SAVED = 57
MT_PAUSE_MESSAGE_LOGGING = 58
MT_RESUME_MESSAGE_LOGGING = 59
MT_RESET_MESSAGE_LOG = 60
SAVE_MESSAGE_LOG = struct.Struct("=256si")
FILE_HEADER = struct.Struct("=6I")  # QuickLogger file format version 1
USER_TYPE = 1234


def save_log(ctl: RawClient, path) -> None:
    name = str(path).encode()
    ctl.send(MT_SAVE_MESSAGE_LOG, SAVE_MESSAGE_LOG.pack(name, len(name)))
    assert ctl.wait_for(MT_MESSAGE_LOG_SAVED, 5.0) is not None, "no MESSAGE_LOG_SAVED"


def read_ql_file(path) -> list[tuple[Header, bytes]]:
    """Parse a QuickLogger version 1 file without pyrtma."""
    raw = path.read_bytes()
    version, total, count, hdr_size, ofs_size, data_size = FILE_HEADER.unpack_from(raw)
    assert (version, hdr_size, ofs_size) == (1, HEADER.size, 4)
    assert total == len(raw)
    pos = FILE_HEADER.size
    headers = [
        Header(*HEADER.unpack_from(raw, pos + i * hdr_size)) for i in range(count)
    ]
    pos += count * hdr_size
    offsets = struct.unpack_from(f"={count}I", raw, pos)
    data = raw[pos + count * ofs_size :]
    assert len(data) == data_size
    return [(h, data[o : o + h.num_data_bytes]) for h, o in zip(headers, offsets)]


@pytest.fixture
def ctl(quicklogger, manager):
    c = RawClient.connect(manager.port, 30)
    c.subscribe(MT_MESSAGE_LOG_SAVED)
    c.send(MT_RESET_MESSAGE_LOG)
    yield c
    c.close()


def payloads(path) -> list[bytes]:
    return [p for h, p in read_ql_file(path) if h.msg_type == USER_TYPE]


def test_quicklogger_saves_what_it_received(ctl, tmp_path):
    sent = [struct.pack("=32si", f"person{i}".encode(), i) for i in range(5)]
    for p in sent:
        ctl.send(USER_TYPE, p)
    out = tmp_path / "ql.bin"
    save_log(ctl, out)
    assert payloads(out) == sent


def test_pyrtma_log_reader_reads_quicklogger_file(ctl, tmp_path):
    import pyrtma.core_defs as cd
    from pyrtma.utils.log_reader import LogReader

    ctl.send(USER_TYPE, b"\0" * 36)
    out = tmp_path / "ql.bin"
    save_log(ctl, out)
    log = LogReader(cd.get_message_definitions()).load([out], exclude=[USER_TYPE])
    types = {m.header.msg_type for m in log._log}
    assert cd.MT_SAVE_MESSAGE_LOG in types


def test_quicklogger_pause_stops_logging(ctl, tmp_path):
    ctl.send(MT_PAUSE_MESSAGE_LOGGING)
    ctl.send(USER_TYPE, b"\x01" * 36)
    ctl.send(MT_RESUME_MESSAGE_LOGGING)
    ctl.send(USER_TYPE, b"\x02" * 36)
    out = tmp_path / "ql.bin"
    save_log(ctl, out)
    assert payloads(out) == [b"\x02" * 36]


MT_RTMA_LOG_ERROR = 42


def send_save(ctl: RawClient, path, length=None) -> None:
    name = str(path).encode()
    ctl.send(
        MT_SAVE_MESSAGE_LOG,
        SAVE_MESSAGE_LOG.pack(name, len(name) if length is None else length),
    )


def test_quicklogger_keeps_running_when_a_save_fails(ctl, quicklogger, tmp_path):
    ctl.subscribe(MT_RTMA_LOG_ERROR)
    kept = b"\x05" * 36
    ctl.send(USER_TYPE, kept)
    send_save(ctl, tmp_path / "missing" / "ql.bin")
    error = ctl.wait_for(MT_RTMA_LOG_ERROR, 5.0)
    assert error is not None
    assert b"Failed to save the message log" in error.payload
    assert quicklogger.alive()
    # The log is kept for the next save.
    out = tmp_path / "ql.bin"
    save_log(ctl, out)
    assert kept in payloads(out)


@pytest.mark.parametrize("length", [100000, -5])
def test_quicklogger_bounds_the_pathname_length(ctl, quicklogger, tmp_path, length):
    out = tmp_path / "ql.bin"
    send_save(ctl, out, length)
    assert ctl.wait_for(MT_MESSAGE_LOG_SAVED, 5.0) is not None
    assert out.exists()
    assert quicklogger.alive()


def test_quicklogger_exits_on_lm_exit(ctl, quicklogger):
    ctl.send(MT_LM_EXIT, dest_mod_id=MID_QUICKLOGGER)
    quicklogger.proc.wait(5)


def test_quicklogger_connects_to_localhost_7111_by_default(
    default_port_manager, tmp_path
):
    from conftest import start_quicklogger

    ql = start_quicklogger(default_port_manager.port, tmp_path)
    ql.stop()


def test_quicklogger_refuses_extra_arguments(tmp_path):
    import subprocess

    from conftest import QL_BIN

    if not QL_BIN.exists():
        pytest.skip(f"QuickLogger not found at {QL_BIN}")
    proc = subprocess.run(
        [str(QL_BIN), "127.0.0.1:1", "extra"], capture_output=True, text=True, timeout=5
    )
    assert proc.returncode == 2
    assert "usage: QuickLogger [SERVER]" in proc.stdout
