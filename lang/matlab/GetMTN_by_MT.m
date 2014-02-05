function MessageTypeName = GetMTN_by_MT( MessageType)

global RTMA;
MessageTypeName = RTMA.MTN_by_MT{MessageType+1};
