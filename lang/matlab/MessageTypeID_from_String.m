function MessageTypeID = MessageTypeID_from_String( MessageTypeString)

    global RTMA;

    switch( class( MessageTypeString))
        case 'char'
            if( isfield( RTMA.MT, MessageTypeString))
                MessageTypeID = RTMA.MT.(MessageTypeString);
            else
                error( ['Unrecognized MessageType: ' MessageTypeString]);
            end
        otherwise
            error( 'MessageType expected to be a string value');
    end
