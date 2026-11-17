// See Net.h.

#ifdef _WIN32
// select() on Windows takes at most FD_SETSIZE sockets, 64 unless it is
// defined before winsock2.h. Only this file uses fd_set.
#define FD_SETSIZE 1024
#include <winsock2.h>
#include <ws2tcpip.h>
#else
#include <arpa/inet.h>
#include <cerrno>
#include <fcntl.h>
#include <netdb.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <unistd.h>
#endif

#include "Net.h"

#include <MyCException.h>

#include <cstdlib>
#include <cstring>

#ifndef MSG_NOSIGNAL
#define MSG_NOSIGNAL 0 // macOS: SO_NOSIGPIPE is set on each socket instead
#endif

namespace net {

#ifdef _WIN32
const Socket kInvalid = INVALID_SOCKET;
#else
const Socket kInvalid = -1;
#endif
const size_t kMaxSockets = FD_SETSIZE;

namespace {

std::string LastError() {
#ifdef _WIN32
  return "WSA error " + std::to_string(WSAGetLastError());
#else
  return strerror(errno);
#endif
}

bool WouldBlock() {
#ifdef _WIN32
  return WSAGetLastError() == WSAEWOULDBLOCK;
#else
  return errno == EAGAIN || errno == EWOULDBLOCK || errno == EINTR;
#endif
}

void Startup() {
#ifdef _WIN32
  static bool started = false;
  if (!started) {
    WSADATA data;
    if (WSAStartup(MAKEWORD(2, 2), &data) != 0)
      throw MyCException("Could not start Winsock");
    started = true;
  }
#endif
}

void SetNonBlocking(Socket s) {
#ifdef _WIN32
  u_long on = 1;
  ioctlsocket(s, FIONBIO, &on);
#else
  fcntl(s, F_SETFL, fcntl(s, F_GETFL, 0) | O_NONBLOCK);
#endif
}

} // namespace

Socket Listen(const char *server_name) {
  Startup();
  std::string name = server_name ? server_name : "";
  size_t colon = name.rfind(':');
  if (colon == std::string::npos)
    throw MyCException("Invalid server name, expected host:port or :port");
  std::string host = name.substr(0, colon);
  std::string port_text = name.substr(colon + 1);
  char *end = NULL;
  long port = strtol(port_text.c_str(), &end, 10);
  if (port_text.empty() || *end != 0 || port < 1 || port > 65535)
    throw MyCException(
        "Invalid server name, the port must be a number from 1 to 65535");

  sockaddr_in address;
  memset(&address, 0, sizeof(address));
  address.sin_family = AF_INET;
  address.sin_port = htons((unsigned short)port);
  if (host.empty()) {
    address.sin_addr.s_addr = htonl(INADDR_ANY);
  } else {
    addrinfo hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    addrinfo *result = NULL;
    if (getaddrinfo(host.c_str(), NULL, &hints, &result) != 0 || result == NULL)
      throw MyCException(("Cannot resolve server host '" + host + "'").c_str());
    address.sin_addr = ((sockaddr_in *)result->ai_addr)->sin_addr;
    freeaddrinfo(result);
  }

  Socket s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
  if (s == kInvalid)
    throw MyCException(("Cannot create listening socket: " + LastError()).c_str());

  // Listen again at once after a restart, while the manager's side of the
  // connections it closed waits in TIME_WAIT, but never share the port.
#ifdef _WIN32
  BOOL exclusive = TRUE;
  setsockopt(s, SOL_SOCKET, SO_EXCLUSIVEADDRUSE, (const char *)&exclusive,
             sizeof(exclusive));
#else
  int reuse = 1;
  setsockopt(s, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));
#endif

  if (bind(s, (sockaddr *)&address, sizeof(address)) != 0) {
    std::string error = LastError();
    Close(s);
    throw MyCException(("Cannot bind to server port, the error is: " + error).c_str());
  }
  if (listen(s, SOMAXCONN) != 0) {
    std::string error = LastError();
    Close(s);
    throw MyCException(("Cannot listen on server port: " + error).c_str());
  }
  SetNonBlocking(s);
  return s;
}

Socket Accept(Socket listener, std::string &addr, uint16_t &port) {
  sockaddr_in peer;
  socklen_t length = sizeof(peer);
  Socket s = accept(listener, (sockaddr *)&peer, &length);
  if (s == kInvalid)
    return kInvalid;
  SetNonBlocking(s);
  int one = 1;
  setsockopt(s, IPPROTO_TCP, TCP_NODELAY, (const char *)&one, sizeof(one));
#if defined(SO_NOSIGPIPE)
  setsockopt(s, SOL_SOCKET, SO_NOSIGPIPE, &one, sizeof(one));
#endif
  char text[INET_ADDRSTRLEN] = "";
  inet_ntop(AF_INET, &peer.sin_addr, text, sizeof(text));
  addr = text;
  port = ntohs(peer.sin_port);
  return s;
}

bool Selectable(Socket s) {
#ifdef _WIN32
  (void)s;
  return true; // Windows limits the number of sockets, checked by the caller
#else
  return s >= 0 && (size_t)s < kMaxSockets;
#endif
}

long Recv(Socket s, char *buffer, size_t size, std::string &error) {
  long n = (long)recv(s, buffer, (int)size, 0);
  if (n > 0)
    return n;
  if (n == 0) {
    error = "Connection closed by the client.";
    return -1;
  }
  if (WouldBlock())
    return 0;
  error = "Connection failed: " + LastError();
  return -1;
}

long Send(Socket s, const char *buffer, size_t size, std::string &error) {
  long n = (long)send(s, buffer, (int)size, MSG_NOSIGNAL);
  if (n >= 0)
    return n;
  if (WouldBlock())
    return 0;
  error = "Send failed: " + LastError();
  return -1;
}

void Close(Socket s) {
  if (s == kInvalid)
    return;
#ifdef _WIN32
  closesocket(s);
#else
  close(s);
#endif
}

bool Select(const std::vector<Socket> &read, const std::vector<Socket> &write,
            double timeout, std::vector<char> &readable,
            std::vector<char> &writable) {
  fd_set rset, wset;
  FD_ZERO(&rset);
  FD_ZERO(&wset);
  Socket highest = 0;
  for (Socket s : read) {
    FD_SET(s, &rset);
    if (s > highest)
      highest = s;
  }
  for (Socket s : write) {
    FD_SET(s, &wset);
    if (s > highest)
      highest = s;
  }
  timeval tv;
  timeval *ptv = NULL;
  if (timeout >= 0) {
    tv.tv_sec = (long)timeout;
    tv.tv_usec = (long)((timeout - (double)tv.tv_sec) * 1e6);
    ptv = &tv;
  }
  int status = select((int)(highest + 1), &rset, write.empty() ? NULL : &wset,
                      NULL, ptv);
  readable.assign(read.size(), 0);
  writable.assign(write.size(), 0);
  if (status < 0) {
#ifndef _WIN32
    if (errno == EINTR)
      return true;
#endif
    return false;
  }
  for (size_t i = 0; i < read.size(); i++)
    readable[i] = FD_ISSET(read[i], &rset) ? 1 : 0;
  for (size_t i = 0; i < write.size(); i++)
    writable[i] = FD_ISSET(write[i], &wset) ? 1 : 0;
  return true;
}

} // namespace net
