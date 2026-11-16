// Definitions for the pyrtma data logger.
//
// The data logger is part of pyrtma and has no C++ implementation. These
// definitions let C++ modules control it and read its replies: it answers
// requests that are addressed to MID_DATA_LOGGER, or broadcast.
//
// Mirrors pyrtma's core_defs/data_logger.yaml: every constant, struct and
// message there is defined here with the same value or layout, which
// tests/core_types checks. Change both together.
//
// Include RTMA_types.h rather than this file directly.

#ifndef _RTMA_DATA_LOGGER_TYPES_H_
#define _RTMA_DATA_LOGGER_TYPES_H_

#include <stdint.h>

// Constants
#define MAX_DATASETS 6
#define DATASET_NAME_LEN 32
#define DATASET_MAX_SIZE_MB 500 // Largest allowed DATASET max_size_mb

// Struct definitions
typedef struct {
  char name[DATASET_NAME_LEN];
  char save_path[256];   // Dataset save directory
  char filename[128];    // Dataset saved file name without the file extension
  char formatter[32];    // Builtin options: quicklogger, json, raw, msg_header
  int32_t max_size_mb;   // Largest file in MB (1 to DATASET_MAX_SIZE_MB); a full
                         // file continues in a new one
  int32_t msg_types[64]; // Message type IDs passed to the dataset formatter
} DATASET;

// Message types and data

#define MT_DATASET_STATUS_REQUEST 62
typedef struct {
  char name[DATASET_NAME_LEN];
} MDF_DATASET_STATUS_REQUEST;

#define MT_DATASET_STATUS 63
typedef struct {
  char name[DATASET_NAME_LEN];
  double timestamp;
  double elapsed_time;
  int32_t is_recording;
  int32_t is_paused;
} MDF_DATASET_STATUS;

#define MT_DATASET_ADD 64
typedef struct {
  DATASET dataset;
} MDF_DATASET_ADD;

#define MT_DATASET_ADDED 65
typedef struct {
  char name[DATASET_NAME_LEN];
} MDF_DATASET_ADDED;

#define MT_DATASET_REMOVE 66
typedef struct {
  char name[DATASET_NAME_LEN];
} MDF_DATASET_REMOVE;

#define MT_DATASET_REMOVED 67
typedef struct {
  char name[DATASET_NAME_LEN];
} MDF_DATASET_REMOVED;

#define MT_DATA_LOGGER_CONFIG_REQUEST 68

#define MT_DATA_LOGGER_CONFIG 69
typedef struct {
  int32_t num_datasets;
  DATASET datasets[6];
} MDF_DATA_LOGGER_CONFIG;

#define MT_DATASET_STARTED 70
typedef struct {
  char name[DATASET_NAME_LEN];
} MDF_DATASET_STARTED;

#define MT_DATASET_STOPPED 71
typedef struct {
  char name[DATASET_NAME_LEN];
} MDF_DATASET_STOPPED;

#define MT_DATASET_SAVED 72
typedef struct {
  char name[DATASET_NAME_LEN];
  char filepath[1024];
} MDF_DATASET_SAVED;

#define MT_DATASET_START 73
typedef struct {
  char name[DATASET_NAME_LEN];
} MDF_DATASET_START;

#define MT_DATASET_STOP 74
typedef struct {
  char name[DATASET_NAME_LEN];
} MDF_DATASET_STOP;

#define MT_DATASET_PAUSE 75
typedef struct {
  char name[DATASET_NAME_LEN];
} MDF_DATASET_PAUSE;

#define MT_DATASET_RESUME 76
typedef struct {
  char name[DATASET_NAME_LEN];
} MDF_DATASET_RESUME;

#define MT_DATA_LOGGER_RESET 77

#define MT_DATA_LOGGER_ERROR 78
typedef struct {
  char dataset_name[DATASET_NAME_LEN];
  char exc_type[64];
  char msg[512];
} MDF_DATA_LOGGER_ERROR;

#define MT_DATA_LOG_TEST_2048 79
typedef struct {
  char raw[2048];
} MDF_DATA_LOG_TEST_2048;

// Message definition hashes, as pyrtma computes them
#define HASH_DATASET_STATUS_REQUEST 0x6b13e892
#define HASH_DATASET_STATUS 0x5ce37a06
#define HASH_DATASET_ADD 0xa90bcee9
#define HASH_DATASET_ADDED 0x4473eef7
#define HASH_DATASET_REMOVE 0xd3110ef2
#define HASH_DATASET_REMOVED 0x0d497a31
#define HASH_DATA_LOGGER_CONFIG_REQUEST 0x91598f0a
#define HASH_DATA_LOGGER_CONFIG 0xeae8779d
#define HASH_DATASET_STARTED 0xe73fb9e1
#define HASH_DATASET_STOPPED 0x541af8e5
#define HASH_DATASET_SAVED 0x8d5f717f
#define HASH_DATASET_START 0x43da6ed3
#define HASH_DATASET_STOP 0xd6a54f5f
#define HASH_DATASET_PAUSE 0xef6bb58f
#define HASH_DATASET_RESUME 0x66f28be7
#define HASH_DATA_LOGGER_RESET 0x1eb32beb
#define HASH_DATA_LOGGER_ERROR 0x75fc60cf
#define HASH_DATA_LOG_TEST_2048 0x6f24b1d1

#endif // _RTMA_DATA_LOGGER_TYPES_H_
