#include "RTMA_Logger.h"

#include "RTMA.h"
#include "RTMA_types.h"
#include "Timing.h"

#include <algorithm>
#include <cctype>
#include <chrono>
#include <cstdio>
#include <cstring>
#include <ctime>
#include <fmt/chrono.h>
#include <fmt/color.h>
#include <fstream>
#include <iomanip>
#include <mutex>
#include <sstream>
#include <stdexcept>

#ifdef _WIN32
#include <io.h>
#include <windows.h>
#else
#include <unistd.h>
#endif

namespace {

bool IsTerminal(FILE *stream) {
#ifdef _WIN32
  return stream != nullptr && _isatty(_fileno(stream)) != 0;
#else
  return stream != nullptr && isatty(fileno(stream)) != 0;
#endif
}

// Windows consoles ignore ANSI escapes until virtual terminal processing is on.
bool PrepareTerminal(FILE *stream) {
#ifdef _WIN32
  if (stream == nullptr)
    return false;
  const intptr_t handle = _get_osfhandle(_fileno(stream));
  DWORD mode = 0;
  if (handle == -1 || !GetConsoleMode(reinterpret_cast<HANDLE>(handle), &mode))
    return false;
  return (mode & ENABLE_VIRTUAL_TERMINAL_PROCESSING) != 0 ||
         SetConsoleMode(reinterpret_cast<HANDLE>(handle),
                        mode | ENABLE_VIRTUAL_TERMINAL_PROCESSING) != 0;
#else
  (void)stream;
  return true;
#endif
}

fmt::text_style LevelStyle(int level) {
  switch (level) {
  case RTMA_LOG_INFO:
    return fmt::fg(fmt::color::blue);
  case RTMA_LOG_WARNING:
    return fmt::fg(fmt::color::dark_red);
  case RTMA_LOG_ERROR:
    return fmt::fg(fmt::color::maroon);
  case RTMA_LOG_CRITICAL:
    return fmt::bg(fmt::color::maroon) | fmt::fg(fmt::color::black);
  default:
    return fmt::fg(fmt::color::green);
  }
}

std::tm LocalTime(std::time_t t) {
  std::tm result{};
#ifdef _WIN32
  localtime_s(&result, &t);
#else
  localtime_r(&t, &result);
#endif
  return result;
}

std::string Basename(const std::string &path) {
  const size_t pos = path.find_last_of("/\\");
  return pos == std::string::npos ? path : path.substr(pos + 1);
}

const char *LevelName(int level) {
  return RTMA_LevelName(level);
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

const std::streamoff kMaxFileBytes = 3 * 1024 * 1024;

// Stops a log call made during an RTMA send from recursing into another send.
thread_local bool t_in_rtma_send = false;

struct RtmaSendGuard {
  RtmaSendGuard() { t_in_rtma_send = true; }
  ~RtmaSendGuard() { t_in_rtma_send = false; }
};

} // namespace

const char *RTMA_LevelName(int level) {
  switch (level) {
  case RTMA_LOG_NOTSET:
    return "NOTSET";
  case RTMA_LOG_ALL:
    return "ALL";
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
  case RTMA_LOG_OFF:
    return "OFF";
  default:
    return "LOG";
  }
}

int RTMA_LevelFromName(const std::string &name) {
  static const struct {
    const char *name;
    int level;
  } levels[] = {{"NOTSET", RTMA_LOG_NOTSET},   {"ALL", RTMA_LOG_ALL},
                {"DEBUG", RTMA_LOG_DEBUG},     {"INFO", RTMA_LOG_INFO},
                {"WARN", RTMA_LOG_WARNING},    {"WARNING", RTMA_LOG_WARNING},
                {"ERROR", RTMA_LOG_ERROR},     {"CRITICAL", RTMA_LOG_CRITICAL},
                {"OFF", RTMA_LOG_OFF}};

  std::string key = name;
  std::transform(key.begin(), key.end(), key.begin(),
                 [](unsigned char c) { return static_cast<char>(std::toupper(c)); });
  // cc_logger spelled levels with an 'l' prefix (lDEBUG).
  for (int attempt = 0; attempt < 2; ++attempt) {
    for (size_t i = 0; i < sizeof(levels) / sizeof(levels[0]); ++i) {
      if (key == levels[i].name)
        return levels[i].level;
    }
    if (attempt == 0 && key.size() > 1 && key[0] == 'L')
      key.erase(0, 1);
    else
      break;
  }
  throw std::invalid_argument("Unknown log level name: " + name);
}

class RTMA_Logger::State {
public:
  State(RTMA_Module *owner, const std::string &name, int initial_level)
      : module(owner), log_name(name), level(initial_level),
        console_level(initial_level), rtma_level(initial_level),
        file_level(initial_level), console_enabled(true), rtma_enabled(true),
        file_enabled(false), file_initialized(false), console_stream(stderr),
        color_mode(RTMA_COLOR_AUTO), name_is_default(true), file_bytes(0),
        terminal_stream(nullptr), terminal_ready(false) {}

  // Members below must be called with `mutex` held.

  std::string FullName(const std::string &suffix) const {
    return suffix.empty() ? log_name : log_name + "." + suffix;
  }

  bool ColorEnabled() {
    if (color_mode == RTMA_COLOR_NEVER)
      return false;
    if (console_stream != terminal_stream) {
      terminal_stream = console_stream;
      terminal_ready = PrepareTerminal(console_stream);
    }
    return color_mode == RTMA_COLOR_ALWAYS ||
           (terminal_ready && IsTerminal(console_stream));
  }

  void Warn(const std::string &text) {
    if (console_stream == nullptr)
      return;
    try {
      fmt::print(console_stream, "RTMA logger: {}\n", text);
    } catch (...) {
    }
  }

  bool OpenFile() {
    file.clear();
    file.open(log_filename.c_str(), std::ios::out | std::ios::app);
    if (!file.is_open())
      return false;
    file.seekp(0, std::ios::end);
    file_bytes = file.tellp();
    if (file_bytes < 0)
      file_bytes = 0;
    return true;
  }

  void CloseFile() {
    if (file.is_open())
      file.close();
    file.clear();
    file_bytes = 0;
  }

  void DisableFile(const char *reason) {
    CloseFile();
    file_enabled = false;
    file_initialized = false;
    Warn(fmt::format("file logging to '{}' disabled: {}", log_filename, reason));
  }

  void RotateFile() {
    CloseFile();
    const std::string backup1 = log_filename + ".1";
    const std::string backup2 = log_filename + ".2";
    const std::string backup3 = log_filename + ".3";
    std::remove(backup3.c_str());
    std::rename(backup2.c_str(), backup3.c_str());
    std::rename(backup1.c_str(), backup2.c_str());
    std::rename(log_filename.c_str(), backup1.c_str());
  }

  void WriteFile(const std::string &line) {
    if (!file.is_open() && !OpenFile()) {
      DisableFile("cannot open file");
      return;
    }
    const std::streamoff size = static_cast<std::streamoff>(line.size());
    if (file_bytes > 0 && file_bytes + size > kMaxFileBytes) {
      RotateFile();
      if (!OpenFile()) {
        DisableFile("cannot reopen file after rotation");
        return;
      }
    }
    file.write(line.data(), static_cast<std::streamsize>(line.size()));
    file.flush();
    if (!file) {
      DisableFile("write failed");
      return;
    }
    file_bytes += size;
  }

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
  FILE *console_stream;
  RTMA_ConsoleColor color_mode;
  bool name_is_default;
  std::ofstream file;
  std::streamoff file_bytes;
  FILE *terminal_stream;
  bool terminal_ready;
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

void RTMA_Logger::Detach() {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  m_State->module = nullptr;
}

void RTMA_Logger::SetAllLevels(int value) {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  m_State->level = value;
  m_State->console_level = value;
  m_State->rtma_level = value;
  m_State->file_level = value;
}

int RTMA_Logger::GetLevel() const {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  return m_State->level;
}
void RTMA_Logger::SetLevel(int value) {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  m_State->level = value;
}

void RTMA_Logger::SetConsoleLevel(int value) {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  m_State->console_level = value;
  if (value < m_State->level)
    m_State->level = value;
}
int RTMA_Logger::GetConsoleLevel() const {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  return m_State->console_level;
}
void RTMA_Logger::SetRTMALevel(int value) {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  m_State->rtma_level = value;
  if (value < m_State->level)
    m_State->level = value;
}
int RTMA_Logger::GetRTMALevel() const {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  return m_State->rtma_level;
}
void RTMA_Logger::SetFileLevel(int value) {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  m_State->file_level = value;
  if (value < m_State->level)
    m_State->level = value;
}
int RTMA_Logger::GetFileLevel() const {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  return m_State->file_level;
}

void RTMA_Logger::SetConsoleEnabled(bool enabled) {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  m_State->console_enabled = enabled;
}
bool RTMA_Logger::IsConsoleEnabled() const {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  return m_State->console_enabled;
}
void RTMA_Logger::SetRTMAEnabled(bool enabled) {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  m_State->rtma_enabled = enabled;
}
bool RTMA_Logger::IsRTMAEnabled() const {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  return m_State->rtma_enabled;
}
void RTMA_Logger::SetFileEnabled(bool enabled) {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  if (enabled && m_State->log_filename.empty())
    throw RTMA_LoggingConfigurationError("A log filename is required before enabling file logging");
  if (!enabled)
    m_State->CloseFile();
  m_State->file_enabled = enabled;
  m_State->file_initialized = enabled;
}
bool RTMA_Logger::IsFileEnabled() const {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  return m_State->file_enabled;
}

void RTMA_Logger::SetConsoleStream(FILE *stream) {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  m_State->console_stream = stream;
}
FILE *RTMA_Logger::GetConsoleStream() const {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  return m_State->console_stream;
}
void RTMA_Logger::SetConsoleColor(RTMA_ConsoleColor mode) {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  m_State->color_mode = mode;
}
RTMA_ConsoleColor RTMA_Logger::GetConsoleColor() const {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  return m_State->color_mode;
}

void RTMA_Logger::SetLogName(const std::string &name) {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  m_State->log_name = name;
  m_State->name_is_default = false;
}
void RTMA_Logger::SetDefaultLogName(const std::string &name) {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  if (m_State->name_is_default)
    m_State->log_name = name;
}
std::string RTMA_Logger::GetLogName() const {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  return m_State->FullName(m_NameSuffix);
}
void RTMA_Logger::SetLogFilename(const std::string &filename) {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  if (m_State->file_initialized)
    throw RTMA_LoggingConfigurationError("Log filename cannot change after file logging is initialized");
  m_State->log_filename = filename;
}
std::string RTMA_Logger::GetLogFilename() const {
  std::lock_guard<std::mutex> lock(m_State->mutex);
  return m_State->log_filename;
}

void RTMA_Logger::LogMessage(int level, const char *function, const char *file,
                             int line, const std::string &message) {
  MDF_RTMA_LOG data{};
  MSG_TYPE type = MT_RTMA_LOG;
  RTMA_Module *module = nullptr;

  {
    std::lock_guard<std::mutex> lock(m_State->mutex);
    State &state = *m_State;
    if (level < state.level || level >= RTMA_LOG_OFF)
      return;

    const auto now = std::chrono::system_clock::now();
    const double epoch_seconds =
        std::chrono::duration<double>(now.time_since_epoch()).count();
    const std::tm local = LocalTime(std::chrono::system_clock::to_time_t(now));
    const std::string name = state.FullName(m_NameSuffix);
    const std::string source_file = file ? file : "";
    const std::string source_function = function ? function : "";
    const std::string source = fmt::format("{}:{}", Basename(source_file), line);

    if (state.console_enabled && level >= state.console_level) {
      try {
        const bool color = state.ColorEnabled();
        auto paint = [color](const fmt::text_style &style, const std::string &text) {
          return color ? fmt::format(style, "{}", text) : text;
        };
        // Pad before styling so ANSI escapes don't count toward column widths.
        fmt::print(state.console_stream, "{} {} {} {} {}\n",
                   paint(fmt::fg(fmt::color::light_slate_gray),
                         fmt::format("[{:%T}]", local)),
                   paint(LevelStyle(level), fmt::format("{:<8}", LevelName(level))),
                   paint(fmt::fg(fmt::color::khaki),
                         fmt::format("{:<24}", "[" + name + "]")),
                   fmt::format("{:<60}", message),
                   paint(fmt::fg(fmt::color::dim_gray), source));
      } catch (...) {
      }
    }

    if (state.file_enabled && level >= state.file_level) {
      state.WriteFile(fmt::format("{:%F %T} {} [{}] {}\t{}\n", local,
                                  LevelName(level), name, message, source));
    }

    if (state.rtma_enabled && level >= state.rtma_level &&
        state.module != nullptr && !t_in_rtma_send) {
      module = state.module;
      type = MessageTypeForLevel(level);
      data.time = epoch_seconds;
      data.level = level;
      data.lineno = line;
      CopyField(data.name, sizeof(data.name), name);
      CopyField(data.pathname, sizeof(data.pathname), source_file);
      CopyField(data.funcname, sizeof(data.funcname), source_function);
      CopyField(data.message, sizeof(data.message), TruncateMessage(message));
    }
  }

  if (module == nullptr)
    return;

  // Sent without the lock so a slow pipe doesn't stall other logging threads.
  RtmaSendGuard guard;
  try {
    if (module->IsConnected()) {
      CMessage log_message(type, &data, sizeof(data));
      module->SendMessage(&log_message);
    }
  } catch (...) {
    std::lock_guard<std::mutex> lock(m_State->mutex);
    m_State->rtma_enabled = false;
  }
}