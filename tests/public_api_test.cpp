#include <RTMA.h>
#include <RTMA_Logger.h>
#include <RTMA_types.h>

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

  // test message size compatibility
  static_assert(sizeof(MDF_RTMA_LOG) == 1936, "MDF_RTMA_LOG must retain its PyRTMA wire layout");

  return 0;
}
