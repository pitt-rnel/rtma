cmake_minimum_required(VERSION 3.15)

project(RTMA VERSION 4.0.0 LANGUAGES CXX)

include(CMakePackageConfigHelpers)
include(CTest)
include(FetchContent)
include(GNUInstallDirs)

option(RTMA_BUILD_MODULES "Build native RTMA modules" ON)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(RTMA_BINARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin)
set(RTMA_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/lib)

set(THREADS_PREFER_PTHREAD_FLAG TRUE)
find_package(Threads REQUIRED)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

set(FMT_INSTALL ON CACHE BOOL "Install fmt with RTMA" FORCE)
FetchContent_Declare(
    fmt
    GIT_REPOSITORY https://github.com/fmtlib/fmt.git
    GIT_TAG 11.1.4
)
FetchContent_MakeAvailable(fmt)

set(RTMA_SOURCES
    src/core/RTMA.cpp
    src/core/RTMA_Logger.cpp
    src/core/MyCException.cpp
    src/core/MyCString.cpp
    src/core/PipeLib/SocketPipe.cpp
    src/core/PipeLib/UPipe.cpp
    src/core/PipeLib/Timing.cpp
)

if(WIN32)
    add_library(RTMA STATIC ${RTMA_SOURCES})
else()
    add_library(RTMA SHARED ${RTMA_SOURCES})
    set_target_properties(RTMA PROPERTIES
        VERSION ${PROJECT_VERSION}
        SOVERSION ${PROJECT_VERSION_MAJOR}
    )
endif()

add_library(RTMA::RTMA ALIAS RTMA)

set_target_properties(RTMA PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY ${RTMA_LIBRARY_OUTPUT_DIRECTORY}
    LIBRARY_OUTPUT_DIRECTORY ${RTMA_LIBRARY_OUTPUT_DIRECTORY}
    RUNTIME_OUTPUT_DIRECTORY ${RTMA_BINARY_OUTPUT_DIRECTORY}
)

foreach(configuration Debug Release RelWithDebInfo MinSizeRel)
    string(TOUPPER ${configuration} configuration_upper)
    set_target_properties(RTMA PROPERTIES
        ARCHIVE_OUTPUT_DIRECTORY_${configuration_upper} ${RTMA_LIBRARY_OUTPUT_DIRECTORY}
        LIBRARY_OUTPUT_DIRECTORY_${configuration_upper} ${RTMA_LIBRARY_OUTPUT_DIRECTORY}
        RUNTIME_OUTPUT_DIRECTORY_${configuration_upper} ${RTMA_BINARY_OUTPUT_DIRECTORY}
    )
endforeach()

target_include_directories(RTMA
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include/internal
)

target_link_libraries(RTMA
    PRIVATE Threads::Threads
    PUBLIC fmt::fmt
)

if(MSVC)
    # Since Visual Studio 2022 17.10, std::mutex's constructor is constexpr and
    # needs a matching msvcp140.dll; code built with it crashes on its first
    # lock when an older msvcp140.dll is loaded, as in hosts that ship their
    # own, such as MATLAB. This keeps the logger's mutex working with any
    # msvcp140.dll, for programs and libraries that link RTMA.lib into such a
    # host.
    target_compile_definitions(RTMA PRIVATE _DISABLE_CONSTEXPR_MUTEX_CONSTRUCTOR)
endif()

if(WIN32)
    target_link_libraries(RTMA PRIVATE ws2_32)

    if(CMAKE_SIZEOF_VOID_P EQUAL 4)
        set_target_properties(RTMA PROPERTIES
            OUTPUT_NAME RTMA32
            OUTPUT_NAME_DEBUG RTMAd32
        )
    else()
        set_target_properties(RTMA PROPERTIES
            OUTPUT_NAME RTMA
            OUTPUT_NAME_DEBUG RTMAd
        )
    endif()
endif()

if(RTMA_BUILD_MODULES)
    add_executable(MessageManager
        src/modules/MessageManager/MessageManager.cpp
        src/modules/MessageManager/Net.cpp)
    target_include_directories(MessageManager PRIVATE include/internal)
    target_link_libraries(MessageManager PRIVATE RTMA)
    # The manager prints its version at startup.
    target_compile_definitions(MessageManager PRIVATE RTMA_VERSION="${PROJECT_VERSION}")
    if(WIN32)
        target_link_libraries(MessageManager PRIVATE ws2_32)
    endif()
    set_target_properties(MessageManager PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${RTMA_BINARY_OUTPUT_DIRECTORY}
    )

    add_executable(QuickLogger src/modules/QuickLogger/QuickLogger.cpp)
    target_include_directories(QuickLogger PRIVATE include/internal)
    target_link_libraries(QuickLogger PRIVATE RTMA)
    set_target_properties(QuickLogger PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${RTMA_BINARY_OUTPUT_DIRECTORY}
    )

    foreach(configuration Debug Release RelWithDebInfo MinSizeRel)
        string(TOUPPER ${configuration} configuration_upper)
        set_target_properties(MessageManager QuickLogger PROPERTIES
            RUNTIME_OUTPUT_DIRECTORY_${configuration_upper} ${RTMA_BINARY_OUTPUT_DIRECTORY}
        )
    endforeach()
endif()

if(BUILD_TESTING)
    add_executable(rtma_public_api_test tests/public_api_test.cpp)
    target_link_libraries(rtma_public_api_test PRIVATE RTMA Threads::Threads)
    add_test(NAME rtma_public_api COMMAND rtma_public_api_test)

    # Compiling this checks the core type headers against pyrtma's core
    # definitions. Regenerate it with tests/core_types/generate.py.
    add_executable(rtma_core_types_test tests/core_types/core_types_test.cpp)
    target_include_directories(rtma_core_types_test PRIVATE
        include include/internal)
    add_test(NAME rtma_core_types COMMAND rtma_core_types_test)

    # The interop tests drive the C++ client library with this; see
    # tests/interop/README.md. It goes in bin/ beside the modules, where the
    # tests look for it.
    add_executable(rtma_test_client tests/interop/test_client.cpp)
    target_include_directories(rtma_test_client PRIVATE include/internal)
    target_link_libraries(rtma_test_client PRIVATE RTMA)
    set_target_properties(rtma_test_client PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${RTMA_BINARY_OUTPUT_DIRECTORY}
    )
    foreach(configuration Debug Release RelWithDebInfo MinSizeRel)
        string(TOUPPER ${configuration} configuration_upper)
        set_target_properties(rtma_test_client PROPERTIES
            RUNTIME_OUTPUT_DIRECTORY_${configuration_upper} ${RTMA_BINARY_OUTPUT_DIRECTORY}
        )
    endforeach()
endif()

install(TARGETS RTMA
    EXPORT RTMATargets
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

if(RTMA_BUILD_MODULES)
    install(TARGETS MessageManager QuickLogger
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    )
endif()

install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(EXPORT RTMATargets
    FILE RTMATargets.cmake
    NAMESPACE RTMA::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/RTMA
)

configure_package_config_file(
    cmake/RTMAConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/RTMAConfig.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/RTMA
)

write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/RTMAConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/RTMAConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/RTMAConfigVersion.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/RTMA
)
