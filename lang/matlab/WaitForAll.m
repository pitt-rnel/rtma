function varargout = WaitForAll( varargin)

% [Message1, Message2, ...] = WaitForAll( ExpectedMsgType1, ExpectedMsgType2, ...)
%
% Wait for all the expecteed message types, one and only one instance of each.
% The function also calls an event hook and checks for common exit
% messages and acts upon them. The received messages are returned as output
% arguments in the same order as the expected message type inputs. An error will
% be generated if more than one instance of any expected message type is received.

ReceivedMessageTypes = {};
for i = 1 : nargin
    M = WaitFor( varargin{:});
    if( strmatch( M.msg_type, ReceivedMessageTypes, 'exact'))
        error( 'More than one instance of the same message type received');
    end
    ReceivedMessageTypes{1,end+1} = M.msg_type;
    idx_out = strmatch( M.msg_type, varargin, 'exact');
    varargout{idx_out} = M;
end
