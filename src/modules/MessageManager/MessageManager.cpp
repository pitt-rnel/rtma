/*
 *  MessageManager - Receives and distributes RTMA messages to/from modules
 *
 *  Meel Velliste 10/28/2008
 *  Emrah Diril  10/14/2011
 *  Jeff Weiss: 09/10/2014 (merged HST RTMA (v2.00) with updates from Dragonfly v2.10)
 */

#include "MessageManager.h"
#include "Debug.h"

#ifdef _UNIX_C
int main(int argc, char *argv[])
#else
int main(int argc, char *argv[])
#endif
{
	try
	{
		char *options;
		char empty_str[] = "";
#ifdef _UNIX_C
		options = (argc > 1) ? argv[1] : empty_str;
#else
		options = (argc > 1) ? argv[1] : empty_str;
// options = (char*) lpCmdLine;
#endif

		CMessageManager* MM = new CMessageManager();
		MM->MainLoop(options);
		delete MM;
		return 0;
	}
	catch (MyCException &E)
	{
		E.AddToStack("MM WinMain- aborting");
		E.ReportToFile();
		return 0;
	}
}

CMessageManager::CMessageManager()
{
	m_Version = "2.11bci";
	m_NextDynamicModId = DYN_MOD_ID_START;

	// Initialize the module record array
	// uid=-1 indicates an unused slot
	for (int i = 0; i < MAX_MODULES; i++)
	{
		m_ConnectedModules[i].Reset();
	}

	InitializeAbsTime();
}

CMessageManager::~CMessageManager()
{
}

void CMessageManager::MainLoop(char *cmd_line_options)
{
	try
	{
		DEBUG_TEXT("Entering Main Loop");

		// Elevate process priority
#ifdef _WINDOWS_C
		BOOL success = SetPriorityClass(GetCurrentProcess(), REALTIME_PRIORITY_CLASS);
		// if( success) printf("Yay!\n");
		// else printf("Too bad!\n");
		success = SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_TIME_CRITICAL);
		// if( success) printf("Yay!\n");
		// else printf("Too bad!\n");
#endif
		// Start managing messages
		if (strlen(cmd_line_options) > 0)
		{
			char *server_name = cmd_line_options;
			UPipeAutoServer::Run(server_name);
		}
		else
		{
			UPipeAutoServer::Run(DEFAULT_PIPE_SERVER_NAME_FOR_MM);
		}

		DEBUG_TEXT("Main Loop Finished");
	}
	catch (MyCException &E)
	{
		E.AddToStack("CMessageManager::MainLoop()");
		throw E;
	}
}

void CMessageManager::HandleData(UPipe *pSourcePipe)
{
	SetMyPriority(THIS_MODULE_BASE_PRIORITY);
	DEBUG_TEXT_("Receiving message from pipe " << pSourcePipe << "... ");
	CMessage M;
	M.Receive(pSourcePipe);
	DEBUG_TEXT("Received message of type " << M.msg_type);

	ProcessMessage(&M, pSourcePipe);
	DistributeMessage(&M);
	SetMyPriority(NORMAL_PRIORITY_CLASS);
}

void CMessageManager::HandleDisconnect(UPipe *pModulePipe)
{
	DEBUG_TEXT_("Pipe " << pModulePipe << " broken");
	// Find module ID
	for (int uid = 0; uid < MAX_MODULES; uid++)
	{
		CModuleRecord *mod = &m_ConnectedModules[uid];
		if (mod->pModulePipe == pModulePipe)
		{
			// Make sure not to send anything to disconnected client
			RemoveSubscription(mod, ALL_MESSAGE_TYPES);

			// Notify that the module has left
			SendGoodbye(mod);

			// Delete module record
			CleanUpModuleRecord(mod);
			DEBUG_TEXT_(", disconnected module " << mod->ModuleID);

			break;
		}
	}
	DEBUG_TEXT("!");
}

void CMessageManager::ProcessMessage(CMessage *M, UPipe *pSourcePipe)
{
	DEBUG_TEXT_("Processing message... ");

	switch (M->msg_type)
	{
	case MT_CONNECT:
		HandleConnect(M, pSourcePipe);
		break;

	case MT_CONNECT_V2:
		HandleConnectV2(M, pSourcePipe);
		break;

	case MT_CLIENT_SET_NAME:
		HandleSetName(M);
		break;

	case MT_PONG:
		break;

	case MT_INTRODUCE:
		SendIntroductions(M->src_mod_id);
		break;

	case MT_FORCE_DISCONNECT:
		HandleForceDisconnect(M);
		break;

	case MT_DISCONNECT:
		HandleModuleDisconnect(M);
		break;

	case MT_MODULE_READY:
		HandleModuleReady(M);
		break;

	case MT_SUBSCRIBE:
		HandleSubscribe(M);
		break;

	case MT_UNSUBSCRIBE:
		HandleUnsubscribe(M);
		break;

	case MT_PAUSE_SUBSCRIPTION:
		HandlePauseSubscription(M);
		break;

	case MT_RESUME_SUBSCRIPTION:
		HandleResumeSubscription(M);
		break;

	default:
		DEBUG_TEXT("Nothing to do!");
		return;
	}
	DEBUG_TEXT("Processed!");
}

void CMessageManager::SendHello(CModuleRecord *mod)
{
	MDF_HELLO hello;
	if ((mod != NULL) && (mod->uid >= 0)){
		mod->SetHello(&hello);
		//printf("Hello: %d\n", hello.mod_id);
		m_OutMsg.Set(MT_HELLO, &hello, sizeof(hello));
		DispatchMessage(&m_OutMsg);
	}
}

void CMessageManager::SendGoodbye(CModuleRecord *mod)
{
	MDF_GOODBYE goodbye;
	if ((mod != NULL) && (mod->uid >= 0)) {
		mod->SetGoodbye(&goodbye);
		//printf("Goodbye: %d\n", goodbye.mod_id);
		m_OutMsg.Set(MT_GOODBYE, &goodbye, sizeof(goodbye));
		DispatchMessage(&m_OutMsg);
	}
}

void CMessageManager::SendPing(MODULE_ID mod_id)
{
	MDF_PING ping;
	memset(&ping, 0, sizeof(ping));
	CModuleRecord *mod = GetRecord(mod_id);
	if ((mod != NULL) && (mod->uid >= 0))
	{
		ping.uid = mod->uid;
		ping.dest_id = mod->ModuleID;
		m_OutMsg.Set(MT_PING, &ping, sizeof(ping));
		DispatchMessage(&m_OutMsg, mod);
	}
}

void CMessageManager::HandleSetName(CMessage *M)
{
	MDF_CLIENT_SET_NAME set_name;
	M->GetData((void *)&set_name);
	CModuleRecord *mod = GetRecord(M->src_mod_id);
	if ((mod != NULL) && (mod->uid >= 0))
	{
		mod->SetName(&(set_name.name[0]));
		//printf("SetName: %d -> %s\n", mod->ModuleID, mod->name);
		SendHello(mod);
	}
}

/*
 * Should be called when forwarding a message from other modules
 * The given message will be forwarded to:
 *  - all subscribed logger modules (ALWAYS)
 *  - if the message has a destination address, and it is subscribed to by that destination
 *    it will be forwarded only there
 *  - if the message has no destination address, it will be forwarded to all subscribed modules
 */
void CMessageManager::DistributeMessage(CMessage *M)
{
	DEBUG_TEXT("Distributing Message...");
	int timing_set = 0;

	CSubscriberList *SL;
	SL = GetSubscriberList(M->msg_type);
	if (SL != NULL)
	{
		UID uid = SL->GetFirstSubscriber();
		while (uid >= 0)
		{
			/* the order of the code in this while loop is important
			   don't modify it unless you know what you're doing
			 */
			CModuleRecord *mod = &m_ConnectedModules[uid];

			int send_it = 0;
			int has_specific_dest = (M->dest_mod_id == 0) ? 0 : 1;

			if (has_specific_dest)
			{
				// send only to the specific destination
				if (mod->ModuleID == M->dest_mod_id)
					send_it = 1;
				else
					send_it = 0;
			}
			else
			{
				// no specific destination address- so should be forwarded to all subscribers for this MT
				send_it = 1;
			}

			// forward everything to logger modules
			if (mod->LoggerStatus)
				send_it = 1;

			if (SL->SubscriptionPaused())
				send_it = 0;

			if (send_it)
			{
				DEBUG_TEXT_("Forwarding message to module " << mod->ModuleID << "... ");
				try
				{
					int status = ForwardMessage(M, mod);
					if (status == 0) {
						LogFailedMessage(M, mod->ModuleID);
						DEBUG_TEXT("Failed to Forward Message!");
					}
					else {
						DEBUG_TEXT("Forwarded!");
					}
				}
				catch (UPipeClosedException& E) {
					DEBUG_TEXT("Failed to Forward Message, destination module socket is closed/dead");
				}
			}

		uid = SL->GetNextSubscriber();
		}
	}
	DEBUG_TEXT("Done distributing!");
}

/*
 *  Should be called internally in MM when sending a message to anybody that cares
 *  The message will be sent to all subscribed modules including loggers
 */
void CMessageManager::DispatchMessage(CMessage *M)
{
	CSubscriberList *SL;

	SL = GetSubscriberList(M->msg_type);
	if (SL != NULL)
	{
		// Send message to all subscribers
		UID uid = SL->GetFirstSubscriber();
		while (uid >= 0)
		{
			CModuleRecord *mod = &m_ConnectedModules[uid];
			SendMessage(M, mod);
			uid = SL->GetNextSubscriber();
		}
	}
}

/*
 *	Should be called internally in MM when sending a message to a module
 *  The message will be sent, even if the module is not subscribed to it
 *  The message will also be forwarded to all subscribed logger modules
 */
void CMessageManager::DispatchMessage(CMessage *M, CModuleRecord *dest_mod)
{
	CSubscriberList *SL;

	// send the message to the module it is intended to, disregarding subscriptions
	//(enables MM to send system message to modules)
	SendMessage(M, dest_mod);

	// CC all logger modules
	SL = GetSubscriberList(M->msg_type);
	if (SL != NULL)
	{
		UID uid = SL->GetFirstSubscriber();

		while (uid >= 0)
		{
			CModuleRecord *mod = &m_ConnectedModules[uid];
			if (mod->LoggerStatus)
				if (mod->ModuleID != dest_mod->ModuleID) // don't send to destination module again
					ForwardMessage(M, mod);

			uid = SL->GetNextSubscriber();
		}
	}
}

/*
 *	Should be called internally in MM when sending a signal to a specific module
 *  The signal will be sent, even if the module is not subscribed to it
 *  The signal will also be forwarded to all subscribed logger modules
 */
void CMessageManager::DispatchSignal(MSG_TYPE sig, CModuleRecord *dest_mod)
{
	m_OutMsg.Set(sig);
	DispatchMessage(&m_OutMsg, dest_mod);
}

/*
 *	Should be called internally in MM when sending a message to all modules
 *  The message will be sent to all connected modules, even if the module is not subscribed to it
 *  The message will also be forwarded to all subscribed logger modules
 */
void CMessageManager::DispatchMessageToAll(CMessage *M)
{
	for (int uid = 0; uid < MAX_MODULES; uid++)
	{
		CModuleRecord *mod = &m_ConnectedModules[uid];
		if (uid >= 0 && mod->ModuleID > 0)
		{
			DispatchMessage(M, mod);
		}
	}
}

void CMessageManager::DispatchSignalToAll(MSG_TYPE sig)
{
	CMessage R(sig);
	DispatchMessageToAll(&R);
}

int CMessageManager::SendMessage(CMessage *M, CModuleRecord *mod)
// overloaded function for RTMA_Module::SendMessage()
// Sends a message to a module, specifying the MessageManager itself as the source module
{
	UPipe *mod_pipe = mod->pModulePipe;
	if (mod_pipe == NULL)
		return 0;

	// Assume that msg_type, num_data_bytes, data - have been filled in
	M->msg_count = 0;
	M->send_time = GetAbsTime();
	M->recv_time = 0.0;
	M->src_host_id = HID_LOCAL_HOST;
	M->src_mod_id = MID_MESSAGE_MANAGER;
	M->dest_mod_id = mod->ModuleID;

	double timeout = 0; // By default use non-blocking write so MM does not get stuck on a frozen module
	if (mod->LoggerStatus)
		timeout = -1; // Logger modules should not lose data, so use blocking write

	int status = M->Send(mod_pipe, timeout);

	return status;
}

int CMessageManager::ForwardMessage(CMessage *M, CModuleRecord *dest_mod)
// Forward a message where the header is already filled in
// Source module field in the header is unaltered
{
	UPipe *mod_pipe = dest_mod->pModulePipe;
	if (mod_pipe == NULL)
		return 0;

	double timeout = 0; // By default use non-blocking write so MM does not get stuck on a frozen module
	if (dest_mod->LoggerStatus)
		timeout = -1; // Logger modules should not lose data, so use blocking write

	int status = M->Send(mod_pipe, timeout);

	return status;
}

int CMessageManager::SendSignal(MSG_TYPE sig, CModuleRecord *dest_mod)
// overloaded function for RTMA_Module::SendSignal()
// returns 0 if module is not connected, or failed to send message to it; 1 on success
{
	m_OutMsg.Set(sig);
	return SendMessage(&m_OutMsg, dest_mod);
}

CModuleRecord *
CMessageManager::GetOpenRecord()
{
	for (int i = 0; i < MAX_MODULES; i++)
	{
		CModuleRecord* mod = &m_ConnectedModules[i];
		if (mod->uid == -1)
		{
			mod->Reset();
			mod->uid = i;
			//printf("CreateNewRecord(%d)\n", mod->uid);
			return mod;
		}
	}
	return NULL;
}

MODULE_ID
CMessageManager::ConnectModule(MODULE_ID module_id, UPipe *pSourcePipe, short logger_status, short daemon_status)
{

	if ((module_id <= MAX_MODULE_ID) && (module_id >= 0) && !ModuleIsConnected(module_id))
	{
		if (pSourcePipe != NULL)
		{
			CModuleRecord *mod = GetOpenRecord();
			if (mod == NULL)
			{
				printf("MessageManager has reached the MAX_MODULES allowed\n.");
				return -1;
			}

			// get the next available module ID from "dynamic" pool
			if (module_id == 0)
				module_id = GetDynamicModuleId();

			if (module_id > 0)
			{
				DEBUG_TEXT("Connecting module " << module_id << " on pipe " << pSourcePipe);

				// Create a module record
				mod->ModuleID = module_id;
				mod->SetUPipe(pSourcePipe);
				mod->LoggerStatus = logger_status;
				mod->DaemonStatus = daemon_status;

				SendAcknowledge(mod);

				// Notify that a client has connected
				// Note: PID and Name will not be filled in
				// Additional HELLO msgs will be sent with
				// CLIENT_SET_NAME and MODULE_READY 
				SendHello(mod);
			}
		}
	}
	else
		module_id = 0; // something went wrong, don't allow the new connection

	return module_id;
}

MODULE_ID
CMessageManager::ConnectModuleV2(MODULE_ID module_id, UPipe *pSourcePipe, MDF_CONNECT_V2 *data)
{

	if ((module_id <= MAX_MODULE_ID) && (module_id >= 0) && !ModuleIsConnected(module_id))
	{
		if (pSourcePipe != NULL)
		{
			CModuleRecord *mod = GetOpenRecord();
			if (mod == NULL)
			{
				printf("MessageManager has reached the MAX_MODULES allowed\n.");
				return -1;
			}

			// get the next available module ID from "dynamic" pool
			if (module_id == 0)
				module_id = GetDynamicModuleId();

			if (module_id > 0)
			{
				DEBUG_TEXT("Connecting module " << module_id << " on pipe " << pSourcePipe);

				mod->ModuleID = module_id;
				mod->SetUPipe(pSourcePipe);
				mod->LoggerStatus = data->logger_status;
				mod->DaemonStatus = data->daemon_status;
				mod->AllowMultiple = data->allow_multiple;
				mod->pid = data->pid;
				mod->SetName(&(data->name[0]));

				SendAcknowledge(mod);

				// Notify that a V2 client has connected
				SendHello(mod);
			}
		}
	}
	else
		module_id = 0; // something went wrong, don't allow the new connection

	return module_id;
}

CModuleRecord *CMessageManager::GetRecord(MODULE_ID module_id)
{
	for (int i = 0; i < MAX_MODULES; i++)
	{
		CModuleRecord* mod = &m_ConnectedModules[i];
		if ((mod->uid >= 0) && (mod->ModuleID == module_id))
		{
			return mod;
		}
	}
	return NULL;
}

void CMessageManager::DisconnectModule(MODULE_ID module_id)
{
	CModuleRecord *mod = GetRecord(module_id);
	if ((mod == NULL) || (mod->uid < 0))
		return;

	// Send ACK
	SendAcknowledge(mod);

	// Make sure not to send anything to disconnected client
	RemoveSubscription(mod, ALL_MESSAGE_TYPES);

	// Notify that the module has left
	SendGoodbye(mod);

	// Close module's pipe
	UPipeAutoServer::_server->DisconnectClient(mod->pModulePipe);

	// Clean up module record
	CleanUpModuleRecord(mod);
}

void CMessageManager::CleanUpModuleRecord(CModuleRecord *mod)
{
	//printf("CleanUpModuleRecord(%d)\n", mod->ModuleID);
	RemoveSubscription(mod, ALL_MESSAGE_TYPES);
	mod->Reset();
}

void CMessageManager::ShutdownModule(MODULE_ID mod_id)
{
	CModuleRecord *mod = GetRecord(mod_id);
	if (mod != NULL && mod->ModuleID > 0)
	{
		MODULE_ID mod_id = mod->ModuleID;
		switch (mod_id)
		{
		case MID_QUICKLOGGER:
			DispatchSignal(MT_LM_EXIT, mod);
			break;

		default:
			DispatchSignal(MT_EXIT, mod);
			break;
		}

		DisconnectModule(mod_id);
	}
}

void CMessageManager::ShutdownAllModules(int shutdown_RTMA, int shutdown_daemons)
{
	for (int uid = 0; uid < MAX_MODULES; uid++)
	{
		CModuleRecord *mod = &m_ConnectedModules[uid];
		if (mod->uid >= 0 && mod->ModuleID > 0)
		{
			if (mod->DaemonStatus)
			{
				if (shutdown_daemons)
					ShutdownModule(mod->ModuleID);
			}
			else
			{
				ShutdownModule(mod->ModuleID);
			}
		}
	}
}

void CMessageManager::AddSubscription(CModuleRecord *mod, MSG_TYPE message_type)
{
	MSG_TYPE mt;

	if ((mod != NULL) && (mod->uid >= 0))
	{
		if (((message_type < 0) || (message_type > MAX_MESSAGE_TYPES)) && (message_type != ALL_MESSAGE_TYPES))
		{
			// send MDF_FAIL_SUBSCRIBE instead of ACK so the module's subscribe function will fail
			MDF_FAIL_SUBSCRIBE data;
			data.mod_id = mod->ModuleID;
			data.msg_type = message_type;
			CMessage R(MT_FAIL_SUBSCRIBE, (void *)&data, sizeof(data));
			DispatchMessage(&R, mod);
			return;
		}

		switch (message_type)
		{
		case ALL_MESSAGE_TYPES:
			for (mt = 0; mt < MAX_MESSAGE_TYPES; mt++)
			{
				CSubscriberList *list = GetSubscriberList(mt);
				if (!list->IsSubscribed(mod->uid))
					list->AddSubscriber(mod->uid);
			}
			break;
		default:
			CSubscriberList *list = GetSubscriberList(message_type);
			if (!list->IsSubscribed(mod->uid))
				list->AddSubscriber(mod->uid);
		}
	}
}

void CMessageManager::RemoveSubscription(CModuleRecord *mod, MSG_TYPE message_type)
{
	// Might wanna add checks here for valid module_id, connected module
	MSG_TYPE mt;

	if ((mod != NULL) && (mod->uid >= 0))
	{
		switch (message_type)
		{
		case ALL_MESSAGE_TYPES:
			for (mt = 0; mt < MAX_MESSAGE_TYPES; mt++)
			{
				GetSubscriberList(mt)->RemoveSubscriber(mod->uid);
			}
			break;
		default:
			GetSubscriberList(message_type)->RemoveSubscriber(mod->uid);
		}
	}
}

void CMessageManager::PauseSubscription(CModuleRecord *mod, MSG_TYPE message_type)
{
	// Might wanna add checks here for valid module_id, connected module
	MSG_TYPE mt;

	switch (message_type)
	{
	case ALL_MESSAGE_TYPES:
		for (mt = 0; mt < MAX_MESSAGE_TYPES; mt++)
		{
			GetSubscriberList(mt)->PauseSubscriber(mod->uid);
		}
		break;
	default:
		GetSubscriberList(message_type)->PauseSubscriber(mod->uid);
	}
}

void CMessageManager::ResumeSubscription(CModuleRecord *mod, MSG_TYPE message_type)
{
	// Might wanna add checks here for valid module_id, connected module
	MSG_TYPE mt;

	switch (message_type)
	{
	case ALL_MESSAGE_TYPES:
		for (mt = 0; mt < MAX_MESSAGE_TYPES; mt++)
		{
			GetSubscriberList(mt)->ResumeSubscriber(mod->uid);
		}
		break;
	default:
		GetSubscriberList(message_type)->ResumeSubscriber(mod->uid);
	}
}

void CMessageManager::HandleConnect(CMessage *M, UPipe *pSourcePipe)
{
	MDF_CONNECT data;
	memset(&data, 0, sizeof(data));
	M->GetData((void *)&data);
	int prev_priority_class = GetMyPriority();
	SetMyPriority(NORMAL_PRIORITY_CLASS);
	MODULE_ID mod_id = ConnectModule(M->src_mod_id, pSourcePipe, data.logger_status, data.daemon_status);
	//printf("Connect: %d\n", mod_id);
	if (mod_id > 0)
	{
		SetMyPriority(prev_priority_class);
	}
}

void CMessageManager::HandleConnectV2(CMessage *M, UPipe *pSourcePipe)
{
	MDF_CONNECT_V2 connect_v2;
	M->GetData((void *)&connect_v2);
	int prev_priority_class = GetMyPriority();
	SetMyPriority(NORMAL_PRIORITY_CLASS);
	MODULE_ID mod_id = ConnectModuleV2(M->src_mod_id, pSourcePipe, &connect_v2);
	//printf("ConnectV2: %d\n", mod_id);
	if (mod_id > 0)
	{
		SetMyPriority(prev_priority_class);
	}
}

void CMessageManager::HandleForceDisconnect(CMessage *M)
{
	MDF_FORCE_DISCONNECT data_MDF_FORCE_DISCONNECT;
	M->GetData(&data_MDF_FORCE_DISCONNECT);
	MODULE_ID mod_id = data_MDF_FORCE_DISCONNECT.mod_id;
	ShutdownModule(mod_id);
}

void CMessageManager::HandleModuleDisconnect(CMessage *M)
{
	int prev_priority_class = GetMyPriority();
	SetMyPriority(NORMAL_PRIORITY_CLASS);
	DisconnectModule(M->src_mod_id);
	SetMyPriority(prev_priority_class);
}

void CMessageManager::HandleModuleReady(CMessage *M)
{
	MDF_MODULE_READY module_ready;
	M->GetData(&module_ready);

	CModuleRecord *mod = GetRecord(M->src_mod_id);
	if ((mod != NULL) && (mod->uid >= 0))
	{
		mod->pid = module_ready.pid;

		// Notify that the module has joined and ready
		SendHello(mod);
	}
}

void CMessageManager::HandleSubscribe(CMessage *M)
{
	MSG_TYPE msg_type_to_subscribe;
	M->GetData(&msg_type_to_subscribe);

	CModuleRecord *mod = GetRecord(M->src_mod_id);
	if ((mod != NULL) && (mod->uid >= 0))
	{
		AddSubscription(mod, msg_type_to_subscribe);
		DEBUG_TEXT_(" Added subscription to msg type " << msg_type_to_subscribe << " for module " << M->src_mod_id << "... ");
		SendAcknowledge(mod);
	}
}

void CMessageManager::HandleUnsubscribe(CMessage *M)
{
	MSG_TYPE msg_type_to_unsubscribe;
	M->GetData(&msg_type_to_unsubscribe);
	CModuleRecord *mod = GetRecord(M->src_mod_id);
	if ((mod != NULL) && (mod->uid >= 0))
	{
		RemoveSubscription(mod, msg_type_to_unsubscribe);
		SendAcknowledge(mod);
	}
}

void CMessageManager::HandlePauseSubscription(CMessage *M)
{
	MSG_TYPE msg_type_to_pause;
	M->GetData(&msg_type_to_pause);
	CModuleRecord *mod = GetRecord(M->src_mod_id);
	if ((mod != NULL) && (mod->uid >= 0))
	{
		PauseSubscription(mod, msg_type_to_pause);
		SendAcknowledge(mod);
	}
}

void CMessageManager::HandleResumeSubscription(CMessage *M)
{

	MSG_TYPE msg_type_to_resume;
	M->GetData(&msg_type_to_resume);
	CModuleRecord *mod = GetRecord(M->src_mod_id);
	if ((mod != NULL) && (mod->uid >= 0))
	{
		ResumeSubscription(mod, msg_type_to_resume);
		SendAcknowledge(mod);
	}
}

CSubscriberList *
CMessageManager::GetSubscriberList(MSG_TYPE message_type)
{
	if (message_type >= MAX_MESSAGE_TYPES || message_type < 0)
		return &m_EmptySubscriberList;
	else
		return &(m_SubscribersToMessageType[message_type]);
}

bool CMessageManager::IsModuleSubscribed(UID uid, MSG_TYPE message_type)
{
	if (message_type >= MAX_MESSAGE_TYPES || message_type < 0)
		return false;

	return GetSubscriberList(message_type)->IsSubscribed(uid);
}

void CMessageManager::SendAcknowledge(CModuleRecord *mod)
{
	if ((mod != NULL) && (mod->uid >= 0))
	{
		DEBUG_TEXT_("Sending ACK to module " << mod->ModuleID << "... ");
		DispatchSignal(MT_ACKNOWLEDGE, mod);
		DEBUG_TEXT("Sent!");
	}
}

void CMessageManager::SendIntroductions(MODULE_ID mod_id)
{
	MDF_HELLO hello;
	CModuleRecord *dest_mod = GetRecord(mod_id);
	if (dest_mod)
	{
		for (int i = 0; i < MAX_MODULES; i++)
		{
			CModuleRecord *mod = &m_ConnectedModules[i];
			if (mod->uid >= 0 && mod->ModuleID > 0)
			{		
				mod->SetHello(&hello);
				//printf("Hello: %d\n", hello.mod_id);
				m_OutMsg.Set(MT_HELLO, &hello, sizeof(hello));
				SendMessage(&m_OutMsg, dest_mod);
			}
		}
	}
}

int CMessageManager::ModuleIsConnected(MODULE_ID mod_id)
{
	if (mod_id < MID_MESSAGE_MANAGER)
		return 0;

	for (int i = 0; i < MAX_MODULES; i++)
	{
		if (m_ConnectedModules[i].ModuleID == mod_id)
		{
			return 1;
		}
	}
	return 0;
}

void CMessageManager::LogFailedMessage(CMessage *M, MODULE_ID mod_id)
{
	MDF_FAILED_MESSAGE data;
	memset(&data, 0, sizeof(data));
	data.dest_mod_id = mod_id;
	data.time_of_failure = GetAbsTime();
	memcpy(&data.msg_header, M, sizeof(RTMA_MSG_HEADER));
	CMessage F(MT_FAILED_MESSAGE, &data, sizeof(data));
	DispatchMessage(&F);
}