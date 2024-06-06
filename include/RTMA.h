// RTMA - RealTime Messaging Architecture
//
// Copyright (c) 2006-2011 Meel Velliste, Sagi Perel, George W. Fraser, M. Chance Spalding, Samuel T. Clanton, Angus McMorland, Andrew S. Whitford, Michael Palazzolo, University of Pittsburgh


#ifndef _RTMA_H_
#define _RTMA_H_
/* ----------------------------------------------------------------------------
   |                              INCLUDES                                    |
   ----------------------------------------------------------------------------*/
#include "OS_defines.h"
#include "Timing.h"
#include "RTMA_types.h"
#include "internal/UPipe.h"

// Sized integer types (added with pyrtma v2.3 updates)
#include <stdint.h>

#include <stdio.h>
#include <string>

// If this is compiled as part of a Matlab MEX file, then this 
// hack helps redirect memory allocation requests to the Matlab
// memory manager. This is important in Matlab because otherwise
// it will have unpredictable behavior and unexplained crashes.
#include "internal/mex_hack.h"

//namespace RTMA {

#define DEFAULT_PIPE_SERVER_NAME_FOR_MODULES "localhost:7111" // Modules connect locally by default
#define DEFAULT_PIPE_SERVER_NAME_FOR_MM ":7111" // MessageManager accepts connections from any incoming interface by default


class RTMA_Logger; // defined in ClientLogger.h (avoid circular import here)

/* ----------------------------------------------------------------------------
   |                       CMessage class                                      |
   ----------------------------------------------------------------------------*/
class CMessage
{
public:

	MSG_TYPE	msg_type; // previously RTMA_MSG_HEADER_FIELDS; (changed for python compatibility)
	MSG_COUNT	msg_count;
	double	send_time;
	double	recv_time;
	HOST_ID		src_host_id;
	MODULE_ID	src_mod_id;
	HOST_ID		dest_host_id;
	MODULE_ID	dest_mod_id;
	int32_t		num_data_bytes;
	int32_t		remaining_bytes;
	int32_t		is_dynamic;
	int32_t		reserved;
	char data[MAX_CONTIGUOUS_MESSAGE_DATA];
	char *large_data;

	CMessage( );
	CMessage( MSG_TYPE mt);
	CMessage( MSG_TYPE mt, void *pData, size_t num_bytes);
	~CMessage( ) noexcept(false);

	void *
	GetDataPointer( void);

	int
	GetData( void *pData);

	int
	SetData( void *pData, size_t num_bytes);

	int
	AllocateData( size_t num_bytes);

	int
	Set( MSG_TYPE mt, void *pData = NULL, size_t num_bytes = 0);

	int
	Receive( UPipe *input_pipe);

	int
	Receive( UPipe *input_pipe, double timeout);

	int
	Send( UPipe *output_pipe);

	int
	Send( UPipe *output_pipe, double timeout);

	bool
	IsDynamic();

	RTMA_MSG_HEADER
	GetHeader( void);
};

/* ----------------------------------------------------------------------------
   |                       RTMA CODE                                           |
   ----------------------------------------------------------------------------*/
class RTMA_Module
{
private:

	UPipeClient *_pipeClient;
	UPipe		*_MMpipe;
	MODULE_ID   m_ModuleID;
	HOST_ID     m_HostID;
	double      m_StartTime;
	int         m_Pid;
	int         m_TimerCount;

	#if (RTMA_PROFILE == TRUE)
		int			     m_NumProfiledMsgs;
		RTMA_MSG_HEADER  m_ProfileData[MAX_PROFILED_MSGS];
	#endif

	int
	NBReadMessage( CMessage *M);
	//Non block read: returns -1 if there was no message in the pipe, or the number of bytes read

protected:
	char        m_Name[MAX_NAME_LEN];
	MSG_COUNT   m_MessageCount;
	MSG_COUNT   m_SelfMessageCount;
	int         m_Connected;
	UPipe       *_pMMPipe; //pipe handle for communicating with the Message Manager

	// logging
	RTMA_Logger *_logger;

	int
	WaitForAcknowledgement(double timeout = -1, CMessage* rcvMsg = NULL); // Waits for MT_ACKNOWLEDGE for up to timeout seconds

	int
	SendMessage( CMessage *M, UPipe *pOutputPipe, MODULE_ID dest_mod_id = 0, HOST_ID dest_host_id = 0);

	int
	SendSignal( MSG_TYPE MessageType, UPipe *pOutputPipe, MODULE_ID dest_mod_id = 0, HOST_ID dest_host_id = 0);
	// Send message that only has the header (no data after the header).

	int
	IncrementMessageCount();
	//increments m_MessageCount by 1, and returns the NEW value

	void
	ReportProfileData( void);
	//reports the profile data to a binary file if RTMA_PROFILE is defined in RTMA_profile.h
public:

	RTMA_Module( );

	//RTMA_Module( MODULE_ID ModuleID, HOST_ID HostID);

	RTMA_Module(MODULE_ID ModuleID, HOST_ID HostID, char* ClientName=(char*)"");

	~RTMA_Module( ) noexcept(false);

	void
	Cleanup( void);
	//contains code executed by the dtor
	
	void
	InitVariables( MODULE_ID ModuleID, HOST_ID HostID, char* name=(char*)"");

	int
	ConnectToMMM( int logger_status=0, int read_dd_file=0, int daemon_status=0);
	// Opens a read and a write connection to the Message Management Module on localhost:7111

	int
	ConnectToMMM( char *server_name, int logger_status=0, int read_dd_file=0, int daemon_status=0);
	// Opens a read and a write connection to the Message Management Module on the specified host and port
	// specified in server_name, e.g. "somehost.com:1234" or "192.168.2.10:8888"

	int
	ConnectToMMM_V2(int logger_status = 0, int allow_multiple = 0, int daemon_status = 0);
	
	int
	ConnectToMMM_V2( char* server_name, int logger_status = 0, int allow_multiple = 0, int daemon_status = 0);

	int
	DisconnectFromMMM( void);

	int
	IsConnected( void);

	int
	SendModuleReady( void);
	// Sends a message that announces that this module is ready

	int
	Subscribe( MSG_TYPE MessageType);
	// MessageType is a specific message ID to subscribe just to that type of message,
	// or ALL_MESSAGE_TYPES to get all message types (useful for debugging);

	int
	Unsubscribe( MSG_TYPE MessageType);
	// MessageType is a specific message ID to unsubscribe from only that message type
	// or ALL_MESSAGE_TYPES to unsubscribe from all message types

	int
	PauseSubscription( MSG_TYPE MessageType);
	// Tell MessageManager to stop sending messages of a specific MessageType,
	// or ALL_MESSAGE_TYPES temporarily, without removing the subscription

	int
	ResumeSubscription( MSG_TYPE MessageType);
	// Tell MessageManager to resume sending messages of a specific MessageType,
	// or ALL_MESSAGE_TYPES after having paused those message types using PauseSubscription

	int
	SendMessage( CMessage *M, MODULE_ID dest_mod_id = 0, HOST_ID dest_host_id = 0);
	// Send a message through the RTMA system. If destination module ID is 0, then the message is broadcast to all modules. If host is 0, then broadcast to all hosts.

	int
	SendMessageRTMA( CMessage *M, MODULE_ID dest_mod_id = 0, HOST_ID dest_host_id = 0);
	// A copy of SendMessage() for the purpose of compiling into a .NET library, because SendMessage() itself conflicts with the Win32 API SendMessage.

	int
	SendSignal( MSG_TYPE MessageType, MODULE_ID dest_mod_id = 0, HOST_ID dest_host_id = 0);
	// Send message that only has the header (no data after the header).
	
	int SendSelfSignal( MSG_TYPE MessageType);
	// Sends signal this this module itself by writing directly to module's input pipe


	int
	ReadMessage( CMessage *M, double timeout = -1);
	// Reads a message from the module input pipe. If timeout is negative, then blocks
	// until message available. If timeout is positive, then blocks up to timeout
	// seconds or till message available. If timeout is 0, then does not block, reads
	// message only if immediately available. Returns 1 if message was read, 0 if no
	// message available, and throws MyCException if there was an error.

	int
	WaitForSignal( MSG_TYPE SigType, int blocking = 1);
	//Waits for SigType message: if blocking- will not return until the requested sig type was received (and will discard all other sigs received)
	//If non blocking- will return 1 if the requested type was received, or 0 if another type was received

	void
	WaitForMessage( CMessage *M, MSG_TYPE MsgType = -1);
	//Waits for a message: 
	//if MsgType is specified- will not return until the requested msg type was received (and will discard all other messages received)
	//if MsgType is not specified- will return the first message received (in this case just a wrapper for ReadMessage) 

	double UpTime( void);

	int GetPid( void);

	int
	GetMessageCount(){ return m_MessageCount; }

	HOST_ID 
	GetHostID() { return m_HostID;}

	MODULE_ID 
	GetModuleID(){ return m_ModuleID;}

	char* GetName() { return m_Name; }

	// log functions
	RTMA_Logger* GetLoggerPointer(void);
	std::string GetLogName(void);
	void SetLogName(const char* log_name);
	int GetLogLevel(void);
	void SetLogLevel(int log_level);
	std::string GetLogFilename(void);
	void SetLogFilename(const char* log_filename);
	void Debug(const char* message, const char* src_func, const char* src_file, int src_line);
	void Info(const char* message, const char* src_func, const char* src_file, int src_line);
	void Warning(const char* message, const char* src_func, const char* src_file, int src_line);
	void Error(const char* message, const char* src_func, const char* src_file, int src_line);
	void Critical(const char* message, const char* src_func, const char* src_file, int src_line);
	// main log function (accepts any level integer)
	void Log(const char* message, int level, const char* src_func, const char* src_file, int src_line);
};

/* ----------------------------------------------------------------------------
   |                       GLOBAL FUNCTIONS                                   |
   ----------------------------------------------------------------------------*/

int
SetMyPriority(int priority_class);

int
GetMyPriority();

//} // namespace RTMA

#endif //_RTMA_H_
