## Plan: Modernize Native RTMA Builds

Replace qmake and hand-maintained Visual Studio projects with root-level CMake 3.15+, building the native `RTMA` library plus `MessageManager` and `QuickLogger`. Add install/export support for `find_package(RTMA CONFIG)`, require C++11, and exclude `lang/`.

**Steps**
1. Create root `CMakeLists.txt` with C++11, target-scoped settings, `Threads`, Debug/Release support, and native-only defaults.
2. Define shared `RTMA` from the six sources in [src/core/RTMA.pro](../../src/core/RTMA.pro); preserve Unix ABI naming/versioning, retain the legacy Windows `RTMA32` and `RTMAd` library names for compatibility, and link `ws2_32` on Windows.
3. Add `MessageManager` and `QuickLogger` executable targets based on their existing `.pro` files.
4. Update [include/OS_defines.h](../../include/OS_defines.h) to detect `_WIN32`, `__linux__`, and `__APPLE__`; retain `_WINDOWS_C`/`_UNIX_C` as compatibility aliases while eliminating build-provided `USE_LINUX`/`USE_WINDOWS`.
5. Update [src/core/PipeLib/SocketPipe.cpp](../../src/core/PipeLib/SocketPipe.cpp) so Linux-only `SO_LINGER` and macOS `SO_NOSIGPIPE` paths are explicitly selected by platform.
6. Add install rules, exported `RTMA::RTMA`, and generated package config/version files. Do not expose `include/internal` as public API.
7. Replace the stale [src/core/PipeLib/Test/Makefile](../../src/core/PipeLib/Test/Makefile) with CTest targets or a bounded MessageManager smoke test.
8. Retire qmake scripts/projects and native `.sln`/`.vcxproj` files after CMake parity is verified; rewrite [build/README.txt](../../build/README.txt).
9. Add Linux GCC/Clang, Windows MSVC, and macOS Clang CI builds, including install plus downstream `find_package` verification.

**Verification**
1. Configure/build/test Debug and Release with GCC and Clang; inspect shared-library SONAME and runtime linkage.
2. Build x64 Debug/Release with MSVC-generated Visual Studio projects and verify the compatibility library names `RTMA32` and `RTMAd`.
3. On macOS, test a client/server connection and disconnect path to validate SIGPIPE handling.
4. Install to a clean prefix and build a minimal external consumer using `find_package(RTMA CONFIG REQUIRED)`.
5. Confirm no qmake, Qt, or language-wrapper dependency remains in the default native build.

**Decisions**
- CMake immediately replaces qmake and maintained native solution files.
- C++11 baseline.
- Installable CMake package included.
- `lang/`, including .NET currently reached through `RTMA.sln`, remains excluded.
- Preserve the legacy Windows `RTMA32` and `RTMAd` library names as an external compatibility contract.
