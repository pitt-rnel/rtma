@echo off
rem Run the tests on Windows, after building with build_msvc_2026.bat.
rem
rem   run_tests.bat [PYTEST_ARGS...]
rem
rem Runs CTest on the Release build in build\cmake, then pytest on tests\ with
rem the python on PATH, so activate the environment that has pytest and pyrtma
rem first. Any arguments go to pytest, such as -k quicklogger or --managers cpp.
rem Both run even if the first fails, and the exit status is nonzero if either
rem failed.

setlocal
pushd "%~dp0"

if not exist build\cmake (
    echo build\cmake not found; build first with build_msvc_2026.bat 1>&2
    popd
    exit /b 1
)

set STATUS=0
ctest --test-dir build\cmake -C Release --output-on-failure
if errorlevel 1 set STATUS=1
python -m pytest tests %*
if errorlevel 1 set STATUS=1

popd
exit /b %STATUS%
