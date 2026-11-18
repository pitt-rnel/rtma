# Changelog

Behavior changes to rtma are recorded here, under "Unreleased", in the same
change that makes them. The version number is chosen at release time.
rtma's versions follow pyrtma's: rtma 4 is the release compatible with
pyrtma 4, and both should be released together.

## Unreleased

Compatible with pyrtma 4: clients in C++, MATLAB, Python and JavaScript
(through pyrtma's web manager) work with either pyrtma's message manager or
this one. See "Compatibility" in README.md.

### Message manager

- Fixed: subscribers were sent every message type. Since the subscriber
  lists became maps, every subscription went into one shared list, so a
  module subscribed to anything was sent everything, and pausing one type
  paused them all.
- Fixed: a core message whose size didn't match its definition, such as a
  SUBSCRIBE with a long payload, overran the manager's stack. Every core
  message (type below 100) is now checked against its definition before it
  is acted on or forwarded, and a client that sends one of another size, or
  a core type that isn't defined, is dropped, as pyrtma's manager does. That
  includes the legacy SUBSCRIPTION_OPTION (7) and MM_READY (94).
- Fixed: FORCE_DISCONNECT of a module that had data waiting could make the
  manager read a deleted pipe and crash.
- Fixed: a server name with a port of five digits was read past the end of
  a buffer, and a port above 65535 wrapped around. Ports must be 1 to 65535.
- Fixed: a fatal error, such as a port already in use, crashed the manager
  on Windows instead of being reported, and exited with status 0 elsewhere.
  It is printed to stderr, written to exception_trace.txt in full, and the
  manager exits with status 1.
- Changed: a client is dropped when its message can't be read or announces
  more than 1 MiB (RTMA_MAX_DATA_BYTES) of data, as pyrtma's manager does.
- Changed: modules are known by their connection. Requests apply to the
  module connected on the connection that sent them, whatever the header's
  src_mod_id says, and a socket must connect before it sends anything else.
- Changed: connections are refused, and closed, as pyrtma's manager refuses
  them: beyond MAX_MODULES (256) modules, with a static ID outside 1 to
  9999, with an ID in use, or when no dynamic ID is free. A refused module
  gets no ACK, HELLO or GOODBYE.
- Changed: a CONNECT_V2 from a connected module updates its name and process
  ID and is announced with a HELLO, without a second ACK.
- Changed: broadcasts from the manager, such as HELLO, GOODBYE and
  FAILED_MESSAGE, have dest_mod_id 0, and DISCONNECT is no longer
  acknowledged.
- Changed: subscribing to ALL_MESSAGE_TYPES replaces a module's other
  subscriptions, pausing a subscription removes it, and resuming one adds
  it, as in pyrtma's manager.
- Changed: the listening socket can be bound again at once after the
  manager stops, while its old connections are in TIME_WAIT, but never
  shared: SO_REUSEADDR on Linux and macOS, SO_EXCLUSIVEADDRUSE on Windows,
  where SO_REUSEADDR let a second manager take the port over silently.
  Connections end gracefully, instead of with a reset on Linux.
- Changed: the manager prints its version, 4.0.0, at startup.

### C++ client library

- Changed: GetAbsTime(), and so message headers' send_time and recv_time,
  read the clock pyrtma's time.perf_counter() reads: CLOCK_MONOTONIC on
  Linux and CLOCK_UPTIME_RAW (mach_absolute_time()) on macOS, where they
  were seconds since 1970, and QueryPerformanceCounter() on Windows, as
  before. Times stamped by C++, MATLAB and Python modules on one machine can
  be compared, and the client's timeouts aren't upset by changes to the
  system time. The clock's zero is arbitrary, usually when the machine
  booted: code that took these times for dates on Linux or macOS must use
  the system time instead. MATLAB's GetAbsTime reads the same clock.
- Added: RTMA_Module(ModuleID, HostID, name), SetModuleName() and
  GetModuleName(). A module's name is sent in CONNECT_V2 and announced in
  HELLO and GOODBYE; set while connected, it is sent with CLIENT_SET_NAME.
- Added: a message's version. CMessage::Set() and the CMessage constructor
  take an optional version, the HASH_ define pyrtma's compiler writes for
  each message, and SendMessage() fills in the hash of a core message, so
  pyrtma clients can check them with read_message(sync_check=True).
  CMessage::reserved is a uint32_t.
- Changed: ConnectToMMM() sends CONNECT_V2, with the module's name and
  process ID, instead of CONNECT. Its daemon_status argument is unused.
- Changed: connecting waits RTMA_CONNECT_TIMEOUT (5 s) for an ACK addressed
  to the module, or to 0, instead of 1 s for any ACK. A module asking for a
  dynamic ID still takes the first.
- Changed: a module created with ID 0 asks for a dynamic ID each time it
  connects. It asked for its previous dynamic ID as a static ID, which the
  managers now refuse.
- Changed: a lost connection, or a message that can't be read, closes the
  connection before ReadMessage() throws, so IsConnected() returns 0
  afterwards, as in pyrtma's client.
- Changed: SendMessage() accepts ALL_HOSTS as a destination, and refuses a
  message of more than RTMA_MAX_DATA_BYTES (1 MiB) of data before sending it.
- Changed: DisconnectFromMMM() waits up to RTMA_DISCONNECT_WAIT (100 ms) for
  the manager to close the connection, as pyrtma's client does, so a module
  can connect again at once with the same static ID.
- Changed: the library is built with _DISABLE_CONSTEXPR_MUTEX_CONSTRUCTOR
  under MSVC, so programs and libraries that link RTMA.lib into a host with
  an older msvcp140.dll, such as MATLAB, don't crash on the logger's first
  lock.
- Fixed: streaming an empty MyCString streamed a null pointer, which crashed
  under MSVC.

### Message definitions

- Changed: RTMA_types.h includes three headers that mirror pyrtma's core
  definitions, one per YAML file: core_types.h (rtma_core.yaml),
  quick_logger_types.h (quick_logger.yaml) and data_logger_types.h
  (data_logger.yaml). Existing includes of RTMA_types.h are unchanged.
- Added: the definitions pyrtma has and the old header lacked:
  MID_DATA_LOGGER, MID_QUICK_LOGGER (MID_QUICKLOGGER is kept as an alias),
  LM_STATUS, the data logger's messages and DATASET, a HASH_ define for every
  core message, and pyrtma's constants. The data logger definitions are for
  controlling pyrtma's data logger, which has no C++ implementation.
- Changed: the aliases are fixed-width types, and MDF_SUBSCRIBE,
  MDF_UNSUBSCRIBE, MDF_PAUSE_SUBSCRIPTION and MDF_RESUME_SUBSCRIPTION are
  structs with a msg_type field, as in the YAML. Every size and layout is
  unchanged.
- Changed: MT_MM_READY, MT_SUBSCRIPTION_OPTION, MIN_STREAM_TYPE, UID and
  RTMA_MESSAGE, which pyrtma doesn't define, are in a legacy section of
  core_types.h. Don't send MM_READY or SUBSCRIPTION_OPTION: both managers
  drop a client that does.

### QuickLogger

- Added: QuickLogger [SERVER] takes the message manager's address, host:port.
  The default is still localhost:7111.
- Changed: QuickLogger connects with the name QuickLogger.
- Fixed: PAUSE_MESSAGE_LOGGING didn't pause logging.
- Fixed: SAVE_MESSAGE_LOG's pathname_length wasn't checked, and a log that
  couldn't be saved, such as to a folder that doesn't exist, stopped
  QuickLogger. The failure is now logged, and the log kept for the next save.

### MATLAB

- Changed: ConnectToMMM( ModuleID, Name, MessageConfig, ...) takes the
  definitions as the RTMA structure, the function pyrtma's compiler writes
  (by handle, name or path), or a MAT file as before. Name, the second
  argument, which was unused, is the module's name; a number there is still
  ignored. Options' values can be the next argument. RTMA_runtime.ModuleID
  is the ID connected with, which the manager chose for a dynamic module.
- Changed: SendMessage and SendSignal send each message's hash as its
  version, from RTMA.hash.
- Changed: ReadMessage skips a message of a type the definitions don't
  define, with a warning the first time each type is seen, instead of
  raising an error.
- Changed: the legacy translator (TranslateRTMAConfigFiles2Matlab) gives
  the same structure as pyrtma's compiler: RTMA.hash, empty structs for
  signals, and string constants without their quotes.
- Fixed: make.m builds the mex again. It compiles the client logger, with
  fmt header-only, from the copy CMake downloads into build/cmake/_deps
  (build the repository first) or from RTMA_FMT_INCLUDE, with /utf-8 and
  _DISABLE_CONSTEXPR_MUTEX_CONSTRUCTOR under MSVC.
- Removed: the timer opcodes from pyrtma's compiled definitions (a pyrtma
  change), which MatlabRTMA rejects.

### Build and tests

- Added: tests/interop, which runs the same scenarios against both message
  managers, with the C++ client (rtma_test_client), QuickLogger, pyrtma's
  data logger and, with --matlab, the MATLAB bindings. tests/core_types
  checks the core headers against pyrtma's YAML. run_tests.sh and
  run_tests.bat run CTest and pytest. See tests/interop/README.md.
- Changed: text files are stored with LF line endings (.gitattributes).
- Changed: the Windows binaries in the repository, lib/RTMA.lib,
  bin/MessageManager.exe, bin/QuickLogger.exe and the 64-bit mex files, are
  built from this release.
- Removed: the 32-bit Windows library and mex (lib/RTMA32.lib,
  MatlabRTMA.mexw32) and the Intel Mac LogReader mex
  (LogReader.mexmaci64), which predated this release. Build them from
  source for those platforms.
