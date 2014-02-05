function MessageData = ReadMessageData( DataTemplate)

    global RTMA;
    MessageData = MatlabRTMA( RTMA.mex_opcode.READ_MESSAGE_DATA, DataTemplate);
