#include "ClientLogger.h"
#include <map>
#include <string>
#include <iostream>
#include <fstream>
#include <chrono>
#include <ctime>
#include <iomanip>
#include <cstring>
#include <cerrno>

#if (defined(_HAS_CXX17) && _HAS_CXX17 > 0)
#include <filesystem>
#endif

const std::map<const char*, int> name_to_level_map{
    {"lNOTSET", LogLevel::lNOTSET},
    {"lALL", LogLevel::lALL},
    {"lDEBUG", LogLevel::lDEBUG},
    {"lINFO", LogLevel::lINFO},
    {"lWARNING", LogLevel::lWARNING},
    {"lERROR", LogLevel::lERROR},
    {"lCRITICAL", LogLevel::lERROR},
    {"lOFF", LogLevel::lOFF},
    {"NOTSET", LogLevel::lNOTSET},
    {"ALL", LogLevel::lALL},
    {"DEBUG", LogLevel::lDEBUG},
    {"INFO", LogLevel::lINFO},
    {"WARNING", LogLevel::lWARNING},
    {"ERROR", LogLevel::lERROR},
    {"CRITICAL", LogLevel::lCRITICAL},
    {"OFF", LogLevel::lOFF}
};

const std::map<int, const char*> level_to_name_map{
    {LogLevel::lNOTSET, "NOTSET"},
    {LogLevel::lALL, "ALL"},
    {LogLevel::lDEBUG, "DEBUG"},
    {LogLevel::lINFO, "INFO"},
    {LogLevel::lWARNING, "WARNING"},
    {LogLevel::lERROR, "ERROR"},
    {LogLevel::lCRITICAL, "CRITICAL"},
    {LogLevel::lOFF, "OFF"},
};

const std::map<int, int>level_to_mt_map{
    {LogLevel::lNOTSET, MT_RTMA_LOG},
    {LogLevel::lALL, MT_RTMA_LOG},
    {LogLevel::lDEBUG, MT_RTMA_LOG_DEBUG},
    {LogLevel::lINFO, MT_RTMA_LOG_INFO},
    {LogLevel::lWARNING, MT_RTMA_LOG_WARNING},
    {LogLevel::lERROR, MT_RTMA_LOG_ERROR},
    {LogLevel::lCRITICAL, MT_RTMA_LOG_CRITICAL},
    {LogLevel::lOFF, MT_RTMA_LOG},
};

const char* levelToName(int level) {
    return level_to_name_map.at(level);
}

std::string levelToNameStr(int level) {
    return (std::string)levelToName(level);
}

int nameToLevel(const char* name) {
    return name_to_level_map.at(name);
}

int levelToMT(int level) {
    return level_to_mt_map.at(level);
}

static int strcpy_safe(char* destination, size_t dest_size, const char* source) {
#ifdef _WIN32
    return strcpy_s(destination, dest_size, source);
#else
    size_t src_len = strlen(source);
    if (destination == nullptr) {
        return EINVAL;
    }
    else if (source == nullptr) {
        destination[0] = 0;
        return EINVAL;
    }
    else if (dest_size < src_len) {
        destination[0] = 0;
        return ERANGE;
    }
    else {
        strcpy(destination, source);
        return 0;
    }
#endif
}

static int localtime_safe(tm* tmDest, time_t const* const sourceTime) {
#ifdef _WIN32
    return localtime_s(tmDest, sourceTime);
#else
    if (tmDest == nullptr) {
        return EINVAL;
    }
    else if (sourceTime == nullptr || &sourceTime < 0) { // || > _MAX__TIME64_T
        tmDest->tm_sec = 0;
        tmDest->tm_min = 0;
        tmDest->tm_hour = 0;
        tmDest->tm_mday = 0;
        tmDest->tm_mon = 0;
        tmDest->tm_year = 0;
        tmDest->tm_wday = 0;
        tmDest->tm_yday = 0;
        tmDest->tm_isdst = 0;
        return EINVAL;
    }
    else {
        tmDest = std::localtime(sourceTime);
        return 0;
    }
#endif
}

RTMA_Logger::RTMA_Logger(const char* log_name, int log_level, RTMA_Module* rtma_client, const char* log_filename) :
    log_name_(log_name),
    level(log_level),
    log_filename_(""),
    rtma_client_(rtma_client)
{
    log_msg_ = new CMessage(MT_RTMA_LOG);
    log_msg_->AllocateData(sizeof(MDF_RTMA_LOG));
    log_msg_data_ = (MDF_RTMA_LOG*)log_msg_->GetDataPointer();
    strcpy_safe(log_msg_data_->name, sizeof(log_msg_data_->name), log_name_.c_str());
    set_log_filename(log_filename);
}

RTMA_Logger::~RTMA_Logger()
{
    delete log_msg_;
};

RTMA_Module* RTMA_Logger::get_rtma_client_pointer(void)
{
    return rtma_client_;
}

void RTMA_Logger::set_rtma_client(RTMA_Module* rtma_client)
{
    rtma_client_ = rtma_client;
}

std::string RTMA_Logger::get_log_name(void)
{
    return log_name_;
}

void RTMA_Logger::set_log_name(const char* log_name) {
    log_name_ = log_name;
}

std::string RTMA_Logger::get_log_filename(void)
{
    return log_filename_;
}

void RTMA_Logger::set_log_filename(const char* log_filename)
{
    log_filename_ = (std::string)log_filename; // set member var
}

void RTMA_Logger::debug(const char* message, const char* src_func, const char* src_file, int src_line)
{
    log(message, LogLevel::lDEBUG, src_func, src_file, src_line);
}

void RTMA_Logger::info(const char* message, const char* src_func, const char* src_file, int src_line)
{
    log(message, LogLevel::lINFO, src_func, src_file, src_line);
}

void RTMA_Logger::warning(const char* message, const char* src_func, const char* src_file, int src_line)
{
    log(message, LogLevel::lWARNING, src_func, src_file, src_line);
}

void RTMA_Logger::error(const char* message, const char* src_func, const char* src_file, int src_line)
{
    log(message, LogLevel::lERROR, src_func, src_file, src_line);
}

void RTMA_Logger::critical(const char* message, const char* src_func, const char* src_file, int src_line)
{
    log(message, LogLevel::lCRITICAL, src_func, src_file, src_line);
}

void RTMA_Logger::log(const char* message, int log_level, const char* src_func, const char* src_file, int src_line)
{
    if (log_level < level)
        return;

    // get time
    const auto time = std::chrono::system_clock::now();
    const auto time_dur = time.time_since_epoch();
    const auto time_ms = std::chrono::duration_cast<std::chrono::milliseconds>(time_dur);
    double time_s = double(time_ms.count()) / 1000.0;
    const time_t now_timet = std::chrono::system_clock::to_time_t(time);
    tm lt;
    localtime_safe(&lt, &now_timet);
    auto dateput = std::put_time(&lt, "%F %T");

    // log to console
#if (__cplusplus >= 201703L) || (defined(_HAS_CXX17) && _HAS_CXX17 > 0)
    const auto src_filename = std::filesystem::path(src_file).filename().string();
#else
    const auto src_filename = (std::string)src_file;
#endif
    std::string src_formatted = src_filename + ":" + std::to_string(src_line);
    std::string msg_formatted = levelToNameStr(log_level) + " [" + log_name_ + "] " + (std::string)message + "\t" + src_formatted;
    std::cout << dateput << " " << msg_formatted << std::endl;


    // log to rtma
    if (rtma_client_->IsConnected())
    {
        log_msg_->msg_type = levelToMT(level);
        log_msg_data_->time = time_s;
        log_msg_data_->level = log_level;
        log_msg_data_->lineno = src_line;
        strcpy_safe(log_msg_data_->pathname, sizeof(log_msg_data_->pathname), src_file);
        strcpy_safe(log_msg_data_->funcname, sizeof(log_msg_data_->funcname), src_func);
        strcpy_safe(log_msg_data_->message, sizeof(log_msg_data_->message), message);
        rtma_client_->SendMessageRTMA(log_msg_);
    }

    // log to file
    if (log_filename_.length() > 0)
    {
        std::ofstream log_file_stream(log_filename_, std::ios_base::out | std::ios_base::app);
        log_file_stream << dateput << " " << msg_formatted << std::endl;
        log_file_stream.close();
    }
}