#ifndef _RTMA_LOGGER_H_
#define _RTMA_LOGGER_H_

#include <cstdio>
#include <memory>
#include <stdexcept>
#include <string>

#include <fmt/format.h>

class RTMA_Module;

enum RTMA_LogLevel {
  RTMA_LOG_NOTSET = -1,
  RTMA_LOG_ALL = 0,
  RTMA_LOG_DEBUG = 10,
  RTMA_LOG_INFO = 20,
  RTMA_LOG_WARNING = 30,
  RTMA_LOG_ERROR = 40,
  RTMA_LOG_CRITICAL = 50,
  RTMA_LOG_OFF = 1000
};

enum RTMA_ConsoleColor {
  RTMA_COLOR_AUTO,
  RTMA_COLOR_ALWAYS,
  RTMA_COLOR_NEVER
};

const char *RTMA_LevelName(int level);

// Accepts "DEBUG", "lDEBUG", "WARN", etc. (case-insensitive); throws std::invalid_argument.
int RTMA_LevelFromName(const std::string &name);

class RTMA_LoggingConfigurationError : public std::runtime_error {
public:
  explicit RTMA_LoggingConfigurationError(const std::string &message)
      : std::runtime_error(message) {}
};

// Define RTMA_NO_AUTO_SOURCE to force the no-location fallback (e.g. C++/CLI or MEX builds).
#if defined(RTMA_NO_AUTO_SOURCE)
#elif defined(__has_builtin)
#if __has_builtin(__builtin_FILE) && __has_builtin(__builtin_FUNCTION) && \
    __has_builtin(__builtin_LINE)
#define RTMA_AUTO_SOURCE 1
#endif
#elif defined(__GNUC__) && __GNUC__ >= 5
#define RTMA_AUTO_SOURCE 1
#elif defined(_MSC_VER) && _MSC_VER >= 1926
#define RTMA_AUTO_SOURCE 1
#endif

#ifdef RTMA_AUTO_SOURCE
#define RTMA_CALLER_FUNCTION __builtin_FUNCTION()
#define RTMA_CALLER_FILE __builtin_FILE()
#define RTMA_CALLER_LINE __builtin_LINE()
#else
#define RTMA_CALLER_FUNCTION ""
#define RTMA_CALLER_FILE ""
#define RTMA_CALLER_LINE 0
#endif

namespace rtma_detail {
template <typename T> struct Identity { typedef T type; };
} // namespace rtma_detail

// Default arguments are evaluated where the format string is converted, i.e. at the
// caller, which is why the format string is wrapped instead of trailing the args.
template <typename... Args> struct RTMA_LogFormat {
  template <typename S>
  RTMA_LogFormat(const S &s, const char *caller_function = RTMA_CALLER_FUNCTION,
                 const char *caller_file = RTMA_CALLER_FILE,
                 int caller_line = RTMA_CALLER_LINE)
      : format(s), function(caller_function), file(caller_file),
        line(caller_line) {}

  fmt::format_string<Args...> format;
  const char *function;
  const char *file;
  int line;
};

#undef RTMA_CALLER_FUNCTION
#undef RTMA_CALLER_FILE
#undef RTMA_CALLER_LINE

// Args are deduced from the log arguments only, never from the format string.
template <typename... Args>
using RTMA_LogFormatFor =
    RTMA_LogFormat<typename rtma_detail::Identity<Args>::type...>;

// Thread-safe, but RTMA output goes through RTMA_Module::SendMessage(), which is not.
//
// The level methods (info(), error(), ...) record the caller's function, file and line
// automatically where the compiler provides __builtin_FILE() and friends; otherwise
// (RTMA_AUTO_SOURCE undefined) they record no location. Log() always takes it explicitly.
class RTMA_Logger {
public:
  RTMA_Logger(RTMA_Module *module, const std::string &log_name,
              int level = RTMA_LOG_INFO);

  template <typename... Args>
  void Debug(RTMA_LogFormatFor<Args...> f, Args &&...args) {
    Log(RTMA_LOG_DEBUG, f.function, f.file, f.line, f.format,
        std::forward<Args>(args)...);
  }

  template <typename... Args>
  void Info(RTMA_LogFormatFor<Args...> f, Args &&...args) {
    Log(RTMA_LOG_INFO, f.function, f.file, f.line, f.format,
        std::forward<Args>(args)...);
  }

  template <typename... Args>
  void Warning(RTMA_LogFormatFor<Args...> f, Args &&...args) {
    Log(RTMA_LOG_WARNING, f.function, f.file, f.line, f.format,
        std::forward<Args>(args)...);
  }

  template <typename... Args>
  void Error(RTMA_LogFormatFor<Args...> f, Args &&...args) {
    Log(RTMA_LOG_ERROR, f.function, f.file, f.line, f.format,
        std::forward<Args>(args)...);
  }

  template <typename... Args>
  void Critical(RTMA_LogFormatFor<Args...> f, Args &&...args) {
    Log(RTMA_LOG_CRITICAL, f.function, f.file, f.line, f.format,
        std::forward<Args>(args)...);
  }

  template <typename... Args>
  void debug(RTMA_LogFormatFor<Args...> f, Args &&...args) {
    Debug(f, std::forward<Args>(args)...);
  }

  template <typename... Args>
  void info(RTMA_LogFormatFor<Args...> f, Args &&...args) {
    Info(f, std::forward<Args>(args)...);
  }

  template <typename... Args>
  void warning(RTMA_LogFormatFor<Args...> f, Args &&...args) {
    Warning(f, std::forward<Args>(args)...);
  }

  template <typename... Args>
  void warn(RTMA_LogFormatFor<Args...> f, Args &&...args) {
    Warning(f, std::forward<Args>(args)...);
  }

  template <typename... Args>
  void error(RTMA_LogFormatFor<Args...> f, Args &&...args) {
    Error(f, std::forward<Args>(args)...);
  }

  template <typename... Args>
  void critical(RTMA_LogFormatFor<Args...> f, Args &&...args) {
    Critical(f, std::forward<Args>(args)...);
  }

  template <typename... Args>
  void Log(int level, const char *function, const char *file, int line,
           fmt::format_string<Args...> format, Args &&...args) {
    LogMessage(level, function, file, line,
               fmt::format(format, std::forward<Args>(args)...));
  }

  RTMA_Logger Child(const std::string &name) const;

  void SetAllLevels(int level);
  int GetLevel() const;
  void SetLevel(int level);

  void SetConsoleLevel(int level);
  int GetConsoleLevel() const;
  void SetRTMALevel(int level);
  int GetRTMALevel() const;
  void SetFileLevel(int level);
  int GetFileLevel() const;

  void SetConsoleEnabled(bool enabled);
  bool IsConsoleEnabled() const;
  void SetRTMAEnabled(bool enabled);
  bool IsRTMAEnabled() const;
  void SetFileEnabled(bool enabled);
  bool IsFileEnabled() const;

  // The stream is not owned and must outlive the logger.
  void SetConsoleStream(FILE *stream);
  FILE *GetConsoleStream() const;
  // AUTO colors only when the console stream is a terminal.
  void SetConsoleColor(RTMA_ConsoleColor mode);
  RTMA_ConsoleColor GetConsoleColor() const;

  void SetLogName(const std::string &name);
  // No-op once SetLogName() has been called explicitly.
  void SetDefaultLogName(const std::string &name);
  std::string GetLogName() const;
  void SetLogFilename(const std::string &filename);
  std::string GetLogFilename() const;

private:
  class State;
  friend class RTMA_Module;

  // Stops RTMA output; called when the owning module is destroyed.
  void Detach();

  RTMA_Logger(const std::shared_ptr<State> &state, const std::string &suffix);
  void LogMessage(int level, const char *function, const char *file, int line,
                  const std::string &message);

  std::shared_ptr<State> m_State;
  std::string m_NameSuffix;
};

// Only for the explicit Log(); the level methods capture the location themselves.
#define RTMA_LOG_SOURCE __func__, __FILE__, __LINE__

#endif