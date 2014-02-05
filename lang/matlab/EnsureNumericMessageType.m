function MessageType = EnsureNumericMessageType( MessageType)

    % If Messagetype is a string, converts it to a numeric message type ID
    % based on the lookup table in the RTMA structure

    global RTMA;

    if( ischar( MessageType))
        if( isfield( RTMA.MT, MessageType))
            MessageType = RTMA.MT.(MessageType);
        else
            error( ['Unrecognized MessageType: ' MessageType]);
        end
    end
