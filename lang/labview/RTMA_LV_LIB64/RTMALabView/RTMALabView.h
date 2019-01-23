// The following ifdef block is the standard way of creating macros which make exporting 
// from a DLL simpler. All files within this DLL are compiled with the RTMALabView_EXPORTS
// symbol defined on the command line. This symbol should not be defined on any project
// that uses this DLL. This way any other project whose source files include this file see 
// RTMALabView_API functions as being imported from a DLL, whereas this DLL sees symbols
// defined with this macro as being exported.
#ifdef RTMALabView_EXPORTS
#define RTMALabView_API __declspec(dllexport)
#else
#define RTMALabView_API __declspec(dllimport)
#endif

// This class is exported from the RTMALabView.dll
class RTMALabView_API CRTMALabView {
public:
	CRTMALabView(void);
	// TODO: add your methods here.
};


//extern RTMALabView_API int nRTMALabView;

RTMALabView_API int fnRTMALabView(void);

RTMALabView_API int InitializeAndConnect( int ModuleID, int HostID, int logger_status=0, int read_dd_file=0, int daemon_status=0);

RTMALabView_API void SetModuleAndHost( int ModuleID, int HostID);

RTMALabView_API int	ConnectToMMM( int logger_status=0, int read_dd_file=0, int daemon_status=0);
	// Opens a read and a write connection to the Message Management Module on localhost:7111

RTMALabView_API	int	ConnectToMMM( char *server_name, int logger_status=0, int read_dd_file=0, int daemon_status=0);
	// Opens a read and a write connection to the Message Management Module on the specified host and port
	// specified in server_name, e.g. "somehost.com:1234" or "192.168.2.10:8888"

RTMALabView_API	int	DisconnectFromMMM( void);

RTMALabView_API	int	IsConnected( void);

RTMALabView_API	int	SendModuleReady( void);
	// Sends a message that announces that this module is ready

RTMALabView_API	int	Subscribe( int MessageType);
	// MessageType is a specific message ID to subscribe just to that type of message,
	// or ALL_MESSAGE_TYPES to get all message types (useful for debugging);

RTMALabView_API	int	Unsubscribe( int MessageType);
	// MessageType is a specific message ID to unsubscribe from only that message type
	// or ALL_MESSAGE_TYPES to unsubscribe from all message types

RTMALabView_API	int	PauseSubscription( int MessageType);
	// Tell MessageManager to stop sending messages of a specific MessageType,
	// or ALL_MESSAGE_TYPES temporarily, without removing the subscription

RTMALabView_API	int	ResumeSubscription( int MessageType);
	// Tell MessageManager to resume sending messages of a specific MessageType,
	// or ALL_MESSAGE_TYPES after having paused those message types using PauseSubscription

//RTMALabView_API	int	SendMessage( CMessage *M, short dest_mod_id = 0, short dest_short = 0);
//	// Send a message through the RTMA system. If destination module ID is 0, then the message is broadcast to all modules. If host is 0, then broadcast to all hosts.

RTMALabView_API	int	SendMessageRTMA( int mt, void *pData, int num_bytes, short dest_mod_id = 0, short dest_host_id = 0);
	// A copy of SendMessage() for the purpose of compiling into a .NET library, because SendMessage() itself conflicts with the Win32 API SendMessage.


RTMALabView_API	int	SendSignal( int MessageType, short dest_mod_id = 0, short dest_host_id = 0);
	// Send message that only has the header (no data after the header).
	
RTMALabView_API	int SendSelfSignal( int MessageType);
	// Sends signal this this module itself by writing directly to module's input pipe

RTMALabView_API	int	ReadMessage( int mt, void *pData, int num_bytes, double timeout = -1);
	// Reads a message from the module input pipe. If timeout is negative, then blocks
	// until message available. If timeout is positive, then blocks up to timeout
	// seconds or till message available. If timeout is 0, then does not block, reads
	// message only if immediately available. Returns 1 if message was read, 0 if no
	// message available, and throws MyCException if there was an error.

RTMALabView_API int ReadMessageTester(int MessageType, int *pData, int num_bytes, double timeout_seconds);

RTMALabView_API	int	WaitForSignal( int SigType, int blocking = 1);
	//Waits for SigType message: if blocking- will not return until the requested sig type was received (and will discard all other sigs received)
	//If non blocking- will return 1 if the requested type was received, or 0 if another type was received

RTMALabView_API	void WaitForMessage( int mt, void *pData, int num_bytes, int MsgType = -1);
	//Waits for a message: 
	//if MsgType is specified- will not return until the requested msg type was received (and will discard all other messages received)
	//if MsgType is not specified- will return the first message received (in this case just a wrapper for ReadMessage) 

//RTMALabView_API	int	SetTimer(unsigned int time_ms);
//	//sets a local timer to expire within the time stated (in ms). Returns timer_id or -1 on failure
//
//RTMALabView_API	int	CancelTimer(int timer_id);
//
//RTMALabView_API	int	SelfNotifyExpiredTimer(int timer_id);
//	//sends MT_TIMER_EXPIRED to m_WrtInputPipe (self input pipe). Returns 0 on failure, 1 on success