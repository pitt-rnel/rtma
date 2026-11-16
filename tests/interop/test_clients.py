"""pyrtma clients through either manager."""

from __future__ import annotations

import time

import pytest

pyrtma = pytest.importorskip("pyrtma")
import pyrtma.core_defs as cd  # noqa: E402


def test_pyrtma_clients_exchange_messages(manager):
    server = f"127.0.0.1:{manager.port}"
    consumer = pyrtma.Client(name="consumer", definitions=cd)
    producer = pyrtma.Client(name="producer", definitions=cd)
    consumer.connect(server)
    producer.connect(server)
    try:
        assert consumer.module_id >= cd.DYN_MOD_ID_START
        assert producer.module_id == consumer.module_id + 1
        consumer.subscribe([cd.MT_RTMA_LOG_INFO])
        # The pyrtma client doesn't wait for the ACK, and the manager reads
        # the two connections in no set order.
        time.sleep(0.3)
        msg = cd.MDF_RTMA_LOG_INFO()
        msg.message = "hello"
        producer.send_message(msg)
        # Clients may log through RTMA too, so look for this message.
        got = None
        for _ in range(20):
            m = consumer.read_message(timeout=1)
            if m is None or m.data.message == "hello":
                got = m
                break
        assert got is not None
        assert got.header.src_mod_id == producer.module_id
    finally:
        consumer.disconnect()
        producer.disconnect()


def test_pyrtma_client_name_reaches_other_modules(manager):
    server = f"127.0.0.1:{manager.port}"
    named = pyrtma.Client(name="named-module", definitions=cd)
    asker = pyrtma.Client(name="asker", definitions=cd)
    named.connect(server)
    asker.connect(server)
    try:
        asker.subscribe([cd.MT_HELLO])
        time.sleep(0.3)
        asker.send_signal(cd.MT_INTRODUCE)
        names = {}
        while (m := asker.read_message(timeout=0.5)) is not None:
            if m.type_id == cd.MT_HELLO:
                names[m.data.mod_id] = m.data.name
        assert names.get(named.module_id) == "named-module"
    finally:
        named.disconnect()
        asker.disconnect()
