// RTMA Client Logger
// 
// Log messages to console and optionally via RTMA and/or to a text file
// Messages include metadata: log level, timestamp, filename, line number, function name
// Logger will ignore any message logged below its "level" value
// 
// Example usage:
// RTMA_Module client = RTMA_Module();
// RTMA_Logger log = RTMA_Logger("log_name", LogLevel::lINFO, &client);
// log.info("example log message", LOG_SRC);
// log.error("example error log", LOG_SRC);

#ifndef _RTMA_LOGGER_H_
#define _RTMA_LOGGER_H_

#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#define _HAS_STD_BYTE 0
#endif

#include <string>
#include <fstream>

#include "RTMA.h"
#include "RTMA_types.h"


// combine function, file and line macros, use to simplify input to log methods
#define LOG_SRC __func__, __FILE__, __LINE__

// default log levels
enum LogLevel :int {
    lNOTSET = -1,
    lALL = 0,
    lDEBUG = 10,
    lINFO = 20,
    lWARNING = 30,
    lERROR = 40,
    lCRITICAL = 50,
    lOFF = 1000
};

const char* levelToName(int level);
std::string levelToNameStr(int level);
int nameToLevel(const char* name);

// avoid msvc deprecated unsafe warnings
static int strcpy_safe(char* destination, size_t dest_size, const char* source);
static int localtime_safe(tm* tmDest, time_t const* const sourceTime);

class RTMA_Logger {
public:
    RTMA_Logger(const char* log_name = "", int log_level = LogLevel::lNOTSET, RTMA_Module* rtma_client = &RTMA_Module(0, 0), const char* log_filename = "");
    ~RTMA_Logger();

    // default log level functions
    void debug(const char* message, const char* src_func, const char* src_file, int src_line);
    void info(const char* message, const char* src_func, const char* src_file, int src_line);
    void warning(const char* message, const char* src_func, const char* src_file, int src_line);
    void error(const char* message, const char* src_func, const char* src_file, int src_line);
    void critical(const char* message, const char* src_func, const char* src_file, int src_line);
    // main log function (accepts any level integer)
    void log(const char* message, int level, const char* src_func, const char* src_file, int src_line);

    // getter and setter methods
    RTMA_Module* get_rtma_client_pointer(void);
    void set_rtma_client(RTMA_Module* rtma_client);
    std::string get_log_name(void);
    void set_log_name(const char*);
    std::string get_log_filename(void);
    void set_log_filename(const char* log_filename);

    // level value is public
    int level;

private:
    std::string log_name_;
    std::string log_filename_;
    RTMA_Module* rtma_client_;
    CMessage* log_msg_;
    MDF_RTMA_LOG* log_msg_data_;
};

#endif