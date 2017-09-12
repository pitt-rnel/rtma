function send_time = LessSafeSendMessage(MT, Data)
% send_time = LessSafeSendMessage(MT, Data)
% Less Safe (but faster) SendMessage (safer than UnsafeSendMessage). 
% MT can be a number or string.
% Data is not checked for correctness.

global RTMA;

% If MessageType is a string, convert it to numeric Message Type ID
MT  = EnsureNumericMessageType( MT);

[status, send_time, msg_count] = MatlabRTMA(RTMA.mex_opcode.SEND_MESSAGE, MT, Data, 0, 0);
if( status == 0) error( 'Could not send message'); end