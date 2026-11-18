//
// Copyright (c) 2009 by Meel Velliste, University of Pittsburgh

#include "UPipe.h"
#include "SocketPipe.h"
#include <OS_defines.h>
#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <ostream>
#include <string.h>

#ifdef _UNIX_C

void Sleep(unsigned int time_ms) {
  TRY {
    // usleep(time_ms*1000); --> obselete function- using nanosleep instead
    struct timespec tim;
    tim.tv_sec = (time_ms / 1000);
    tim.tv_nsec = (time_ms % 1000) * 1000000;
    nanosleep(&tim, NULL);
  }
  CATCH_and_THROW("void Sleep(unsigned int time_ms)");
}
#endif

// Parses a server address string. If server_addr
// contains a ":" then the string before the colon is treated as a hostname
// or IP address (output in server_name) and the string after colon is converted
// to a number and output in port_no. If there is no colon then server_addr is
// treated as a local pipe name and is copied to the server_name output (on
// Windows, "\\.\pipe\" will be prepended to the output string in server_name,
// and on Unix, "/tmp/" will be prepended so that the file stub for the pipe
// will be created in the /tmp directory by default unless the server_addr
// contains any "/" characters.). port_no will be -1 if local pipe.
UPipeFactory::ServerType
UPipeFactory::ParseServerAddress(const char *server_addr, char *server_name,
                                 short *port_no) {
  TRY {
    int len = 0, i;
    ServerType type = NamedPipe;
    bool directory_specified = false;

    len = (int)strlen(server_addr);
    if (len > MAX_SERVER_ADDR_LENGTH)
      throw UPipeException("Invalid server name, exceeds 512 characters");

    for (i = 0; i < len; i++) {
      if (server_addr[i] == 0) { // if a named pipe- break at string end
        break;
      }
      if (server_addr[i] ==
          '/') { // if a named pipe in a specified Unix directory
        directory_specified = true;
      }
      if (server_addr[i] == ':') { // if a socket- break at ':'
        type = Socket;
        break;
      }
    }

    // copy name & terminating NULL
    char tmp_server_name[MAX_SERVER_ADDR_LENGTH + 1] = {0};
    strncpy(tmp_server_name, server_addr, i);
    tmp_server_name[i] = 0;

    // set port
    switch (type) {
    case NamedPipe:
      *port_no = -1;
      break;

    case Socket: {
      // The port is the rest of the string after ':', a number from 1 to
      // 65535. It is returned as a short; a port above 32767 wraps around,
      // and htons() recovers it.
      const char *str_port = server_addr + i + 1;
      char *end = NULL;
      long port = strtol(str_port, &end, 10);
      if (*str_port == 0 || *end != 0 || port < 1 || port > 65535)
        throw UPipeException(
            "Invalid server name, the port must be a number from 1 to 65535");
      *port_no = (short)(unsigned short)port;
      break;
    }
    }

    // Prepend directory name to output if need be
    server_name[0] = 0;
    switch (type) {
    case NamedPipe: {
#ifdef _WINDOWS_C
      char pipe_dir[100] =
          "\\\\.\\pipe\\"; // required prefix for windows named pipe
#else
      char pipe_dir[100] = "/tmp/"; // default prefix for Unix named pipe
      if (directory_specified)
        pipe_dir[0] = 0;
#endif
      strcpy(server_name, pipe_dir);
      break;
    }

    case Socket:
      break;
    }

    // Concatenate server name to output
    strcat(server_name, tmp_server_name);

    return type;
  }
  CATCH_and_THROW("UPipe::ParseServerAddress");
}

UPipeClient *UPipeFactory::CreateClient(char *server_addr) {
  TRY {
    if ((int)strlen(server_addr) > MAX_SERVER_ADDR_LENGTH)
      throw UPipeException("Server address string exceeds max length");

    char server_name[MAX_SERVER_ADDR_LENGTH];
    short port_no;
    ServerType type = ParseServerAddress(server_addr, server_name, &port_no);
    switch (type) {
    case NamedPipe: {
      // #ifdef _UNIX_C
      // UnixNamedPipeClient *pNamedPipeClient = new UnixNamedPipeClient(
      // server_name); #else WinNamedPipeClient pNamedPipeClient = new
      // WinNamedPipeClient( server_name); #endif return (UPipeClient*)
      // pNamedPipeClient;
      throw UPipeException("Named pipes not yet implemented");
      break;
    }
    case Socket: {
      SocketPipeClient *pSocketClient =
          new SocketPipeClient(server_name, port_no);
      return (UPipeClient *)pSocketClient;
      break;
    }
    default:
      throw UPipeException("Unhandled client type");
    }
  }
  CATCH_and_THROW("UPipeClient::Create");
}
