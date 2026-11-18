function MessageTypeName = GetMTN_by_MT( MessageType)

% MessageTypeName = GetMTN_by_MT( MessageType)
%
% Returns the name of a numeric message type, or '' if the loaded message
% definitions don't define it.

global RTMA;
index = MessageType + 1;
if( index >= 1 && index <= numel( RTMA.MTN_by_MT) && ischar( RTMA.MTN_by_MT{index}))
    MessageTypeName = RTMA.MTN_by_MT{index};
else
    MessageTypeName = '';
end
