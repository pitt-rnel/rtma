#include <stdio.h>
#include "RTMA.h"

#define MID_PRODUCER 10
#define MID_CONSUMER 11

#define MT_REQUEST_TEST_DATA 101
#define MT_TEST_DATA 102

typedef struct {
	int a;
	int b;
	double x;
} MDF_TEST_DATA;

void TestProducer( char *server_address)
{
	RTMA_Module mod( MID_PRODUCER, 0);
	if( strlen( server_address) > 0) mod.ConnectToMMM( server_address);
	else mod.ConnectToMMM();
	mod.Subscribe( MT_REQUEST_TEST_DATA);
	mod.Subscribe( MT_EXIT);
	mod.Subscribe( MT_KILL);
	mod.SendModuleReady();
	bool run = true;
	while( run) {
		CMessage m;
		std::cout << "Waiting for message" << std::endl;
		mod.ReadMessage( &m);
		std::cout << "Received message " << m.msg_type << std::endl;
		CMessage M( MT_TEST_DATA);
		MDF_TEST_DATA data;
		switch( m.msg_type) {
			case MT_REQUEST_TEST_DATA:
				data.a = 3;
				data.b = 47;
				data.x = 123.456;
				M.SetData( &data, sizeof(data));
				mod.SendMessageRTMA( &M);
				std::cout << "Sent message " << M.msg_type << std::endl;
				break;
			case MT_EXIT:
			case MT_KILL:
				run = false;
				break;
		}
	}
}

void TestConsumer( char *server_address)
{
	RTMA_Module mod( MID_CONSUMER, 0);
	if( strlen( server_address) > 0) mod.ConnectToMMM( server_address);
	else mod.ConnectToMMM();
	mod.Subscribe( MT_TEST_DATA);
	mod.Subscribe( MT_EXIT);
	mod.Subscribe( MT_KILL);
	mod.SendModuleReady();
	int run = true;
	while( run) {
		mod.SendSignal( MT_REQUEST_TEST_DATA);
		std::cout << "Sent request for data" << std::endl;
		CMessage M;
		mod.ReadMessage( &M);
		std::cout << "Received message " << M.msg_type << std::endl;
		MDF_TEST_DATA data;
		switch( M.msg_type) {
			case MT_TEST_DATA:
				M.GetData( &data);
				std::cout << "Data = [a: " << data.a << ", b: " << data.b << ", x: " << data.x << "]" << std::endl;
				break;
			case MT_EXIT:
			case MT_KILL:
				run = false;
				break;
		}
		Sleep( 1000);
	}
}

int main( int argc, char *argv[])
{
	try {

		if( argc < 2) throw MyCException( "Need a command-line argument that specifies 'producer' or 'consumer'");
		char *option = argv[1];
		if( strcmp( option, "producer")==0) {
			if( argc > 2) TestProducer( argv[2]); // If server address specified, then use it
			else TestProducer( "");
		} else if( strcmp( option, "consumer")==0) {
			if( argc > 2) TestConsumer( argv[2]); // If server address specified, then use it
			else TestConsumer( "");
		} else {
			throw MyCException( "Command-line argument must be 'producer' or 'consumer'");
		}
	}
	catch( UPipeClosedException &e)
	{
		MyCString s;
		e.AppendTraceToString( s);
		std::cout << "UPipeClosedException: " << s.GetContent() << std::endl;
	}
	catch( UPipeException &e)
	{
		MyCString s;
		e.AppendTraceToString( s);
		std::cout << "UPipeException: " << s.GetContent() << std::endl;
	}
	catch( MyCException &e)
	{
		MyCString s;
		e.AppendTraceToString( s);
		std::cout << "MyCException: " << s.GetContent() << std::endl;
	}
	catch(...)
	{
		MyCString s;
		std::cout << "Unknown Exception!" << std::endl;
	}
	
	std::cout << "Exiting cleanly." << std::endl;
}
