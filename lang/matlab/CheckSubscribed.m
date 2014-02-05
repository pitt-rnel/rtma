function CheckSubscribed( MessageType)

    global RTMA_runtime;

    if( strmatch( MessageType, RTMA_runtime.Subscribed, 'exact'))
    else
        error_message = ['MessageType "' MessageType '" not subscribed'];
        error( error_message);
    end
