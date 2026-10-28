#include <RTMA.h>
#include <RTMA_Logger.h>
#include <RTMA_types.h>

#include <cstdio>
#include <memory>
#include <string>
#include <thread>
#include <vector>

namespace {

bool FileExists(const std::string &path) {
  FILE *f = std::fopen(path.c_str(), "rb");
  if (f == nullptr)
    return false;
  std::fclose(f);
  return true;
}

int TestChildOutlivesModule() {
  std::unique_ptr<RTMA_Logger> child;
  {
    RTMA_Module temp(7, 0);
    temp.Logger().SetConsoleEnabled(false);
    child.reset(new RTMA_Logger(temp.Logger().Child("kid")));
  }
  child->info(RTMA_LOG_SOURCE, "logged after the module is gone");
  return child->GetLogName() == "Module 7.kid" ? 0 : 1;
}

int TestFileRotation() {
  const std::string path = "rtma_rotation_test.log";
  for (const char *suffix : {"", ".1", ".2", ".3", ".4"})
    std::remove((path + suffix).c_str());

  RTMA_Module module(8, 0);
  RTMA_Logger &logger = module.Logger();
  logger.SetConsoleEnabled(false);
  logger.SetRTMAEnabled(false);
  logger.SetLogFilename(path);
  logger.SetFileEnabled(true);

  const std::string text(1000, 'x');
  for (int i = 0; i < 11000; ++i)
    logger.info(RTMA_LOG_SOURCE, "{}", text);
  logger.SetFileEnabled(false);

  const bool ok = FileExists(path) && FileExists(path + ".1") &&
                  FileExists(path + ".2") && FileExists(path + ".3") &&
                  !FileExists(path + ".4");
  for (const char *suffix : {"", ".1", ".2", ".3"})
    std::remove((path + suffix).c_str());
  return ok ? 0 : 1;
}

int TestConsoleStreamAndTruncation() {
  FILE *capture = std::tmpfile();
  if (capture == nullptr)
    return 1;

  RTMA_Module module(9, 0);
  RTMA_Logger &logger = module.Logger();
  logger.SetRTMAEnabled(false);
  logger.SetConsoleStream(capture);
  logger.SetConsoleColor(RTMA_COLOR_NEVER);
  logger.info(RTMA_LOG_SOURCE, "{}", std::string(2000, 'y'));
  logger.SetConsoleStream(stderr);

  std::fflush(capture);
  std::rewind(capture);
  std::string out;
  char buffer[4096];
  size_t n;
  while ((n = std::fread(buffer, 1, sizeof(buffer), capture)) > 0)
    out.append(buffer, n);
  std::fclose(capture);

  return out.size() >= 2000 && out.find('\x1b') == std::string::npos ? 0 : 1;
}

int TestThreadedLogging() {
  RTMA_Module module(10, 0);
  RTMA_Logger &logger = module.Logger();
  logger.SetConsoleEnabled(false);
  logger.SetRTMAEnabled(false);

  std::vector<std::thread> threads;
  for (int t = 0; t < 4; ++t)
    threads.emplace_back([&logger]() {
      for (int i = 0; i < 200; ++i)
        logger.info(RTMA_LOG_SOURCE, "message {}", i);
    });
  for (int i = 0; i < 200; ++i) {
    logger.SetAllLevels(i % 2 ? RTMA_LOG_DEBUG : RTMA_LOG_INFO);
    logger.SetLogName("thread-test");
    logger.GetLogName();
  }
  for (std::thread &thread : threads)
    thread.join();
  return 0;
}

} // namespace

int main() {
  CMessage message;
  if (message.IsDynamic())
    return 1;

  RTMA_Module module(99, 0);
  RTMA_Logger &logger = module.Logger();
  logger.SetConsoleEnabled(true);
  logger.SetRTMAEnabled(false);
  if (logger.GetConsoleStream() != stderr || logger.GetConsoleColor() != RTMA_COLOR_AUTO)
    return 1;
  logger.SetConsoleStream(stdout);
  logger.SetConsoleColor(RTMA_COLOR_ALWAYS);
  if (RTMA_LevelFromName("lwarn") != RTMA_LOG_WARNING ||
      RTMA_LevelFromName("Critical") != RTMA_LOG_CRITICAL)
    return 1;
  try {
    RTMA_LevelFromName("bogus");
    return 1;
  } catch (const std::invalid_argument &) {
  }
  module.info(RTMA_LOG_SOURCE, "client logger forwarding works");
  logger.SetLogFilename("rtma_public_api_test.log");
  logger.SetFileEnabled(true);
  logger.SetAllLevels(RTMA_LOG_DEBUG);
  logger.debug(RTMA_LOG_SOURCE, "public API test {}", 1);
  logger.warning(RTMA_LOG_SOURCE, "warning test");
  logger.error(RTMA_LOG_SOURCE, "error test");

  try {
    logger.SetLogFilename("other.log");
    return 1;
  } catch (const RTMA_LoggingConfigurationError &) {
  }

  logger.SetFileEnabled(false);
  logger.SetLogFilename("other.log");

  RTMA_Module named(5, 0);
  named.Logger().SetLogName("Custom");
  named.InitVariables(6, 0);
  named.Logger().SetDefaultLogName("Module 6");
  if (named.Logger().GetLogName() != "Custom")
    return 1;

  if (TestChildOutlivesModule() || TestFileRotation() ||
      TestConsoleStreamAndTruncation() || TestThreadedLogging())
    return 1;

  // test message size compatibility
  static_assert(sizeof(MDF_RTMA_LOG) == 1936, "MDF_RTMA_LOG must retain its PyRTMA wire layout");

  return 0;
}
