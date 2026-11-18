#ifndef _MESSAGEMANAGER_H_
#define _MESSAGEMANAGER_H_

#include "RTMA.h"
#include <MyCString.h>
#include <OS_defines.h>
#include <RTMA_types.h>
#include <UPipe.h>
#include <cstdint>
#include <cstdio>
#include <stdlib.h>
#include <string.h>
#include <unordered_map>
#include <unordered_set>
#include <vector>

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
  int32_t pid;
  char *addr;
  char *name;
  // Message types this module subscribes to, ALL_MESSAGE_TYPES among them. The
  // routing table holds a module subscribed to ALL_MESSAGE_TYPES under that
  // type alone.
  std::unordered_set<MSG_TYPE> subs;

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
    subs.clear();
  }

  bool SubAll() const { return subs.count(ALL_MESSAGE_TYPES) != 0; }

  ~CModuleRecord() { Reset(); }
};

// Module IDs subscribed to one message type. The key ALL_MESSAGE_TYPES holds
// the modules subscribed to every type, which no other key holds.
typedef std::unordered_set<MODULE_ID> CSubscriberSet;

class CMessageManager : public UPipeAutoServer {
public:
  CMessageManager();
  ~CMessageManager();

  void MainLoop(char *cmd_line_options);

private:
  MODULE_ID m_NextDynamicModId;
  std::unordered_map<MODULE_ID, CModuleRecord> m_ConnectedModules;
  // The connected module on each pipe. A pipe that hasn't connected has none.
  std::unordered_map<UPipe *, MODULE_ID> m_ModuleByPipe;
  // Only types with subscribers have an entry.
  std::unordered_map<MSG_TYPE, CSubscriberSet> m_Subscribers;
  CMessage m_OutMsg;
  MyCString m_Version;

  MODULE_ID GetDynamicModuleId() {
    for (int attempts = 0; attempts <= MAX_MODULE_ID - DYN_MOD_ID_START; ++attempts) {
      MODULE_ID curr_id = m_NextDynamicModId;
      m_NextDynamicModId = (curr_id == MAX_MODULE_ID)
        ? DYN_MOD_ID_START : curr_id + 1;
      if (!ModuleIsConnected(curr_id))
        return curr_id;
    }
    return 0; // all dynamic IDs are in use
  }

  [[noreturn]] void DropSender(UPipe *pSourcePipe, const char *format, ...);
  // Logs why the module on pSourcePipe is dropped, and throws
  // UPipeClosedException, so that UPipeAutoServer::Run() disconnects it and
  // HandleDisconnect() sends its GOODBYE. Only for the pipe being handled.

  CModuleRecord *GetRecordByPipe(UPipe *pipe);

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

  CModuleRecord *ConnectModule(UPipe *pSourcePipe, MODULE_ID requested_id,
                               short logger_status, int32_t pid,
                               const char *name);
  // Connects the module on pSourcePipe, sends its ACK and HELLO, and returns
  // its record. A refused module is dropped with DropSender().

  CModuleRecord *GetRecord(MODULE_ID module_id);

  void DisconnectModule(MODULE_ID module_id);

  void CleanUpModuleRecord(CModuleRecord *mod);

  void ShutdownModule(MODULE_ID module_id);

  void ShutdownAllModules(int shutdown_RTMA = 1, int shutdown_daemons = 1);

  void AddSubscription(CModuleRecord *mod, MSG_TYPE message_type);

  void RemoveSubscription(CModuleRecord *mod, MSG_TYPE message_type);

  void PauseSubscription(CModuleRecord *mod, MSG_TYPE msg_type_to_pause);

  void ResumeSubscription(CModuleRecord *mod, MSG_TYPE msg_type_to_resume);

  void DropSubscriber(CModuleRecord *mod, MSG_TYPE message_type);

  void Unroute(CModuleRecord *mod, MSG_TYPE message_type);
  // Takes the module out of the routing table for the type, leaving its
  // subscription to it.

  void RemoveAllSubscriptions(CModuleRecord *mod);

  void GetSubscribers(MSG_TYPE message_type, std::vector<MODULE_ID> &ids) const;
  // The modules subscribed to message_type or to ALL_MESSAGE_TYPES. A copy,
  // so that sending to them can't invalidate it.

  void SendAcknowledge(CModuleRecord *mod);

  void SendIntroductions(CModuleRecord *dest_mod);

  void SendHello(CModuleRecord *mod);

  void SendGoodbye(CModuleRecord *mod);

  void SendPing(MODULE_ID mod_id);

  void HandleSetName(CMessage *m, CModuleRecord *mod);

  void HandleForceDisconnect(CMessage *m);

  void HandleModuleReady(CMessage *m, CModuleRecord *mod);

  MSG_TYPE SubscriptionType(CMessage *m);

  void HandleConnect(CMessage *m, UPipe *pSourcePipe);

  void HandleConnectV2(CMessage *m, UPipe *PSourcePipe);

  void UpdateConnection(CMessage *m, CModuleRecord *mod);

  int SendMessage(CMessage *m, CModuleRecord *dest_mod, MODULE_ID dest_mod_id);
  // Sends a message from the manager to dest_mod, with dest_mod_id in its
  // header: the module's ID, or 0 for a broadcast.

  int SendSignal(MSG_TYPE sig, CModuleRecord *dest_mod);
  // dest_mod_id= module id that should be put in dest_mod_id in message header

  int ForwardMessage(CMessage *m, CModuleRecord *mod);

  int ModuleIsConnected(MODULE_ID mod_id) const;

  void LogFailedMessage(CMessage *m, MODULE_ID mod_id);
  // sends a message to logger modules indicating that a message failed to be
  // forwarded to one of the modules
};

#endif //_MESSAGEMANAGER_H_
