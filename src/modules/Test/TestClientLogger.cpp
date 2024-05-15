#include "RTMA.h"
#include "ClientLogger.h"
#include <chrono>
#include <thread>
#include <iostream>

#define MM_IP "localhost:7111"
#define LOG_FILENAME1 "./test_logfile1.txt"
#define LOG_FILENAME2 "./test_logfile2.txt"

using namespace std::chrono_literals;

int main(int argc, char** argv) {
    int log_level = LogLevel::lINFO;
    std::cout << "Starting logger test, log level = " << levelToNameStr(log_level) << std::endl;
    std::this_thread::sleep_for(250ms);
    RTMA_Module client = RTMA_Module(0,0);
    client.SetLogName("TestClientLog");

    client.Info("Setting log1 filename", LOG_SRC);
    client.SetLogFilename(LOG_FILENAME1);
    client.Info("This should be the first message in logfile1", LOG_SRC);

    // confirm client is set
    if (client.GetLoggerPointer()->get_rtma_client_pointer() == &client)
        client.Info("RTMA client set successfully", LOG_SRC);
    else
        client.Error("RTMA client not set", LOG_SRC);

    client.Info("Connecting to MMM", LOG_SRC);
    client.ConnectToMMM((char*) MM_IP);
    client.Info("Connected. This should be first log sent via RTMA.", LOG_SRC);
    std::this_thread::sleep_for(250ms);
    
    client.Warning("Test warning 1", LOG_SRC);
    std::this_thread::sleep_for(250ms);
    client.Error("Test error 1", LOG_SRC);
    std::this_thread::sleep_for(250ms);
    client.Critical("Test critical 1", LOG_SRC);
    std::this_thread::sleep_for(250ms);
    

    client.Info("Clearing log1 filename", LOG_SRC);
    client.SetLogFilename(""); // this should close file and not open a new one
    client.Info("This should not log to file", LOG_SRC);
    client.SetLogFilename(LOG_FILENAME2);
    client.Info("But this should log to file2", LOG_SRC);
    client.SetLogFilename(LOG_FILENAME1);
    client.Info("log1 set back to file1", LOG_SRC);
    std::this_thread::sleep_for(250ms);

    client.Info("Disconnecting RTMA client", LOG_SRC);
    client.DisconnectFromMMM();
    client.Info("RTMA Disconnected 1", LOG_SRC);
    std::cout << "Done" << std::endl;
    
    return 0;
}