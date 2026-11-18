// rtma_test_client: drives the C++ client library for the interop tests.
//
//   rtma_test_client SERVER SCENARIO MOD_ID [ARGS...]
//
//   connect [NAME]      connect with NAME, and stay until stdin closes
//   rename NAME         connect, then set the name, and stay
//   connect_twice       connect, disconnect, and connect again
//   echo COUNT          reply to COUNT messages of type 1001 with type 1002
//   send BYTES DEST_MOD DEST_HOST [VERSION]
//                       send one message of type 1001
//   module_ready        send MODULE_READY, and stay until stdin closes
//   read_once           read one message
//
// Each scenario prints key=value lines on stdout, which test_cpp_client.py
// reads, and exits with status 0 unless something unexpected failed. Errors
// that a scenario expects are reported as error=... lines.

#include <MyCException.h>
#include <RTMA.h>
#include <RTMA_types.h>
#include <Timing.h>

#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>

namespace {

const MSG_TYPE MT_TEST_REQUEST = 1001;
const MSG_TYPE MT_TEST_REPLY = 1002;

void Print(const std::string &line) {
  std::cout << line << std::endl; // endl flushes, so the test sees each line
}

std::string Trace(const MyCException &E) {
  MyCString err;
  E.AppendTraceToString(err);
  std::string text = err.GetContent() ? err.GetContent() : "";
  for (char &c : text)
    if (c == '\n' || c == '\r')
      c = ' ';
  return text;
}

double Seconds() {
  using namespace std::chrono;
  return duration<double>(steady_clock::now().time_since_epoch()).count();
}

// Connect, report the module ID and how long connecting took.
bool Connect(RTMA_Module &module, char *server) {
  double start = Seconds();
  try {
    module.ConnectToMMM(server);
  } catch (MyCException &E) {
    Print("connect_seconds=" + std::to_string(Seconds() - start));
    Print("error=" + Trace(E));
    return false;
  }
  Print("connect_seconds=" + std::to_string(Seconds() - start));
  Print("module_id=" + std::to_string(module.GetModuleID()));
  return true;
}

// Stay connected until stdin closes.
int ScenarioConnect(RTMA_Module &module, char *server) {
  if (!Connect(module, server))
    return 0;
  Print("pid=" + std::to_string(module.GetPid()));
  std::string line;
  while (std::getline(std::cin, line)) {
  }
  module.DisconnectFromMMM();
  Print("disconnected");
  return 0;
}

// Connect, disconnect, and connect again.
int ScenarioConnectTwice(RTMA_Module &module, char *server) {
  if (!Connect(module, server))
    return 1;
  module.DisconnectFromMMM();
  if (!Connect(module, server))
    return 0;
  module.DisconnectFromMMM();
  Print("reconnected");
  return 0;
}

// Connect, then set the module's name, and stay until stdin closes.
int ScenarioRename(RTMA_Module &module, char *server, const char *name) {
  if (!Connect(module, server))
    return 1;
  module.SetModuleName(name);
  Print("renamed");
  std::string line;
  while (std::getline(std::cin, line)) {
  }
  module.DisconnectFromMMM();
  return 0;
}

// Answer each MT_TEST_REQUEST with an MT_TEST_REPLY of the same data to its
// sender, COUNT times.
int ScenarioEcho(RTMA_Module &module, char *server, int count) {
  if (!Connect(module, server))
    return 1;
  module.Subscribe(MT_TEST_REQUEST);
  Print("ready");
  CMessage M;
  int answered = 0;
  while (answered < count) {
    if (!module.ReadMessage(&M, 5.0)) {
      Print("error=timed out");
      return 1;
    }
    if (M.msg_type != MT_TEST_REQUEST)
      continue;
    Print("recv msg_type=" + std::to_string(M.msg_type) +
          " msg_count=" + std::to_string(M.msg_count) +
          " src_mod_id=" + std::to_string(M.src_mod_id) +
          " dest_mod_id=" + std::to_string(M.dest_mod_id) +
          " num_data_bytes=" + std::to_string(M.num_data_bytes) +
          " reserved=" + std::to_string((unsigned)M.reserved));
    std::vector<char> data(M.num_data_bytes);
    M.GetData(data.data());
    CMessage R(MT_TEST_REPLY, data.data(), (int)data.size());
    module.SendMessage(&R, M.src_mod_id);
    ++answered;
  }
  module.DisconnectFromMMM();
  return 0;
}

// Send one message to the module and host given, with the version given.
int ScenarioSend(RTMA_Module &module, char *server, int bytes, int dest_mod,
                 int dest_host, uint32_t version) {
  if (!Connect(module, server))
    return 1;
  std::vector<char> data(bytes, 'x');
  CMessage M(MT_TEST_REQUEST, data.data(), bytes, version);
  try {
    module.SendMessage(&M, (MODULE_ID)dest_mod, (HOST_ID)dest_host);
    Print("sent");
  } catch (MyCException &E) {
    Print("error=" + Trace(E));
  }
  return 0;
}

// Send MODULE_READY, a core message, and stay connected until stdin closes.
int ScenarioModuleReady(RTMA_Module &module, char *server) {
  if (!Connect(module, server))
    return 1;
  module.SendModuleReady();
  Print("sent");
  std::string line;
  while (std::getline(std::cin, line)) {
  }
  module.DisconnectFromMMM();
  return 0;
}

// Read one message, and report what happened.
int ScenarioReadOnce(RTMA_Module &module, char *server) {
  if (!Connect(module, server))
    return 1;
  CMessage M;
  try {
    int got = module.ReadMessage(&M, 5.0);
    Print("got=" + std::to_string(got) + " msg_type=" + std::to_string(M.msg_type));
  } catch (MyCException &E) {
    Print("error=" + Trace(E));
  }
  Print("connected=" + std::to_string(module.IsConnected()));
  return 0;
}

} // namespace

int main(int argc, char *argv[]) {
  if (argc < 4) {
    std::fprintf(stderr, "usage: %s SERVER SCENARIO MOD_ID [ARGS...]\n", argv[0]);
    return 2;
  }
  char *server = argv[1];
  std::string scenario = argv[2];
  MODULE_ID mod_id = (MODULE_ID)std::atoi(argv[3]);

  RTMA_Module module(mod_id, 0);
  module.Logger().SetConsoleEnabled(false);
  module.Logger().SetRTMAEnabled(false);

  try {
    if (scenario == "connect") {
      if (argc > 4)
        module.SetModuleName(argv[4]);
      return ScenarioConnect(module, server);
    }
    if (scenario == "connect_twice")
      return ScenarioConnectTwice(module, server);
    if (scenario == "rename")
      return ScenarioRename(module, server, argv[4]);
    if (scenario == "echo")
      return ScenarioEcho(module, server, argc > 4 ? std::atoi(argv[4]) : 1);
    if (scenario == "send")
      return ScenarioSend(module, server, std::atoi(argv[4]), std::atoi(argv[5]),
                          std::atoi(argv[6]),
                          argc > 7 ? (uint32_t)std::strtoul(argv[7], NULL, 0) : 0);
    if (scenario == "module_ready")
      return ScenarioModuleReady(module, server);
    if (scenario == "read_once")
      return ScenarioReadOnce(module, server);
  } catch (MyCException &E) {
    Print("error=" + Trace(E));
    return 1;
  }
  std::fprintf(stderr, "unknown scenario: %s\n", scenario.c_str());
  return 2;
}
