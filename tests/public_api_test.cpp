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

  // test message size compatibility
  static_assert(sizeof(MDF_RTMA_LOG) == 1936, "MDF_RTMA_LOG must retain its PyRTMA wire layout");

  return 0;
}
