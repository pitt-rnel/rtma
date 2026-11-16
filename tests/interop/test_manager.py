"""Message manager behavior, the same on both managers.

pyrtma's manager is the reference. Tests marked ``cpp_gap`` describe where
the C++ MessageManager doesn't match it yet.
"""

from __future__ import annotations

import struct
import threading
import time

import pytest

from rtma_raw import (
    ALL_MESSAGE_TYPES,
    DYN_MOD_ID_START,
    MAX_MODULES,
    MSG_TYPE,
    MT_ACKNOWLEDGE,
    MT_CONNECT_V2,
    MT_DISCONNECT,
    MT_FORCE_DISCONNECT,
    MT_GOODBYE,
    MT_HELLO,
    MT_INTRODUCE,
    MT_PAUSE_SUBSCRIPTION,
    MT_RESUME_SUBSCRIPTION,
    MT_SUBSCRIBE,
    MT_UNSUBSCRIBE,
    CONNECT_V2,
    Hello,
    RawClient,
)

PAYLOAD = b"\x01" * 8
A, B, C = 1001, 1002, 1003  # user message types


@pytest.fixture
def pair(manager):
    """A consumer (module 20) and a producer (module 21)."""
    consumer = RawClient.connect(manager.port, 20)
    producer = RawClient.connect(manager.port, 21)
    yield consumer, producer
    consumer.close()
    producer.close()


# Routing ----------------------------------------------------------------


def test_routes_only_subscribed_types(pair):
    consumer, producer = pair
    consumer.subscribe(A)
    producer.send(B, PAYLOAD)
    producer.send(A, PAYLOAD)
    assert consumer.user_types() == [A]


def test_unsubscribed_type_is_not_delivered(pair):
    consumer, producer = pair
    consumer.subscribe(A)
    consumer.control(MT_UNSUBSCRIBE, A)
    producer.send(A, PAYLOAD)
    assert consumer.user_types() == []


def test_directed_message_goes_only_to_its_destination(manager, pair):
    consumer, producer = pair
    other = RawClient.connect(manager.port, 22)
    consumer.subscribe(A)
    other.subscribe(A)
    producer.send(A, PAYLOAD, dest_mod_id=20)
    assert consumer.user_types() == [A]
    assert other.user_types() == []


def test_logger_is_sent_messages_addressed_to_others(manager, pair):
    consumer, producer = pair
    logger = RawClient.connect(manager.port, 25, logger=True)
    logger.subscribe(A)
    producer.send(A, PAYLOAD, dest_mod_id=20)
    assert logger.user_types() == [A]


def test_forwarded_header_is_unchanged(pair):
    consumer, producer = pair
    consumer.subscribe(A)
    producer.send(A, PAYLOAD, msg_count=777)
    msg = consumer.wait_for(A)
    assert msg is not None
    assert msg.header.msg_count == 777
    assert msg.header.src_mod_id == 21
    assert msg.header.num_data_bytes == len(PAYLOAD)
    assert msg.payload == PAYLOAD


def test_pause_affects_only_that_type(pair):
    consumer, producer = pair
    consumer.subscribe(A, C)
    consumer.control(MT_PAUSE_SUBSCRIPTION, A)
    producer.send(A, PAYLOAD)
    producer.send(C, PAYLOAD)
    assert consumer.user_types() == [C]


def test_pause_then_resume(pair):
    consumer, producer = pair
    consumer.subscribe(A)
    consumer.control(MT_PAUSE_SUBSCRIPTION, A)
    producer.send(A, PAYLOAD)
    assert consumer.user_types() == []
    consumer.control(MT_RESUME_SUBSCRIPTION, A)
    producer.send(A, PAYLOAD)
    assert consumer.user_types() == [A]


def test_subscribe_all_receives_every_type(pair):
    consumer, producer = pair
    consumer.subscribe(ALL_MESSAGE_TYPES)
    producer.send(A, PAYLOAD)
    producer.send(B, PAYLOAD)
    assert consumer.user_types() == [A, B]


def test_individual_unsubscribe_is_ignored_while_subscribed_to_all(pair):
    consumer, producer = pair
    consumer.subscribe(A)
    consumer.subscribe(ALL_MESSAGE_TYPES)
    consumer.control(MT_UNSUBSCRIBE, B)
    producer.send(B, PAYLOAD)
    assert consumer.user_types() == [B]


def test_unsubscribe_all_removes_every_subscription(pair):
    consumer, producer = pair
    consumer.subscribe(A)
    consumer.subscribe(ALL_MESSAGE_TYPES)
    consumer.control(MT_UNSUBSCRIBE, ALL_MESSAGE_TYPES)
    producer.send(A, PAYLOAD)
    producer.send(B, PAYLOAD)
    assert consumer.user_types() == []


# Connecting -------------------------------------------------------------


@pytest.mark.parametrize("mod_id", [-1, DYN_MOD_ID_START])
def test_static_id_out_of_range_is_refused(manager, mod_id):
    c = RawClient(manager.port)
    c.mod_id = mod_id
    c.send_connect()
    assert not c.acked()
    assert c.is_closed()


def test_dynamic_ids_start_at_dyn_mod_id_start(manager):
    first = RawClient.connect(manager.port)
    second = RawClient.connect(manager.port)
    assert first.mod_id == DYN_MOD_ID_START
    assert second.mod_id == DYN_MOD_ID_START + 1


def test_static_id_in_dynamic_range_is_refused(manager):
    c = RawClient(manager.port)
    c.mod_id = DYN_MOD_ID_START + 500
    c.send_connect()
    assert not c.acked()
    assert c.is_closed()


def test_duplicate_static_id_is_refused_without_goodbye(manager):
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_GOODBYE)
    owner = RawClient.connect(manager.port, 30)  # noqa: F841 (kept open)
    dup = RawClient(manager.port)
    dup.mod_id = 30
    dup.send_connect()
    assert not dup.acked()
    assert dup.is_closed()
    goodbyes = [m for m in watcher.collect() if m.msg_type == MT_GOODBYE]
    assert goodbyes == []


def test_message_before_connect_is_dropped(manager):
    consumer = RawClient.connect(manager.port, 20)
    consumer.subscribe(A)
    early = RawClient(manager.port)
    early.mod_id = 22
    early.send(A, PAYLOAD)
    assert consumer.user_types() == []
    assert early.is_closed()


def test_connect_from_connected_module_is_ignored(manager):
    # Unlike CONNECT_V2, which updates the name.
    module = RawClient.connect(manager.port, 21)
    module.send_connect()
    assert not module.acked(0.5)
    assert manager.accepts_clients()


def test_requests_apply_to_the_sending_connection(pair):
    # The manager knows a module by its connection, not by the header's
    # src_mod_id.
    consumer, producer = pair
    producer.send(MT_SUBSCRIBE, MSG_TYPE.pack(A), src_mod_id=20)
    assert producer.acked()
    consumer.send(A, PAYLOAD)
    assert producer.user_types() == [A]
    producer.send(A, PAYLOAD)
    assert consumer.user_types() == []


def test_connections_beyond_max_modules_are_refused(manager):
    clients = [RawClient.connect(manager.port) for _ in range(MAX_MODULES)]
    extra = RawClient(manager.port)
    extra.send_connect()
    assert not extra.acked()
    assert extra.is_closed()
    for c in clients:
        c.close()


def test_connect_v2_name_is_announced(manager):
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_HELLO)
    module = RawClient.connect(manager.port, 21, name="v2-module")  # noqa: F841
    msg = watcher.wait_for(
        MT_HELLO, where=lambda m: Hello.parse(m.payload).mod_id == 21
    )
    assert msg is not None
    assert Hello.parse(msg.payload).name == "v2-module"


def test_connect_v2_after_connect_updates_name(manager):
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_HELLO)
    module = RawClient.connect(manager.port, 21)
    watcher.collect()
    module.send(MT_CONNECT_V2, CONNECT_V2.pack(0, 0, 0, 21, 4321, b"renamed"))
    msg = watcher.wait_for(
        MT_HELLO, where=lambda m: Hello.parse(m.payload).mod_id == 21
    )
    assert msg is not None
    assert Hello.parse(msg.payload).name == "renamed"
    # The module waits for one ACK only, so a second would be a stray reply.
    assert [m for m in module.collect() if m.msg_type == MT_ACKNOWLEDGE] == []


def test_broadcast_hello_has_no_destination(manager):
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_HELLO)
    module = RawClient.connect(manager.port, 21)  # noqa: F841
    msg = watcher.wait_for(
        MT_HELLO, where=lambda m: Hello.parse(m.payload).mod_id == 21
    )
    assert msg is not None
    assert msg.header.dest_mod_id == 0


def test_introduce_lists_connected_modules(manager):
    # Kept open: a client that is garbage collected closes its connection.
    others = [  # noqa: F841
        RawClient.connect(manager.port, 21, name="one"),
        RawClient.connect(manager.port, 22, name="two"),
    ]
    asker = RawClient.connect(manager.port, 20)
    # pyrtma's manager routes the replies like any HELLO, so the asker
    # subscribes to them. The C++ manager sends them either way.
    asker.subscribe(MT_HELLO)
    asker.send(MT_INTRODUCE)
    hellos = [
        Hello.parse(m.payload) for m in asker.collect(0.5) if m.msg_type == MT_HELLO
    ]
    assert {h.mod_id for h in hellos} == {20, 21, 22}
    assert {h.name for h in hellos if h.mod_id in (21, 22)} == {"one", "two"}


def test_disconnect_announces_goodbye(manager):
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_GOODBYE)
    leaving = RawClient.connect(manager.port, 21)
    leaving.send(MT_DISCONNECT)
    msg = watcher.wait_for(MT_GOODBYE)
    assert msg is not None
    assert Hello.parse(msg.payload).mod_id == 21


def test_disconnect_is_not_acknowledged(manager):
    logger = RawClient.connect(manager.port, 25, logger=True)
    logger.subscribe(ALL_MESSAGE_TYPES)
    leaving = RawClient.connect(manager.port, 21)
    logger.collect()
    leaving.send(MT_DISCONNECT)
    seen = logger.collect()
    assert MT_GOODBYE in [m.msg_type for m in seen]
    acks = [
        m for m in seen if m.msg_type == MT_ACKNOWLEDGE and m.header.dest_mod_id == 21
    ]
    assert acks == []


def test_closed_connection_announces_goodbye(manager):
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_GOODBYE)
    RawClient.connect(manager.port, 21).close()
    msg = watcher.wait_for(MT_GOODBYE)
    assert msg is not None
    assert Hello.parse(msg.payload).mod_id == 21


def test_force_disconnect_of_a_busy_module(manager):
    if manager.kind == "pyrtma":
        pytest.skip("pyrtma's manager doesn't implement FORCE_DISCONNECT")
    watcher = RawClient.connect(manager.port, 20)
    watcher.subscribe(MT_GOODBYE)
    ctl = RawClient.connect(manager.port, 30)
    # The busy module's pipe often has data in the same select() as the
    # FORCE_DISCONNECT that deletes it, which the manager used to read after
    # deleting it.
    for _ in range(30):
        victim = RawClient.connect(manager.port, 40)
        stop = threading.Event()

        def spam():
            try:
                while not stop.is_set():
                    victim.send(A, PAYLOAD)
            except OSError:
                pass

        sender = threading.Thread(target=spam)
        sender.start()
        time.sleep(0.002)
        ctl.send(MT_FORCE_DISCONNECT, struct.pack("=i", 40))
        goodbye = watcher.wait_for(
            MT_GOODBYE, where=lambda m: Hello.parse(m.payload).mod_id == 40
        )
        stop.set()
        sender.join()
        victim.close()
        assert goodbye is not None
    assert manager.accepts_clients()


# Malformed input --------------------------------------------------------


def test_oversized_payload_drops_client(manager):
    c = RawClient.connect(manager.port, 21)
    c.send(A, b"", num_data_bytes=2 * 1024 * 1024)
    assert c.is_closed()
    assert manager.accepts_clients()


def test_core_message_with_wrong_size_drops_client(manager):
    c = RawClient.connect(manager.port, 21)
    c.send(MT_SUBSCRIBE, MSG_TYPE.pack(A) + b"\x41" * 4096)
    assert c.is_closed()
    assert manager.accepts_clients()


def test_unknown_core_type_drops_client(manager):
    c = RawClient.connect(manager.port, 21)
    c.send(7, struct.pack("=iii", A, 0, 0))  # legacy SUBSCRIPTION_OPTION
    assert c.is_closed()
    assert manager.accepts_clients()
