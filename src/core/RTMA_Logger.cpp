#include "RTMA_Logger.h"

#include "RTMA.h"
#include "RTMA_types.h"
#include "Timing.h"

#include <cstdio>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <mutex>
#include <sstream>

namespace {

const char *LevelName(int level) {
  switch (level) {
  case RTMA_LOG_DEBUG:
    return "DEBUG";
  case RTMA_LOG_INFO:
    return "INFO";
  case RTMA_LOG_WARNING:
    return "WARNING";
  case RTMA_LOG_ERROR:
    return "ERROR";
  case RTMA_LOG_CRITICAL:
    return "CRITICAL";
  default:
    return "LOG";
  }
}

MSG_TYPE MessageTypeForLevel(int level) {
  switch (level) {
  case RTMA_LOG_DEBUG:
    return MT_RTMA_LOG_DEBUG;
  case RTMA_LOG_INFO:
    return MT_RTMA_LOG_INFO;
  case RTMA_LOG_WARNING:
    return MT_RTMA_LOG_WARNING;
  case RTMA_LOG_ERROR:
    return MT_RTMA_LOG_ERROR;
  case RTMA_LOG_CRITICAL:
    return MT_RTMA_LOG_CRITICAL;
  default:
    return MT_RTMA_LOG;
  }
}

void CopyField(char *destination, size_t size, const std::string &source) {
  if (size == 0)
    return;
  const size_t count = source.size() < size - 1 ? source.size() : size - 1;
  memcpy(destination, source.data(), count);
  destination[count] = '\0';
}

std::string TruncateMessage(const std::string &message) {
  const char suffix[] = "[TRUNCATED]";
  if (message.size() < MAX_LOG_LENGTH)
    return message;
  return message.substr(0, MAX_LOG_LENGTH - sizeof(suffix)) + suffix;
}

void RotateFileIfNeeded(const std::string &filename) {
  const long max_file_size = 3L * 1024L * 1024L;
  std::ifstream input(filename.c_str(), std::ios::binary | std::ios::ate);
  if (!input || input.tellg() < max_file_size)
    return;

  const std::string backup3 = filename + ".3";
  const std::string backup2 = filename + ".2";
  const std::string backup1 = filename + ".1";
  std::remove(backup3.c_str());
  std::rename(backup2.c_str(), backup3.c_str());
  std::rename(backup1.c_str(), backup2.c_str());
  std::rename(filename.c_str(), backup1.c_str());
}

} // namespace

class RTMA_Logger::State {
public:
  State(RTMA_Module *owner, const std::string &name, int initial_level)
      : module(owner), log_name(name), level(initial_level),
        console_level(initial_level), rtma_level(initial_level),
        file_level(initial_level), console_enabled(true), rtma_enabled(true),
        file_enabled(false), file_initialized(false) {}

  RTMA_Module *module;
  std::string log_name;
  std::string log_filename;
  int level;
  int console_level;
  int rtma_level;
  int file_level;
  bool console_enabled;
  bool rtma_enabled;
  bool file_enabled;
  bool file_initialized;
  std::mutex mutex;
};

RTMA_Logger::RTMA_Logger(RTMA_Module *module, const std::string &log_name,
                         int level)
    : m_State(new State(module, log_name, level)) {}

RTMA_Logger::RTMA_Logger(const std::shared_ptr<State> &state,
                         const std::string &suffix)
    : m_State(state), m_NameSuffix(suffix) {}

RTMA_Logger RTMA_Logger::Child(const std::string &name) const {
  const std::string suffix = m_NameSuffix.empty() ? name : m_NameSuffix + "." + name;
  return RTMA_Logger(m_State, suffix);
}

void RTMA_Logger::SetAllLevels(int value) {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  m_State->level = value;
  m_State->console_level = value;
  m_State->rtma_level = value;
  m_State->file_level = value;
}

int RTMA_Logger::GetLevel() const { return m_State->level; }
void RTMA_Logger::SetLevel(int value) { m_State->level = value; }

void RTMA_Logger::SetConsoleLevel(int value) {
  m_State->console_level = value;
  if (value < m_State->level)
    m_State->level = value;
}
int RTMA_Logger::GetConsoleLevel() const { return m_State->console_level; }
void RTMA_Logger::SetRTMALevel(int value) {
  m_State->rtma_level = value;
  if (value < m_State->level)
    m_State->level = value;
}
int RTMA_Logger::GetRTMALevel() const { return m_State->rtma_level; }
void RTMA_Logger::SetFileLevel(int value) {
  m_State->file_level = value;
  if (value < m_State->level)
    m_State->level = value;
}
int RTMA_Logger::GetFileLevel() const { return m_State->file_level; }

void RTMA_Logger::SetConsoleEnabled(bool enabled) { m_State->console_enabled = enabled; }
bool RTMA_Logger::IsConsoleEnabled() const { return m_State->console_enabled; }
void RTMA_Logger::SetRTMAEnabled(bool enabled) { m_State->rtma_enabled = enabled; }
bool RTMA_Logger::IsRTMAEnabled() const { return m_State->rtma_enabled; }
void RTMA_Logger::SetFileEnabled(bool enabled) {
  if (enabled && m_State->log_filename.empty())
    throw RTMA_LoggingConfigurationError("A log filename is required before enabling file logging");
  m_State->file_enabled = enabled;
  m_State->file_initialized = enabled;
}
bool RTMA_Logger::IsFileEnabled() const { return m_State->file_enabled; }

void RTMA_Logger::SetLogName(const std::string &name) { m_State->log_name = name; }
std::string RTMA_Logger::GetLogName() const {
  return m_NameSuffix.empty() ? m_State->log_name : m_State->log_name + "." + m_NameSuffix;
}
void RTMA_Logger::SetLogFilename(const std::string &filename) {
  if (m_State->file_initialized)
    throw RTMA_LoggingConfigurationError("Log filename cannot change after file logging is initialized");
  m_State->log_filename = filename;
}
std::string RTMA_Logger::GetLogFilename() const { return m_State->log_filename; }

void RTMA_Logger::LogMessage(int level, const char *function, const char *file,
                             int line, const std::string &message) {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  if (level < m_State->level || level >= RTMA_LOG_OFF)
    return;

  const std::string name = GetLogName();
  const std::string bounded_message = TruncateMessage(message);
  const std::string source_file = file ? file : "";
  const std::string source_function = function ? function : "";
  const std::string formatted = fmt::format("{} - {} - {} - {} - {}:{}\n",
                                             LevelName(level), GetAbsTime(), name,
                                             bounded_message, source_function, line);

  if (m_State->console_enabled && level >= m_State->console_level)
    fmt::print(stderr, "{}", formatted);

  if (m_State->file_enabled && level >= m_State->file_level) {
    RotateFileIfNeeded(m_State->log_filename);
    std::ofstream output(m_State->log_filename.c_str(), std::ios::app);
    output << formatted;
  }

  if (m_State->rtma_enabled && level >= m_State->rtma_level) {
    try {
      if (m_State->module != NULL && m_State->module->IsConnected()) {
        MDF_RTMA_LOG data{};
        data.time = GetAbsTime();
        data.level = level;
        data.lineno = line;
        CopyField(data.name, sizeof(data.name), name);
        CopyField(data.pathname, sizeof(data.pathname), source_file);
        CopyField(data.funcname, sizeof(data.funcname), source_function);
        CopyField(data.message, sizeof(data.message), bounded_message);
        CMessage log_message(MessageTypeForLevel(level), &data, sizeof(data));
        m_State->module->SendMessage(&log_message);
      }
    } catch (...) {
      m_State->rtma_enabled = false;
    }
  }
}