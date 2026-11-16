"""A minimal RTMA client that works at the wire level.

It builds and parses headers itself and depends on nothing but the standard
library, so the tests can send exactly the bytes a C, MATLAB or misbehaving
client would, to either message manager.
"""

from __future__ import annotations

import select
import socket
import struct
import time
from typing import Callable, NamedTuple

# RTMA_MSG_HEADER, native byte order with standard sizes (48 bytes, no padding).
HEADER = struct.Struct("=iiddhhhhiiiI")

ALL_MESSAGE_TYPES = 0x7FFFFFFF
DYN_MOD_ID_START = 10000
MAX_MODULES = 256

MT_ACKNOWLEDGE = 2
MT_CONNECT_V2 = 4
MT_FAILED_MESSAGE = 8
MT_CONNECT = 13
MT_DISCONNECT = 14
MT_SUBSCRIBE = 15
MT_UNSUBSCRIBE = 16
MT_MODULE_READY = 26
MT_INTRODUCE = 31
MT_HELLO = 32
MT_GOODBYE = 33
MT_PAUSE_SUBSCRIPTION = 85
MT_RESUME_SUBSCRIPTION = 86

# Struct layouts of the core messages the tests build or read.
CONNECT = struct.Struct("=hh")  # logger_status, daemon_status
CONNECT_V2 = struct.Struct("=hhhhi32s")  # logger_status, 2 reserved, mod_id, pid, name
MSG_TYPE = struct.Struct("=i")
HELLO = struct.Struct("=ihH32s32s")  # pid, mod_id, port, addr, name


class ConnectionClosed(Exception):
    """The manager closed the connection."""


class Header(NamedTuple):
    msg_type: int
    msg_count: int
    send_time: float
    recv_time: float
    src_host_id: int
    src_mod_id: int
    dest_host_id: int
    dest_mod_id: int
    num_data_bytes: int
    remaining_bytes: int
    is_dynamic: int
    reserved: int


class Msg(NamedTuple):
    header: Header
    payload: bytes

    @property
    def msg_type(self) -> int:
        return self.header.msg_type


class Hello(NamedTuple):
    pid: int
    mod_id: int
    port: int
    addr: str
    name: str

    @classmethod
    def parse(cls, payload: bytes) -> "Hello":
        pid, mod_id, port, addr, name = HELLO.unpack(payload[: HELLO.size])
        return cls(pid, mod_id, port, _cstr(addr), _cstr(name))


def _cstr(b: bytes) -> str:
    return b.split(b"\0", 1)[0].decode("ascii", "replace")


class RawClient:
    """One TCP connection to a message manager."""

    def __init__(self, port: int, host: str = "127.0.0.1", timeout: float = 5.0):
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.mod_id = 0
        self.msg_count = 1
        self._rx = b""

    # Connecting ---------------------------------------------------------

    @classmethod
    def connect(
        cls,
        port: int,
        mod_id: int = 0,
        *,
        logger: bool = False,
        name: str | None = None,
        timeout: float = 3.0,
    ) -> "RawClient":
        """Open a connection and connect as a module.

        Sends CONNECT_V2 when a name is given, and CONNECT otherwise, then
        waits for the ACK. A module asking for a dynamic ID takes the ID the
        ACK is addressed to.

        Raises:
            AssertionError: No ACK arrived.
        """
        c = cls(port)
        c.mod_id = mod_id
        c.send_connect(logger=logger, name=name)
        ack = c.wait_for(MT_ACKNOWLEDGE, timeout)
        assert ack is not None, f"no ACK for CONNECT (mod_id={mod_id})"
        if mod_id == 0:
            c.mod_id = ack.header.dest_mod_id
        return c

    def send_connect(self, *, logger: bool = False, name: str | None = None) -> None:
        if name is None:
            self.send(MT_CONNECT, CONNECT.pack(int(logger), 0))
        else:
            body = CONNECT_V2.pack(int(logger), 0, 0, self.mod_id, 4242, name.encode())
            self.send(MT_CONNECT_V2, body)

    # Sending ------------------------------------------------------------

    def send(
        self,
        msg_type: int,
        payload: bytes = b"",
        *,
        dest_mod_id: int = 0,
        dest_host_id: int = 0,
        num_data_bytes: int | None = None,
        msg_count: int | None = None,
    ) -> None:
        """Send one message. ``num_data_bytes`` can be set to lie about the size."""
        size = len(payload) if num_data_bytes is None else num_data_bytes
        count = self.msg_count if msg_count is None else msg_count
        header = HEADER.pack(
            msg_type,
            count,
            time.time(),
            0.0,
            0,
            self.mod_id,
            dest_host_id,
            dest_mod_id,
            size,
            0,
            0,
            0,
        )
        self.msg_count += 1
        self.sock.sendall(header + payload)

    def control(self, msg_type: int, subject: int, *, wait_ack: bool = True) -> None:
        """Send SUBSCRIBE, UNSUBSCRIBE, PAUSE or RESUME for one type."""
        self.send(msg_type, MSG_TYPE.pack(subject))
        if wait_ack:
            assert self.wait_for(MT_ACKNOWLEDGE, 3.0) is not None, "no ACK"

    def subscribe(self, *types: int) -> None:
        for t in types:
            self.control(MT_SUBSCRIBE, t)

    # Receiving ----------------------------------------------------------

    def _fill(self, n: int, deadline: float) -> bool:
        while len(self._rx) < n:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return False
            ready, _, _ = select.select([self.sock], [], [], remaining)
            if not ready:
                return False
            try:
                chunk = self.sock.recv(65536)
            except (ConnectionResetError, ConnectionAbortedError) as e:
                raise ConnectionClosed(str(e)) from e
            if not chunk:
                raise ConnectionClosed("closed by the manager")
            self._rx += chunk
        return True

    def read(self, timeout: float = 0.5) -> Msg | None:
        """Read one message, or return None if none arrives in time."""
        deadline = time.monotonic() + timeout
        if not self._fill(HEADER.size, deadline):
            return None
        header = Header(*HEADER.unpack(self._rx[: HEADER.size]))
        total = HEADER.size + header.num_data_bytes
        # The header has arrived, so allow a moment more for its payload.
        if not self._fill(total, max(deadline, time.monotonic() + 1.0)):
            raise AssertionError(f"payload of MT={header.msg_type} never arrived")
        payload = self._rx[HEADER.size : total]
        self._rx = self._rx[total:]
        return Msg(header, payload)

    def collect(self, quiet: float = 0.3) -> list[Msg]:
        """Read until nothing arrives for ``quiet`` seconds."""
        out = []
        while (m := self.read(quiet)) is not None:
            out.append(m)
        return out

    def user_types(self, quiet: float = 0.3) -> list[int]:
        """Collect, and return the types of user messages (100 and up)."""
        return [m.msg_type for m in self.collect(quiet) if m.msg_type > 99]

    def wait_for(
        self,
        msg_type: int,
        timeout: float = 2.0,
        where: Callable[[Msg], bool] | None = None,
    ) -> Msg | None:
        """Read until a message of this type (that ``where`` accepts) arrives."""
        deadline = time.monotonic() + timeout
        while (remaining := deadline - time.monotonic()) > 0:
            m = self.read(remaining)
            if m is None:
                return None
            if m.msg_type == msg_type and (where is None or where(m)):
                return m
        return None

    def acked(self, timeout: float = 1.0) -> bool:
        """Return True if an ACK for this module arrives in time.

        With a static ID, only an ACK addressed to it or to 0 counts. A module
        asking for a dynamic ID takes any ACK, as pyrtma's client does. A
        connection the manager closes first counts as not acknowledged.
        """

        def ours(m: Msg) -> bool:
            return self.mod_id == 0 or m.header.dest_mod_id in (0, self.mod_id)

        try:
            ack = self.wait_for(MT_ACKNOWLEDGE, timeout, where=ours)
        except ConnectionClosed:
            return False
        return ack is not None

    def is_closed(self, timeout: float = 2.0) -> bool:
        """Return True if the manager closes this connection within ``timeout``.

        Messages that arrive meanwhile are discarded.
        """
        deadline = time.monotonic() + timeout
        try:
            while time.monotonic() < deadline:
                self.read(deadline - time.monotonic())
        except ConnectionClosed:
            return True
        return False

    def close(self) -> None:
        self.sock.close()
