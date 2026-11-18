//////////////////////////////////////////////////////////////////////
//
// UPipe - an abstract base class that represents one end of a
//         bi-directional universal pipe,
//         i.e. one that works on any operating system and is either
//         a local or a network pipe. The member functions throw a
//         UPipeException on failure. A functional UPipe object
//         cannot be constructed directly, but rather is returned
//         by UPipeClient::Connect()
//
// UPipeClient - an abstract base class for a client that connects
//               to a server, such as the message manager
//
// The library used to have a server side too (UPipeServer, SocketPipeServer
// and UPipeAutoServer), which only the message manager used. The manager now
// has its own non-blocking sockets, in src/modules/MessageManager.
//
// Copyright (c) 2009 by Meel Velliste, University of Pittsburgh

#ifndef _UPIPE_H_
#define _UPIPE_H_

#include "../OS_defines.h"

#ifdef _WINDOWS_C
// prevent WINSOCK1 from being included (included from within windows.h)
#ifndef _WINSOCKAPI_
#define _WINSOCKAPI_
#endif
// WINDOWS only h files
#include <windows.h>
#else
/*	LINUX   only h files*/
#include <unistd.h>
#endif

/*Non OS specific h files*/

#include <cstdint>
#include <cstdlib>

// If this is compiled as part of a Matlab MEX file, then this
// hack helps redirect memory allocation requests to the Matlab
// memory manager. This is important in Matlab because otherwise
// it will have unpredictable behavior and unexplained crashes.
#include "mex_hack.h"

#include "../MyCException.h"
#include <MyCString.h>

// windows only functions
#ifdef _WINDOWS_C
#else // unix only functions

void Sleep(unsigned int time_ms);

#endif

// An exception class specific to this UPipe library
class UPipeException : public MyCException {
public:
  UPipeException() : MyCException() {}
  UPipeException(const char *err_str, int error_code = 0)
      : MyCException(err_str, error_code) {}
  UPipeException(MyCString &str, int error_code = 0)
      : MyCException(str, error_code) {}
};

class UPipeClosedException : public UPipeException {
public:
  UPipeClosedException() : UPipeException() {}
  UPipeClosedException(const char *err_str, int error_code = 0)
      : UPipeException(err_str, error_code) {}
  UPipeClosedException(MyCString &str, int error_code = 0)
      : UPipeException(str, error_code) {}
};

class UPipeSignalException : public UPipeException {
public:
  UPipeSignalException() : UPipeException() {}
  UPipeSignalException(const char *err_str, int error_code = 0)
      : UPipeException(err_str, error_code) {}
  UPipeSignalException(MyCString &str, int error_code = 0)
      : UPipeException(str, error_code) {}
};

// short-hand for try and catch that can be put in every single function so as
// to build a stack trace for each error that occurs
#define TRY try
#define CATCH_and_THROW(FunctionName)                                          \
  catch (UPipeSignalException & E) {                                           \
    E.AddToStack((FunctionName));                                              \
    throw E;                                                                   \
  }                                                                            \
  catch (UPipeClosedException & E) {                                           \
    E.AddToStack((FunctionName));                                              \
    throw E;                                                                   \
  }                                                                            \
  catch (UPipeException & E) {                                                 \
    E.AddToStack((FunctionName));                                              \
    throw E;                                                                   \
  }                                                                            \
  catch (MyCException & E) {                                                   \
    E.AddToStack((FunctionName));                                              \
    throw E;                                                                   \
  }                                                                            \
  catch (...) {                                                                \
    MyCException E("Caught unknown exception");                                \
    E.AddToStack((FunctionName));                                              \
    throw E;                                                                   \
  }

class UPipe {
public:
  virtual ~UPipe() {}

  // Obtains the capacity of the pipe, i.e. how many bytes can be written
  // to the pipe without being read out the other end.
  virtual int GetCapacity(void) = 0;

  // Makes a blocking call to read n_bytes bytes from the pipe into
  // data_buffer. Does not return until the requested number of bytes
  // are read.
  void Read(void *data_buffer, int n_bytes) {
    TRY { Read(data_buffer, n_bytes, -1); }
    CATCH_and_THROW("UPipe::Read");
  }

  // Reads n_bytes bytes from the pipe into data_buffer, blockingly
  // if timeout is -1, non-blockingly if timeout is 0 and timing out
  // after timeout seconds otherwise. Returns the number of bytes read.
  virtual int Read(void *data_buffer, int n_bytes, double timeout) = 0;

  // Makes a blocking call to write n_bytes from data_buffer to the pipe. Does
  // not return until the requested number of bytes have been written. Returns
  // number of bytes written.
  int Write(void *data_buffer, int n_bytes) {
    TRY { return Write(data_buffer, n_bytes, -1); }
    CATCH_and_THROW("UPipe::Write");
  }

  // Writes n_bytes from data_buffer into the pipe. If the pipe does not have
  // enough capacity to write all the bytes, then the call blocks and does not
  // return until enough bytes are read out from the other end that the write
  // call can complete writing all the data. If timeout is -1, waits
  // indefinitely. If a timeout in seconds is given, only waits that long. If
  // timeout is 0, then never blocks (if no space in pipe, then returns with 0).
  // Returns number of bytes written.
  virtual int Write(void *data_buffer, int n_bytes, double timeout) = 0;
  virtual int GetIpAddress(char *addr, uint16_t *port, int bufsz) = 0;
};

class UPipeClient {
public:
  UPipeClient() { _pServerPipe = NULL; }

  // Connects to the server that was configured through the Create() method
  UPipe *Connect(void) {
    TRY {
      if (_pServerPipe != NULL)
        return _pServerPipe;
      return DoConnect();
    }
    CATCH_and_THROW("UPipeClient::Connect");
  }

  // Disconnects from the server
  void Disconnect(void) {
    TRY {
      if (_pServerPipe == NULL)
        return;
      DoDisconnect();
      delete _pServerPipe;
      _pServerPipe = NULL;
    }
    CATCH_and_THROW("UPipeClient::Disconnect");
  }

  // Destructor makes sure we disconnect cleanly
  virtual ~UPipeClient() {
    if (_pServerPipe != NULL)
      delete _pServerPipe;
  }

protected:
  UPipe *_pServerPipe;
  virtual UPipe *DoConnect(void) = 0;
  virtual void DoDisconnect(void) = 0;
};

class UPipeFactory {
public:
  // Creates a pipe client and configures it as either local pipe
  // or socket client, depending on the input string.
  // If server_addr contains a ":" then the string before the colon is treated
  // as a hostname or IP address and the string after colon is port number. If
  // there is no colon then server_addr is treated as a local pipe name. On
  // Unix, if a local pipe, the system will look for the file-system stub for
  // the pipe in /tmp by default unless the name contains "/" characters in
  // which case the specifid path is used.
  static UPipeClient *CreateClient(char *server_addr);

  // The maximum allowed length of string passed to CreateClient
  static const int MAX_SERVER_ADDR_LENGTH = 1024;

private:
  // Enum type that specifies server type
  typedef enum { NamedPipe, Socket } ServerType;
  static ServerType ParseServerAddress(const char *server_addr,
                                       char *server_name, short *port_no);
};

///////////////////////////////////////////////////////////////////////////////
//
// UPipeAutoClient - the highest level interface provided by the PipeLib
// library.

// Implements a simple pipe client that connects to a server automatically
// and keeps trying to re-connect if connection fails.
class UPipeAutoClient {
protected:
  UPipeClient *_client;
  bool _keepRunning;

public:
  UPipeAutoClient() {
    _client = NULL;
    _keepRunning = false;
  }
  ~UPipeAutoClient() {
    if (_client != NULL) {
      _client->Disconnect();
      delete _client;
    }
  }

  void Run(char *ServerName) {
    // Connect to server
    _client = UPipeFactory::CreateClient(ServerName);
    UPipe *server_pipe = _client->Connect();

    _keepRunning = true;
    while (_keepRunning) {
      try {
        // Call the Main() implemented by a derived class
        Main(server_pipe);
      } catch (UPipeClosedException) {
        // If the connection to the server fails, perform
        // cleanup so we can connect again
        _client->Disconnect();
      }
      server_pipe = ReConnect();
    }
  }

  // Keeps trying to reconnect to the server
  UPipe *ReConnect(void) {
    while (true) {
      try {
        return _client->Connect();
      } catch (UPipeException) {
        Sleep(200);
      }
    }
  }

  // Main() - An abstract method to be implemented by a derived class to
  // perform whatever operations a client module may need. Gets called from
  // within Run() after the auto-client manages to get connected
  // to the server.
  virtual void Main(UPipe *pServerPipe) = 0;
};

#endif // _UPIPE_H_
