This directory contains legacy build artifacts. The native C++ build is configured
from the repository root with CMake; Qt/qmake is not required.

On Linux or macOS:

	cmake -S . -B build/cmake -DCMAKE_BUILD_TYPE=Release
	cmake --build build/cmake --parallel
	ctest --test-dir build/cmake --output-on-failure
	cmake --install build/cmake --prefix /desired/install/prefix

On Windows, generate a Visual Studio solution with CMake:

	cmake -S . -B build/cmake -G "Visual Studio 17 2022" -A x64
	cmake --build build/cmake --config Release
	cmake --install build/cmake --config Release --prefix C:\desired\install\prefix

The native build produces the RTMA C++ library plus MessageManager and QuickLogger.
For compatibility, 32-bit Windows builds retain the RTMA32 name and 64-bit Debug
Windows builds retain the RTMAd name. Language wrappers under lang/ have separate
build processes and are not part of this build.
