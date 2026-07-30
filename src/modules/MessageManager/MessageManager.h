#ifndef _MESSAGEMANAGER_H_
#define _MESSAGEMANAGER_H_

#include "RTMA.h"
#include "bit_operations.h"
#include <sys/timeb.h>
#include <time.h>
#include "Debug.h"

#ifdef _UNIX_C
	#include <pthread.h>
	#include <limits.h> //where PIPE_BUF is located
#endif

class CModuleRecord
{
public:
	MODULE_ID   ModuleID;
	UPipe       *pModulePipe;
	short       LoggerStatus;
	short		DaemonStatus;
	short		AllowMultiple;
	uint16_t	port;
	int32_t		uid;
	int32_t		pid;
	char*		addr;
	char*    	name;
	
	CModuleRecord( ) {
		name = NULL;
		addr = NULL;
		Reset();
	}

	void SetName(char* src_name) {
		if (name != NULL) {
			myfree(name);
		}
		name = (char*) malloc(MAX_NAME_LEN);
		if (name != NULL) {
			memcpy(name, src_name, MAX_NAME_LEN);
			name[MAX_NAME_LEN - 1] = '\0';
		}
	}

	void SetUPipe(UPipe* pipe) {
		if (addr != NULL) {
			myfree(addr);
			addr = NULL;

		}


		pModulePipe = pipe;

		port = 0;

		if (pipe == NULL) {
			return;
		}

		addr = (char*)malloc(MAX_NAME_LEN);
		if (addr != NULL) {
			memset(addr, 0, MAX_NAME_LEN);

			if (!pipe->GetIpAddress(addr, &port, MAX_NAME_LEN)) {

				addr[0] = '\0';

				port = 0;

			}

		}
	}

	void SetHello(MDF_HELLO *hello) {
		if (hello == NULL) {

			return;

		}

		memset(hello, 0, sizeof(*hello));



		hello->uid = uid;
		hello->mod_id = ModuleID;
		hello->pid = pid;
		hello->port = port;

		if (addr != NULL) {
			strncpy(hello->addr, addr, sizeof(hello->addr) - 1);

		}

		if (name != NULL) {
			strncpy(hello->name, name, sizeof(hello->name) - 1);

		}
	}

	void SetGoodbye(MDF_GOODBYE *goodbye) {
		goodbye->uid = uid;
		goodbye->mod_id = ModuleID;
		goodbye->pid = pid;
		goodbye->port = port;

		if (addr != NULL) {
			memcpy(goodbye->addr, addr, sizeof(goodbye->addr));
		}
		else {
			goodbye->addr[0] = '\0';
		}

		if (name != NULL) {
			memcpy(goodbye->name, name, sizeof(goodbye->name));
		}
		else {
			goodbye->name[0] = '\0';
		}
	}

	void myfree(char* p) {
		free(p);
	}

	void
	Reset(void) {

		if (name != NULL) {
			myfree(name);
			name = NULL;
		}

		if (addr != NULL) {
			myfree(addr);
			addr = NULL;
		}


		ModuleID = -1;

		pModulePipe = NULL;

		LoggerStatus = 0;
		DaemonStatus = 0;
		AllowMultiple = 0;
		port = 0;

		pid = 0;
		uid = -1;
	}

	~CModuleRecord() {

		Reset();
	}
};

class CListItem
{
friend class CList;
private:
	CListItem *next;
	CListItem *prev;

public:
	int data;
	int flags;

	CListItem( ) {
		CListItem( 0);
	}
	CListItem( int i) {
		data = i;
		flags = 0;
		next = NULL;
		prev = NULL;
	}
};

class CList
{
private:
	CListItem head;
	CListItem tail;

public:

	CList( ) {
		head.next = &tail;
		head.prev = NULL;
		tail.next = NULL;
		tail.prev = &head;
	}

	~CList( ) {
		CListItem *item = GetFirstItem();
		while( item != NULL) {
			CListItem *next_item = GetNextItem( item);
			delete item;
			item = next_item;
		}
	}

	void
	InsertItemBefore( CListItem *new_item, CListItem *item) {
		new_item->prev = item->prev;
		new_item->next = item;
		new_item->prev->next = new_item;
		item->prev = new_item;
	}

	void
	AppendItem( CListItem *item) {
		InsertItemBefore( item, &tail);
	}

	void
	RemoveItem( CListItem *item) {
		item->prev->next = item->next;
		item->next->prev = item->prev;
		delete item;
	}

	CListItem *
	GetFirstItem( void) {
		if( head.next == &tail) return NULL;
		else return head.next;
	}

	CListItem *
	GetNextItem( CListItem *current_item) {
		if( current_item == NULL) return NULL;
		if( current_item->next == &tail) return NULL;
		else return current_item->next;
	}

	bool
	DoesItemExist( CListItem *search_item) {
		CListItem *item = GetFirstItem();
		while( item != NULL) {			
			if(item->data == search_item->data) 
				return true;
			item = GetNextItem( item);
		}
		return false;
	}
};

#define SUBSCRIBER_FLAG_PAUSE  			0x01


class CSubscriberList : protected CList
{
private:

	CListItem *m_CurrentItem;

public:

	CSubscriberList( ) {
		m_CurrentItem = NULL;
	}

	void
	AddSubscriber(UID uid) {
		CListItem *subscriber = new CListItem(uid);
		AppendItem( subscriber);
	}

	void
	RemoveSubscriber(UID uid) {
		CListItem *current_item = GetFirstItem();
		while( current_item != NULL) {
			CListItem *next_item = GetNextItem(current_item);
			if( current_item->data == uid) {
				RemoveItem(current_item);
			}
			current_item = next_item;
		}
	}

	void
	PauseSubscriber(UID uid) {
		CListItem *current_item = GetFirstItem();
		while( current_item != NULL) {
			if( current_item->data == uid) {
				set_flag_bits( current_item->flags, SUBSCRIBER_FLAG_PAUSE);
				break;
			}
			current_item = GetNextItem( current_item);
		}
	}

	void
	ResumeSubscriber(UID uid) {
		CListItem *current_item = GetFirstItem();
		while( current_item != NULL) {
			if( current_item->data == uid) {
				clear_flag_bits( current_item->flags, SUBSCRIBER_FLAG_PAUSE);
				break;
			}
			current_item = GetNextItem( current_item);
		}
	}

	int
	SubscriptionPaused(void) {
		int is_paused = 0;
		if( m_CurrentItem != NULL) {
			if( check_flag_bits( m_CurrentItem->flags, SUBSCRIBER_FLAG_PAUSE)) {
				is_paused = 1;
			}
		}
		return is_paused;
	}

	UID
	GetFirstSubscriber(void) {
		m_CurrentItem = GetFirstItem();
		if( m_CurrentItem == NULL) {
			return -1;
		} else {
			return m_CurrentItem->data;
		}
	}

	UID
	GetNextSubscriber(void) {
		m_CurrentItem = GetNextItem( m_CurrentItem);
		if( m_CurrentItem == NULL) {
			return -1;
		} else {
			return m_CurrentItem->data;
		}
	}
	
	bool
	IsSubscribed(UID uid){
		CListItem subscriber = CListItem(uid);
		return DoesItemExist(&subscriber);
	}

};


class CMessageManager : public UPipeAutoServer
{
public:

	CMessageManager( );
	~CMessageManager( );

	void
	MainLoop( char *cmd_line_options);

private:
	MODULE_ID		m_NextDynamicModId;
	CModuleRecord   m_ConnectedModules[MAX_MODULES];
	CSubscriberList m_SubscribersToMessageType[MAX_MESSAGE_TYPES];
	CSubscriberList m_EmptySubscriberList;
	CMessage		m_OutMsg;
	MyCString       m_Version;

	MODULE_ID GetDynamicModuleId()
	{
		MODULE_ID curr_id = m_NextDynamicModId;

		if (curr_id > MAX_MODULE_ID) {
			printf("All dynamic IDs are in use.\n");
			return 0;
		}
		else {
			// update offset to next available dynamic module ID
			m_NextDynamicModId++;
			return curr_id;
		}
	}

	void
	HandleData( UPipe *pClientPipe);
	// Override of abstract base class method. Gets called whenever data is ready on any input pipe.

	void
	HandleDisconnect( UPipe *pClientPipe);
	// Override of virtual base class method to handle unexpected module disconnect cleanly

	void
	ProcessMessage( CMessage *M, UPipe *pSourcePipe);

	void
	DistributeMessage( CMessage *M);
	//Forwards the message to all subscribers and Logger modules, without changing the headers

	void
	DispatchMessage( CMessage *M);
	//Sends the message to all subscribers and Logger modules, headers specifying the message came from MM

	void
	DispatchMessage( CMessage *M, CModuleRecord *dest_mod);
	//Sends the message only to the specified mod_id and Logger modules, headers specifying the message came from MM

	void
	DispatchSignal( MSG_TYPE sig, CModuleRecord *dest_mod);
	//Sends the signal only to the specified mod_id and Logger modules, headers specifying the message came from MM

	void
	DispatchMessageToAll( CMessage *M);
	//Dispatches a message to each connected module (and each Logger module)

	void
	DispatchSignalToAll( MSG_TYPE sig);
	//Dispatches a signal to each connected module (and each Logger module)

	MODULE_ID
	ConnectModule( MODULE_ID module_id, UPipe *pSourcePipe, short logger_status, short daemon_status);

	MODULE_ID
	ConnectModuleV2( MODULE_ID module_id, UPipe *pSourcePipe, MDF_CONNECT_V2 *connect);

	CModuleRecord* GetOpenRecord();

	CModuleRecord* GetRecord(MODULE_ID module_id);

	void
	DisconnectModule(MODULE_ID module_id);

	void
	CleanUpModuleRecord(CModuleRecord *mod);

	void
	ShutdownModule(MODULE_ID module_id);

	void
	ShutdownAllModules(int shutdown_RTMA=1, int shutdown_daemons=1);

	void
	AddSubscription(CModuleRecord *mod, MSG_TYPE message_type);

	void
	RemoveSubscription(CModuleRecord *mod, MSG_TYPE message_type);
	
	void
	PauseSubscription(CModuleRecord *mod, MSG_TYPE msg_type_to_pause);

	void
	ResumeSubscription(CModuleRecord *mod, MSG_TYPE msg_type_to_resume);

	CSubscriberList *
	GetSubscriberList( MSG_TYPE message_type);

	bool
	IsModuleSubscribed(UID uid, MSG_TYPE message_type);

	void 
	SendAcknowledge(CModuleRecord* mod);
	
	void
	SendIntroductions(MODULE_ID mod_id);

	void 
	SendHello(CModuleRecord *mod);

	void 
	SendGoodbye(CModuleRecord* mod);

	void 
	SendPing(MODULE_ID mod_id);

	void 
	HandleSetName(CMessage *m);

	void 
	HandleForceDisconnect(CMessage *m);

	void 
	HandleModuleDisconnect(CMessage *m);

	void 
	HandleModuleReady(CMessage *m);

	void 
	HandleSubscribe(CMessage *m);

	void 
	HandleUnsubscribe(CMessage *m);

	void 
	HandlePauseSubscription(CMessage *m);

	void 
	HandleResumeSubscription(CMessage *m);

	void 
	HandleConnect(CMessage *m, UPipe* pSourcePipe);

	void 
	HandleConnectV2(CMessage *m, UPipe* PSourcePipe);

	int
	SendMessage( CMessage *m, CModuleRecord *dest_mod);
	
	int
	SendSignal( MSG_TYPE sig, CModuleRecord *dest_mod);
	//dest_mod_id= module id that should be put in dest_mod_id in message header

	int
	ForwardMessage(CMessage *m, CModuleRecord* mod);

	int
	ModuleIsConnected(MODULE_ID mod_id);

	void
	LogFailedMessage( CMessage *m, MODULE_ID mod_id);
	//sends a message to logger modules indicating that a message failed to be forwarded to one of the modules
};


#endif //_MESSAGEMANAGER_H_
