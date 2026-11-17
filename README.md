## Introduction

This readme was based on the readme for the open-source version of RTMA, Dragonfly (https://github.com/dragonfly-msg/dragonfly). It is possible that some of the setup instructions here are incorrect.
Please report any issues by reporting on github or bugging your preferred RNEL engineer.

RTMA is a simple messaging system that helps programmers create modular distributed 
applications rapidly. It hides the complexities of socket programming and data translation, also provides a uniform 
high-level API in each of the supported programming languages (C++, MATLAB, Python, JavaScript) 
and operating systems (Windows, Linux, macOS). Therefore, programmers are able to write each part of 
their application in their programming language of choice and on their operating system of choice 
without having to worry about how the modules will communicate with each other.

RTMA consists of several components: a central message exchange daemon (MessageManager), 
a data logger daemon (QuickLogger), and utilities to create message definitions in all supported programming languages.

This repository holds the C++ MessageManager, the C++ client library, QuickLogger and the MATLAB bindings.
The Python client, a Python message manager, a data logger, the message definition compiler and a
web manager for JavaScript clients are in [pyrtma](https://github.com/pitt-rnel/pyrtma), and the
JavaScript client is [rtma-js](https://github.com/pitt-rnel/rtma-js). rtma 4 is released together
with pyrtma 4; see [Compatibility](#compatibility) and [CHANGELOG.md](CHANGELOG.md).

RTMA uses a client-server architecture where MessageManager is the central server and software 
modules that would like to talk to each other are the clients. MessageManager keeps a listening socket for modules 
to connect to and start sending messages. All messages go through MessageManager which forwards 
them to the connected modules based on their subscriptions. Modules connect to MessageManager, subscribe 
to message types they care about, send messages that will be forwarded by MessageManager to all modules 
that have subscribed to those message types, and receive messages that they themselves have subscribed to. 
The modules remain independent of each other and do not have to know which modules will consume their messages or 
where the messages they consume originate.


## History

The Real-Time Messaging Architecture (RTMA) was first developed by Meel Velliste and Sagi Perel
for use in the development of brain-computer interface development.

Publications whose experiments utilized RTMA Messaging include:
- Velliste, M., Perel, S., Spalding, M. C., Whitford, A. S., & Schwartz, A. B. (2008). **Cortical control of a prosthetic arm for self-feeding.** Nature, 453(7198), 1098-101. doi:10.1038/nature06996
- Clanton, S. T., McMorland, A. J. C., Zohny, Z., Jeffries, S. M., Rasmussen, R. G., Flesher, S. N., & Velliste, M. (2013). **Seven Degree of Freedom Cortical Control of a Robotic Arm.** In C. Guger, B. Z. Allison, & G. Edlinger (Eds.), Brain-Computer Interface Research (pp. 73-81). Berlin, Heidelberg: Springer Berlin Heidelberg. doi:10.1007/978-3-642-36083-1
- Collinger, J. L., Wodlinger, B., Downey, J. E., Wang, W., Tyler-Kabara, E. C., Weber, D. J., McMorland, A. J. C., Velliste, M., Boninger, M. L., Schwartz, A. B. (2012). **High-performance neuroprosthetic control by an individual with tetraplegia.** The Lancet. doi:10.1016/S0140-6736(12)61816-9

## Prerequisites

Bare minimum requirements are CMake 3.15 or newer and a C++11-capable compiler.
RTMA supports MSVC on Windows and GCC or Clang on Linux and macOS. If you'd like to
have support for other languages, see below for their separate requirements:

#### Python
The Python bindings in `lang/python` are obsolete: use [pyrtma](https://github.com/pitt-rnel/pyrtma) instead.
These instructions are kept for existing users of the bindings.
- Version >= 2.6 (python3.7 preferred)
- Install swig >= 2.0.3 (make sure swig executable is on Path. Latest SWIG 4.1 works.) (http://www.swig.org/download.html)
- Install Clang and ctypeslib2 python packages (ctypeslib2 v2.2.2 known to work)
	`pip install clang` and `pip install ctypeslib2==2.2.2`
- Previously a package called "ctypesgen" was used instead of clang/ctypeslib2. This has recently been updated to support Python3 and can be used as an alternative to clang/ctypeslib2 if there are any issues with clang/ctypeslib2. This package can be found on GitHub.
- Install LLVM-Clang compiler (version 11.0 known to work)
  - Windows/Linux: http://releases.llvm.org/download.html
  - MacOS: Install XCode command line tools (Clang is default compiler on MacOS). You may also need to link libclang.dylib to a standard library location (e.g. ~/lib or where ever you copy libRTMA.dylib, see Linux/Mac Installation step 4. below)
  - Note: the latest version of LLVM may not work with the clang python bindings. For best results, check python bindings version with `pip show clang` and install the same version of LLVM.


#### C&#35;
- Windows only, Visual Studio 2005 or later. Latest VS2022 preferred.
- The .NET bindings are not maintained, and haven't been tested with this release.

#### Matlab 
- Version R2017b or newer
- Configure Matlab to recognize the Visual Studio C++ compiler (`mex -setup C++`)

#### Tests
- Python 3.10 or newer with pyrtma 4 and pytest 8.4 or newer, for example in a conda environment


## Installation

#### Linux/Mac

Clone the repository and compile the source as follows:

1. In a terminal execute the following from the repository root, or run `./make.sh`, which does the same:
```shell
cmake -S . -B build/cmake -DCMAKE_BUILD_TYPE=Release
cmake --build build/cmake --parallel
```
To install in a desired prefix directory, run:
```shell
cmake --install build/cmake --prefix /desired/install/prefix
```

2. Create `RTMA` environment variable and set it to where your RTMA folder is (optional but can be used when building C++ modules)

3. If you plan to use the matlab interface, build the repository first (step 1): the mex compiles the
   client library's logger with the fmt library, which CMake downloads into `build/cmake/_deps`. Set
   `RTMA_FMT_INCLUDE` to the include folder of another copy of fmt to use that instead. Then start
   matlab and execute the following:
```matlab
cd RTMA/lang/matlab
make
cd RTMA/src/modules/QuickLogger/LogReader
make
```
   The LogReader's `make` needs the `RTMA` environment variable (step 2).

4. If you plan to use the obsolete python interface, append `RTMA/lang/python` to `PYTHONPATH` environment variable
        

#### Windows

If you'd like to compile from source, clone the repository and follow these instructions:

1. Generate and build a Visual Studio solution from the repository root, or run `build_msvc_2026.bat`,
   which does the same:
```shell
cmake -S . -B build/cmake -G "Visual Studio 18 2026" -A x64
cmake --build build/cmake --config Release
```
   The library is built into `lib` and the modules into `bin`, where the repository also tracks
   prebuilt Windows binaries. A `git checkout`, `reset` or `stash` that restores a tracked
   `lib/RTMA.lib` can leave it newer than the sources, so that the build doesn't rebuild it and links
   the modules against the old library. If that happens, rebuild everything with
   `cmake --build build/cmake --config Release --clean-first`.
To install in a desired prefix directory, run:
```shell
cmake --install build/cmake --config Release --prefix C:\desired\install\prefix
```

2. Create `RTMA` environment variable and set it to where your RTMA folder is (optional, but can be used to build C++ modules)

3. If you plan to use the obsolete python 2/3 interfaces, 
    * Set `PYTHON2_BASE` and `PYTHON3_BASE` environment variables to respective python 2 and 3 install locations (e.g. C:\Python\Anaconda3 and C:\Python\Anaconda3\envs\py27)
    * Set `PYTHON2_LIB` and `PYTHON3_LIB` environment variables (ex: %PYTHON3_BASE%\libs)
    * Set `PYTHON2_INCLUDE` and `PYTHON3_INCLUDE` environment variables (ex: %PYTHON3_BASE%\include)
    * Build `RTMA\lang\python\PyRTMA.sln` with Visual Studio (tested with VS 2019)
    * Add `%RTMA%\lang\python` to `PYTHONPATH` environment variable
	
4. If you plan to use the Matlab interface, build the repository first (step 1), then start matlab and
   execute the following (see the Linux/Mac instructions about fmt and the `RTMA` variable):
```matlab
cd RTMA\lang\matlab
make
cd RTMA\src\modules\QuickLogger\LogReader
make
```
    Note that 64-bit Windows mex files are tracked in the repo and this step is usually unecessary when running 64-bit Windows


## Running

Start the message manager, then the modules. The C++ MessageManager and QuickLogger take the server
address as their first argument, `host:port`, or `:port` for every interface:
```shell
bin/MessageManager                  # listens on :7111, every interface
bin/MessageManager 127.0.0.1:7112   # only on localhost, port 7112
bin/QuickLogger                     # connects to localhost:7111
bin/QuickLogger 192.168.1.10:7111
```
`MessageManager --help` and `QuickLogger --help` show their usage. The MessageManager takes the same
timeout options as pyrtma's manager:

- `--stall-timeout SECONDS` drops a client that sends part of a message and then nothing more for that
  long (default 5), and `--no-stall-timeout` never drops it, for example while it is paused in a
  debugger.
- `--logger-timeout SECONDS` drops a logger that takes no data for that long. By default the manager
  waits for loggers as long as it takes, so they miss nothing.

The manager serves every client without blocking: a module whose connection can't take a message
misses it, and the manager reports that with FAILED_MESSAGE.


## Testing

The tests run the same scenarios against pyrtma's message manager and the C++ one, with clients in
each language. With pyrtma and pytest installed in the active Python environment, build the repository,
then run every test, CTest and pytest:
```shell
./run_tests.sh             # Linux or macOS
run_tests.bat              # Windows
run_tests.bat --matlab     # also the MATLAB tests, slower to start
```
Arguments go to pytest. See [tests/interop/README.md](tests/interop/README.md).


## Compatibility

Clients in every language work with either message manager of this release:

| Client | pyrtma manager 4 | C++ MessageManager 4 |
|---|---|---|
| pyrtma client 4, and its data logger | Yes | Yes |
| C++ client library 4, and QuickLogger | Yes | Yes |
| MATLAB, with the mex built from this release | Yes | Yes |
| rtma-js, through pyrtma's web manager | Yes | Yes |

The interop tests check each of these but rtma-js. Modules built against the last stable release
(`master`) have to be rebuilt: both managers drop a client that sends a core message (type below 100)
this release doesn't define, such as the DEBUG_TEXT the last release's QuickLogger sends, several core
message types and module IDs now have new meanings, and dynamic module IDs start at 10000. See
[CHANGELOG.md](CHANGELOG.md).


## Directory Organization
- `bin`    
    executable modules
- `build`    
    source code build scripts
- `examples`    
    example programs showing how to use RTMA
- `include`  
    include files for the C++ API
- `lang`     
    APIs for other languages
- `lib`      
    library files for the C++ API
- `src`      
    source code for C++ API and executable modules
- `tests`      
    tests of the C++ API, the message definitions and interoperability with pyrtma


## API Summary
- ConnectToMMM(ModuleID, ServerAddress)
- DisconnectFromMMM()
- Subscribe(MessageType)
- Unsubscribe(MessageType)
- ReadMessage(Timeout)
- SendMessage(MessageType, MessageData)
- SendSignal(MessageType)


## Example Code
`RTMA/examples` folder contains ready to run modules in all supported languages. See the README.txt file 
in each example folder for further information.


## Creating Message Definitions
Message definitions are written in YAML and compiled by pyrtma's compiler into definitions for C/C++,
MATLAB, Python and JavaScript:
```shell
python -m pyrtma.compile -i my_messages.defs --c --matlab --python --javascript -o out -n my_messages
```
See pyrtma's documentation for the YAML format. The compiled C header includes a `HASH_` define for
each message, which a C++ module can pass to `CMessage::Set()` as the message's version, and the MATLAB
definitions function can be passed to `ConnectToMMM` directly. The core definitions, in `RTMA_types.h`,
mirror pyrtma's core YAML files.

The rest of this section describes the older way, still supported: C header files, which
`lang/matlab/TranslateRTMAConfigFiles2Matlab.m` translates into a MAT file for MATLAB.

RTMA uses standard C header files to describe message definitions.

Each message consists of a message type and an optional message body. 

The message type is an integer that should be selected to uniquely identify each message. 
It is set with a `#define` statement and the name of the message needs to begin with `MT_`.
Here is an example: 
```C
#define MT_ROBOT_FEEDBACK               100
```
        
The message body is a `struct` composed of one or more data fields which can be standard [C data types](http://en.wikipedia.org/wiki/C_data_types) 
and other structs. The struct has to have the same message name as the message type, and it needs to begin with `MDF_`. 
Here is an example:
```C
typedef struct {
  double    position;
  double    velocity;
  double    force;
} MDF_ROBOT_FEEDBACK;
```

Here is a more complex example:
```C
typedef struct {
    int     SerialNo;
    int     Flags;
    double  dt;
} SAMPLE_HEADER;

#define MAX_ROBOT_FEEDBACK_DIMS     10
typedef struct {
  SAMPLE_HEADER sample_header;
  double        position[MAX_ROBOT_FEEDBACK_DIMS];
  double        velocity[MAX_ROBOT_FEEDBACK_DIMS];
  double        force[MAX_ROBOT_FEEDBACK_DIMS];
} MDF_ROBOT_FEEDBACK;
```
The message body fields need to be manually padded for [data alignment](http://en.wikipedia.org/wiki/Data_alignment) as necessary. 
The following is an example of how to define the fields for 64-bit alignment:
```C
typedef struct {
  int source_index;    		
  int reserved;        		// for 64-bit alignment
  double source_timestamp;
} MDF_RAW_SAMPLE_RESPONSE;
```
If you are not sure how to align message fields on your system, it is safe to use 64-bit alignment. 
Even if your system is not 64-bit, or if you have a mixture of systems with different alignment requirements,
this practice will ensure proper alignment.
