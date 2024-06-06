#ifndef _RTMA_TYPES_H_ // this is commented out becuase make_config fails with it
#define _RTMA_TYPES_H_

// Sized integer types (added with pyrtma v2.3 updates)
#include <stdint.h>

#include "DataLoggerTypes.h" // new from pyrtma v2.3

// Types used in the RTMA system

typedef int16_t MODULE_ID;
typedef int16_t HOST_ID;
typedef int32_t MSG_TYPE;
typedef int32_t MSG_COUNT;

// Maximums for the entire RTMA system
#define MAX_MODULES       200  //maximal number of modules in the system
#define DYN_MOD_ID_START  100  //module ID where pool of dynamic IDs begin
#define MAX_HOSTS         5    //maximal number of hosts in the system
#define MAX_MESSAGE_TYPES 10000 //maximal number of message types in the system

// new constants from pyrtma v2.3 core_defs.yaml
#define MAX_ACTIVE_CLIENTS 256
#define MAX_SUBSCRIBERS 256
#define MAX_SUBS 256
#define MAX_NAME_LEN 32
#define MAX_LOG_LENGTH 1024
#define MESSAGE_TRAFFIC_SIZE 64
#define MAX_MESSAGE_SIZE 65535

// Maximums for core modules
#define MAX_RTMA_MSG_TYPE  99 // Message types below 100 are reserved for RTMA core
#define MAX_RTMA_MODULE_ID  9 // Module ID-s below 10 are reserved for RTMA core

// Header fields for all messages passed through RTMA
// Following macro was commented out for compatibility with ctypesgen2 v2.2.2 python package (used for Python3 compatiblity) All references to this macro in this file and in RTMA.h were replaced with actual values
//#define RTMA_MSG_HEADER_FIELDS \
//	MSG_TYPE	msg_type; \
//	MSG_COUNT	msg_count; \
//	double	send_time; \
//	double	recv_time; \
//	HOST_ID		src_host_id; \
//	MODULE_ID	src_mod_id; \
//	HOST_ID		dest_host_id; \
//	MODULE_ID	dest_mod_id; \
//	int			num_data_bytes; \
//	int			remaining_bytes; \
//	int			is_dynamic; \
//	int			reserved
// msg_type - Message type ID
// msg_count - Source message count (per source, starting from 1)
// send_time - Time at source when message sent (Seconds since 0:00:00 on Jan 1, 1970)
// recv_time - Time at final destination when message received (Seconds since 0:00:00 on Jan 1, 1970)
// src_host_id - ID number of the host computer where the message originates
// src_mod_id - ID number of the program module where the message originates
// dest_host_id - ID number of the host computer intended to receive this message
// dest_mod_id - ID number of the module ID intended to receive this message
// num_data_bytes - Number of data bytes following this header
// remaining_bytes - If message data is too large to fit in one message, then this value is non-zero
//                   and represents the number of data bytes still to follow in subsequent messages
// is_dynamic - if true, then message data is a serialized form of Dynamic Data.
// reserved - for 64-bit alignment (if you ever change the fields, remember they have to be
//	          16-, 32- and 64-bit aligned, i.e. no single field crosses a 2-, 4-, or 8-byte boundary)

// Header for messages passed through RTMA
typedef struct {
	MSG_TYPE	msg_type; // previously RTMA_MSG_HEADER_FIELDS; (changed for python compatibility)
	MSG_COUNT	msg_count;
	double	send_time;
	double	recv_time;
	HOST_ID		src_host_id;
	MODULE_ID	src_mod_id;
	HOST_ID		dest_host_id;
	MODULE_ID	dest_mod_id;
	int32_t		num_data_bytes;
	int32_t		remaining_bytes;
	int32_t		is_dynamic;
	int32_t		reserved;
} RTMA_MSG_HEADER;

#define MAX_CONTIGUOUS_MESSAGE_DATA 9000

typedef struct {
	MSG_TYPE	msg_type; // previously RTMA_MSG_HEADER_FIELDS; (changed for python compatibility)
	MSG_COUNT	msg_count;
	double	send_time;
	double	recv_time;
	HOST_ID		src_host_id;
	MODULE_ID	src_mod_id;
	HOST_ID		dest_host_id;
	MODULE_ID	dest_mod_id;
	int32_t		num_data_bytes;
	int32_t		remaining_bytes;
	int32_t		is_dynamic;
	int32_t		reserved;
	char data[MAX_CONTIGUOUS_MESSAGE_DATA];
} RTMA_MESSAGE;


// Module ID-s of core modules
#define MID_MESSAGE_MANAGER     0
#define MID_DATA_LOGGER         4
#define MID_QUICKLOGGER         5

#define HID_LOCAL_HOST  0
#define HID_ALL_HOSTS   0x7FFF

typedef char STRING_DATA[];   //message data type for variable length string messages

// Used for subscribing to all message types
#define ALL_MESSAGE_TYPES  0x7FFFFFFF

// Messages sent by MessageManager to modules
#define MT_EXIT            0
#define MT_KILL			   1
#define MT_ACKNOWLEDGE     2
#define MT_CONNECT_V2      4 // new from pyrtma v2.3
typedef struct {
	int16_t logger_status;
	int16_t daemon_status;
	int16_t allow_multiple;
	MODULE_ID mod_id;
	int32_t pid;
	char name[MAX_NAME_LEN];
} MDF_CONNECT_V2;

#define MT_FAIL_SUBSCRIBE  6
typedef struct { 
	MODULE_ID mod_id; 
	int16_t reserved; 
	MSG_TYPE msg_type;
} MDF_FAIL_SUBSCRIBE;

#define MT_FAILED_MESSAGE  8 // Sent by MM when it cannot forward a message to a module
typedef struct { 
	MODULE_ID dest_mod_id;
	int16_t reserved[3];
	double time_of_failure;
	RTMA_MSG_HEADER msg_header;
} MDF_FAILED_MESSAGE;
// Messages sent by modules to MessageManager
#define MT_CONNECT         13

typedef struct {
	int16_t logger_status;
	int16_t daemon_status;
} MDF_CONNECT;
#define MT_DISCONNECT     14

// Subscription messages
#define MT_SUBSCRIBE      15
typedef MSG_TYPE MDF_SUBSCRIBE;
#define MT_UNSUBSCRIBE    16
typedef MSG_TYPE MDF_UNSUBSCRIBE;

//Messages sent by all modules
#define MT_MODULE_READY   26
typedef struct { int pid; } MDF_MODULE_READY;

// New types from pyrtma v2.3 core types
#define MT_MESSAGE_TRAFFIC 30
typedef struct {
	uint32_t seqno;
	uint32_t sub_seqno;
	double start_timestamp;
	double end_timestamp;
	MSG_TYPE msg_type[MESSAGE_TRAFFIC_SIZE];
	uint16_t msg_count[MESSAGE_TRAFFIC_SIZE];
} MDF_MESSAGE_TRAFFIC;

#define MT_ACTIVE_CLIENTS 31
typedef struct {
	double timestamp;
	int16_t num_clients;
	int16_t padding;
	int32_t reserved;
	MODULE_ID client_mod_id[MAX_ACTIVE_CLIENTS];
	int32_t client_pid[MAX_ACTIVE_CLIENTS];
} MDF_ACTIVE_CLIENTS;

#define MT_CLIENT_INFO 32
typedef struct {
	char addr[32];
	int32_t uid;
	int32_t pid;
	MODULE_ID mod_id;
	int16_t is_logger;
	int16_t is_unique;
	uint16_t port;
	char name[MAX_NAME_LEN];
} MDF_CLIENT_INFO;

#define MT_CLIENT_CLOSED 33
typedef MDF_CLIENT_INFO MDF_CLIENT_CLOSED;

#define MT_CLIENT_SET_NAME 34
typedef struct { char name[MAX_NAME_LEN]; } MDF_CLIENT_SET_NAME;

#define MT_RTMA_LOG 40
typedef struct {
	double time;
	int32_t level;
	int32_t lineno;
	char name[128];
	char pathname[512];
	char funcname[256];
	char message[MAX_LOG_LENGTH];
} MDF_RTMA_LOG;

#define MT_RTMA_LOG_CRITICAL 41
typedef MDF_RTMA_LOG MDF_RTMA_LOG_CRITICAL;
#define MT_RTMA_LOG_ERROR 42
typedef MDF_RTMA_LOG MDF_RTMA_LOG_ERROR;
#define MT_RTMA_LOG_WARNING 43
typedef MDF_RTMA_LOG MDF_RTMA_LOG_WARNING;
#define MT_RTMA_LOG_INFO 44
typedef MDF_RTMA_LOG MDF_RTMA_LOG_INFO;
#define MT_RTMA_LOG_DEBUG 45
typedef MDF_RTMA_LOG MDF_RTMA_LOG_DEBUG;

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

//Messages sent to LoggerModule
#define MT_LM_EXIT        55

// Messages for QuickLogger Module
// MT_SAVE_MESSAGE_LOG - Tells QuickLogger to dump its current message buffer
// to the named file
#define MT_SAVE_MESSAGE_LOG        56
#define MAX_LOGGER_FILENAME_LENGTH    256
typedef struct {
	char pathname[MAX_LOGGER_FILENAME_LENGTH];  // File path name where to save data
	int32_t pathname_length;                 // Number of characters in path name
} MDF_SAVE_MESSAGE_LOG;

// Response to MT_MESSAGE_LOG_SAVED after QuickLogger has saved the file
#define MT_MESSAGE_LOG_SAVED       57
// MT_PAUSE_MESSAGE_LOGGING - Tells QuickLogger to not put incoming messages
// in the log until further notice
#define MT_PAUSE_MESSAGE_LOGGING   58
#define MT_RESUME_MESSAGE_LOGGING  59
#define MT_RESET_MESSAGE_LOG       60
#define MT_DUMP_MESSAGE_LOG        61

#define MT_TIMING_MESSAGE          80
typedef struct {
	uint16_t timing[MAX_MESSAGE_TYPES];
	int32_t ModulePID[MAX_MODULES]; //0 if not connected
	double send_time;
} MDF_TIMING_MESSAGE;

#define MT_FORCE_DISCONNECT 82
typedef struct { int32_t mod_id; } MDF_FORCE_DISCONNECT;

#define MT_MM_ERROR         83
typedef STRING_DATA MDF_MM_ERROR;
#define MT_MM_INFO          84
typedef STRING_DATA MDF_MM_INFO;
#define MT_PAUSE_SUBSCRIPTION   85
#define MT_RESUME_SUBSCRIPTION  86
typedef MSG_TYPE MDF_PAUSE_SUBSCRIPTION;
typedef MSG_TYPE MDF_RESUME_SUBSCRIPTION;

#define MT_DEBUG_TEXT     91
typedef STRING_DATA MDF_DEBUG_TEXT;

// Messages sent by core modules when they have finished initializing and are ready to serve
#define MT_LM_READY             96

#endif //_RTMA_TYPES_H_
