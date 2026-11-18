// Definitions for the C++ QuickLogger module.
//
// Mirrors pyrtma's core_defs/quick_logger.yaml: every constant and message
// there is defined here with the same value or layout, which tests/core_types
// checks. Change both together.
//
// Include RTMA_types.h rather than this file directly.

#ifndef _RTMA_QUICK_LOGGER_TYPES_H_
#define _RTMA_QUICK_LOGGER_TYPES_H_

#include <stdint.h>

// Constants
#define MAX_LOGGER_FILENAME_LENGTH 256

// Message types and data

#define MT_LM_STATUS 54
typedef struct {
  uint32_t is_logging;
  uint32_t max_msgs;
  uint32_t hdr_bufsz;
  uint32_t data_bufsz;
  uint32_t msg_count;
  uint32_t hdr_total;
  uint32_t data_total;
  uint32_t ofs_total;
} MDF_LM_STATUS;

// Tells QuickLogger to exit
#define MT_LM_EXIT 55

// Tells QuickLogger to save its message buffer to the named file
#define MT_SAVE_MESSAGE_LOG 56
typedef struct {
  char pathname[MAX_LOGGER_FILENAME_LENGTH]; // File path name where to save data
  int32_t pathname_length;                   // Number of characters in path name
} MDF_SAVE_MESSAGE_LOG;

// Sent by QuickLogger once it has saved the file
#define MT_MESSAGE_LOG_SAVED 57

// Tells QuickLogger to stop adding incoming messages to the log until
// further notice
#define MT_PAUSE_MESSAGE_LOGGING 58
#define MT_RESUME_MESSAGE_LOGGING 59
#define MT_RESET_MESSAGE_LOG 60
#define MT_DUMP_MESSAGE_LOG 61

// Sent by QuickLogger when it has finished initializing and is ready
#define MT_LM_READY 96

// Message definition hashes, as pyrtma computes them
#define HASH_LM_STATUS 0x2da5b6a1
#define HASH_LM_EXIT 0x35dd547b
#define HASH_SAVE_MESSAGE_LOG 0x67637e79
#define HASH_MESSAGE_LOG_SAVED 0x66e84ae5
#define HASH_PAUSE_MESSAGE_LOGGING 0x20c1e922
#define HASH_RESUME_MESSAGE_LOGGING 0x0d1a3e77
#define HASH_RESET_MESSAGE_LOG 0x68ec4aab
#define HASH_DUMP_MESSAGE_LOG 0xf9d7e2bf
#define HASH_LM_READY 0x4863b960

#endif // _RTMA_QUICK_LOGGER_TYPES_H_
