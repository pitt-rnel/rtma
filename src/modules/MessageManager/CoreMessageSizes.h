// The payload size of each core message type, from the core type headers.
//
// The message manager drops a client that sends a core message (type below
// 100) of another size, or of a type that isn't defined here, as pyrtma's
// manager does. tests/core_types checks this table against pyrtma's core
// definitions.

#ifndef _CORE_MESSAGE_SIZES_H_
#define _CORE_MESSAGE_SIZES_H_

#include <RTMA_types.h>

// Returns the payload size of a core message type, 0 for a signal, or -1 for
// a type that isn't a defined core message.
inline int CoreMessageSize(MSG_TYPE msg_type) {
  switch (msg_type) {
  // core_types.h
  case MT_EXIT:
  case MT_KILL:
  case MT_ACKNOWLEDGE:
  case MT_DISCONNECT:
  case MT_INTRODUCE:
    return 0;
  case MT_CONNECT_V2:
    return sizeof(MDF_CONNECT_V2);
  case MT_FAIL_SUBSCRIBE:
    return sizeof(MDF_FAIL_SUBSCRIBE);
  case MT_FAILED_MESSAGE:
    return sizeof(MDF_FAILED_MESSAGE);
  case MT_CONNECT:
    return sizeof(MDF_CONNECT);
  case MT_SUBSCRIBE:
    return sizeof(MDF_SUBSCRIBE);
  case MT_UNSUBSCRIBE:
    return sizeof(MDF_UNSUBSCRIBE);
  case MT_MODULE_READY:
    return sizeof(MDF_MODULE_READY);
  case MT_PING:
    return sizeof(MDF_PING);
  case MT_PONG:
    return sizeof(MDF_PONG);
  case MT_HELLO:
    return sizeof(MDF_HELLO);
  case MT_GOODBYE:
    return sizeof(MDF_GOODBYE);
  case MT_CLIENT_SET_NAME:
    return sizeof(MDF_CLIENT_SET_NAME);
  case MT_RTMA_LOG:
  case MT_RTMA_LOG_CRITICAL:
  case MT_RTMA_LOG_ERROR:
  case MT_RTMA_LOG_WARNING:
  case MT_RTMA_LOG_INFO:
  case MT_RTMA_LOG_DEBUG:
    return sizeof(MDF_RTMA_LOG);
  case MT_FORCE_DISCONNECT:
    return sizeof(MDF_FORCE_DISCONNECT);
  case MT_PAUSE_SUBSCRIPTION:
    return sizeof(MDF_PAUSE_SUBSCRIPTION);
  case MT_RESUME_SUBSCRIPTION:
    return sizeof(MDF_RESUME_SUBSCRIPTION);

  // quick_logger_types.h
  case MT_LM_EXIT:
  case MT_MESSAGE_LOG_SAVED:
  case MT_PAUSE_MESSAGE_LOGGING:
  case MT_RESUME_MESSAGE_LOGGING:
  case MT_RESET_MESSAGE_LOG:
  case MT_DUMP_MESSAGE_LOG:
  case MT_LM_READY:
    return 0;
  case MT_LM_STATUS:
    return sizeof(MDF_LM_STATUS);
  case MT_SAVE_MESSAGE_LOG:
    return sizeof(MDF_SAVE_MESSAGE_LOG);

  // data_logger_types.h
  case MT_DATA_LOGGER_CONFIG_REQUEST:
  case MT_DATA_LOGGER_RESET:
    return 0;
  case MT_DATASET_STATUS_REQUEST:
    return sizeof(MDF_DATASET_STATUS_REQUEST);
  case MT_DATASET_STATUS:
    return sizeof(MDF_DATASET_STATUS);
  case MT_DATASET_ADD:
    return sizeof(MDF_DATASET_ADD);
  case MT_DATASET_ADDED:
    return sizeof(MDF_DATASET_ADDED);
  case MT_DATASET_REMOVE:
    return sizeof(MDF_DATASET_REMOVE);
  case MT_DATASET_REMOVED:
    return sizeof(MDF_DATASET_REMOVED);
  case MT_DATA_LOGGER_CONFIG:
    return sizeof(MDF_DATA_LOGGER_CONFIG);
  case MT_DATASET_STARTED:
    return sizeof(MDF_DATASET_STARTED);
  case MT_DATASET_STOPPED:
    return sizeof(MDF_DATASET_STOPPED);
  case MT_DATASET_SAVED:
    return sizeof(MDF_DATASET_SAVED);
  case MT_DATASET_START:
    return sizeof(MDF_DATASET_START);
  case MT_DATASET_STOP:
    return sizeof(MDF_DATASET_STOP);
  case MT_DATASET_PAUSE:
    return sizeof(MDF_DATASET_PAUSE);
  case MT_DATASET_RESUME:
    return sizeof(MDF_DATASET_RESUME);
  case MT_DATA_LOGGER_ERROR:
    return sizeof(MDF_DATA_LOGGER_ERROR);
  case MT_DATA_LOG_TEST_2048:
    return sizeof(MDF_DATA_LOG_TEST_2048);

  default:
    return -1;
  }
}

#endif // _CORE_MESSAGE_SIZES_H_
