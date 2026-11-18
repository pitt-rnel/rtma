#ifndef _MESSAGEMANAGER_H_
#define _MESSAGEMANAGER_H_

// The RTMA message manager.
//
// One thread serves every module with non-blocking sockets and select(), as
// pyrtma's manager does, so no client can hold up the others:
//
// - Each connection's bytes are buffered until a whole message has arrived.
//   A client that sends part of a message and then nothing more for the
//   stall timeout is dropped.
// - A message for a module other than a logger is sent whole or not at all:
//   one whose connection can't take it now misses it, and FAILED_MESSAGE
//   reports that. What a connection takes of a message is finished later,
//   when it can take more, so a message is never cut short.
// - Loggers are waited for, so they miss nothing; with a logger timeout, a
//   logger that takes no data for that long is dropped.
// - A module dropped while messages are being sent, because a send failed,
//   leaves the routing tables at once; its GOODBYE is sent and its socket
//   closed after the current message.

#include "NonBlockingSocket.h"

#include <RTMA.h>
#include <RTMA_types.h>

#include <chrono>
#include <cstdint>
#include <deque>
#include <memory>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

typedef std::chrono::steady_clock Clock;

// One client connection: its socket, the bytes received of the message being
// read, and the bytes still to send.
struct CConnection {
  NonBlockingSocket::Socket sock = NonBlockingSocket::kInvalid;
  std::string addr;
  uint16_t port = 0;

  std::vector<char> rx; // received bytes not yet handled
  size_t rx_start = 0;  // first unhandled byte in rx
  size_t rx_end = 0;    // one past the last received byte
  Clock::time_point last_rx;

  std::deque<std::string> tx; // bytes still to send, in order
  size_t tx_offset = 0;       // bytes of tx.front() already sent

  bool closing = false; // dropped; closed at the end of the current round
  MODULE_ID module_id = -1;

  size_t Buffered() const { return rx_end - rx_start; }
};

class CModuleRecord {
public:
  MODULE_ID ModuleID = -1;
  CConnection *conn = NULL;
  short LoggerStatus = 0;
  int32_t pid = 0;
  std::string name;
  // Message types this module subscribes to. ALL_MESSAGE_TYPES replaces the
  // individual types, as in pyrtma's manager.
  std::unordered_set<MSG_TYPE> subs;

  void SetName(const char *src_name) {
    name.assign(src_name ? src_name : "");
    if (name.size() > MAX_NAME_LEN - 1)
      name.resize(MAX_NAME_LEN - 1);
  }

  bool SubAll() const { return subs.count(ALL_MESSAGE_TYPES) != 0; }

  // HELLO and GOODBYE have the same layout.
  void Describe(MDF_HELLO *hello) const;

  std::string Label() const;
};

// Module IDs subscribed to one message type. The key ALL_MESSAGE_TYPES holds
// the modules subscribed to every type; they hold no other subscriptions.
typedef std::unordered_set<MODULE_ID> CSubscriberSet;

class CMessageManager {
public:
  CMessageManager();
  ~CMessageManager();

  // Seconds a client may stall partway through sending a message before it
  // is dropped; negative never drops it.
  double stall_timeout = 5.0;
  // Seconds a logger may take no data before it is dropped; negative waits
  // as long as it takes.
  double logger_timeout = -1.0;

  // Listens on server_name and serves modules until a fatal error.
  void MainLoop(const char *server_name);

private:
  MyCString m_Version;
  NonBlockingSocket::Socket m_Listener = NonBlockingSocket::kInvalid;
  std::vector<std::unique_ptr<CConnection>> m_Connections;
  std::vector<CConnection *> m_PendingRemovals;

  MODULE_ID m_NextDynamicModId;
  std::unordered_map<MODULE_ID, CModuleRecord> m_ConnectedModules;
  // Only types with subscribers have an entry.
  std::unordered_map<MSG_TYPE, CSubscriberSet> m_Subscribers;

  // The event loop.
  void AcceptConnections();
  void ReadFrom(CConnection *conn);
  void HandleBuffered(CConnection *conn);
  void Flush(CConnection *conn);
  void DropStalled();
  void FinishRemovals();

  // Drops a connection: it leaves the routing tables at once, and its
  // GOODBYE is sent and its socket closed by FinishRemovals(). error says
  // whether the reason is logged as an error, or as a warning.
  void Drop(CConnection *conn, const std::string &reason, bool error = true);

  // Handling a message.
  void HandleMessage(CConnection *conn, CMessage *M);
  void ProcessMessage(CMessage *M, CConnection *conn, CModuleRecord *src);
  CModuleRecord *GetRecord(MODULE_ID module_id);
  CModuleRecord *GetRecord(CConnection *conn);

  // Connecting and disconnecting.
  MODULE_ID GetDynamicModuleId();
  CModuleRecord *ConnectModule(CConnection *conn, MODULE_ID requested_id,
                               short logger_status, int32_t pid,
                               const char *name);
  void HandleConnect(CMessage *M, CConnection *conn);
  void HandleConnectV2(CMessage *M, CConnection *conn);
  void UpdateConnection(CMessage *M, CModuleRecord *mod);
  void HandleSetName(CMessage *M, CModuleRecord *mod);
  void HandleModuleReady(CMessage *M, CModuleRecord *mod);
  void HandleForceDisconnect(CMessage *M);
  bool ModuleIsConnected(MODULE_ID module_id) const;

  // Subscriptions.
  MSG_TYPE SubscriptionType(CMessage *M);
  void AddSubscriber(CModuleRecord *mod, MSG_TYPE message_type);
  void DropSubscriber(CModuleRecord *mod, MSG_TYPE message_type);
  void RemoveAllSubscriptions(CModuleRecord *mod);
  void AddSubscription(CModuleRecord *mod, MSG_TYPE message_type);
  void RemoveSubscription(CModuleRecord *mod, MSG_TYPE message_type);
  void GetSubscribers(MSG_TYPE message_type, std::vector<MODULE_ID> &ids) const;

  // Sending. Wire() is a message's bytes: its header, then its data.
  static std::string Wire(CMessage *M);
  // Sends to a module other than a logger, whole or not at all. Returns
  // false if its connection can't take the message now.
  bool TrySend(CModuleRecord *mod, const std::string &wire);
  // Sends to a logger, waiting until it has taken everything queued for it.
  void SendToLogger(CModuleRecord *mod, const std::string &wire);
  // Sends a message from another module, or from the manager, to one
  // recipient: loggers are waited for, and a module that can't take it is
  // reported with FAILED_MESSAGE.
  void Deliver(CModuleRecord *mod, const std::string &wire, CMessage *M);

  void DistributeMessage(CMessage *M);
  // A message from the manager: to its subscribers (dest_mod == NULL), or to
  // dest_mod and to subscribed loggers.
  void SendFromManager(CMessage *M, CModuleRecord *dest_mod = NULL);
  void SendSignal(MSG_TYPE sig, CModuleRecord *dest_mod);
  void SendAcknowledge(CModuleRecord *mod);
  void SendHello(CModuleRecord *mod);
  void SendGoodbye(CModuleRecord *mod);
  void SendIntroductions(CModuleRecord *dest_mod);
  void SendFailedMessage(CMessage *M, MODULE_ID dest_mod_id);
};

#endif //_MESSAGEMANAGER_H_
