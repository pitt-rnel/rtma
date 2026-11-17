"""Command-line options for the tests under tests/.

pytest reads options only from conftest files it loads at startup, which for
python -m pytest tests (as run_tests.sh and run_tests.bat run it) is this
one, so the interop tests' options are defined here rather than in
tests/interop/conftest.py.
"""

# The message managers; the same as KINDS in tests/interop/conftest.py.
KINDS = ("pyrtma", "cpp")


def pytest_addoption(parser):
    parser.addoption(
        "--matlab",
        nargs="?",
        const="matlab",
        default=None,
        help="Run the MATLAB tests, with this MATLAB executable (default: matlab on PATH).",
    )
    parser.addoption(
        "--managers",
        default=",".join(KINDS),
        help="Comma-separated message managers to test: pyrtma, cpp. Default: both.",
    )
