#ifndef _MESSAGEMANAGER_H_
#define _MESSAGEMANAGER_H_

#include "RTMA.h"
#include "bit_operations.h"
#include <MyCString.h>
#include <OS_defines.h>
#include <RTMA_types.h>
#include <UPipe.h>
#include <cstdint>
#include <cstdio>
#include <list>
#include <malloc.h>
#include <string.h>

#ifdef _WINDOWS_C
#include <Windows.h>
#endif

#ifdef _UNIX_C
#include <limits.h> //where PIPE_BUF is located
#include <pthread.h>
#endif

class CModuleRecord {
public:
  MODULE_ID ModuleID;
  UPipe *pModulePipe;
  short LoggerStatus;
  short DaemonStatus;
  short AllowMultiple;
  uint16_t port;
  int32_t uid;
  int32_t pid;
  char *addr;
  char *name;

  CModuleRecord() {
    name = NULL;
    addr = NULL;
    Reset();
  }

  void SetName(const char *src_name) {
    if (name != NULL) {
      free(name);
      name = NULL;
    }
    name = (char *)malloc(MAX_NAME_LEN);
    if (name != NULL) {
      memset(name, 0, MAX_NAME_LEN);
      if (src_name != NULL) {
        strncpy(name, src_name, MAX_NAME_LEN - 1);
      }
    }
  }

  void SetUPipe(UPipe *pipe) {
    if (addr != NULL) {
      free(addr);
      addr = NULL;
    }

    pModulePipe = pipe;

    port = 0;

    if (pipe == NULL) {
      return;
    }

    addr = (char *)malloc(MAX_NAME_LEN);
    if (addr != NULL) {
      memset(addr, 0, MAX_NAME_LEN);

      if (!pipe->GetIpAddress(addr, &port, MAX_NAME_LEN)) {

        addr[0] = '\0';

        port = 0;
      }
    }
  }

  void SetHello(MDF_HELLO *hello) const {
    if (hello == NULL) {

      return;
    }

    memset(hello, 0, sizeof(*hello));

    hello->uid = uid;
    hello->mod_id = ModuleID;
    hello->pid = pid;
    hello->port = port;

    if (addr != NULL) {
      strncpy(hello->addr, addr, sizeof(hello->addr) - 1);
    }

    if (name != NULL) {
      strncpy(hello->name, name, sizeof(hello->name) - 1);
    }
  }

  void SetGoodbye(MDF_GOODBYE *goodbye) const {
    if (goodbye == NULL) {
      return;
    }
    memset(goodbye, 0, sizeof(*goodbye));
    goodbye->uid = uid;
    goodbye->mod_id = ModuleID;
    goodbye->pid = pid;
    goodbye->port = port;

    if (addr != NULL) {
      strncpy(goodbye->addr, addr, sizeof(goodbye->addr) - 1);
    }

    if (name != NULL) {
      strncpy(goodbye->name, name, sizeof(goodbye->name) - 1);
    }
  }

  void Reset(void) {

    if (name != NULL) {
      free(name);
      name = NULL;
    }

    if (addr != NULL) {
      free(addr);
      addr = NULL;
    }

    ModuleID = -1;

    pModulePipe = NULL;

    LoggerStatus = 0;
    DaemonStatus = 0;
    AllowMultiple = 0;
    port = 0;

    pid = 0;
    uid = -1;
  }

  ~CModuleRecord() { Reset(); }
};

constexpr auto SUBSCRIBER_FLAG_PAUSE = 0x01;

class CSubscriberList {
private:
  struct Subscriber {
    UID uid;
    int flags;
  };

  std::list<Subscriber> m_Subscribers;

public:
  CSubscriberList() {}

  void AddSubscriber(UID uid) {
    m_Subscribers.push_back({uid, 0});
  }

  void RemoveSubscriber(UID uid) {
    for (auto item = m_Subscribers.begin(); item != m_Subscribers.end();) {
      if (item->uid == uid) {
        item = m_Subscribers.erase(item);
      } else {
        ++item;
      }
    }
  }

  void PauseSubscriber(UID uid) {
    for (std::list<Subscriber>::iterator item = m_Subscribers.begin();
         item != m_Subscribers.end(); ++item) {
      if (item->uid == uid) {
        set_flag_bits(item->flags, SUBSCRIBER_FLAG_PAUSE);
        break;
      }
    }
  }

  void ResumeSubscriber(UID uid) {
    for (std::list<Subscriber>::iterator item = m_Subscribers.begin();
         item != m_Subscribers.end(); ++item) {
      if (item->uid == uid) {
        clear_flag_bits(item->flags, SUBSCRIBER_FLAG_PAUSE);
        break;
      }
    }
  }

  // Iterator access for range-based iteration
  std::list<Subscriber>::const_iterator begin() const {
    return m_Subscribers.begin();
  }

  std::list<Subscriber>::const_iterator end() const {
    return m_Subscribers.end();
  }

  // Helper methods to access iterator data
  UID GetUID(std::list<Subscriber>::const_iterator it) const {
    return it->uid;
  }

  bool IsPaused(std::list<Subscriber>::const_iterator it) const {
    return check_flag_bits(it->flags, SUBSCRIBER_FLAG_PAUSE);
  }

  bool IsSubscribed(UID uid) {
    for (std::list<Subscriber>::const_iterator item = m_Subscribers.begin();
         item != m_Subscribers.end(); ++item) {
      if (item->uid == uid) {
        return true;
      }
    }
    return false;
  }
};

class CMessageManager : public UPipeAutoServer {
public:
  CMessageManager();
  ~CMessageManager();

  void MainLoop(char *cmd_line_options);

private:
  MODULE_ID m_NextDynamicModId;
  CModuleRecord m_ConnectedModules[MAX_MODULES];
  CSubscriberList m_SubscribersToMessageType[MAX_MESSAGE_TYPES];
  CSubscriberList m_EmptySubscriberList;
  CMessage m_OutMsg;
  MyCString m_Version;

  MODULE_ID GetDynamicModuleId() {
    MODULE_ID curr_id = m_NextDynamicModId;

    if (curr_id > MAX_MODULE_ID) {
      printf("All dynamic IDs are in use.\n");
      return 0;
    } else {
      // update offset to next available dynamic module ID
      m_NextDynamicModId++;
      return curr_id;
    }
  }

  void HandleData(UPipe *pClientPipe);
  // Override of abstract base class method. Gets called whenever data is ready
  // on any input pipe.

  void HandleDisconnect(UPipe *pClientPipe);
  // Override of virtual base class method to handle unexpected module
  // disconnect cleanly

  void ProcessMessage(CMessage *M, UPipe *pSourcePipe);

  void DistributeMessage(CMessage *M);
  // Forwards the message to all subscribers and Logger modules, without
  // changing the headers

  void DispatchMessage(CMessage *M);
  // Sends the message to all subscribers and Logger modules, headers specifying
  // the message came from MM

  void DispatchMessage(CMessage *M, CModuleRecord *dest_mod);
  // Sends the message only to the specified mod_id and Logger modules, headers
  // specifying the message came from MM

  void DispatchSignal(MSG_TYPE sig, CModuleRecord *dest_mod);
  // Sends the signal only to the specified mod_id and Logger modules, headers
  // specifying the message came from MM

  void DispatchMessageToAll(CMessage *M);
  // Dispatches a message to each connected module (and each Logger module)

  void DispatchSignalToAll(MSG_TYPE sig);
  // Dispatches a signal to each connected module (and each Logger module)

  MODULE_ID
  ConnectModule(MODULE_ID module_id, UPipe *pSourcePipe, short logger_status,
                short daemon_status);

  MODULE_ID
  ConnectModuleV2(MODULE_ID module_id, UPipe *pSourcePipe,
                  MDF_CONNECT_V2 *connect);

  CModuleRecord *GetOpenRecord();

  CModuleRecord *GetRecord(MODULE_ID module_id);

  void DisconnectModule(MODULE_ID module_id);

  void CleanUpModuleRecord(CModuleRecord *mod);

  void ShutdownModule(MODULE_ID module_id);

  void ShutdownAllModules(int shutdown_RTMA = 1, int shutdown_daemons = 1);

  void AddSubscription(CModuleRecord *mod, MSG_TYPE message_type);

  void RemoveSubscription(CModuleRecord *mod, MSG_TYPE message_type);

  void PauseSubscription(CModuleRecord *mod, MSG_TYPE msg_type_to_pause);

  void ResumeSubscription(CModuleRecord *mod, MSG_TYPE msg_type_to_resume);

  CSubscriberList *GetSubscriberList(MSG_TYPE message_type);

  bool IsModuleSubscribed(UID uid, MSG_TYPE message_type);

  void SendAcknowledge(CModuleRecord *mod);

  void SendIntroductions(MODULE_ID mod_id);

  void SendHello(CModuleRecord *mod);

  void SendGoodbye(CModuleRecord *mod);

  void SendPing(MODULE_ID mod_id);

  void HandleSetName(CMessage *m);

  void HandleForceDisconnect(CMessage *m);

  void HandleModuleDisconnect(CMessage *m);

  void HandleModuleReady(CMessage *m);

  void HandleSubscribe(CMessage *m);

  void HandleUnsubscribe(CMessage *m);

  void HandlePauseSubscription(CMessage *m);

  void HandleResumeSubscription(CMessage *m);

  void HandleConnect(CMessage *m, UPipe *pSourcePipe);

  void HandleConnectV2(CMessage *m, UPipe *PSourcePipe);

  int SendMessage(CMessage *m, CModuleRecord *dest_mod);

  int SendSignal(MSG_TYPE sig, CModuleRecord *dest_mod);
  // dest_mod_id= module id that should be put in dest_mod_id in message header

  int ForwardMessage(CMessage *m, CModuleRecord *mod);

  int ModuleIsConnected(MODULE_ID mod_id) const;

  void LogFailedMessage(CMessage *m, MODULE_ID mod_id);
  // sends a message to logger modules indicating that a message failed to be
  // forwarded to one of the modules
};

#endif //_MESSAGEMANAGER_H_
