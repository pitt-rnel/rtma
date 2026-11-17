#!/bin/bash
# Run the tests on Linux or macOS, after building with make.sh.
#
#   ./run_tests.sh [PYTEST_ARGS...]
#
# Runs CTest on build/cmake, then pytest on tests/ with the python on PATH,
# so activate the environment that has pytest and pyrtma first. Any arguments
# go to pytest, such as -k quicklogger or --managers cpp. Both run even if
# the first fails, and the exit status is nonzero if either failed.

cd "$(dirname "$0")" || exit 1

if [ ! -d build/cmake ]; then
    echo "build/cmake not found; build first with make.sh" >&2
    exit 1
fi

status=0
ctest --test-dir build/cmake --output-on-failure || status=1
python -m pytest tests "$@" || status=1
exit $status
