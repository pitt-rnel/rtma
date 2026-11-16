// RTMA core definitions.
//
// Mirrors pyrtma's core_defs/rtma_core.yaml: every constant, alias, ID and
// struct there is defined here with the same value or layout, which
// tests/core_types checks. Change both together.
//
// Include RTMA_types.h rather than this file directly.

#ifndef _RTMA_CORE_TYPES_H_
#define _RTMA_CORE_TYPES_H_

#include <stdint.h>

// Constants
#define MAX_MODULES 256         // Most modules connected at once
#define DYN_MOD_ID_START 10000  // First dynamic module ID (10000 to MAX_MODULE_ID)
#define MAX_MODULE_ID 32000
#define MAX_HOSTS 5
#define MAX_MESSAGE_TYPES 10000
#define MAX_RTMA_MSG_TYPE 99    // Message types below 100 are reserved for RTMA core
#define MAX_RTMA_MODULE_ID 9    // Module IDs below 10 are reserved for RTMA core
#define MAX_CONTIGUOUS_MESSAGE_DATA 9000
#define ALL_MESSAGE_TYPES 0x7FFFFFFF // Subscribe to every message type
#define MAX_ACTIVE_CLIENTS 256
#define MAX_SUBSCRIBERS 256
#define MAX_SUBS 256
#define MAX_NAME_LEN 32         // Module name length limit
#define MAX_LOG_LENGTH 1024
#define MESSAGE_TRAFFIC_SIZE 64
#define MAX_MESSAGE_SIZE 65535

// Type aliases
typedef int16_t MODULE_ID;
typedef int16_t HOST_ID;
typedef int32_t MSG_TYPE;
typedef int32_t MSG_COUNT;

// Host IDs
#define HID_LOCAL_HOST 0
#define HID_ALL_HOSTS 0x7FFF

// Module IDs of core modules
#define MID_MESSAGE_MANAGER 0
#define MID_DATA_LOGGER 4
#define MID_QUICK_LOGGER 5

// Header of every message.
//
// msg_type        - Message type ID
// msg_count       - Source message count (per source, starting from 1)
// send_time       - Time at source when message sent
// recv_time       - Time at final destination when message received
// src_host_id     - ID of the host where the message originates
// src_mod_id      - ID of the module where the message originates
// dest_host_id    - ID of the host the message is for (0 for all)
// dest_mod_id     - ID of the module the message is for (0 for all)
// num_data_bytes  - Number of data bytes following this header
// remaining_bytes - Unused
// is_dynamic      - Unused
// reserved        - The message definition's version (its HASH_ value), or 0
//                   if the sender doesn't fill it in
typedef struct {
  MSG_TYPE msg_type;
  MSG_COUNT msg_count;
  double send_time;
  double recv_time;
  HOST_ID src_host_id;
  MODULE_ID src_mod_id;
  HOST_ID dest_host_id;
  MODULE_ID dest_mod_id;
  int32_t num_data_bytes;
  int32_t remaining_bytes;
  int32_t is_dynamic;
  uint32_t reserved;
} RTMA_MSG_HEADER;

// Message types and data

// Sent by MessageManager to modules
#define MT_EXIT 0
#define MT_KILL 1
#define MT_ACKNOWLEDGE 2

// Connect with a module name and process ID
#define MT_CONNECT_V2 4
typedef struct {
  int16_t logger_status;
  int16_t reserved;
  int16_t reserved1;
  MODULE_ID mod_id;
  int32_t pid;
  char name[MAX_NAME_LEN];
} MDF_CONNECT_V2;

// Sent instead of an ACK when a SUBSCRIBE names an invalid message type
#define MT_FAIL_SUBSCRIBE 6
typedef struct {
  MODULE_ID mod_id;
  int16_t reserved;
  MSG_TYPE msg_type;
} MDF_FAIL_SUBSCRIBE;

// Sent by MessageManager when it cannot forward a message to a module
#define MT_FAILED_MESSAGE 8
typedef struct {
  MODULE_ID dest_mod_id;
  int16_t reserved[3];
  double time_of_failure;
  RTMA_MSG_HEADER msg_header;
} MDF_FAILED_MESSAGE;

#define MT_CONNECT 13
typedef struct {
  int16_t logger_status;
  int16_t daemon_status;
} MDF_CONNECT;

#define MT_DISCONNECT 14

#define MT_SUBSCRIBE 15
typedef struct {
  MSG_TYPE msg_type;
} MDF_SUBSCRIBE;

#define MT_UNSUBSCRIBE 16
typedef struct {
  MSG_TYPE msg_type;
} MDF_UNSUBSCRIBE;

#define MT_MODULE_READY 26
typedef struct {
  int32_t pid;
} MDF_MODULE_READY;

// Test connection sent at regular interval to inactive (quiet) clients
#define MT_PING 29
typedef struct {
  MODULE_ID dest_id;
} MDF_PING;

// Test response
#define MT_PONG 30
typedef struct {
  MODULE_ID src_id;
} MDF_PONG;

// MessageManager sends a HELLO for each connected module to the module
// requesting the introduction
#define MT_INTRODUCE 31

// Notification message when a module joins
#define MT_HELLO 32
typedef struct {
  int32_t pid;
  MODULE_ID mod_id;
  uint16_t port;
  char addr[MAX_NAME_LEN];
  char name[MAX_NAME_LEN];
} MDF_HELLO;

// Notification message when a module leaves
#define MT_GOODBYE 33
typedef struct {
  int32_t pid;
  MODULE_ID mod_id;
  uint16_t port;
  char addr[MAX_NAME_LEN];
  char name[MAX_NAME_LEN];
} MDF_GOODBYE;

// Set a module's name after connecting with CONNECT
#define MT_CLIENT_SET_NAME 34
typedef struct {
  char name[MAX_NAME_LEN];
} MDF_CLIENT_SET_NAME;

// Structured client log messages, based on Python's LogRecord. The
// level-specific message types share this payload so clients can subscribe
// at their desired severity.
#define MT_RTMA_LOG 40
#define MT_RTMA_LOG_CRITICAL 41
#define MT_RTMA_LOG_ERROR 42
#define MT_RTMA_LOG_WARNING 43
#define MT_RTMA_LOG_INFO 44
#define MT_RTMA_LOG_DEBUG 45
typedef struct {
  double time;      // time of log (unix time)
  int32_t level;    // 0 NOTSET, 10 DEBUG, 20 INFO, 30 WARNING, 40 ERROR, 50 CRITICAL
  int32_t lineno;   // source code line number where message was logged
  char name[128];   // name of the logger or module
  char pathname[512]; // name of source file
  char funcname[256]; // name of function making log
  char message[MAX_LOG_LENGTH]; // formatted message
} MDF_RTMA_LOG;

typedef MDF_RTMA_LOG MDF_RTMA_LOG_CRITICAL;
typedef MDF_RTMA_LOG MDF_RTMA_LOG_ERROR;
typedef MDF_RTMA_LOG MDF_RTMA_LOG_WARNING;
typedef MDF_RTMA_LOG MDF_RTMA_LOG_INFO;
typedef MDF_RTMA_LOG MDF_RTMA_LOG_DEBUG;

#define MT_FORCE_DISCONNECT 82
typedef struct {
  int32_t mod_id;
} MDF_FORCE_DISCONNECT;

#define MT_PAUSE_SUBSCRIPTION 85
typedef struct {
  MSG_TYPE msg_type;
} MDF_PAUSE_SUBSCRIPTION;

#define MT_RESUME_SUBSCRIPTION 86
typedef struct {
  MSG_TYPE msg_type;
} MDF_RESUME_SUBSCRIPTION;

// Message definition hashes, as pyrtma computes them
#define HASH_EXIT 0x095e0546
#define HASH_KILL 0x82fc702d
#define HASH_ACKNOWLEDGE 0xb725b581
#define HASH_CONNECT_V2 0xec9f6e4b
#define HASH_FAIL_SUBSCRIBE 0xd9c42f25
#define HASH_FAILED_MESSAGE 0x2ede9f3e
#define HASH_CONNECT 0xf4fdcff3
#define HASH_DISCONNECT 0xd0126bf9
#define HASH_SUBSCRIBE 0xd4d36cf2
#define HASH_UNSUBSCRIBE 0x1eb9ad72
#define HASH_MODULE_READY 0xfd0e0311
#define HASH_PING 0xe0f77418
#define HASH_PONG 0x00800232
#define HASH_INTRODUCE 0x6f4769e8
#define HASH_HELLO 0x62c8ac68
#define HASH_GOODBYE 0xa3afbd32
#define HASH_CLIENT_SET_NAME 0x603e34fe
#define HASH_RTMA_LOG 0x3766ee8b
#define HASH_RTMA_LOG_CRITICAL 0x84847fc2
#define HASH_RTMA_LOG_ERROR 0x90e927c3
#define HASH_RTMA_LOG_WARNING 0x755854d8
#define HASH_RTMA_LOG_INFO 0x2b1cb124
#define HASH_RTMA_LOG_DEBUG 0xaa3a1188
#define HASH_FORCE_DISCONNECT 0x335c7bbf
#define HASH_PAUSE_SUBSCRIPTION 0xf58f6ef5
#define HASH_RESUME_SUBSCRIPTION 0x5be0ec3f

// Legacy definitions, not in pyrtma's core definitions. They are kept for
// existing code and may be removed in a later version.

#define MID_QUICKLOGGER MID_QUICK_LOGGER // Old name of MID_QUICK_LOGGER
#define MIN_STREAM_TYPE 9000 // Unused
typedef int32_t UID;         // Unused

// Message header followed by data. Unused.
typedef struct {
  MSG_TYPE msg_type;
  MSG_COUNT msg_count;
  double send_time;
  double recv_time;
  HOST_ID src_host_id;
  MODULE_ID src_mod_id;
  HOST_ID dest_host_id;
  MODULE_ID dest_mod_id;
  int32_t num_data_bytes;
  int32_t remaining_bytes;
  int32_t is_dynamic;
  uint32_t reserved;
  char data[MAX_CONTIGUOUS_MESSAGE_DATA];
} RTMA_MESSAGE;

// Not sent by any module in this repository, and not handled by either
// message manager. pyrtma's message manager drops a client that sends a core
// message type it doesn't define, so do not send these.
#define MT_MM_READY 94
#define MT_SUBSCRIPTION_OPTION 7
typedef struct {
  MSG_TYPE msg_type;
  int32_t option;
  int32_t value;
} MDF_SUBSCRIPTION_OPTION;

#endif // _RTMA_CORE_TYPES_H_
