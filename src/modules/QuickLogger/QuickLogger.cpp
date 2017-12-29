/*
 *  QuickLogger - Logs RTMA messages in an attempt to save data or for debugging
 *  Meel Velliste 10/28/2008
 *  
 */
#include "QuickLogger.h"
#include <ctime>

CQuickLogger QL;

int main( void)
{
	try
	{
		//std::cout << "[main] QuickLogger started..." << std::endl;

		// Run the module
		QL.MainFunction();
	}
	catch(MyCException &E)
	{
		MyCString err("QuickLogger: main():");
		E.AppendTraceToString( err);
		std::cout << err;
		return -1;
	}
	return 0;
}

CQuickLogger::CQuickLogger()
{
	TRY {
		// Pre-allocate buffer space for storing messages
		_MessageBufrr.PreallocateBuffer( QL_NUM_PREALLOC_MESSAGES, sizeof( RTMA_MSG_HEADER), QL_NUM_PREALLOC_DATABYTES);
		_logging = true; // By default, start logging immediately
	} CATCH_and_THROW( "CQuickLogger::CQuickLogger()");
}

CQuickLogger::~CQuickLogger()
{
	TRY {
	} CATCH_and_THROW( "CQuickLogger::~CQuickLogger()");
}

void CQuickLogger::MainFunction()
{
	TRY {
		CMessage M;
		MDF_SAVE_MESSAGE_LOG FilenameData;
		char Filename[MAX_LOGGER_FILENAME_LENGTH+1];

		// Get connected
		int logger_status = 1;
		InitVariables( MID_QUICKLOGGER, 0);
		ConnectToMMM( logger_status);
		Subscribe( ALL_MESSAGE_TYPES);
		if( SetMyPriority(NORMAL_PRIORITY_CLASS) == 0) throw MyCException( "SetMyPriority failed");
		SendSignal( MT_LM_READY);
		SendModuleReady(); //just so we have the PID

		// Do logging
		try
		{
			// Display the size of pre-allocated buffers
			Status( (MyCString) "Pre-allocated space for " + _MessageBufrr.GetNumPreallocMessages() + " messages");
			Status( (MyCString) "Pre-allocated space for " + _MessageBufrr.GetNumPreallocDataBytes() + " data bytes");

			_logging = true; // Start logging immediately by default
			while( 1) {
				ReadMessage( &M);
				//Status( (MyCString) "Received Message (msg_type = " + M.msg_type + ")");
				bool saved = _MessageBufrr.SaveMessage( &M);
				if( !saved) {
					//Status( "Message buffer was full, saving log to QuickLoggerDump.bin");
					//_MessageBufrr.SaveDatafile( "QuickLoggerDump.bin");
					// TODO: revert to the version that saves dump files, but update executive to pause logging during intertrial. Dump files should only save if buffer unexpectedly fills during trial.
					//Status( (MyCString) "\nMessage buffer full, dumping to file");
					//AutoDumpBuffer(); // Commented out to stop saving dump files between trials. There is a risk that data could be lost if buffer overflows during a trial.
					Status( (MyCString) "\nMessage buffer full, resetting buffer. Data may be lost if not in intertrial!");
					_MessageBufrr.ClearBuffer( );
					//Status( "Log saved, message buffer has been reset");
					Status( "Message buffer has been reset");
					// Save the message again to the now cleared buffer
					_MessageBufrr.SaveMessage( &M);
				}
				switch( M.msg_type) {
					case MT_SAVE_MESSAGE_LOG:
						M.GetData( &FilenameData);
						FilenameData.pathname[FilenameData.pathname_length] = 0; // Make sure string is zero-terminated
						_MessageBufrr.SaveDatafile( FilenameData.pathname);
						SendSignal( MT_MESSAGE_LOG_SAVED);
						Status( (MyCString) "Saved Data to '" + FilenameData.pathname + "':");
						Status( (MyCString) "    Num messages: " + _MessageBufrr.GetNumMessages());
						Status( (MyCString) "    Num data bytes: " + _MessageBufrr.GetNumDataBytes());
						_MessageBufrr.ClearBuffer( );
						break;
					case MT_PAUSE_MESSAGE_LOGGING:
						Status( "Logging paused!");
						_logging = false;
						break;
					case MT_RESUME_MESSAGE_LOGGING:
						Status( "Logging resumed!");
						_logging = true;
						break;
					case MT_RESET_MESSAGE_LOG:
						Status( "Resetting the message log");
						_MessageBufrr.ClearBuffer( );
						break;
					case MT_DUMP_MESSAGE_LOG:
						//Status( "Dumping message log to QuickLoggerDump.bin");
						Status( "Dumping message log");
						//_MessageBufrr.SaveDatafile( "QuickLoggerDump.bin");
						AutoDumpBuffer();
						break;
					case MT_LM_EXIT:
						//_MessageBufrr.SaveDatafile( "QuickLoggerDump.bin");
						Status( "Auto dumping and Exiting");
						AutoDumpBuffer();
						return;
					default:
						break;
				}
			}
		}
		catch(MyCException &E)
		{
			_MessageBufrr.SaveDatafile( "QuickLoggerDump.bin");
			E.AddToStack("Caught MyCException, saving message log to QuickLoggerDump.bin");
			throw E;
		}
		catch(...)
		{
			_MessageBufrr.SaveDatafile( "QuickLoggerDump.bin");
			throw MyCException( "Caught unknown exception, saving message log to QuickLoggerDump.bin");
		}
	} CATCH_and_THROW( "void CQuickLogger::MainFunction()");
}

void CQuickLogger::Status(const MyCString& msg)
{
	TRY {
		time_t ltime;
		struct tm *tm;
		// output timestamp right before it start saving the data in the buffer
		ltime = time(NULL);
		tm = localtime(&ltime);
		char t_str[16];
		std::strftime(t_str,sizeof(t_str),"%I:%M:%S",tm);
		std::cout << t_str << " " << msg.GetContent() << std::endl;
		//std::cout << tm->tm_hour << ":" << tm->tm_min << ":" << tm->tm_sec << "    " << msg.GetContent() << std::endl;
		CMessage S( MT_DEBUG_TEXT, msg.GetContent(), msg.GetLen());
		SendMessage( &S);
	} CATCH_and_THROW( "void CQuickLogger::Status(const MyCString& msg)");
}

void CQuickLogger::DumpBuffer( char *Filename)
{
  TRY {
    time_t ltime;
    struct tm *tm;
    // output timestamp right before it start saving the data in the buffer
    ltime = time(NULL);
    tm = localtime(&ltime);
    printf("Dumping buffer to %s\n",Filename);
    printf("Starting Buffer Dump (%d-%d-%d %d:%d:%d)\n", tm->tm_year+1900, tm->tm_mon+1, tm->tm_mday, tm->tm_hour, tm->tm_min, tm->tm_sec);
    _MessageBufrr.SaveDatafile( Filename );
    printf("Buffer Dump Done (%d-%d-%d %d:%d:%d)\n", tm->tm_year+1900, tm->tm_mon+1, tm->tm_mday, tm->tm_hour, tm->tm_min, tm->tm_sec);
    Status( (MyCString) "Saved Data to '" + Filename + "':");
    Status( (MyCString) "    Num messages: " + _MessageBufrr.GetNumMessages());
    Status( (MyCString) "    Num data bytes: " + _MessageBufrr.GetNumDataBytes());
  } CATCH_and_THROW( "void DumpBuffer( char Filename[MAX_LOGGER_FILENAME_LENGTH+1])")
}

void CQuickLogger::AutoDumpBuffer()
{
  TRY {
    char Filename[MAX_LOGGER_FILENAME_LENGTH+1];
    time_t ltime;
    struct tm *tm;

    // get current time
    ltime=time(NULL);
    tm=localtime(&ltime);

    // define dump file name : QuickLogger.Dump.<ts>,bin
    sprintf( \
      Filename, \
      "QuickLogger.Dump.%04d%02d%02d%02d%02d%02d.bin", \
      tm->tm_year+1900, \
      tm->tm_mon+1, \
      tm->tm_mday, \
      tm->tm_hour, \
      tm->tm_min, \
      tm->tm_sec);
    printf("Auto Dumping Buffer to %s\n", Filename );
    DumpBuffer(Filename);
  } CATCH_and_THROW( "void AutoDumpBuffer()")
}