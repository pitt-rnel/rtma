#ifndef _RTMA_LOGGER_H_
#define _RTMA_LOGGER_H_

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

class RTMA_LoggingConfigurationError : public std::runtime_error {
public:
  explicit RTMA_LoggingConfigurationError(const std::string &message)
      : std::runtime_error(message) {}
};

class RTMA_Logger {
public:
  RTMA_Logger(RTMA_Module *module, const std::string &log_name,
              int level = RTMA_LOG_INFO);

  template <typename... Args>
  void Debug(const char *function, const char *file, int line,
             fmt::format_string<Args...> format, Args &&...args) {
    Log(RTMA_LOG_DEBUG, function, file, line, format,
        std::forward<Args>(args)...);
  }

  template <typename... Args>
  void Info(const char *function, const char *file, int line,
            fmt::format_string<Args...> format, Args &&...args) {
    Log(RTMA_LOG_INFO, function, file, line, format, std::forward<Args>(args)...);
  }

  template <typename... Args>
  void Warning(const char *function, const char *file, int line,
               fmt::format_string<Args...> format, Args &&...args) {
    Log(RTMA_LOG_WARNING, function, file, line, format,
        std::forward<Args>(args)...);
  }

  template <typename... Args>
  void Error(const char *function, const char *file, int line,
             fmt::format_string<Args...> format, Args &&...args) {
    Log(RTMA_LOG_ERROR, function, file, line, format, std::forward<Args>(args)...);
  }

  template <typename... Args>
  void Critical(const char *function, const char *file, int line,
                fmt::format_string<Args...> format, Args &&...args) {
    Log(RTMA_LOG_CRITICAL, function, file, line, format,
        std::forward<Args>(args)...);
  }

  template <typename... Args>
  void debug(const char *function, const char *file, int line,
             fmt::format_string<Args...> format, Args &&...args) {
    Debug(function, file, line, format, std::forward<Args>(args)...);
  }

  template <typename... Args>
  void info(const char *function, const char *file, int line,
            fmt::format_string<Args...> format, Args &&...args) {
    Info(function, file, line, format, std::forward<Args>(args)...);
  }

  template <typename... Args>
  void warning(const char *function, const char *file, int line,
               fmt::format_string<Args...> format, Args &&...args) {
    Warning(function, file, line, format, std::forward<Args>(args)...);
  }

  template <typename... Args>
  void warn(const char *function, const char *file, int line,
            fmt::format_string<Args...> format, Args &&...args) {
    Warning(function, file, line, format, std::forward<Args>(args)...);
  }

  template <typename... Args>
  void error(const char *function, const char *file, int line,
             fmt::format_string<Args...> format, Args &&...args) {
    Error(function, file, line, format, std::forward<Args>(args)...);
  }

  template <typename... Args>
  void critical(const char *function, const char *file, int line,
                fmt::format_string<Args...> format, Args &&...args) {
    Critical(function, file, line, format, std::forward<Args>(args)...);
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

  void SetLogName(const std::string &name);
  std::string GetLogName() const;
  void SetLogFilename(const std::string &filename);
  std::string GetLogFilename() const;

private:
  class State;

  RTMA_Logger(const std::shared_ptr<State> &state, const std::string &suffix);
  void LogMessage(int level, const char *function, const char *file, int line,
                  const std::string &message);

  std::shared_ptr<State> m_State;
  std::string m_NameSuffix;
};

#define RTMA_LOG_SOURCE __func__, __FILE__, __LINE__

#endif