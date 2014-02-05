function MessageDataFormat = GetMDF_by_MT( MessageType)

global RTMA;
MessageDataFormat = RTMA.MDF_by_MT{MessageType+1};
