// This file may be of historical interest. It represents the original rough design of RTMA, 
// written down as pseudo-code

// RTMA - RealTime Messaging Architecture
//
// Meel Velliste, Jan 2006

MessageManger is Module 0


// Header for all messages passed through RTMA
typedef struct {
	msg_count; // Source message count (per source, starting from 1 when source connects to MMM)
	send_time; // Time at source when message sent (Seconds since 0:00:00 on Jan 1, 1970)
	recv_time; // Time at final destination when message received (Seconds since 0:00:00 on Jan 1, 1970)
	src_host_id; // ID number of the host computer where the message originates
	src_mod_id; // ID number of the program module where the message originates
	dest_host_id; // ID number of the host computer intended to receive this message
	dest_mod_id; // ID number of the module ID intended to receive this message
	msg_type; // Message type ID
	num_data_bytes; // Number of data bytes following this header
} MESSAGE_HEADER;

// Make sure all functions check for validity of their arguments


//
// Functions for application modules to communicate through the RTMA
//

// Global variables in C (class members in C++).
// This means that two modules should never share the same address space if using C.
MMPipeHandle
ModulePipeHandle
ThisModuleID
MessageCount

ConnectToMMM( ) -> Status
// Opens a read and a write connection to the Message Management Module
{
	MessageCount = 1;
	Create pipe called "Module_pipe_<ThisModuleID>";
	Open read handle to "Module_pipe_<ThisModuleID>" -> ModulePipeHandle;
	Open write handle to "MessageManager_pipe" -> MMPipeHandle;
	Send a CONNECT message to MMM;
	Wait for ACK;
}


DisconnectFromMMM( )
{
	Unsubscribe( ALL_MESSAGE_TYPES);
	Send a DISCONNECT message with ThisModuleID to MMM;
	Wait for ACK;
	Close MMPipeHandle;
	Close ModulePipeHandle;
	Destroy the pipe named "Module_pipe_<ThisModuleID>";
	MessageCount = 0;
}

Subscribe( MessageType) -> Status
// MessageType is a specific message ID to subscribe just to that type of message,
// or ALL_MESSAGE_TYPES to get all message types (useful for debugging);
{
	Send a SUBSCRIBE message with MessageType to MMM;
	Wait for ACK;
}

Unsubscribe( MessageType) -> Status
// MessageType is a specific message ID to unsubscribe from only that message type
// or ALL_MESSAGE_TYPES to unsubscribe from all message types
{
	Send an UNSUBSCRIBE message with MessageType to MMM;
	Wait for ACK;
}

SendMessage( Message)
{
	Assume that msg_type and data have been filled in
	Fill in the rest of the header
	Take care to write the entire message to MMPipeHandle in one write call

	MessageCount++;
}

ReadMessage( ) -> Message, Status
{
	Read sizeof(MESSAGE_HEADER) bytes from ModulePipeHandle
	Get num_data_bytes from header
	Read num_data_bytes from ModulePipeHandle
}

SendSignal( MessageType)
// Send message that only has the header (no data after the header).
{
	Create a message structure;
	Fill in msg_type;
	SendMessage( message);
}

//
// Data structures and functions that implement the Message Manager
//

// A list of modules registered for each type of message
//
// [0]
// [1]-->(Module5)-->(Module1)-->(Module7)
// [2]
// [3]-->(Module3)
// [4]-->(Module1)-->(Module8)
//  .
//  .
// [n-1]-->(Module7)-->(Module3)
// [n]

typedef struct {
	ModuleID;
	HostID;
	pNext;
} SubscriberRecord;

#define MAX_MESSAGE_TYPES <large number>
SubscriberRecord* SubscribersToMessageType[MAX_MESSAGE_TYPES];

MessageManagerMainLoop( )
{
	FOREVER {
		M = ReadMessage( );
		SubscriberList = ProcessMessage( M);
		DispatchMessage( M, SubscriberList);
	}
}

ProcessMessage( M) -> SubscriberList
{
	SubscriberList = EMPTY;
	switch( M.msg_type) {
	case CONNECT: ConnectModule( M.src_mod_id);
	case DISCONNECT: DisconnectModule( M.src_mod_id);
	case SUBSCRIBE: AddSubscription( M.src_mod_id, M.data.desired_msg_type);
	case UNSUBSCRIBE: RemoveSubscription( M.src_mod_id, M.data.desired_msg_type);
	default: SubscriberList = GetSubscriberList( M.msg_type);
	}
}

ConnectModule( module_id)
{
	Create module record
	Open write handle to module's pipe
	Keep module's pipe handle in module record
	Send ACK to module
}

DisconnectModule( module_id)
{
	Close handle to module's pipe
	Delete module record
	Cancel all the subscriptions of the module
	Send ACK to module
}

AddSubscription( module_id, message_type)
{
	if a particular message_type
		Add module entry in SubscribersToMessageType[message_type];
	if ALL_MESSAGE_TYPES
		Add module entry in SubscribersToMessageType[*];
	Send ACK to module
}

RemoveSubscription( module_id, message_type)
{
	if a particular message_type
		Find and remove the module's entry in SubscribersToMessageType[message_type];
	if ALL_MESSAGE_TYPES
		Find and remove the module's entries in SubscribersToMessageType[*];
	Send ACK to module (unless called from DisconnectModule)
}

GetSubscriberList( message_type) -> SubscriberList
{
	Return list from SubscribersToMessageType[message_type];
}
