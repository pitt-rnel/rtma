// Non-blocking TCP sockets for the message manager's event loop.
//
// The manager reads and writes every client without blocking, from one
// thread, as pyrtma's manager does. This is the little it needs from the
// platform: a listening socket, accepted connections, recv and send that
// return at once, and select(). The client library's UPipe classes are
// unchanged.

#ifndef _MM_NET_H_
#define _MM_NET_H_

#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

namespace net {

#ifdef _WIN32
typedef uintptr_t Socket; // SOCKET
#else
typedef int Socket;
#endif
extern const Socket kInvalid;

// The most sockets one select() can watch, the listening socket included.
// On Linux and macOS a descriptor must also be below this.
extern const size_t kMaxSockets;

// Opens a listening socket on server_name, "host:port" or ":port" for every
// interface. Throws MyCException if the address is invalid or the port
// can't be bound.
Socket Listen(const char *server_name);

// Accepts a pending connection, non-blocking and with TCP_NODELAY, and gives
// its peer's address and port. Returns kInvalid when none is pending.
Socket Accept(Socket listener, std::string &addr, uint16_t &port);

// True if select() can watch the socket (see kMaxSockets).
bool Selectable(Socket s);

// Receives up to size bytes. Returns the number received, 0 if none are
// available yet, or -1 if the connection was closed or failed; error then
// says why.
long Recv(Socket s, char *buffer, size_t size, std::string &error);

// Sends up to size bytes. Returns the number sent, 0 if the connection can't
// take any now, or -1 if it failed; error then says why.
long Send(Socket s, const char *buffer, size_t size, std::string &error);

void Close(Socket s);

// Waits up to timeout seconds (or forever, if negative) until a socket in
// read can be read or one in write can be written, and sets the matching
// flags. Returns false if select() failed.
bool Select(const std::vector<Socket> &read, const std::vector<Socket> &write,
            double timeout, std::vector<char> &readable,
            std::vector<char> &writable);

} // namespace net

#endif // _MM_NET_H_
