// RTMALabView.cpp : Defines the entry point for the DLL application.
//


#include "stdafx.h"
#include "RTMALabView.h"
#include "rtma.h"


#ifdef _MANAGED
#pragma managed(push, off)
#endif

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
					 )
{
    return TRUE;
}

#ifdef _MANAGED
#pragma managed(pop)
#endif

static RTMA_Module rtma( 22222, 0);

// This is an example of an exported variable
//RTMALabView_API int nRTMALabView=0;

// This is an example of an exported function.
//RTMALabView_API int fnRTMALabView(void)
//{
//	return 42;
//}

// This is the constructor of a class that has been exported.
// see RTMALabView.h for the class definition
RTMALabView_API CRTMALabView::CRTMALabView()
{
	return;
}

RTMALabView_API int InitializeAndConnect(char *server_name, int ModuleID, int HostID, int logger_status, int read_dd_file, int daemon_status)
{
	try {
	   rtma.InitVariables( ModuleID, HostID );	
	   return rtma.ConnectToMMM( server_name, logger_status, read_dd_file, daemon_status );
	}
	catch(...) 
	{
		return -1;
	}
}

RTMALabView_API void SetModuleAndHost( int ModuleID, int HostID)
{
	rtma.InitVariables( ModuleID, HostID );
}

RTMALabView_API int	ConnectToMMM( int logger_status, int read_dd_file, int daemon_status)
{
	// Opens a read and a write connection to the Message Management Module on localhost:7111
	return rtma.ConnectToMMM( logger_status, read_dd_file, daemon_status );
}


RTMALabView_API	int	ConnectToMMM( char *server_name, int logger_status, int read_dd_file, int daemon_status)
{
	try {
	// Opens a read and a write connection to the Message Management Module on the specified host and port
	// specified in server_name, e.g. "somehost.com:1234" or "192.168.2.10:8888"
	return rtma.ConnectToMMM( DEFAULT_PIPE_SERVER_NAME_FOR_MODULES, logger_status, read_dd_file, daemon_status );
	}
	catch(...) 
	{
		return -1;
	}
}

RTMALabView_API	int	DisconnectFromMMM( void)
{
try{
	return rtma.DisconnectFromMMM();
	}
	catch(...)
	{
	return -1;
	}
}

RTMALabView_API	int	IsConnected( void)
{
	return rtma.IsConnected();
}

RTMALabView_API	int	SendModuleReady( void)
{
	// Sends a message that announces that this module is ready
	return rtma.SendModuleReady();
}

RTMALabView_API	int	Subscribe( int MessageType)
{
	// MessageType is a specific message ID to subscribe just to that type of message,
	// or ALL_MESSAGE_TYPES to get all message types (useful for debugging);
	return rtma.Subscribe( MessageType );
}

RTMALabView_API	int	Unsubscribe( int MessageType)
{
	// MessageType is a specific message ID to unsubscribe from only that message type
	// or ALL_MESSAGE_TYPES to unsubscribe from all message types
	return rtma.Unsubscribe( MessageType );
}

RTMALabView_API	int	PauseSubscription( int MessageType)
{
	// Tell MessageManager to stop sending messages of a specific MessageType,
	// or ALL_MESSAGE_TYPES temporarily, without removing the subscription
	return rtma.PauseSubscription( MessageType );
}

RTMALabView_API	int	ResumeSubscription( int MessageType)
{
	// Tell MessageManager to resume sending messages of a specific MessageType,
	// or ALL_MESSAGE_TYPES after having paused those message types using PauseSubscription
	return rtma.ResumeSubscription( MessageType );
}

//RTMALabView_API	int	SendMessage( CMessage *M, short dest_mod_id , short dest_short )
//{
//	// Send a message through the RTMA system. If destination module ID is 0, then the message is broadcast to all modules. If host is 0, then broadcast to all hosts.
//	return rtma.SendMessageRTMA( 
RTMALabView_API	int	SendMessageRTMA( int mt, void *pData, int num_bytes, short dest_mod_id , short dest_host_id )
{
	try{
	// A copy of SendMessage() for the purpose of compiling into a .NET library, because SendMessage() itself conflicts with the Win32 API SendMessage.
	return rtma.SendMessageRTMA( &CMessage( mt, pData, num_bytes), dest_mod_id, dest_host_id );
	}
	catch(...) 
	{
		return -1;
	}
}

RTMALabView_API	int	SendSignal( int MessageType, short dest_mod_id , short dest_host_id )
{
	try{
	// Send message that only has the header (no data after the header).
	return rtma.SendSignal( MessageType, dest_mod_id, dest_host_id );
	}
	catch(...) 
	{
		return -1;
	}
}

RTMALabView_API	int SendSelfSignal( int MessageType)
{
	// Sends signal this this module itself by writing directly to module's input pipe
	return rtma.SendSelfSignal( MessageType );
}

RTMALabView_API	int	ReadMessage(int *mt, void *pData, int num_bytes, double timeout )
{
	// Reads a message from the module input pipe. If timeout is negative, then blocks
	// until message available. If timeout is positive, then blocks up to timeout
	// seconds or till message available. If timeout is 0, then does not block, reads
	// message only if immediately available. Returns 1 if message was read, 0 if no
	// message available, and throws MyCException if there was an error
	try{
	CMessage msg;
	int rez = rtma.ReadMessage( &msg, timeout );
	if (rez){
		*mt = msg.msg_type;
		msg.GetData( pData );
	}
	return rez;
	}
	catch(...){
		return -1;
	}
}

RTMALabView_API int ReadMessageTester(int MessageType, int *pData, int num_bytes, double timeout_seconds)
{
	try{
	pData[0] = 55;
	return 1;
	}
	catch(...) 
	{
		return -1;
	}
}

RTMALabView_API	int	WaitForSignal( int SigType, int blocking )
{
	//Waits for SigType message: if blocking- will not return until the requested sig type was received (and will discard all other sigs received)
	//If non blocking- will return 1 if the requested type was received, or 0 if another type was received
	return rtma.WaitForSignal( SigType, blocking );
}

RTMALabView_API	void WaitForMessage( int mt, void *pData, int num_bytes, int MsgType )
{
	//Waits for a message: 
	//if MsgType is specified- will not return until the requested msg type was received (and will discard all other messages received)
	//if MsgType is not specified- will return the first message received (in this case just a wrapper for ReadMessage) 
	rtma.WaitForMessage( &CMessage( mt, pData, num_bytes), MsgType );
	
}

//RTMALabView_API	int	SetTimer(unsigned int time_ms);
//	//sets a local timer to expire within the time stated (in ms). Returns timer_id or -1 on failure
//
//RTMALabView_API	int	CancelTimer(int timer_id);
//
//RTMALabView_API	int	SelfNotifyExpiredTimer(int timer_id);
//	//sends MT_TIMER_EXPIRED to m_WrtInputPipe (self input pipe). Returns 0 on failure, 1 on success
//

