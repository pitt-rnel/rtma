"""Fixtures that start the message managers and core modules under test.

Each test that takes ``manager`` runs once against the pyrtma message
manager and once against the C++ MessageManager, each started fresh on a
free loopback port. See README.md for how to run the tests.
"""

from __future__ import annotations

import os
import pathlib
import socket
import subprocess
import sys
import time

import pytest

from rtma_raw import MT_MODULE_READY, ConnectionClosed, RawClient

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
EXE = ".exe" if os.name == "nt" else ""
KINDS = ("pyrtma", "cpp")

# Where QuickLogger connects when it is given no address.
QUICKLOGGER_PORT = 7111
MT_LM_READY = 96

try:
    from pyrtma.__version__ import __version__ as PYRTMA_VERSION
except ImportError:
    PYRTMA_VERSION = None


def _binary(env: str, name: str) -> pathlib.Path:
    path = os.environ.get(env)
    return pathlib.Path(path) if path else REPO / "bin" / (name + EXE)


MM_BIN = _binary("RTMA_MM_BIN", "MessageManager")
QL_BIN = _binary("RTMA_QL_BIN", "QuickLogger")
CLIENT_BIN = _binary("RTMA_TEST_CLIENT_BIN", "rtma_test_client")


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "cpp_gap(reason): expected to fail on the C++ MessageManager until it "
        "matches pyrtma. Strict: a test that passes there fails, so the marker "
        "has to be removed with the fix.",
    )
    config.addinivalue_line(
        "markers",
        "ql_gap(reason): expected to fail with the C++ QuickLogger until it is "
        "fixed. Strict, like cpp_gap.",
    )
    config.addinivalue_line(
        "markers",
        "client_gap(reason): expected to fail with the C++ client library until "
        "it matches pyrtma's client. Strict, like cpp_gap.",
    )


def pytest_report_header(config):
    pyrtma = f"pyrtma {PYRTMA_VERSION}" if PYRTMA_VERSION else "pyrtma NOT FOUND"
    return [
        f"interop: {pyrtma} (python {sys.executable})",
        f"interop: MessageManager {MM_BIN} ({'found' if MM_BIN.exists() else 'NOT FOUND'})",
        f"interop: QuickLogger {QL_BIN} ({'found' if QL_BIN.exists() else 'NOT FOUND'})",
        f"interop: test client {CLIENT_BIN} ({'found' if CLIENT_BIN.exists() else 'NOT FOUND'})",
    ]


def pytest_generate_tests(metafunc):
    if "manager_kind" in metafunc.fixturenames:
        chosen = [k.strip() for k in metafunc.config.getoption("--managers").split(",")]
        unknown = set(chosen) - set(KINDS)
        if unknown:
            raise pytest.UsageError(f"--managers: unknown {sorted(unknown)}")
        metafunc.parametrize("manager_kind", chosen)


def pytest_collection_modifyitems(config, items):
    for item in items:
        params = getattr(getattr(item, "callspec", None), "params", {})
        gap = item.get_closest_marker("cpp_gap")
        if gap and params.get("manager_kind") == "cpp":
            item.add_marker(
                pytest.mark.xfail(strict=True, reason=f"C++ MM gap: {gap.args[0]}")
            )
        for name, label in (("ql_gap", "QuickLogger"), ("client_gap", "C++ client")):
            gap = item.get_closest_marker(name)
            if gap:
                item.add_marker(
                    pytest.mark.xfail(strict=True, reason=f"{label} gap: {gap.args[0]}")
                )


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield
    setattr(item, f"rep_{report.when}", report)
    return report


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def port_in_use(port: int) -> bool:
    with socket.socket() as s:
        s.settimeout(0.2)
        return s.connect_ex(("127.0.0.1", port)) == 0


class Process:
    """A child process whose output goes to a log file."""

    def __init__(self, name: str, cmd: list[str], log: pathlib.Path, cwd: pathlib.Path):
        self.name = name
        self.log = log
        self._log_file = open(log, "wb")
        self.proc = subprocess.Popen(
            cmd, stdout=self._log_file, stderr=subprocess.STDOUT, cwd=cwd
        )

    def alive(self) -> bool:
        return self.proc.poll() is None

    def log_tail(self, n: int = 40) -> str:
        self._log_file.flush()
        lines = self.log.read_text(errors="replace").splitlines()
        return "\n".join(lines[-n:])

    def stop(self) -> None:
        if self.alive():
            self.proc.terminate()
            try:
                self.proc.wait(5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(5)
        self._log_file.close()


class Manager(Process):
    """A message manager listening on ``127.0.0.1:port``."""

    def __init__(self, kind: str, port: int, tmp: pathlib.Path, args: tuple = ()):
        self.kind = kind
        self.port = port
        if kind == "cpp":
            cmd = [str(MM_BIN), f"127.0.0.1:{port}"]
        else:
            cmd = [
                sys.executable,
                "-m",
                "pyrtma.manager",
                "-a",
                "127.0.0.1",
                "-p",
                str(port),
                "--log-level",
                "WARN",
            ]
            if port == QUICKLOGGER_PORT:
                # Clients wait for the manager to close the connection when
                # they disconnect, which leaves the manager's side of each in
                # TIME_WAIT. -d sets SO_REUSEADDR, so the next test's manager
                # can listen on the same fixed port.
                cmd.append("-d")
        cmd += list(args)
        super().__init__(f"{kind} manager", cmd, tmp / f"{kind}_manager.log", tmp)
        self._wait_listening()

    def _wait_listening(self, timeout: float = 15.0) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if not self.alive():
                raise RuntimeError(f"{self.name} exited at startup:\n{self.log_tail()}")
            if port_in_use(self.port):
                return
            time.sleep(0.05)
        raise RuntimeError(
            f"{self.name} not listening on {self.port}:\n{self.log_tail()}"
        )

    def accepts_clients(self) -> bool:
        """Return True if the manager is running and connects a new module."""
        if not self.alive():
            return False
        try:
            RawClient.connect(self.port).close()
            return True
        except (OSError, AssertionError, ConnectionClosed):
            return False


def _require(kind: str) -> None:
    if PYRTMA_VERSION is None:
        pytest.skip("pyrtma is not importable")
    if kind == "cpp" and not MM_BIN.exists():
        pytest.skip(f"C++ MessageManager not found at {MM_BIN}; set RTMA_MM_BIN")


def _report_logs(request, *procs: Process) -> None:
    rep = getattr(request.node, "rep_call", None)
    if rep is not None and rep.failed:
        for p in procs:
            print(f"\n----- {p.name} log ({p.log}) -----\n{p.log_tail()}")


@pytest.fixture
def cpp_manager(request, tmp_path):
    """A fresh C++ MessageManager, for tests of what only it does.

    Skipped when --managers leaves out cpp.
    """
    if "cpp" not in request.config.getoption("--managers").split(","):
        pytest.skip("--managers leaves out cpp")
    _require("cpp")
    mm = Manager("cpp", free_port(), tmp_path)
    yield mm
    _report_logs(request, mm)
    mm.stop()


@pytest.fixture
def manager(request, manager_kind, tmp_path):
    """A fresh message manager of each kind, on a free port."""
    _require(manager_kind)
    mm = Manager(manager_kind, free_port(), tmp_path)
    yield mm
    _report_logs(request, mm)
    mm.stop()


def start_quicklogger(port: int, tmp_path: pathlib.Path, *args: str) -> Process:
    """Start the C++ QuickLogger, and wait until it is recording.

    QuickLogger sends LM_READY after its SUBSCRIBE, and the manager handles a
    connection's messages in order, so LM_READY means it is recording.

    Args:
        port: The manager's port, for watching for LM_READY.
        tmp_path: Where its log goes.
        args: Its arguments; with none, it connects to localhost:7111.
    """
    if not QL_BIN.exists():
        pytest.skip(f"QuickLogger not found at {QL_BIN}; set RTMA_QL_BIN")
    watcher = RawClient.connect(port, 31)
    watcher.subscribe(MT_LM_READY)
    ql = Process(
        "QuickLogger", [str(QL_BIN), *args], tmp_path / "quicklogger.log", tmp_path
    )
    try:
        ready = watcher.wait_for(
            MT_LM_READY, 15.0, where=lambda m: m.header.src_mod_id == 5
        )
        if ready is None:
            ql.stop()
            raise AssertionError(f"QuickLogger sent no LM_READY:\n{ql.log_tail()}")
    finally:
        watcher.close()
    return ql


@pytest.fixture
def quicklogger(request, manager, tmp_path):
    """The C++ QuickLogger, connected to ``manager`` and recording."""
    ql = start_quicklogger(manager.port, tmp_path, f"127.0.0.1:{manager.port}")
    yield ql
    _report_logs(request, ql)
    ql.stop()


@pytest.fixture
def default_port_manager(request, manager_kind, tmp_path):
    """A manager on port 7111, where QuickLogger connects by default."""
    _require(manager_kind)
    if port_in_use(QUICKLOGGER_PORT):
        pytest.skip(f"port {QUICKLOGGER_PORT} is in use")
    mm = Manager(manager_kind, QUICKLOGGER_PORT, tmp_path)
    yield mm
    _report_logs(request, mm)
    mm.stop()


@pytest.fixture
def data_logger(request, manager, tmp_path):
    """The pyrtma data logger, connected and subscribed.

    The data logger sends MODULE_READY after its SUBSCRIBE, so MODULE_READY
    means it will see requests.
    """
    import pyrtma.core_defs as cd

    watcher = RawClient.connect(manager.port, 31)
    watcher.subscribe(MT_MODULE_READY)
    cmd = [
        sys.executable,
        "-m",
        "pyrtma.data_logger",
        "-m",
        f"127.0.0.1:{manager.port}",
        "-d",
        cd.__file__,
        "--write-period",
        "0.2",
        "--log-level",
        "WARN",
    ]
    dl = Process("data logger", cmd, tmp_path / "data_logger.log", tmp_path)
    try:
        ready = watcher.wait_for(
            MT_MODULE_READY,
            15.0,
            where=lambda m: m.header.src_mod_id == cd.MID_DATA_LOGGER,
        )
        assert ready is not None, f"data logger sent no MODULE_READY:\n{dl.log_tail()}"
    finally:
        watcher.close()
    yield dl
    _report_logs(request, dl)
    dl.stop()
