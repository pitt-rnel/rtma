function M = CheckForMessage( varargin)

% M = CheckForMessage( ExpectedMessageType1, ExpectedMessageType2, ...)
%
% Check if there is a message in the module's input pipe. If there is
% and it is one of the expected types, then return it. The function also
% calls an event hook and checks for common exit messages and acts upon them.


  % Verify that the requested message_types exist
    for i = 1 : nargin
        CheckMessageTypeExist( varargin{i});
        CheckSubscribed( varargin{i});
    end
    
    M = ReadMessage( 'non-blocking');
    if( ~isempty( M))
        M = PreprocessMessage( M, varargin);
    end
