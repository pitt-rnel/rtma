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

// Defined by CMake from the project's version.
#ifndef RTMA_VERSION
#define RTMA_VERSION "unknown"
#endif
#include <MyCException.h>
#include <Timing.h>

// (std::min) and (std::max) are in parentheses: windows.h, which RTMA.h
// includes, defines min and max as macros.
#include <algorithm>
#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <random>

namespace {

void Log(const char *level, const char *format, ...) {
  char text[1024];
  va_list args;
  va_start(args, format);
  vsnprintf(text, sizeof(text), format, args);
  va_end(args);
  fprintf(stderr, "%s - %s\n", level, text);
  fflush(stderr);
}

double Seconds(Clock::duration d) {
  return std::chrono::duration<double>(d).count();
}

// A client whose message can't be handled is dropped with this.
struct DropClient {
  std::string reason;
};

[[noreturn]] void DropSender(const char *format, ...) {
  char text[512];
  va_list args;
  va_start(args, format);
  vsnprintf(text, sizeof(text), format, args);
  va_end(args);
  throw DropClient{text};
}

// How long each select() waits at most. It also bounds how late a stalled
// client is dropped.
const double kSelectTimeout = 0.1;

// Bytes read from one connection in one round, so one busy client can't
// keep the others waiting.
const size_t kReadBudget = 4 * 1024 * 1024;

bool ParseSeconds(const char *text, double &seconds) {
  char *end = NULL;
  seconds = strtod(text, &end);
  return end != text && *end == 0 && seconds > 0;
}

int Usage(const char *problem) {
  if (problem)
    fprintf(stderr, "MessageManager: %s\n", problem);
  fprintf(problem ? stderr : stdout,
          "usage: MessageManager [SERVER] [--stall-timeout SECONDS | "
          "--no-stall-timeout] [--logger-timeout SECONDS]\n\n"
          "SERVER is host:port, or :port for every interface; the default "
          "is " DEFAULT_PIPE_SERVER_NAME_FOR_MM ".\n"
          "--stall-timeout  drop a client that stops partway through a "
          "message for this long (default 5)\n"
          "--no-stall-timeout  never drop such a client\n"
          "--logger-timeout  drop a logger that takes no data for this long "
          "(default: wait as long as it takes)\n");
  return problem ? 2 : 0;
}

} // namespace

int main(int argc, char *argv[]) {
  const char *server = DEFAULT_PIPE_SERVER_NAME_FOR_MM;
  double stall_timeout = 5.0;
  double logger_timeout = -1.0;
  bool server_given = false;
  for (int i = 1; i < argc; i++) {
    std::string arg = argv[i];
    if (arg == "-h" || arg == "--help")
      return Usage(NULL);
    if (arg == "--no-stall-timeout") {
      stall_timeout = -1.0;
    } else if (arg == "--stall-timeout" || arg == "--logger-timeout") {
      double seconds;
      if (i + 1 >= argc || !ParseSeconds(argv[i + 1], seconds))
        return Usage((arg + " needs a number of seconds greater than 0").c_str());
      (arg == "--stall-timeout" ? stall_timeout : logger_timeout) = seconds;
      i++;
    } else if (!server_given && arg.compare(0, 2, "--") != 0) {
      server = argv[i];
      server_given = true;
    } else {
      return Usage(("unexpected argument " + arg).c_str());
    }
  }

  try {
    CMessageManager MM;
    MM.stall_timeout = stall_timeout;
    MM.logger_timeout = logger_timeout;
    MM.MainLoop(server);
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

// Module records --------------------------------------------------------

void CModuleRecord::Describe(MDF_HELLO *hello) const {
  memset(hello, 0, sizeof(*hello));
  hello->mod_id = ModuleID;
  hello->pid = pid;
  if (conn != NULL) {
    hello->port = conn->port;
    strncpy(hello->addr, conn->addr.c_str(), sizeof(hello->addr) - 1);
  }
  strncpy(hello->name, name.c_str(), sizeof(hello->name) - 1);
}

std::string CModuleRecord::Label() const {
  std::string label = "module " + std::to_string(ModuleID);
  if (!name.empty())
    label += " " + name;
  if (conn != NULL)
    label += " (" + conn->addr + ":" + std::to_string(conn->port) + ")";
  return label;
}

// The event loop ----------------------------------------------------------

CMessageManager::CMessageManager() {
  m_Version = RTMA_VERSION;
  m_NextDynamicModId = DYN_MOD_ID_START;
  InitializeAbsTime();
}

CMessageManager::~CMessageManager() {
  for (auto &conn : m_Connections)
    NonBlockingSocket::Close(conn->sock);
  NonBlockingSocket::Close(m_Listener);
}

void CMessageManager::MainLoop(const char *server_name) {
  try {
    printf("RTMA MessageManager %s\n", m_Version.GetContent());
    m_Listener = NonBlockingSocket::Listen(server_name);
    printf("server_addr = [%s]\n", server_name);
    fflush(stdout);

    std::mt19937 shuffle_rng(12345);
    std::vector<NonBlockingSocket::Socket> rlist, wlist;
    std::vector<CConnection *> rconns, wconns;
    std::vector<char> readable, writable;
    Clock::time_point next_stall_check = Clock::now();

    for (;;) {
      rlist.assign(1, m_Listener);
      rconns.assign(1, NULL);
      wlist.clear();
      wconns.clear();
      for (auto &conn : m_Connections) {
        rlist.push_back(conn->sock);
        rconns.push_back(conn.get());
        if (!conn->tx.empty()) {
          wlist.push_back(conn->sock);
          wconns.push_back(conn.get());
        }
      }
      if (!NonBlockingSocket::Select(rlist, wlist, kSelectTimeout, readable, writable))
        throw MyCException("select() failed");

      // Randomly order the connections with data, so none is always
      // served first.
      std::vector<CConnection *> ready;
      for (size_t i = 1; i < rlist.size(); i++)
        if (readable[i])
          ready.push_back(rconns[i]);
      std::shuffle(ready.begin(), ready.end(), shuffle_rng);
      // Dropped connections are only marked closing here, and deleted by
      // FinishRemovals() at the end of the round, so every pointer in ready
      // and wconns stays valid until then.
      for (CConnection *conn : ready)
        if (!conn->closing)
          ReadFrom(conn);

      for (size_t i = 0; i < wlist.size(); i++)
        if (writable[i] && !wconns[i]->closing)
          Flush(wconns[i]);

      if (readable[0])
        AcceptConnections();

      if (Clock::now() >= next_stall_check) {
        DropStalled();
        next_stall_check = Clock::now() +
                           std::chrono::milliseconds((int)(kSelectTimeout * 1000));
      }
      FinishRemovals();
    }
  } catch (MyCException &E) {
    E.AddToStack("CMessageManager::MainLoop()");
    throw;
  }
}

void CMessageManager::AcceptConnections() {
  for (;;) {
    std::string addr;
    uint16_t port = 0;
    NonBlockingSocket::Socket s = NonBlockingSocket::Accept(m_Listener, addr, port);
    if (s == NonBlockingSocket::kInvalid)
      return;
    // The listening socket and this one have to fit in one select().
    if (m_Connections.size() + 2 > NonBlockingSocket::kMaxSockets || !NonBlockingSocket::Selectable(s)) {
      Log("WARNING",
          "Refusing a connection from %s:%u: select() can watch at most %u "
          "sockets.",
          addr.c_str(), port, (unsigned)NonBlockingSocket::kMaxSockets);
      NonBlockingSocket::Close(s);
      continue;
    }
    std::unique_ptr<CConnection> conn(new CConnection);
    conn->sock = s;
    conn->addr = addr;
    conn->port = port;
    conn->last_rx = Clock::now();
    m_Connections.push_back(std::move(conn));
  }
}

void CMessageManager::ReadFrom(CConnection *conn) {
  size_t budget = kReadBudget;
  while (budget > 0 && !conn->closing) {
    // Room for the rest of the message being read, or for a header.
    size_t want = sizeof(RTMA_MSG_HEADER);
    if (conn->Buffered() >= sizeof(RTMA_MSG_HEADER)) {
      RTMA_MSG_HEADER header;
      memcpy(&header, &conn->rx[conn->rx_start], sizeof(header));
      if (header.num_data_bytes >= 0 && header.num_data_bytes <= RTMA_MAX_DATA_BYTES)
        want = sizeof(header) + header.num_data_bytes;
    }
    want = (std::max)(want, (size_t)64 * 1024);
    if (conn->rx_start > 0 && conn->rx.size() - conn->rx_start < want) {
      // Move what is left to the front, keeping the buffer small.
      memmove(conn->rx.data(), conn->rx.data() + conn->rx_start, conn->Buffered());
      conn->rx_end -= conn->rx_start;
      conn->rx_start = 0;
    }
    if (conn->rx.size() < want)
      conn->rx.resize(want);

    std::string error;
    long n = NonBlockingSocket::Recv(conn->sock, conn->rx.data() + conn->rx_end,
                       conn->rx.size() - conn->rx_end, error);
    if (n < 0) {
      Drop(conn, error, false);
      return;
    }
    if (n == 0)
      return;
    conn->rx_end += n;
    conn->last_rx = Clock::now();
    budget -= (std::min)(budget, (size_t)n);
    HandleBuffered(conn);
  }
}

void CMessageManager::HandleBuffered(CConnection *conn) {
  while (!conn->closing && conn->Buffered() >= sizeof(RTMA_MSG_HEADER)) {
    RTMA_MSG_HEADER header;
    memcpy(&header, &conn->rx[conn->rx_start], sizeof(header));
    if (header.num_data_bytes < 0 || header.num_data_bytes > RTMA_MAX_DATA_BYTES) {
      Drop(conn, "Invalid num_data_bytes (" + std::to_string(header.num_data_bytes) +
                     ") for MT=" + std::to_string(header.msg_type) + "; it must be 0 to " +
                     std::to_string(RTMA_MAX_DATA_BYTES) +
                     ". Header may be corrupted.");
      return;
    }
    size_t total = sizeof(header) + header.num_data_bytes;
    if (conn->Buffered() < total)
      return; // the rest hasn't arrived

    CMessage M;
    M.Set(header.msg_type, &conn->rx[conn->rx_start + sizeof(header)],
          header.num_data_bytes, header.reserved);
    M.msg_count = header.msg_count;
    M.send_time = header.send_time;
    M.recv_time = header.recv_time;
    M.src_host_id = header.src_host_id;
    M.src_mod_id = header.src_mod_id;
    M.dest_host_id = header.dest_host_id;
    M.dest_mod_id = header.dest_mod_id;
    M.remaining_bytes = header.remaining_bytes;
    M.is_dynamic = header.is_dynamic;
    conn->rx_start += total;
    if (conn->rx_start == conn->rx_end)
      conn->rx_start = conn->rx_end = 0;

    try {
      HandleMessage(conn, &M);
    } catch (DropClient &drop) {
      Drop(conn, drop.reason);
      return;
    } catch (MyCException &E) {
      MyCString err;
      E.AppendTraceToString(err);
      Drop(conn, std::string("Unexpected error while handling MT=") +
                     std::to_string(M.msg_type) + ": " +
                     (err.GetContent() ? err.GetContent() : ""));
      return;
    }
  }
}

void CMessageManager::Flush(CConnection *conn) {
  while (!conn->tx.empty()) {
    const std::string &chunk = conn->tx.front();
    std::string error;
    long n = NonBlockingSocket::Send(conn->sock, chunk.data() + conn->tx_offset,
                       chunk.size() - conn->tx_offset, error);
    if (n < 0) {
      Drop(conn, error);
      return;
    }
    if (n == 0)
      return;
    conn->tx_offset += n;
    if (conn->tx_offset == chunk.size()) {
      conn->tx.pop_front();
      conn->tx_offset = 0;
    }
  }
}

void CMessageManager::DropStalled() {
  if (stall_timeout < 0)
    return;
  Clock::time_point now = Clock::now();
  for (auto &conn : m_Connections) {
    if (conn->closing || conn->Buffered() == 0)
      continue;
    double idle = Seconds(now - conn->last_rx);
    if (idle < stall_timeout)
      continue;
    size_t expected = sizeof(RTMA_MSG_HEADER);
    if (conn->Buffered() >= sizeof(RTMA_MSG_HEADER)) {
      RTMA_MSG_HEADER header;
      memcpy(&header, &conn->rx[conn->rx_start], sizeof(header));
      expected += header.num_data_bytes;
    }
    Drop(conn.get(),
         "Stalled: sent " + std::to_string(conn->Buffered()) + " of " +
             std::to_string(expected) + " bytes of a message, then nothing for " +
             std::to_string((int)idle) + " s.",
         false);
  }
}

void CMessageManager::Drop(CConnection *conn, const std::string &reason, bool error) {
  if (conn->closing)
    return;
  conn->closing = true;
  CModuleRecord *mod = GetRecord(conn);
  std::string who = mod ? mod->Label()
                        : conn->addr + ":" + std::to_string(conn->port);
  Log(error ? "ERROR" : "WARNING", "DROPPING - %s - %s", who.c_str(),
      reason.c_str());
  // Out of the routing tables at once, so nothing more is sent to it.
  if (mod != NULL)
    RemoveAllSubscriptions(mod);
  m_PendingRemovals.push_back(conn);
}

void CMessageManager::FinishRemovals() {
  // A GOODBYE that fails to send drops more modules, which join the queue.
  while (!m_PendingRemovals.empty()) {
    CConnection *conn = m_PendingRemovals.front();
    m_PendingRemovals.erase(m_PendingRemovals.begin());
    CModuleRecord *mod = GetRecord(conn);
    if (mod != NULL) {
      MODULE_ID id = mod->ModuleID;
      SendGoodbye(mod);
      m_ConnectedModules.erase(id);
    }
    // Send what is still queued, such as an EXIT, if the connection takes it.
    std::string error;
    while (!conn->tx.empty()) {
      const std::string &chunk = conn->tx.front();
      long n = NonBlockingSocket::Send(conn->sock, chunk.data() + conn->tx_offset,
                         chunk.size() - conn->tx_offset, error);
      if (n <= 0)
        break;
      conn->tx_offset += n;
      if (conn->tx_offset == chunk.size()) {
        conn->tx.pop_front();
        conn->tx_offset = 0;
      }
    }
    NonBlockingSocket::Close(conn->sock);
    conn->sock = NonBlockingSocket::kInvalid;
    for (auto it = m_Connections.begin(); it != m_Connections.end(); ++it) {
      if (it->get() == conn) {
        m_Connections.erase(it);
        break;
      }
    }
  }
}

// Handling a message ------------------------------------------------------

CModuleRecord *CMessageManager::GetRecord(MODULE_ID module_id) {
  auto it = m_ConnectedModules.find(module_id);
  return it == m_ConnectedModules.end() ? NULL : &it->second;
}

CModuleRecord *CMessageManager::GetRecord(CConnection *conn) {
  if (conn->module_id < 0)
    return NULL;
  CModuleRecord *mod = GetRecord(conn->module_id);
  return (mod != NULL && mod->conn == conn) ? mod : NULL;
}

bool CMessageManager::ModuleIsConnected(MODULE_ID module_id) const {
  return m_ConnectedModules.count(module_id) != 0;
}

void CMessageManager::HandleMessage(CConnection *conn, CMessage *M) {
  // Core messages must match their definitions, as in pyrtma's manager. A
  // client whose core definitions don't match the manager's is dropped
  // before its message is acted on or forwarded.
  if (M->msg_type <= MAX_RTMA_MSG_TYPE) {
    int expected = CoreMessageSize(M->msg_type);
    if (expected < 0)
      DropSender("Unknown core message type MT=%d received.", M->msg_type);
    if (M->num_data_bytes != expected)
      DropSender("MT=%d announced %d data bytes, but its core definition has "
                 "%d. The client's core definitions don't match the "
                 "manager's.",
                 M->msg_type, M->num_data_bytes, expected);
  }

  // The sender is the module connected on this connection, whatever the
  // header's src_mod_id says. A module must connect before anything else.
  CModuleRecord *src = GetRecord(conn);
  if (src == NULL && M->msg_type != MT_CONNECT && M->msg_type != MT_CONNECT_V2)
    DropSender("Sent MT=%d before CONNECT; a module must connect first.",
               M->msg_type);

  ProcessMessage(M, conn, src);
  if (!conn->closing || M->msg_type == MT_DISCONNECT)
    DistributeMessage(M);
}

void CMessageManager::ProcessMessage(CMessage *M, CConnection *conn,
                                     CModuleRecord *src) {
  switch (M->msg_type) {
  case MT_CONNECT:
    // A CONNECT from a connected module carries nothing new.
    if (src == NULL)
      HandleConnect(M, conn);
    break;
  case MT_CONNECT_V2:
    if (src == NULL)
      HandleConnectV2(M, conn);
    else
      UpdateConnection(M, src);
    break;
  case MT_CLIENT_SET_NAME:
    HandleSetName(M, src);
    break;
  case MT_INTRODUCE:
    SendIntroductions(src);
    break;
  case MT_FORCE_DISCONNECT:
    HandleForceDisconnect(M);
    break;
  case MT_DISCONNECT:
    // Its GOODBYE is sent, and its connection closed, after this message is
    // forwarded. No ACK, as in pyrtma's manager.
    Drop(conn, "Disconnected.", false);
    break;
  case MT_MODULE_READY:
    HandleModuleReady(M, src);
    break;
  case MT_SUBSCRIBE:
  case MT_RESUME_SUBSCRIPTION:
    // As in pyrtma's manager, resuming a subscription subscribes again.
    AddSubscription(src, SubscriptionType(M));
    SendAcknowledge(src);
    break;
  case MT_UNSUBSCRIBE:
  case MT_PAUSE_SUBSCRIPTION:
    // A paused subscription is removed; clients keep track of what they
    // paused.
    RemoveSubscription(src, SubscriptionType(M));
    SendAcknowledge(src);
    break;
  default:
    break;
  }
}

// Connecting and disconnecting ------------------------------------------

MODULE_ID CMessageManager::GetDynamicModuleId() {
  for (int attempts = 0; attempts <= MAX_MODULE_ID - DYN_MOD_ID_START; ++attempts) {
    MODULE_ID id = m_NextDynamicModId;
    m_NextDynamicModId = (id == MAX_MODULE_ID) ? DYN_MOD_ID_START : id + 1;
    if (!ModuleIsConnected(id))
      return id;
  }
  return 0; // all dynamic IDs are in use
}

CModuleRecord *CMessageManager::ConnectModule(CConnection *conn, MODULE_ID requested_id,
                                              short logger_status, int32_t pid,
                                              const char *name) {
  // A refused module is dropped before it takes an ID, so it gets no ACK,
  // HELLO or GOODBYE, as in pyrtma's manager.
  if (m_ConnectedModules.size() >= MAX_MODULES)
    DropSender("The limit of %d modules (MAX_MODULES) is reached. Closing "
               "connection.",
               MAX_MODULES);

  MODULE_ID module_id = requested_id;
  if (module_id == 0) {
    module_id = GetDynamicModuleId();
    if (module_id <= 0)
      DropSender("All dynamic module IDs are in use.");
  } else if (module_id < 1 || module_id >= DYN_MOD_ID_START) {
    DropSender("Invalid module ID %d. Static module IDs must be 1 to %d.",
               module_id, DYN_MOD_ID_START - 1);
  } else if (ModuleIsConnected(module_id)) {
    DropSender("Module ID %d is already in use. Closing connection.", module_id);
  }

  CModuleRecord &mod = m_ConnectedModules[module_id];
  mod.ModuleID = module_id;
  mod.conn = conn;
  mod.LoggerStatus = logger_status;
  mod.pid = pid;
  mod.SetName(name);
  conn->module_id = module_id;

  SendAcknowledge(&mod);
  // A module that connected with CONNECT has no name or PID yet;
  // CLIENT_SET_NAME and MODULE_READY send further HELLOs with them.
  SendHello(&mod);
  return &mod;
}

void CMessageManager::HandleConnect(CMessage *M, CConnection *conn) {
  // CONNECT asks for the module ID in its header.
  MDF_CONNECT data;
  M->GetData(&data);
  ConnectModule(conn, M->src_mod_id, data.logger_status, 0, NULL);
}

void CMessageManager::HandleConnectV2(CMessage *M, CConnection *conn) {
  // CONNECT_V2 asks for the module ID in its data, as in pyrtma.
  MDF_CONNECT_V2 data;
  M->GetData(&data);
  data.name[MAX_NAME_LEN - 1] = 0;
  ConnectModule(conn, data.mod_id, data.logger_status, data.pid, data.name);
}

// A CONNECT_V2 from a connected module updates its name and process ID, and a
// HELLO announces them; no ACK is sent, because the client waits for only one.
// A different module ID or logger status is logged and ignored. This is what
// pyrtma's manager does.
void CMessageManager::UpdateConnection(CMessage *M, CModuleRecord *mod) {
  MDF_CONNECT_V2 data;
  M->GetData(&data);
  data.name[MAX_NAME_LEN - 1] = 0;
  if (data.mod_id != 0 && data.mod_id != mod->ModuleID)
    Log("WARNING", "%s - Already connected; ignoring the requested ID %d.",
        mod->Label().c_str(), data.mod_id);
  if ((data.logger_status != 0) != (mod->LoggerStatus != 0))
    Log("WARNING",
        "%s - Already connected; ignoring the change of logger status to %d.",
        mod->Label().c_str(), data.logger_status);
  mod->SetName(data.name);
  mod->pid = data.pid;
  SendHello(mod);
}

void CMessageManager::HandleSetName(CMessage *M, CModuleRecord *mod) {
  MDF_CLIENT_SET_NAME data;
  M->GetData(&data);
  data.name[MAX_NAME_LEN - 1] = 0;
  mod->SetName(data.name);
  SendHello(mod);
}

void CMessageManager::HandleModuleReady(CMessage *M, CModuleRecord *mod) {
  MDF_MODULE_READY data;
  M->GetData(&data);
  mod->pid = data.pid;
  SendHello(mod);
}

void CMessageManager::HandleForceDisconnect(CMessage *M) {
  MDF_FORCE_DISCONNECT data;
  M->GetData(&data);
  CModuleRecord *mod = GetRecord((MODULE_ID)data.mod_id);
  if (mod == NULL || mod->conn->closing)
    return;
  SendSignal(MT_EXIT, mod);
  Drop(mod->conn, "Forced to disconnect by FORCE_DISCONNECT.", false);
}

// Subscriptions -------------------------------------------------------------

MSG_TYPE CMessageManager::SubscriptionType(CMessage *M) {
  // SUBSCRIBE, UNSUBSCRIBE, PAUSE_SUBSCRIPTION and RESUME_SUBSCRIPTION share
  // this layout, and the size has been checked.
  MDF_SUBSCRIBE data;
  M->GetData(&data);
  return data.msg_type;
}

void CMessageManager::DropSubscriber(CModuleRecord *mod, MSG_TYPE message_type) {
  auto it = m_Subscribers.find(message_type);
  if (it != m_Subscribers.end()) {
    it->second.erase(mod->ModuleID);
    if (it->second.empty())
      m_Subscribers.erase(it);
  }
  mod->subs.erase(message_type);
}

void CMessageManager::RemoveAllSubscriptions(CModuleRecord *mod) {
  std::vector<MSG_TYPE> types(mod->subs.begin(), mod->subs.end());
  for (MSG_TYPE mt : types)
    DropSubscriber(mod, mt);
}

// Subscriptions work as in pyrtma's manager: ALL_MESSAGE_TYPES is a
// subscription like any other. Subscribing to it adds it beside a module's
// other subscriptions, unsubscribing from it ends only it, and other types can
// be subscribed and unsubscribed while it is in place. A module's subs hold
// every type it subscribes to, ALL_MESSAGE_TYPES among them; the routing
// table holds a module subscribed to ALL_MESSAGE_TYPES under that type alone,
// so a message reaches it once, and its other types return to the table when
// it unsubscribes from ALL_MESSAGE_TYPES.
void CMessageManager::AddSubscription(CModuleRecord *mod, MSG_TYPE message_type) {
  if ((message_type < 0 || message_type >= MAX_MESSAGE_TYPES) &&
      message_type != ALL_MESSAGE_TYPES) {
    // FAIL_SUBSCRIBE, before the ACK, so the module's subscribe call fails.
    MDF_FAIL_SUBSCRIBE data{};
    data.mod_id = mod->ModuleID;
    data.msg_type = message_type;
    CMessage R(MT_FAIL_SUBSCRIBE, &data, sizeof(data));
    SendFromManager(&R, mod);
    return;
  }
  mod->subs.insert(message_type);
  if (message_type == ALL_MESSAGE_TYPES) {
    for (MSG_TYPE other : mod->subs)
      if (other != ALL_MESSAGE_TYPES)
        Unroute(mod, other);
    m_Subscribers[ALL_MESSAGE_TYPES].insert(mod->ModuleID);
  } else if (!mod->SubAll()) {
    m_Subscribers[message_type].insert(mod->ModuleID);
  }
}

void CMessageManager::RemoveSubscription(CModuleRecord *mod, MSG_TYPE message_type) {
  mod->subs.erase(message_type);
  Unroute(mod, message_type);
  if (message_type == ALL_MESSAGE_TYPES)
    for (MSG_TYPE other : mod->subs)
      m_Subscribers[other].insert(mod->ModuleID);
}

void CMessageManager::Unroute(CModuleRecord *mod, MSG_TYPE message_type) {
  auto it = m_Subscribers.find(message_type);
  if (it != m_Subscribers.end()) {
    it->second.erase(mod->ModuleID);
    if (it->second.empty())
      m_Subscribers.erase(it);
  }
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

// Sending -------------------------------------------------------------------

std::string CMessageManager::Wire(CMessage *M) {
  RTMA_MSG_HEADER header = M->GetHeader();
  std::string wire(sizeof(header) + M->num_data_bytes, '\0');
  memcpy(&wire[0], &header, sizeof(header));
  if (M->num_data_bytes > 0)
    memcpy(&wire[sizeof(header)], M->GetDataPointer(), M->num_data_bytes);
  return wire;
}

bool CMessageManager::TrySend(CModuleRecord *mod, const std::string &wire) {
  CConnection *conn = mod->conn;
  if (conn->closing)
    return true; // being dropped; not a failure to report
  // Queued bytes go first; while some are left, a new message can't go.
  if (!conn->tx.empty()) {
    Flush(conn);
    if (conn->closing)
      return true;
    if (!conn->tx.empty())
      return false;
  }
  std::string error;
  long n = NonBlockingSocket::Send(conn->sock, wire.data(), wire.size(), error);
  if (n < 0) {
    Drop(conn, error);
    return true;
  }
  if (n == 0)
    return false;
  // What the connection didn't take is sent when it can take more, so the
  // message isn't cut short.
  if ((size_t)n < wire.size()) {
    conn->tx.push_back(wire.substr(n));
    conn->tx_offset = 0;
  }
  return true;
}

void CMessageManager::SendToLogger(CModuleRecord *mod, const std::string &wire) {
  CConnection *conn = mod->conn;
  if (conn->closing)
    return;
  conn->tx.push_back(wire);
  Clock::time_point start = Clock::now();
  for (;;) {
    Flush(conn);
    if (conn->closing || conn->tx.empty())
      return;
    double wait = 1.0;
    if (logger_timeout >= 0) {
      double left = logger_timeout - Seconds(Clock::now() - start);
      if (left <= 0) {
        char reason[128];
        snprintf(reason, sizeof(reason),
                 "Logger module did not accept data within %g s.", logger_timeout);
        Drop(conn, reason);
        return;
      }
      wait = (std::min)(wait, left);
    }
    std::vector<char> readable, writable;
    std::vector<NonBlockingSocket::Socket> none, sock(1, conn->sock);
    NonBlockingSocket::Select(none, sock, wait, readable, writable);
  }
}

void CMessageManager::Deliver(CModuleRecord *mod, const std::string &wire, CMessage *M) {
  if (mod->LoggerStatus) {
    SendToLogger(mod, wire);
  } else if (!TrySend(mod, wire)) {
    // A module that can't take the message now misses it; it isn't waited
    // for, and isn't dropped.
    SendFailedMessage(M, mod->ModuleID);
  }
}

void CMessageManager::DistributeMessage(CMessage *M) {
  // Messages to invalid destinations aren't forwarded, as in pyrtma's
  // manager. ALL_HOSTS is a valid host.
  if (M->dest_mod_id < 0 || M->dest_mod_id > MAX_MODULE_ID) {
    Log("ERROR", "Got invalid dest_mod_id [%d] from module %d; not forwarded.",
        M->dest_mod_id, M->src_mod_id);
    return;
  }
  if (M->dest_host_id != HID_ALL_HOSTS &&
      (M->dest_host_id < 0 || M->dest_host_id > MAX_HOSTS)) {
    Log("ERROR", "Got invalid dest_host_id [%d] from module %d; not forwarded.",
        M->dest_host_id, M->src_mod_id);
    return;
  }

  std::vector<MODULE_ID> subscribers;
  GetSubscribers(M->msg_type, subscribers);
  if (subscribers.empty())
    return;
  std::string wire = Wire(M);
  for (MODULE_ID id : subscribers) {
    // Looked up for each one: a failed send can drop a module.
    CModuleRecord *mod = GetRecord(id);
    if (mod == NULL || mod->conn->closing)
      continue;
    // A message with a destination goes only there, and to logger modules.
    if (M->dest_mod_id != 0 && mod->ModuleID != M->dest_mod_id && !mod->LoggerStatus)
      continue;
    Deliver(mod, wire, M);
  }
}

void CMessageManager::SendFromManager(CMessage *M, CModuleRecord *dest_mod) {
  M->src_host_id = 0;
  M->src_mod_id = MID_MESSAGE_MANAGER;
  M->dest_host_id = 0;
  M->dest_mod_id = dest_mod ? dest_mod->ModuleID : 0;
  M->msg_count = 0; // messages from the manager carry no count
  M->send_time = GetAbsTime();
  M->recv_time = 0.0;
  if (M->reserved == 0)
    M->reserved = CoreMessageHash(M->msg_type);
  std::string wire = Wire(M);

  std::vector<MODULE_ID> subscribers;
  GetSubscribers(M->msg_type, subscribers);
  if (dest_mod != NULL && !dest_mod->conn->closing)
    Deliver(dest_mod, wire, M);
  for (MODULE_ID id : subscribers) {
    CModuleRecord *mod = GetRecord(id);
    if (mod == NULL || mod == dest_mod || mod->conn->closing)
      continue;
    // A directed message goes to subscribed loggers too.
    if (dest_mod != NULL && !mod->LoggerStatus)
      continue;
    Deliver(mod, wire, M);
  }
}

void CMessageManager::SendSignal(MSG_TYPE sig, CModuleRecord *dest_mod) {
  CMessage M(sig);
  SendFromManager(&M, dest_mod);
}

void CMessageManager::SendAcknowledge(CModuleRecord *mod) {
  CMessage M(MT_ACKNOWLEDGE);
  M.src_mod_id = MID_MESSAGE_MANAGER;
  M.dest_mod_id = mod->ModuleID;
  M.msg_count = 0;
  M.send_time = GetAbsTime();
  M.reserved = CoreMessageHash(MT_ACKNOWLEDGE);
  std::string wire = Wire(&M);
  Deliver(mod, wire, &M);
  // Every logger is sent a copy, as in pyrtma's manager, except the
  // requester: a logger sent its own ACK twice would take the copy as the
  // reply to its next request.
  std::vector<MODULE_ID> loggers;
  for (auto &entry : m_ConnectedModules)
    if (entry.second.LoggerStatus && entry.first != mod->ModuleID)
      loggers.push_back(entry.first);
  for (MODULE_ID id : loggers) {
    CModuleRecord *logger = GetRecord(id);
    if (logger != NULL && !logger->conn->closing)
      SendToLogger(logger, wire);
  }
}

void CMessageManager::SendHello(CModuleRecord *mod) {
  MDF_HELLO hello;
  mod->Describe(&hello);
  CMessage M(MT_HELLO, &hello, sizeof(hello));
  SendFromManager(&M);
}

void CMessageManager::SendGoodbye(CModuleRecord *mod) {
  MDF_GOODBYE goodbye;
  mod->Describe((MDF_HELLO *)&goodbye);
  CMessage M(MT_GOODBYE, &goodbye, sizeof(goodbye));
  SendFromManager(&M);
}

void CMessageManager::SendIntroductions(CModuleRecord *dest_mod) {
  std::vector<MODULE_ID> ids;
  for (auto &entry : m_ConnectedModules)
    ids.push_back(entry.first);
  for (MODULE_ID id : ids) {
    CModuleRecord *mod = GetRecord(id);
    if (mod == NULL || mod->conn->closing)
      continue;
    MDF_HELLO hello;
    mod->Describe(&hello);
    CMessage M(MT_HELLO, &hello, sizeof(hello));
    M.src_mod_id = MID_MESSAGE_MANAGER;
    M.dest_mod_id = dest_mod->ModuleID;
    M.msg_count = 0;
    M.send_time = GetAbsTime();
    M.reserved = CoreMessageHash(MT_HELLO);
    if (dest_mod->conn->closing)
      return;
    Deliver(dest_mod, Wire(&M), &M);
  }
}

void CMessageManager::SendFailedMessage(CMessage *M, MODULE_ID dest_mod_id) {
  // No report of a failed report, or of a log message, which modules send
  // freely.
  switch (M->msg_type) {
  case MT_FAILED_MESSAGE:
  case MT_RTMA_LOG:
  case MT_RTMA_LOG_CRITICAL:
  case MT_RTMA_LOG_ERROR:
  case MT_RTMA_LOG_WARNING:
  case MT_RTMA_LOG_INFO:
  case MT_RTMA_LOG_DEBUG:
    return;
  default:
    break;
  }
  MDF_FAILED_MESSAGE data;
  memset(&data, 0, sizeof(data));
  data.dest_mod_id = dest_mod_id;
  data.time_of_failure = GetAbsTime();
  data.msg_header = M->GetHeader();
  CMessage F(MT_FAILED_MESSAGE, &data, sizeof(data));
  SendFromManager(&F);
}
