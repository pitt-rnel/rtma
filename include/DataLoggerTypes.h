#ifndef _DATA_LOGGER_TYPES_H_
#define _DATA_LOGGER_TYPES_H_

// Types from pyrtma data logger

#include <stdint.h>

#define MAX_DATA_SETS 6

// struct defs
typedef struct {
	char name[32];
	char sub_dir_fmt[128];
	char file_name_fmt[128];
	char formatter[32];
	int32_t subdivide_interval;
	int32_t msg_types[32];
} DATA_SET;

typedef struct {
	char name[32];
	char base_path[256];
	char dir_fmt[128];
	int16_t num_data_sets;
	int16_t unused;
	DATA_SET data_sets[MAX_DATA_SETS];
} DATA_COLLECTION;

typedef struct {
	char name[32];
	char formatter[32];
	char save_path[256];
	int32_t subdivide_interval;
	int32_t msg_types[32];
} DATA_SET_INFO;

typedef struct {
	char name[32];
	char save_path[256];
	int16_t num_data_sets;
	int16_t unused;
	DATA_SET data_sets[MAX_DATA_SETS];
} DATA_COLLECTION_INFO;

// message defs

#define MT_DATA_LOGGER_STATUS 62
typedef struct {
	double timestamp;
	double elapsed_time;
	int32_t is_recording;
	int32_t is_paused;
} MDF_DATA_LOGGER_STATUS;

#define MT_DATA_LOGGER_STATUS_REQUEST 63

#define MT_ADD_DATA_COLLECTION 64
typedef struct { DATA_COLLECTION collection; } MDF_ADD_DATA_COLLECTION;

#define MT_REMOVE_DATA_COLLECTION 65
typedef struct { char collection_name[32]; } MDF_REMOVE_DATA_COLLECTION;

#define MT_ADD_DATA_SET 66
typedef struct {
	char collection_name[32];
	char name[32];
} MDF_ADD_DATA_SET;

#define MT_REMOVE_DATA_SET 67
typedef MDF_ADD_DATA_SET MDF_REMOVE_DATA_SET;

#define MT_DATA_COLLECTION_CONFIG_REQUEST 68
#define MT_DATA_COLLECTION_CONFIG 69
typedef MDF_ADD_DATA_COLLECTION MDF_DATA_COLLECTION_CONFIG;

#define MT_DATA_COLLECTION_STARTED 70
typedef struct { DATA_COLLECTION_INFO collection; } MDF_DATA_COLLECTION_STARTED;

#define MT_DATA_COLLECTION_STOPPED 71
typedef MDF_DATA_COLLECTION_STARTED MDF_DATA_COLLECTION_STOPPED;

#define MT_DATA_COLLECTION_SAVED 72
#define MT_DATA_LOGGER_START 73
#define MT_DATA_LOGGER_STOP 74
#define MT_DATA_LOGGER_PAUSE 75
#define MT_DATA_LOGGER_RESUME 76
#define MT_DATA_LOGGER_RESET 77
#define MT_DATA_LOGGER_ERROR 78
typedef struct { char msg[512]; } MDF_DATA_LOGGER_ERROR;

#define MT_DATA_LOGGER_METADATA_UPDATE 79
typedef struct { char json[512]; } MDF_DATA_LOGGER_METADATA_UPDATE;

#define MT_DATA_LOGGER_METADATA_REQUEST 87
#define MT_DATA_LOGGER_METADATA 88
typedef struct { char json[1024]; } MDF_DATA_LOGGER_METADATA;

#define MT_DATA_LOG_TEST_2048 89
typedef struct { char raw[2048]; } MDF_DATA_LOG_TEST_2048;

#endif