#include "RTMA.h"

#include "MyCException.h"

#include "Debug.h"

#include "ClientLogger.h"

//namespace RTMA {

//////////////////////////////////////////////////////////////////////////////
//////////////////// GLOBAL VARIABLES/////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

#ifdef _UNIX_C
	//the macro is defined in windows.h for Win systems, but may not exist on Unix
	#ifndef min
	#define min(a,b)            (((a) < (b)) ? (a) : (b))
	#endif
#endif


//////////////////////////////////////////////////////////////////////////////
//////////////////// CMessage ////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

CMessage::CMessage( )
{
	TRY {
		large_data = NULL;
		Set( -1, NULL, 0);
	} CATCH_and_THROW( "CMessage::CMessage( )");
}

CMessage::CMessage( MSG_TYPE mt)
{
	TRY {
		large_data = NULL;
		Set( mt, NULL, 0);
	} CATCH_and_THROW( "CMessage::CMessage( MSG_TYPE mt)");
}

CMessage::CMessage( MSG_TYPE mt, void *pData, size_t num_bytes)
{
	TRY {
		large_data = NULL;
		Set( mt, pData, num_bytes);
	} CATCH_and_THROW( "CMessage::CMessage( MSG_TYPE mt, void *pData, size_t num_bytes)");
}

CMessage::~CMessage( ) noexcept(false)
{
	TRY {
		if( large_data != NULL) {
			free( large_data);
			large_data = NULL;
		}
	} CATCH_and_THROW( "CMessage::~CMessage( )");
}

void *
CMessage::GetDataPointer( void)
{
	TRY {
		if( num_data_bytes > MAX_CONTIGUOUS_MESSAGE_DATA) return (void *) large_data;
		else return (void *) data;
	} CATCH_and_THROW( "CMessage::GetDataPointer( void)");
}

int
CMessage::GetData( void *pData)
{
	TRY {
		if( num_data_bytes > 0) {
			if( num_data_bytes > MAX_CONTIGUOUS_MESSAGE_DATA) {
				memcpy( pData, large_data, num_data_bytes);
			} else {
				memcpy( pData, &(data[0]), num_data_bytes);
			}
			return num_data_bytes;
		} else {
			return 0;
		}
	} CATCH_and_THROW( "CMessage::GetData( void *pData)");
}

int
CMessage::SetData( void *pData, size_t num_bytes)
{
	TRY {
		if( !AllocateData( num_bytes)) return 0;

		if( num_bytes > MAX_CONTIGUOUS_MESSAGE_DATA) {

			memcpy( large_data, pData, num_bytes);

		} else {

			if( num_bytes > 0) memcpy( data, pData, num_bytes);

		}
		return 1;
	} CATCH_and_THROW( "CMessage::SetData( void *pData, size_t num_bytes)");
}

int
CMessage::AllocateData( size_t num_bytes)
{
	TRY {
		if( large_data != NULL) {
			free( large_data);
			large_data = NULL;
		}

		if( num_bytes > MAX_CONTIGUOUS_MESSAGE_DATA) {

			large_data = (char*) malloc( num_bytes);
			if( large_data == NULL) return 0;

		}
		num_data_bytes = (int) num_bytes;
		return 1;
	} CATCH_and_THROW( "CMessage::AllocateData( size_t num_bytes)");
}

int
CMessage::Set( MSG_TYPE mt, void *pData, size_t num_bytes)
{
	TRY {
		msg_type = mt;

		//all the fields below will be filled when sending the message
		msg_count = 0;
		send_time = 0;
		recv_time = 0.0;
		src_host_id = 0;
		src_mod_id = 0;
		dest_host_id = 0;
		dest_mod_id = 0;
		num_data_bytes = 0;
		remaining_bytes = -1;
		is_dynamic = 0;
		reserved = 0;

		return SetData( pData, num_bytes);
	} CATCH_and_THROW( "CMessage::Set( MSG_TYPE mt, void *pData, size_t num_bytes)");
}

int
CMessage::Receive( UPipe *input_pipe)
// Receive a message from the pipe.
{
	TRY {
		return Receive( input_pipe, -1);
	} CATCH_and_THROW( "CMessage::Receive( UPipe *input_pipe)");
}

int
CMessage::Receive( UPipe *input_pipe, double timeout)
// Receive a message from the pipe. Time out after timeout seconds.
// If timeout is -1, then wait forever.
{
	TRY {
		if( input_pipe == NULL) return -4;

		int total_bytes_read;
		int nbytes_to_read = sizeof( RTMA_MSG_HEADER);
		int nbytes_read = input_pipe->Read( this, nbytes_to_read, timeout);
		if( nbytes_read == 0) {
			if( timeout == -1) return -1;
			else return 0;
		}
		if( nbytes_read < nbytes_to_read) return -2;
		total_bytes_read = nbytes_read;
		if( num_data_bytes > 0) {
			void *pData = (void*) &data[0];
			if( num_data_bytes > MAX_CONTIGUOUS_MESSAGE_DATA) {
				AllocateData( num_data_bytes);
				pData = large_data;
			}
			input_pipe->Read( pData, num_data_bytes);
			total_bytes_read += num_data_bytes;
		}
		return total_bytes_read;
	} CATCH_and_THROW( "CMessage::Receive( UPipe *input_pipe, double timeout)");
}

int
CMessage::Send( UPipe *output_pipe)
{
	TRY {
		return Send( output_pipe, -1);
	} CATCH_and_THROW( "CMessage::Send( UPipe *output_pipe)");
}

int
CMessage::Send( UPipe *output_pipe, double timeout)
{
	TRY {
		if( output_pipe == NULL) return 0;

		// If message data is contiguous, then send in a single write call
		// else send header and data separately
		int nbytes_to_send;
		int nbytes_written = 0;
		int success = 1;
		if( num_data_bytes <= MAX_CONTIGUOUS_MESSAGE_DATA) {

			// Send header and data
			nbytes_to_send = sizeof( RTMA_MSG_HEADER) + num_data_bytes;
			nbytes_written = output_pipe->Write( this, nbytes_to_send, timeout);
			if( nbytes_written < nbytes_to_send) success = 0;

		} else {

			// Send header
			nbytes_to_send = sizeof( RTMA_MSG_HEADER);
			nbytes_written = output_pipe->Write( this, nbytes_to_send, timeout);
			if( nbytes_written < nbytes_to_send) success = 0;

			// Send data
			if( success) {
			        nbytes_to_send = num_data_bytes;
			        nbytes_written += output_pipe->Write( large_data, nbytes_to_send, timeout);
				if( nbytes_written < nbytes_to_send) success = 0;
			}
		}

		return success;
	} CATCH_and_THROW( "CMessage::Send( UPipe *output_pipe, double timeout)");
}

bool
CMessage::IsDynamic()
{
	TRY {
		if (is_dynamic) return true;
		return false;
	} CATCH_and_THROW( "CMessage::IsDynamic()");
}

RTMA_MSG_HEADER
CMessage::GetHeader(void)
{
	TRY {
		RTMA_MSG_HEADER header;
		memset( &header, 0, sizeof( header));

		header.dest_host_id = dest_host_id;
		header.dest_mod_id  = dest_mod_id;
		header.msg_count    = msg_count;
		header.msg_type     = msg_type;
		header.num_data_bytes  = num_data_bytes;
		header.recv_time       = recv_time;
		header.remaining_bytes = remaining_bytes;
		header.send_time       = send_time;
		header.src_host_id     = src_host_id;
		header.src_mod_id      = src_mod_id;
		header.is_dynamic      = is_dynamic;
		
		return header;
	} CATCH_and_THROW( "CMessage::GetHeader(void)");
}


//////////////////////////////////////////////////////////////////////////////
//////////////////// RTMA_Module /////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

RTMA_Module::RTMA_Module( )
{
	TRY {
		InitVariables( -1, -1);
	} CATCH_and_THROW( "RTMA_Module::RTMA_Module( )");
}

RTMA_Module::RTMA_Module( MODULE_ID ModuleID, HOST_ID HostID)
{
	TRY {
		InitVariables( ModuleID, HostID);
	} CATCH_and_THROW( "RTMA_Module::RTMA_Module( MODULE_ID ModuleID, HOST_ID HostID)");
}

void RTMA_Module::InitVariables( MODULE_ID ModuleID, HOST_ID HostID)
{
	TRY {
		_pipeClient = NULL;
		_MMpipe = NULL;
		char log_name[50];
		sprintf(log_name, "Module % d", ModuleID);
		_logger = new RTMA_Logger(log_name, LogLevel::lINFO);
		_logger->set_rtma_client(this);
		m_ModuleID = ModuleID;
		m_HostID = HostID;
		m_MessageCount = 0;
		m_SelfMessageCount = 0;
		m_StartTime = GetAbsTime();
		m_Connected = 0;
		#ifdef _UNIX_C
			m_Pid = getpid();
		#else
			m_Pid = _getpid();
		#endif
		//m_TimerCount=1;
		//Gm_TimerThreadInfo.thread_exists = 0;

		InitializeAbsTime();

	} CATCH_and_THROW( "void RTMA_Module::InitVariables( MODULE_ID ModuleID, HOST_ID HostID)");
}

RTMA_Module::~RTMA_Module( ) noexcept(false)
{
	TRY {
		Cleanup();
	} CATCH_and_THROW( "RTMA_Module::~RTMA_Module( )");
}

void
RTMA_Module::Cleanup( void)
{
	TRY {
	 // if(Gm_TimerThreadInfo.thread_exists == 1) // m_TimerCount > 1)
		//{
		//#ifdef _UNIX_C
		//  Gm_TimerThreadInfo.keep_running = 0;
		//  pthread_join(Gm_TimerThreadInfo.thread_handle, NULL);
		//  pthread_mutex_destroy(&Gm_TimerThreadInfo.tMutex);
		//#else
		//  TerminateThread(Gm_TimerThreadInfo.thread_handle, 0);
		//  CloseHandle(Gm_TimerThreadInfo.thread_handle);
		//  //The system closes the mutex handle automatically when the process terminates
		//#endif
		//  Gm_TimerThreadInfo.thread_exists = 0;
		//}
		
		if( m_Connected) {
			DisconnectFromMMM( );
		}
		delete _logger;
	} CATCH_and_THROW( "RTMA_Module::Cleanup( void)");
}

int
RTMA_Module::ConnectToMMM( int logger_status, int read_dd_file, int daemon_status)
// Opens a read and a write connection to the Message Management Module
{
	TRY {
		return ConnectToMMM( DEFAULT_PIPE_SERVER_NAME_FOR_MODULES, logger_status, read_dd_file, daemon_status );
	} CATCH_and_THROW( "RTMA_Module::ConnectToMMM( int logger_status, int read_dd_file, int daemon_status)");
}

int
RTMA_Module::ConnectToMMM( char *server_name, int logger_status, int read_dd_file, int daemon_status)
// Opens a read and a write connection to the Message Management Module
{
	TRY {
		// Connect to server
		_pipeClient = UPipeFactory::CreateClient( server_name);
		_MMpipe = _pipeClient->Connect();

		MDF_CONNECT data;
		
		if(logger_status) {
			data.logger_status = 1;
		} else {
			data.logger_status = 0;
		}

		if(daemon_status) {
			data.daemon_status = 1;
		} else {
			data.daemon_status = 0;
		}

		m_MessageCount = 1;
		m_SelfMessageCount = 1;
		CMessage M(MT_CONNECT, (void*) &data, sizeof(MDF_CONNECT) );
		SendMessage( &M);
		
		CMessage ackMsg;
		int status = WaitForAcknowledgement( 1, &ackMsg); // Wait for up to 3 seconds
		if( status == 0){
		    throw MyCException( "Did not receive ACK from MessageManager upon CONNECT");
		}

		// save own module ID from ACK if asked to be assigned dynamic ID
		if (m_ModuleID == 0)
			m_ModuleID = ackMsg.dest_mod_id;

		m_Connected = 1;

		return status;

	} CATCH_and_THROW( "RTMA_Module::ConnectToMMM( char *server_name, int logger_status, int read_dd_file, int daemon_status)");
}

int
RTMA_Module::DisconnectFromMMM( void)
{
	TRY {
		//int status;
		DEBUG_TEXT_("DisconnectFromMMM():");
		if(m_Connected)
		{
			try {
				// Try to disconnect cleanly at RTMA level
				SendSignal( MT_DISCONNECT);//this could go to a dead pipe- but it won't be blocking
			} catch(...) {
				// If clean disconnect fails then we must be already disconnected
			}
		}

		if( _pipeClient != NULL) {
			try {
				// Try to disconnect cleanly at Pipe level
				_pipeClient->Disconnect();
				delete _pipeClient;
			} catch(...) {
				// If clean disconnect fails then we must be already disconnected
			}
		}
		m_MessageCount = 0;
		m_SelfMessageCount = 0;
		m_Connected = 0;
		_pipeClient = NULL;
		return 1;
	} CATCH_and_THROW( "RTMA_Module::DisconnectFromMMM( void)");
}

int
RTMA_Module::IsConnected( void)
{
	TRY {
		if( !m_Connected) {
			// If we think we are disconnected, then we can be pretty sure of it
			return 0;
		} else {
			// If we think we are connected, then double check by trying to read pipe
			char dummy_buffer;
			try {
				_MMpipe->Read( &dummy_buffer, 0, 0);
				return 1;
			} catch( UPipeException) {
				return 0;
			//} catch (UPipeClosedException) {
			//    return 0;
			}
		}
	} CATCH_and_THROW( "RTMA_Module::IsConnected( void)");
}

int
RTMA_Module::SendModuleReady( void)
{
	TRY {
		MDF_MODULE_READY data;
		data.pid = GetPid();
		CMessage M(MT_MODULE_READY, (void*) &data, sizeof(data));//send pid
		int status = SendMessage( &M);
		return status;
	} CATCH_and_THROW( "RTMA_Module::SendModuleReady( void)");
}

int
RTMA_Module::Subscribe( MSG_TYPE MessageType)
// MessageType is a specific message ID to subscribe just to that type of message,
// or ALL_MESSAGE_TYPES to get all message types (useful for debugging);
{
	TRY {
		DEBUG_TEXT( "Subscribing to message type " << MessageType);
		CMessage M( MT_SUBSCRIBE, &MessageType, sizeof( MessageType));
		SendMessage( &M);
		//		int status = WaitForAcknowledgement();
		return(1);
	} CATCH_and_THROW( "RTMA_Module::Subscribe( MSG_TYPE MessageType)");
}


int
RTMA_Module::Unsubscribe( MSG_TYPE MessageType)
// MessageType is a specific message ID to unsubscribe from only that message type
// or ALL_MESSAGE_TYPES to unsubscribe from all message types
{
	TRY {
		CMessage M( MT_UNSUBSCRIBE, &MessageType, sizeof( MessageType));
		SendMessage( &M);
		//		int status = WaitForAcknowledgement();
		return(1);
	} CATCH_and_THROW( "RTMA_Module::Unsubscribe( MSG_TYPE MessageType)");
}

int
RTMA_Module::PauseSubscription( MSG_TYPE MessageType)
// Tell MessageManager to stop sending messages of a specific MessageType,
// or ALL_MESSAGE_TYPES temporarily, without removing the subscription
{
	TRY {
		CMessage M( MT_PAUSE_SUBSCRIPTION, &MessageType, sizeof( MessageType));
		SendMessage( &M);
		//		int status = WaitForAcknowledgement();
		return(1);
	} CATCH_and_THROW( "RTMA_Module::PauseSubscription( MSG_TYPE MessageType)");
}

int
RTMA_Module::ResumeSubscription( MSG_TYPE MessageType)
// Tell MessageManager to resume sending messages of a specific MessageType,
// or ALL_MESSAGE_TYPES after having paused those message types using PauseSubscription
{
	TRY {
		CMessage M( MT_RESUME_SUBSCRIPTION, &MessageType, sizeof( MessageType));
		SendMessage( &M);
		//		int status = WaitForAcknowledgement();
		return(1);
	} CATCH_and_THROW( "RTMA_Module::ResumeSubscription( MSG_TYPE MessageType)");
}

int
RTMA_Module::WaitForAcknowledgement( double timeout, CMessage* rcvMsg)
{
	TRY 
	{
		int ret = 0;

		CMessage M;
		DEBUG_TEXT_( "Waiting for ACK... ");
		if( timeout == -1) 
		{	// Wait forever
			do { 
				ReadMessage( &M); 
			} while( M.msg_type != MT_ACKNOWLEDGE);
			
			DEBUG_TEXT( "Got ACK!");
			ret = 1; //return 1;
		} 
		else 
		{   // Wait up to timeout seconds
			double time_remaining = timeout;
			double beginning_time = GetAbsTime();
			while( time_remaining > 0) {
				int status = ReadMessage( &M, time_remaining);
				if( status == 0) break;
				if( status < 0) throw MyCException( "Error while waiting for MT_ACKNOWLEDGE");
				if( M.msg_type == MT_ACKNOWLEDGE) {
					DEBUG_TEXT( "Got ACK!");
					ret = 1;//return 1;
					break;
				}
				double time_now = GetAbsTime();
				double time_waited = time_now - beginning_time;
				time_remaining = timeout - time_waited;
			}

			if (time_remaining <= 0)
				DEBUG_TEXT( "timed out!");
		}

		if ((ret == 1) && rcvMsg) {
			rcvMsg->msg_count   = M.msg_count;
			rcvMsg->send_time   = M.send_time;
			rcvMsg->recv_time   = M.recv_time;
			rcvMsg->src_host_id = M.src_host_id;
			rcvMsg->src_mod_id  = M.src_mod_id;
			rcvMsg->dest_mod_id = M.dest_mod_id;
		}

		return ret;
	} 
	CATCH_and_THROW( "RTMA_Module::WaitForAcknowledgement( double timeout)");
}

int
RTMA_Module::SendMessage( CMessage *M, UPipe *output_pipe, MODULE_ID dest_mod_id, HOST_ID dest_host_id)
{
	TRY {
		if( output_pipe == NULL) return 0;

		// Verify that the module & host ids are valid
		if(dest_mod_id < 0 || dest_mod_id > MAX_MODULES)
		{
			MyCString err("RTMA_Module::SendMessage: Got invalid dest_mod_id [");
			err += MyCString(dest_mod_id) + "]";
			MyCException E(err);
			throw E;
		}

		if(dest_host_id < 0 || dest_host_id > MAX_HOSTS)
		{
			MyCString err("RTMA_Module::SendMessage: Got invalid dest_host_id [");
			err += MyCString(dest_host_id) + "]";
			MyCException E(err);
			throw E;
		}

		// Assume that msg_type, num_data_bytes, data - have been filled in
		M->msg_count   = m_MessageCount;
		M->send_time   = GetAbsTime();
		M->recv_time   = 0.0;
		M->src_host_id = m_HostID;
		M->src_mod_id  = m_ModuleID;
		M->dest_host_id = dest_host_id;
		M->dest_mod_id = dest_mod_id;	

		int status = M->Send( output_pipe);

		m_MessageCount++;

		return status;
	} CATCH_and_THROW( "RTMA_Module::SendMessage( CMessage *M, UPipe *output_pipe, MODULE_ID dest_mod_id, HOST_ID dest_host_id)");
}

int
RTMA_Module::SendMessage( CMessage *M, MODULE_ID dest_mod_id, HOST_ID dest_host_id)
{
	TRY {
		return SendMessage( M, _MMpipe, dest_mod_id, dest_host_id);
	} CATCH_and_THROW( "RTMA_Module::SendMessage( CMessage *M, MODULE_ID dest_mod_id, HOST_ID dest_host_id)");
}
int
RTMA_Module::SendMessageRTMA( CMessage *M, MODULE_ID dest_mod_id, HOST_ID dest_host_id)
{
	TRY {
		return SendMessage( M, _MMpipe, dest_mod_id, dest_host_id);
	} CATCH_and_THROW( "RTMA_Module::SendMessageRTMA( CMessage *M, MODULE_ID dest_mod_id, HOST_ID dest_host_id)");
}

int
RTMA_Module::SendSignal( MSG_TYPE MessageType, UPipe *output_pipe, MODULE_ID dest_mod_id, HOST_ID dest_host_id)
// Send message that only has the header (no data after the header).
{
	TRY {
		CMessage M( MessageType);
		return SendMessage( &M, output_pipe, dest_mod_id, dest_host_id);
	} CATCH_and_THROW( "RTMA_Module::SendSignal( MSG_TYPE MessageType, UPipe *output_pipe, MODULE_ID dest_mod_id, HOST_ID dest_host_id)");
}

int
RTMA_Module::SendSignal( MSG_TYPE MessageType, MODULE_ID dest_mod_id, HOST_ID dest_host_id)
// Send message that only has the header (no data after the header).
{
	TRY {
		CMessage M( MessageType);	
		return SendMessage( &M, dest_mod_id, dest_host_id);
	} CATCH_and_THROW( "RTMA_Module::SendSignal( MSG_TYPE MessageType, MODULE_ID dest_mod_id, HOST_ID dest_host_id)");
}

int
RTMA_Module::SendSelfSignal( MSG_TYPE sig)
// Sends signal this this module itself
{
	TRY {
		return SendSignal( sig, m_ModuleID, m_HostID);
	} CATCH_and_THROW( "RTMA_Module::SendSelfSignal( MSG_TYPE sig)");
}


int
RTMA_Module::NBReadMessage( CMessage *M)
{
	TRY {
		return ReadMessage( M, 0);
	} CATCH_and_THROW( "RTMA_Module::NBReadMessage( CMessage *M)");
}

int
RTMA_Module::ReadMessage( CMessage *M, double timeout)
{
	TRY {
		int status;

		status = M->Receive( _MMpipe, timeout);
		if(status < 0) throw MyCException( "Failed to read message");
		
		M->recv_time = GetAbsTime();

		if(status==0) return 0;
		else return 1;
	} CATCH_and_THROW( "RTMA_Module::ReadMessage( CMessage *M, double timeout)");
}

int
RTMA_Module::WaitForSignal( MSG_TYPE SigType, int blocking)
//Waits for SigType message: if blocking- will not return until the requested sig type was received. 
//If non blocking- will return 1 if the requested type was received, or 0 if another type was received
{
	TRY {
		CMessage M;

		while(1)
		{
			ReadMessage( &M);
			
			if(blocking)
			{
				if( M.msg_type == SigType) return 1;
			}else{//non blocking
				return ( M.msg_type == SigType)? 1 : 0;
			}		
		}
	} CATCH_and_THROW( "RTMA_Module::WaitForSignal( MSG_TYPE SigType, int blocking)");
}


void
RTMA_Module::WaitForMessage( CMessage *M, MSG_TYPE MsgType)
//Waits for a message: 
//if MsgType is specified- will not return until the requested msg type was received.
//if MsgType is not specified- will return the first message received (in this case just a wrapper for ReadMessage) 
{
	TRY {
		while(1)
		{
			ReadMessage( M);
			
			if(MsgType!= -1)
			{
				if( M->msg_type == MsgType) return;
			}else{//non blocking
				return;
			}		
		}
	} CATCH_and_THROW( "RTMA_Module::WaitForMessage( CMessage *M, MSG_TYPE MsgType)");
}

int
RTMA_Module::IncrementMessageCount()
//increments m_MessageCount by 1, and returns the NEW value
{
	TRY {
		m_MessageCount++;
		return m_MessageCount;
	} CATCH_and_THROW( "RTMA_Module::IncrementMessageCount()");
}


double
RTMA_Module::UpTime( void)
{
	TRY {
		return GetAbsTime() - m_StartTime;
	} CATCH_and_THROW( "RTMA_Module::UpTime( void)");
}

int 
RTMA_Module::GetPid( void)
{
	TRY {
		return m_Pid;
	} CATCH_and_THROW( "RTMA_Module::GetPid( void)");
}

RTMA_Logger* RTMA_Module::GetLoggerPointer( void)
{
	TRY{
		return _logger;
	} CATCH_and_THROW("RTMA_Module::GetLoggerPointer( void)");
}

std::string RTMA_Module::GetLogName(void)
{
	TRY{
		return _logger->get_log_name();
	} CATCH_and_THROW("RTMA_Module::GetLogName( void)");
}

void RTMA_Module::SetLogName(const char* log_name)
{
	TRY{
		_logger->set_log_name(log_name);
	} CATCH_and_THROW("RTMA_Module::SetLogName(const char* log_name)");
}

int RTMA_Module::GetLogLevel(void)
{
	TRY{
		return _logger->level;
	} CATCH_and_THROW("RTMA_Module::GetLogLevel(void)");
}

void RTMA_Module::SetLogLevel(int log_level)
{
	TRY{
		_logger->level = log_level;
	} CATCH_and_THROW("RTMA_Module::SetLogLevel(int log_level)");
}

std::string RTMA_Module::GetLogFilename(void)
{
	TRY{
		return _logger->get_log_filename();
	} CATCH_and_THROW("RTMA_Module::GetLogFilename(void)");
}

void RTMA_Module::SetLogFilename(const char* log_filename)
{
	TRY{
		_logger->set_log_filename(log_filename);
	} CATCH_and_THROW("RTMA_Module::SetLogFilename(const char* log_filename)");
}

void RTMA_Module::Debug(const char* message, const char* src_func, const char* src_file, int src_line)
{
	TRY{
		_logger->debug(message, src_func, src_file, src_line);
	} CATCH_and_THROW("RTMA_Module::Debug(const char* message, const char* src_func, const char* src_file, int src_line)");
}

void RTMA_Module::Info(const char* message, const char* src_func, const char* src_file, int src_line)
{
	TRY{
		_logger->info(message, src_func, src_file, src_line);
	} CATCH_and_THROW("RTMA_Module::Info(const char* message, const char* src_func, const char* src_file, int src_line)");
}

void RTMA_Module::Warning(const char* message, const char* src_func, const char* src_file, int src_line)
{
	TRY{
		_logger->warning(message, src_func, src_file, src_line);
	} CATCH_and_THROW("RTMA_Module::Warning(const char* message, const char* src_func, const char* src_file, int src_line)");
}

void RTMA_Module::Error(const char* message, const char* src_func, const char* src_file, int src_line)
{
	TRY{
		_logger->error(message, src_func, src_file, src_line);
	} CATCH_and_THROW("RTMA_Module::Error(const char* message, const char* src_func, const char* src_file, int src_line)");
}

void RTMA_Module::Critical(const char* message, const char* src_func, const char* src_file, int src_line)
{
	TRY{
		_logger->critical(message, src_func, src_file, src_line);
	} CATCH_and_THROW("RTMA_Module::Critical(const char* message, const char* src_func, const char* src_file, int src_line)");
}

void RTMA_Module::Log(const char* message, int level, const char* src_func, const char* src_file, int src_line)
{
	TRY{
		_logger->log(message, level, src_func, src_file, src_line);
	} CATCH_and_THROW("RTMA_Module::Log(const char* message, int level, const char* src_func, const char* src_file, int src_line)");
}

/*
 * Opens a handle to this process (specified by m_Pid), and sets the priority class accordingly
 * (Does not set priority for all threads - just for the main thread)
 * 
 * Returns 1 on success, 0 on failure
 */
int
SetMyPriority(int priority_class)
{
	/*
	TRY {
#ifdef _UNIX_C
		//sched_setscheduler
		return 1;
#else
		HANDLE hProcess = GetCurrentProcess();//not need to close this pseudo handle
		if(hProcess == NULL)
			return 0;

		if( SetPriorityClass(hProcess, priority_class) == 0)
		{
			return 0;
		}else{
			return 1;
		}
#endif
	} CATCH_and_THROW( "SetMyPriority(int priority_class)");
	*/
	return 1;
}


int
GetMyPriority()
//returns the priority class, or 0 on failure
{
	TRY {
#ifdef _UNIX_C
		return 1;
#else
		HANDLE hProcess = GetCurrentProcess();//not need to close this pseudo handle
		if(hProcess == NULL)
			return 0;
		
		int priority_class = GetPriorityClass(hProcess);
		if( priority_class == 0)
		{
			return 0;
		}else{
			return priority_class;
		}
#endif
	} CATCH_and_THROW( "GetMyPriority()");
}

//} // namespace RTMA

