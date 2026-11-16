"""The pyrtma data logger through either manager, driven at the wire level.

The requests are raw headers with no version, as a C or MATLAB client
sends them.
"""

from __future__ import annotations

import pytest

from rtma_raw import RawClient

cd = pytest.importorskip("pyrtma.core_defs")
from pyrtma.utils.log_reader import LogReader  # noqa: E402

REPLIES = (
    cd.MT_DATASET_ADDED,
    cd.MT_DATASET_STARTED,
    cd.MT_DATASET_STOPPED,
    cd.MT_DATASET_SAVED,
    cd.MT_DATASET_REMOVED,
    cd.MT_DATA_LOGGER_CONFIG,
    cd.MT_DATA_LOGGER_ERROR,
)


@pytest.fixture
def ctl(data_logger, manager):
    c = RawClient.connect(manager.port, 30)
    c.subscribe(*REPLIES)
    yield c
    c.close()


def request(ctl: RawClient, msg) -> None:
    ctl.send(msg.type_id, bytes(msg), dest_mod_id=cd.MID_DATA_LOGGER)


def reply(ctl: RawClient, msg_type: int, timeout: float = 5.0):
    m = ctl.wait_for(msg_type, timeout)
    assert (
        m is not None
    ), f"no {cd.get_message_definitions().message_name_from_id(msg_type)}"
    return m


def named(cls, name: str):
    m = cls()
    m.name = name
    return m


def test_config_reply_is_addressed_to_requester(ctl):
    ctl.send(cd.MT_DATA_LOGGER_CONFIG_REQUEST, dest_mod_id=cd.MID_DATA_LOGGER)
    m = reply(ctl, cd.MT_DATA_LOGGER_CONFIG)
    assert m.header.src_mod_id == cd.MID_DATA_LOGGER
    assert m.header.dest_mod_id == ctl.mod_id
    assert m.header.num_data_bytes == cd.MDF_DATA_LOGGER_CONFIG.type_size


def test_dataset_records_and_saves(ctl, tmp_path):
    add = cd.MDF_DATASET_ADD()
    add.dataset.name = "interop"
    add.dataset.save_path = str(tmp_path)
    add.dataset.filename = "rec"
    add.dataset.formatter = "quicklogger"
    add.dataset.max_size_mb = 500
    add.dataset.msg_types[0] = cd.MT_RTMA_LOG_INFO
    request(ctl, add)
    reply(ctl, cd.MT_DATASET_ADDED)

    request(ctl, named(cd.MDF_DATASET_START, "interop"))
    reply(ctl, cd.MT_DATASET_STARTED)
    for i in range(3):
        log = cd.MDF_RTMA_LOG_INFO()
        log.message = f"record {i}"
        ctl.send(cd.MT_RTMA_LOG_INFO, bytes(log))
    request(ctl, named(cd.MDF_DATASET_STOP, "interop"))
    reply(ctl, cd.MT_DATASET_STOPPED)
    saved = cd.MDF_DATASET_SAVED.from_buffer_copy(
        reply(ctl, cd.MT_DATASET_SAVED).payload
    )

    log = LogReader(cd.get_message_definitions()).load([saved.filepath])
    messages = [
        m.data.message for m in log._log if m.header.msg_type == cd.MT_RTMA_LOG_INFO
    ]
    assert messages == ["record 0", "record 1", "record 2"]
