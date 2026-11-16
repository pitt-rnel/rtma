# Interop tests

These tests run the same scenarios against the pyrtma message manager and the
C++ MessageManager, so that clients in any language behave the same with
either one. pyrtma's manager is the reference.

They cover:

- `test_manager.py`: routing, subscriptions, connecting, HELLO, GOODBYE,
  INTRODUCE and malformed input, using a wire-level client (`rtma_raw.py`)
  that sends exactly the bytes a C or MATLAB module would.
- `test_clients.py`: pyrtma clients through each manager.
- `test_quicklogger.py`: the C++ QuickLogger through each manager, with its
  files read back directly and by pyrtma's `LogReader`.
- `test_data_logger.py`: the pyrtma data logger through each manager,
  controlled with raw requests addressed to it.

Every test that takes the `manager` fixture runs twice, once per manager,
each started fresh on a free loopback port.

## Requirements

- Python 3.10 or newer with pyrtma 4 importable, and pytest 8.4 or newer.
  pytest-timeout is optional.
- The C++ MessageManager and QuickLogger, built as described in the
  repository README. The tests look for them in `bin/`, or where the
  `RTMA_MM_BIN` and `RTMA_QL_BIN` environment variables point.

Without pyrtma every test is skipped. Without a C++ binary, the tests that
need it are skipped and the pyrtma ones still run.

## Running

From the repository root, on Linux or macOS:

```
python -m pip install "pytest>=8.4" pytest-timeout
python -m pip install -e /path/to/pyrtma      # or pyrtma from a wheel
cmake -S . -B build && cmake --build build
python -m pytest tests/interop
```

On Windows, after building with `build_msvc_2026.bat` or CMake:

```
py -m pip install "pytest>=8.4" pytest-timeout
py -m pip install -e C:\path\to\pyrtma
py -m pytest tests\interop
```

To test binaries somewhere else, such as a Debug build:

```
set RTMA_MM_BIN=C:\path\to\MessageManager.exe
set RTMA_QL_BIN=C:\path\to\QuickLogger.exe
```

Useful options:

- `--managers cpp` or `--managers pyrtma` tests one manager only.
- `-k quicklogger` runs the tests whose names match.
- `-rxX` lists expected failures and unexpected passes in the summary.

The pytest header shows which pyrtma, MessageManager and QuickLogger were
found. When a test fails, the logs of the processes it started are printed
after it.

## Ports

Managers listen on `127.0.0.1` only, so no firewall prompt should appear on
Windows. QuickLogger always connects to `localhost:7111`, so its tests start
their manager on port 7111, and are skipped if something already listens
there. Stop any message manager you have running before running them.

## Expected failures

Tests marked `cpp_gap` are expected to fail on the C++ MessageManager, and
`ql_gap` tests with the C++ QuickLogger, until those match pyrtma. The marks
are strict: a marked test that passes is reported as a failure, so a fix
must remove its mark. A clean run shows only passes and expected failures
(`x`).
