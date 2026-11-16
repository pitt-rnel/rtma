/*
 *  MessageManager - Receives and distributes RTMA messages to/from modules
 *
 *  Meel Velliste 10/28/2008
 *  Emrah Diril  10/14/2011
 *  Jeff Weiss: 09/10/2014 (merged HST RTMA (v2.00) with updates from Dragonfly
 * v2.10)
 */

#include "MessageManager.h"
#include "CoreMessages.h"
#include "Debug.h"
#include <MyCException.h>
#include <OS_defines.h>
#include <RTMA.h>
#include <RTMA_types.h>
#include <Timing.h>
#include <UPipe.h>
#include <cstdarg>
#include <cstdio>
#include <string.h>
#include <vector>

#ifdef _WINDOWS_C
#include <Windows.h>
#endif

#ifdef _UNIX_C
int main(int argc, char *argv[])
#else
int main(int argc, char *argv[])
#endif
{
  try {
    char *options;
    char empty_str[] = "";
    options = (argc > 1) ? argv[1] : empty_str;

    CMessageManager *MM = new CMessageManager();
    MM->MainLoop(options);
    delete MM;
    return 0;
  } catch (MyCException &E) {
    E.AddToStack("MM WinMain- aborting");
    E.ReportToFile();
    MyCString err("MessageManager: fatal error:");
    E.AppendTraceToString(err);
    fprintf(stderr, "%s\n", err.GetContent());
    return 1;
  }
}

CMessageManager::CMessageManager() {
  m_Version = "4.0.0";
  m_NextDynamicModId = DYN_MOD_ID_START;

  InitializeAbsTime();
}

CMessageManager::~CMessageManager() {}

void CMessageManager::MainLoop(char *cmd_line_options) {
  try {
    printf("RTMA MessageManager %s\n", m_Version.GetContent());
    DEBUG_TEXT("Entering Main Loop");

    // Elevate process priority
#ifdef _WINDOWS_C
    BOOL success =
        SetPriorityClass(GetCurrentProcess(), REALTIME_PRIORITY_CLASS);
    // if( success) printf("Yay!\n");
    // else printf("Too bad!\n");
    success =
        SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_TIME_CRITICAL);
    // if( success) printf("Yay!\n");
    // else printf("Too bad!\n");
#endif
    // Start managing messages
    if (strlen(cmd_line_options) > 0) {
      char *server_name = cmd_line_options;
      UPipeAutoServer::Run(server_name);
    } else {
      UPipeAutoServer::Run(DEFAULT_PIPE_SERVER_NAME_FOR_MM);
    }

    DEBUG_TEXT("Main Loop Finished");
  } catch (MyCException &E) {
    E.AddToStack("CMessageManager::MainLoop()");
    throw E;
  }
}

CModuleRecord *CMessageManager::GetRecordByPipe(UPipe *pipe) {
  auto it = m_ModuleByPipe.find(pipe);
  if (it == m_ModuleByPipe.end())
    return NULL;
  return GetRecord(it->second);
}

void CMessageManager::DropSender(UPipe *pSourcePipe, const char *format, ...) {
  char reason[512];
  va_list args;
  va_start(args, format);
  vsnprintf(reason, sizeof(reason), format, args);
  va_end(args);

  CModuleRecord *mod = GetRecordByPipe(pSourcePipe);
  char addr[MAX_NAME_LEN] = "";
  uint16_t port = 0;
  try {
    pSourcePipe->GetIpAddress(addr, &port, sizeof(addr));
  } catch (...) {
  }
  if (mod != NULL)
    fprintf(stderr, "DROPPING - module %d (%s:%u) - %s\n", mod->ModuleID,
            addr, port, reason);
  else
    fprintf(stderr, "DROPPING - %s:%u - %s\n", addr, port, reason);
  throw UPipeClosedException(reason);
}

void CMessageManager::HandleData(UPipe *pSourcePipe) {
  SetMyPriority(THIS_MODULE_BASE_PRIORITY);
  DEBUG_TEXT_("Receiving message from pipe " << pSourcePipe << "... ");
  CMessage M;
  int status;
  try {
    status = M.Receive(pSourcePipe);
  } catch (UPipeClosedException &) {
    throw;
  } catch (MyCException &E) {
    MyCString err;
    E.AppendTraceToString(err);
    DropSender(pSourcePipe, "Failed to read a message: %s", err.GetContent());
  }
  if (status == -3)
    DropSender(pSourcePipe,
               "Invalid num_data_bytes (%d) for MT=%d; it must be 0 to %d. "
               "Header may be corrupted.",
               M.num_data_bytes, M.msg_type, RTMA_MAX_DATA_BYTES);
  if (status < 0)
    DropSender(pSourcePipe, "Failed to read a message (status %d)", status);
  DEBUG_TEXT("Received message of type " << M.msg_type);

  // Core messages must match their definitions, as in pyrtma's manager. A
  // client whose core definitions don't match the manager's is dropped
  // before its message is acted on or forwarded.
  if (M.msg_type <= MAX_RTMA_MSG_TYPE) {
    int expected = CoreMessageSize(M.msg_type);
    if (expected < 0)
      DropSender(pSourcePipe, "Unknown core message type MT=%d received.",
                 M.msg_type);
    if (M.num_data_bytes != expected)
      DropSender(pSourcePipe,
                 "MT=%d announced %d data bytes, but its core definition has "
                 "%d. The client's core definitions don't match the "
                 "manager's.",
                 M.msg_type, M.num_data_bytes, expected);
  }

  // Failures to send to other modules are caught where they are sent, so an
  // exception here is about this module's message: drop it, rather than
  // stop the manager.
  try {
    ProcessMessage(&M, pSourcePipe);
    DistributeMessage(&M);
  } catch (UPipeClosedException &) {
    throw;
  } catch (MyCException &E) {
    MyCString err;
    E.AppendTraceToString(err);
    DropSender(pSourcePipe, "Unexpected error while handling MT=%d: %s",
               M.msg_type, err.GetContent());
  }
  SetMyPriority(NORMAL_PRIORITY_CLASS);
}

void CMessageManager::HandleDisconnect(UPipe *pModulePipe) {
  DEBUG_TEXT_("Pipe " << pModulePipe << " broken");
  for (auto it = m_ConnectedModules.begin(); it != m_ConnectedModules.end();
       ++it) {
    CModuleRecord *mod = &it->second;
    if (mod->pModulePipe == pModulePipe) {
      // Make sure not to send anything to disconnected client
      RemoveAllSubscriptions(mod);

      // Notify that the module has left
      SendGoodbye(mod);

      // Delete module record
      m_ModuleByPipe.erase(pModulePipe);
      CleanUpModuleRecord(mod);
      DEBUG_TEXT_(", disconnected module " << mod->ModuleID);

      m_ConnectedModules.erase(it);
      break;
    }
  }
  DEBUG_TEXT("!");
}

void CMessageManager::ProcessMessage(CMessage *M, UPipe *pSourcePipe) {
  DEBUG_TEXT_("Processing message... ");

  // The sender is the module connected on this pipe, whatever the header's
  // src_mod_id says. A module must connect before it does anything else.
  CModuleRecord *src = GetRecordByPipe(pSourcePipe);
  if (src == NULL && M->msg_type != MT_CONNECT &&
      M->msg_type != MT_CONNECT_V2)
    DropSender(pSourcePipe,
               "Sent MT=%d before CONNECT; a module must connect first.",
               M->msg_type);

  switch (M->msg_type) {
  case MT_CONNECT:
    // A CONNECT from a connected module carries nothing new.
    if (src == NULL)
      HandleConnect(M, pSourcePipe);
    break;

  case MT_CONNECT_V2:
    if (src == NULL)
      HandleConnectV2(M, pSourcePipe);
    else
      UpdateConnection(M, src);
    break;

  case MT_CLIENT_SET_NAME:
    HandleSetName(M, src);
    break;

  case MT_PONG:
    break;

  case MT_INTRODUCE:
    SendIntroductions(src);
    break;

  case MT_FORCE_DISCONNECT:
    HandleForceDisconnect(M);
    break;

  case MT_DISCONNECT:
    DisconnectModule(src->ModuleID);
    break;

  case MT_MODULE_READY:
    HandleModuleReady(M, src);
    break;

  case MT_SUBSCRIBE:
    AddSubscription(src, SubscriptionType(M));
    SendAcknowledge(src);
    break;

  case MT_UNSUBSCRIBE:
    RemoveSubscription(src, SubscriptionType(M));
    SendAcknowledge(src);
    break;

  case MT_PAUSE_SUBSCRIPTION:
    PauseSubscription(src, SubscriptionType(M));
    SendAcknowledge(src);
    break;

  case MT_RESUME_SUBSCRIPTION:
    ResumeSubscription(src, SubscriptionType(M));
    SendAcknowledge(src);
    break;

  default:
    DEBUG_TEXT("Nothing to do!");
    return;
  }
  DEBUG_TEXT("Processed!");
}

MSG_TYPE CMessageManager::SubscriptionType(CMessage *M) {
  // SUBSCRIBE, UNSUBSCRIBE, PAUSE_SUBSCRIPTION and RESUME_SUBSCRIPTION share
  // this layout, and HandleData() has checked the size.
  MDF_SUBSCRIBE data;
  M->GetData(&data);
  return data.msg_type;
}

void CMessageManager::SendHello(CModuleRecord *mod) {
  MDF_HELLO hello;
  if (mod != NULL) {
    mod->SetHello(&hello);
    // printf("Hello: %d\n", hello.mod_id);
    m_OutMsg.Set(MT_HELLO, &hello, sizeof(hello));
    DispatchMessage(&m_OutMsg);
  }
}

void CMessageManager::SendGoodbye(CModuleRecord *mod) {
  MDF_GOODBYE goodbye;
  if (mod != NULL) {
    mod->SetGoodbye(&goodbye);
    // printf("Goodbye: %d\n", goodbye.mod_id);
    m_OutMsg.Set(MT_GOODBYE, &goodbye, sizeof(goodbye));
    DispatchMessage(&m_OutMsg);
  }
}

void CMessageManager::SendPing(MODULE_ID mod_id) {
  MDF_PING ping;
  memset(&ping, 0, sizeof(ping));
  CModuleRecord *mod = GetRecord(mod_id);
  if (mod != NULL) {
    ping.dest_id = mod->ModuleID;
    m_OutMsg.Set(MT_PING, &ping, sizeof(ping));
    DispatchMessage(&m_OutMsg, mod);
  }
}

void CMessageManager::HandleSetName(CMessage *M, CModuleRecord *mod) {
  MDF_CLIENT_SET_NAME set_name;
  M->GetData((void *)&set_name);
  set_name.name[MAX_NAME_LEN - 1] = 0;
  mod->SetName(&(set_name.name[0]));
  SendHello(mod);
}

/*
 * Should be called when forwarding a message from other modules
 * The given message will be forwarded to:
 *  - all subscribed logger modules (ALWAYS)
 *  - if the message has a destination address, and it is subscribed to by that
 * destination it will be forwarded only there
 *  - if the message has no destination address, it will be forwarded to all
 * subscribed modules
 */
void CMessageManager::DistributeMessage(CMessage *M) {
  DEBUG_TEXT("Distributing Message...");

  std::vector<MODULE_ID> subscribers;
  GetSubscribers(M->msg_type, subscribers);
  for (MODULE_ID module_id : subscribers) {
    auto mod_it = m_ConnectedModules.find(module_id);
    if (mod_it == m_ConnectedModules.end()) {
      DEBUG_TEXT("Skipping invalid subscriber module id " << module_id);
      continue;
    }
    CModuleRecord *mod = &mod_it->second;

    // A message with a destination goes only there, and to logger modules.
    if (M->dest_mod_id != 0 && mod->ModuleID != M->dest_mod_id &&
        !mod->LoggerStatus)
      continue;

    DEBUG_TEXT_("Forwarding message to module " << mod->ModuleID << "... ");
    try {
      int status = ForwardMessage(M, mod);
      if (status == 0) {
        LogFailedMessage(M, mod->ModuleID);
        DEBUG_TEXT("Failed to Forward Message!");
      } else {
        DEBUG_TEXT("Forwarded!");
      }
    } catch (MyCException &) {
      // The module is removed when its socket reports the failure.
      DEBUG_TEXT("Failed to Forward Message, destination module socket is "
                 "closed/dead");
    }
  }
  DEBUG_TEXT("Done distributing!");
}

/*
 *  Should be called internally in MM when sending a message to anybody that
 * cares The message will be sent to all subscribed modules including loggers
 */
void CMessageManager::DispatchMessage(CMessage *M) {
  std::vector<MODULE_ID> subscribers;
  GetSubscribers(M->msg_type, subscribers);
  for (MODULE_ID module_id : subscribers) {
    auto mod_it = m_ConnectedModules.find(module_id);
    if (mod_it == m_ConnectedModules.end()) {
      DEBUG_TEXT("Skipping invalid subscriber module id " << module_id);
      continue;
    }

    CModuleRecord *mod = &mod_it->second;
    try {
      // A broadcast has no destination, as in pyrtma's manager.
      SendMessage(M, mod, 0);
    } catch (MyCException &) {
      // The module is removed when its socket reports the failure.
      DEBUG_TEXT("Failed to send MM message, destination module socket is closed/dead");
    }
  }
}

/*
 *	Should be called internally in MM when sending a message to a module
 *  The message will be sent, even if the module is not subscribed to it
 *  The message will also be forwarded to all subscribed logger modules
 */
void CMessageManager::DispatchMessage(CMessage *M, CModuleRecord *dest_mod) {
  // send the message to the module it is intended to, disregarding
  // subscriptions
  //(enables MM to send system message to modules)
  // A failed send is ignored here: the module is removed when its socket
  // reports the failure, and the module being handled isn't dropped for it.
  try {
    SendMessage(M, dest_mod, dest_mod->ModuleID);
  } catch (MyCException &) {
    DEBUG_TEXT("Failed to send MM message, destination module socket is closed/dead");
  }

  // CC all logger modules
  std::vector<MODULE_ID> subscribers;
  GetSubscribers(M->msg_type, subscribers);
  for (MODULE_ID module_id : subscribers) {
    auto mod_it = m_ConnectedModules.find(module_id);
    if (mod_it == m_ConnectedModules.end()) {
      DEBUG_TEXT("Skipping invalid subscriber module id " << module_id);
      continue;
    }

    CModuleRecord *mod = &mod_it->second;
    if (mod->LoggerStatus && mod->ModuleID != dest_mod->ModuleID) {
      // don't send to destination module again
      try {
        ForwardMessage(M, mod);
      } catch (MyCException &) {
        DEBUG_TEXT("Failed to copy MM message to logger, socket is closed/dead");
      }
    }
  }
}

/*
 *	Should be called internally in MM when sending a signal to a specific
 * module The signal will be sent, even if the module is not subscribed to it
 *  The signal will also be forwarded to all subscribed logger modules
 */
void CMessageManager::DispatchSignal(MSG_TYPE sig, CModuleRecord *dest_mod) {
  m_OutMsg.Set(sig);
  DispatchMessage(&m_OutMsg, dest_mod);
}

/*
 *	Should be called internally in MM when sending a message to all modules
 *  The message will be sent to all connected modules, even if the module is not
 * subscribed to it The message will also be forwarded to all subscribed logger
 * modules
 */
void CMessageManager::DispatchMessageToAll(CMessage *M) {
  for (auto &entry : m_ConnectedModules) {
    DispatchMessage(M, &entry.second);
  }
}

void CMessageManager::DispatchSignalToAll(MSG_TYPE sig) {
  CMessage R(sig);
  DispatchMessageToAll(&R);
}

int CMessageManager::SendMessage(CMessage *M, CModuleRecord *mod,
                                 MODULE_ID dest_mod_id)
// overloaded function for RTMA_Module::SendMessage()
// Sends a message to a module, specifying the MessageManager itself as the
// source module
{
  UPipe *mod_pipe = mod->pModulePipe;
  if (mod_pipe == NULL)
    return 0;

  // Assume that msg_type, num_data_bytes, data - have been filled in
  M->msg_count = 0;
  M->send_time = GetAbsTime();
  M->recv_time = 0.0;
  M->src_host_id = HID_LOCAL_HOST;
  M->src_mod_id = MID_MESSAGE_MANAGER;
  M->dest_mod_id = dest_mod_id;

  double timeout = 0; // By default use non-blocking write so MM does not get
                      // stuck on a frozen module
  if (mod->LoggerStatus)
    timeout = -1; // Logger modules should not lose data, so use blocking write

  int status = M->Send(mod_pipe, timeout);

  return status;
}

int CMessageManager::ForwardMessage(CMessage *M, CModuleRecord *dest_mod)
// Forward a message where the header is already filled in
// Source module field in the header is unaltered
{
  UPipe *mod_pipe = dest_mod->pModulePipe;
  if (mod_pipe == NULL)
    return 0;

  double timeout = 0; // By default use non-blocking write so MM does not get
                      // stuck on a frozen module
  if (dest_mod->LoggerStatus)
    timeout = -1; // Logger modules should not lose data, so use blocking write

  int status = M->Send(mod_pipe, timeout);

  return status;
}

int CMessageManager::SendSignal(MSG_TYPE sig, CModuleRecord *dest_mod)
// overloaded function for RTMA_Module::SendSignal()
// returns 0 if module is not connected, or failed to send message to it; 1 on
// success
{
  m_OutMsg.Set(sig);
  return SendMessage(&m_OutMsg, dest_mod, dest_mod->ModuleID);
}

CModuleRecord *CMessageManager::ConnectModule(UPipe *pSourcePipe,
                                             MODULE_ID requested_id,
                                             short logger_status, int32_t pid,
                                             const char *name) {
  // A refused module is dropped before it takes an ID, so it gets no ACK,
  // HELLO or GOODBYE, as in pyrtma's manager.
  if (m_ConnectedModules.size() >= MAX_MODULES)
    DropSender(pSourcePipe,
               "The limit of %d modules (MAX_MODULES) is reached. Closing "
               "connection.",
               MAX_MODULES);

  MODULE_ID module_id = requested_id;
  if (module_id == 0) {
    // get the next available module ID from "dynamic" pool
    module_id = GetDynamicModuleId();
    if (module_id <= 0)
      DropSender(pSourcePipe, "All dynamic module IDs are in use.");
  } else if (module_id < 1 || module_id >= DYN_MOD_ID_START) {
    // DYN_MOD_ID_START is the first dynamic ID, so it can't be static.
    DropSender(pSourcePipe,
               "Invalid module ID %d. Static module IDs must be 1 to %d.",
               module_id, DYN_MOD_ID_START - 1);
  } else if (ModuleIsConnected(module_id)) {
    DropSender(pSourcePipe, "Module ID %d is already in use. Closing connection.",
               module_id);
  }

  DEBUG_TEXT("Connecting module " << module_id << " on pipe " << pSourcePipe);

  auto insert_result = m_ConnectedModules.emplace(module_id, CModuleRecord{});

  CModuleRecord *mod = &insert_result.first->second;
  mod->ModuleID = module_id;
  mod->SetUPipe(pSourcePipe);
  mod->LoggerStatus = logger_status;
  mod->pid = pid;
  if (name != NULL)
    mod->SetName(name);
  m_ModuleByPipe[pSourcePipe] = module_id;

  SendAcknowledge(mod);

  // Notify that a client has connected. A module that connected with CONNECT
  // has no name or PID yet; CLIENT_SET_NAME and MODULE_READY send further
  // HELLOs with them.
  SendHello(mod);
  return mod;
}

CModuleRecord *CMessageManager::GetRecord(MODULE_ID module_id) {
  auto it = m_ConnectedModules.find(module_id);
  if (it != m_ConnectedModules.end()) {
    return &it->second;
  }
  return NULL;
}

void CMessageManager::DisconnectModule(MODULE_ID module_id) {
  CModuleRecord *mod = GetRecord(module_id);
  if (mod == NULL)
    return;

  // Make sure not to send anything to disconnected client
  RemoveAllSubscriptions(mod);

  // Notify that the module has left
  SendGoodbye(mod);

  // Close module's pipe
  m_ModuleByPipe.erase(mod->pModulePipe);
  UPipeAutoServer::_server->DisconnectClient(mod->pModulePipe);

  // Clean up module record
  CleanUpModuleRecord(mod);
  m_ConnectedModules.erase(module_id);
}

void CMessageManager::CleanUpModuleRecord(CModuleRecord *mod) {
  // printf("CleanUpModuleRecord(%d)\n", mod->ModuleID);
  if (mod != NULL) {
    mod->Reset();
  }
}

void CMessageManager::ShutdownModule(MODULE_ID mod_id) {
  CModuleRecord *mod = GetRecord(mod_id);
  if (mod != NULL && mod->ModuleID > 0) {
    MODULE_ID mod_id = mod->ModuleID;
    switch (mod_id) {
    case MID_QUICKLOGGER:
      DispatchSignal(MT_LM_EXIT, mod);
      break;

    default:
      DispatchSignal(MT_EXIT, mod);
      break;
    }

    DisconnectModule(mod_id);
  }
}

void CMessageManager::ShutdownAllModules(int shutdown_RTMA,
                                         int shutdown_daemons) {
  std::vector<MODULE_ID> module_ids;
  module_ids.reserve(m_ConnectedModules.size());
  for (const auto &entry : m_ConnectedModules) {
    const CModuleRecord &mod = entry.second;
    if (mod.ModuleID > 0) {
      if (mod.DaemonStatus) {
        if (shutdown_daemons)
          module_ids.push_back(entry.first);
      } else {
        module_ids.push_back(entry.first);
      }
    }
  }

  for (MODULE_ID module_id : module_ids) {
    ShutdownModule(module_id);
  }
}

void CMessageManager::AddSubscriber(CModuleRecord *mod,
                                    MSG_TYPE message_type) {
  m_Subscribers[message_type].insert(mod->ModuleID);
  mod->subs.insert(message_type);
}

void CMessageManager::DropSubscriber(CModuleRecord *mod,
                                     MSG_TYPE message_type) {
  auto it = m_Subscribers.find(message_type);
  if (it != m_Subscribers.end()) {
    it->second.erase(mod->ModuleID);
    if (it->second.empty())
      m_Subscribers.erase(it);
  }
  mod->subs.erase(message_type);
}

void CMessageManager::RemoveAllSubscriptions(CModuleRecord *mod) {
  if (mod == NULL)
    return;
  std::vector<MSG_TYPE> types(mod->subs.begin(), mod->subs.end());
  for (MSG_TYPE mt : types)
    DropSubscriber(mod, mt);
}

void CMessageManager::GetSubscribers(MSG_TYPE message_type,
                                     std::vector<MODULE_ID> &ids) const {
  ids.clear();
  auto it = m_Subscribers.find(message_type);
  if (it != m_Subscribers.end())
    ids.insert(ids.end(), it->second.begin(), it->second.end());
  if (message_type != ALL_MESSAGE_TYPES) {
    it = m_Subscribers.find(ALL_MESSAGE_TYPES);
    if (it != m_Subscribers.end())
      ids.insert(ids.end(), it->second.begin(), it->second.end());
  }
}

// Subscriptions work as in pyrtma's manager. ALL_MESSAGE_TYPES replaces a
// module's individual subscriptions, and while it is in place, individual
// SUBSCRIBE and UNSUBSCRIBE requests are ignored. Unsubscribing from
// ALL_MESSAGE_TYPES removes every subscription.
void CMessageManager::AddSubscription(CModuleRecord *mod,
                                      MSG_TYPE message_type) {
  if (mod == NULL)
    return;

  if (((message_type < 0) || (message_type >= MAX_MESSAGE_TYPES)) &&
      (message_type != ALL_MESSAGE_TYPES)) {
    // send MDF_FAIL_SUBSCRIBE instead of ACK so the module's subscribe
    // function will fail
    MDF_FAIL_SUBSCRIBE data{};
    data.mod_id = mod->ModuleID;
    data.msg_type = message_type;
    CMessage R(MT_FAIL_SUBSCRIBE, (void *)&data, sizeof(data));
    DispatchMessage(&R, mod);
    return;
  }

  if (message_type == ALL_MESSAGE_TYPES) {
    RemoveAllSubscriptions(mod);
    AddSubscriber(mod, ALL_MESSAGE_TYPES);
  } else if (!mod->SubAll()) {
    AddSubscriber(mod, message_type);
  }
}

void CMessageManager::RemoveSubscription(CModuleRecord *mod,
                                         MSG_TYPE message_type) {
  if (mod == NULL)
    return;

  if (message_type == ALL_MESSAGE_TYPES)
    RemoveAllSubscriptions(mod);
  else if (!mod->SubAll())
    DropSubscriber(mod, message_type);
}

// As in pyrtma's manager, a paused subscription is removed, and resuming
// subscribes again. Clients keep track of what they paused.
void CMessageManager::PauseSubscription(CModuleRecord *mod,
                                        MSG_TYPE message_type) {
  RemoveSubscription(mod, message_type);
}

void CMessageManager::ResumeSubscription(CModuleRecord *mod,
                                         MSG_TYPE message_type) {
  AddSubscription(mod, message_type);
}

void CMessageManager::HandleConnect(CMessage *M, UPipe *pSourcePipe) {
  // CONNECT asks for the module ID in its header.
  MDF_CONNECT data;
  M->GetData((void *)&data);
  ConnectModule(pSourcePipe, M->src_mod_id, data.logger_status, 0, NULL);
}

void CMessageManager::HandleConnectV2(CMessage *M, UPipe *pSourcePipe) {
  // CONNECT_V2 asks for the module ID in its data, as in pyrtma.
  MDF_CONNECT_V2 data;
  M->GetData((void *)&data);
  data.name[MAX_NAME_LEN - 1] = 0;
  ConnectModule(pSourcePipe, data.mod_id, data.logger_status, data.pid,
                data.name);
}

// Clients used to send both CONNECT and CONNECT_V2, in either order, for
// managers that didn't support CONNECT_V2. The first one connects the module
// and is acknowledged. A CONNECT_V2 after that updates the module's name and
// process ID, and a HELLO announces them; no ACK is sent, because the client
// waits for only one. The module ID and logger status can't change while the
// module is connected, so a different request is logged and ignored. This is
// what pyrtma's manager does.
void CMessageManager::UpdateConnection(CMessage *M, CModuleRecord *mod) {
  MDF_CONNECT_V2 data;
  M->GetData((void *)&data);
  data.name[MAX_NAME_LEN - 1] = 0;
  if (data.mod_id != 0 && data.mod_id != mod->ModuleID)
    fprintf(stderr,
            "WARNING - module %d - Already connected; ignoring the requested "
            "ID %d.\n",
            mod->ModuleID, data.mod_id);
  if ((data.logger_status != 0) != (mod->LoggerStatus != 0))
    fprintf(stderr,
            "WARNING - module %d - Already connected; ignoring the change of "
            "logger status to %d.\n",
            mod->ModuleID, data.logger_status);
  mod->SetName(data.name);
  mod->pid = data.pid;
  SendHello(mod);
}

void CMessageManager::HandleForceDisconnect(CMessage *M) {
  MDF_FORCE_DISCONNECT data_MDF_FORCE_DISCONNECT;
  M->GetData(&data_MDF_FORCE_DISCONNECT);
  MODULE_ID mod_id = data_MDF_FORCE_DISCONNECT.mod_id;
  ShutdownModule(mod_id);
}

void CMessageManager::HandleModuleReady(CMessage *M, CModuleRecord *mod) {
  MDF_MODULE_READY module_ready;
  M->GetData(&module_ready);
  mod->pid = module_ready.pid;

  // Notify that the module has joined and ready
  SendHello(mod);
}

void CMessageManager::SendAcknowledge(CModuleRecord *mod) {
  if (mod != NULL) {
    DEBUG_TEXT_("Sending ACK to module " << mod->ModuleID << "... ");
    DispatchSignal(MT_ACKNOWLEDGE, mod);
    DEBUG_TEXT("Sent!");
  }
}

void CMessageManager::SendIntroductions(CModuleRecord *dest_mod) {
  MDF_HELLO hello;
  if (dest_mod) {
    for (auto &entry : m_ConnectedModules) {
      CModuleRecord *mod = &entry.second;
      if (mod->ModuleID > 0) {
        mod->SetHello(&hello);
        // printf("Hello: %d\n", hello.mod_id);
        m_OutMsg.Set(MT_HELLO, &hello, sizeof(hello));
        SendMessage(&m_OutMsg, dest_mod, dest_mod->ModuleID);
      }
    }
  }
}

int CMessageManager::ModuleIsConnected(MODULE_ID mod_id) const {
  if (mod_id < MID_MESSAGE_MANAGER)
    return 0;

  return m_ConnectedModules.find(mod_id) != m_ConnectedModules.end();
}

void CMessageManager::LogFailedMessage(CMessage *M, MODULE_ID mod_id) {
  MDF_FAILED_MESSAGE data;
  memset(&data, 0, sizeof(data));
  data.dest_mod_id = mod_id;
  data.time_of_failure = GetAbsTime();
  memcpy(&data.msg_header, M, sizeof(RTMA_MSG_HEADER));
  CMessage F(MT_FAILED_MESSAGE, &data, sizeof(data));
  DispatchMessage(&F);
}