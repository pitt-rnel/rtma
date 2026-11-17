function Message = ReadMessage( arg)

% Message = ReadMessage( timeout)
% Message = ReadMessage( blocking_or_not)
%
% Tries to read a message from RTMA. TIMEOUT is a how long
% (in seconds) we wait for the message before timing out. If timeout
% is -1, then wait forever (i.e. blocking call). If timeout is 0
% then check for message and return immediately (i.e. non-blocking).
% Alternatively, 'blocking' or 'non-blocking' can be specified as
% a string argument.
debug = 0;

global RTMA;

if( nargin < 1)
    timeout = -1; % Blocking call
    blocking = true;
else
    if( ischar( arg))
        switch( arg)
            case 'blocking', blocking = true; timeout = -1;
            case 'non-blocking', blocking = false; timeout = 0;
            otherwise, error( 'The blocking_or_not argument to ReadMessage should be either ''blocking'' or ''non-blocking''');
        end
    else
        % By default, input argument is a timeout value in seconds
        timeout = arg;
        if( timeout == -1)
            blocking = true;
        else
            blocking = false;
        end
    end
end

if debug;   fprintf('Reading header...'); end  %#ok<*UNRCH>

% Read message headers until one of a type the loaded definitions define.
% A message of another type can't be decoded, so it is discarded with a
% warning, once per type, and reading goes on with the time that is left.
start = tic;
while( true)
    if( blocking) % If infinitely blocking, then keep doing reads with timeout to allow Ctrl-C
        Message = [];
        while( isempty( Message))
            Message = MatlabRTMA( RTMA.mex_opcode.READ_MESSAGE_HDR, RTMA.MESSAGE_HEADER, .2);
        end
    else % If non-blocking or specified timeout, then use timeout value directly
        Message = MatlabRTMA( RTMA.mex_opcode.READ_MESSAGE_HDR, RTMA.MESSAGE_HEADER, timeout);
    end
    if( isempty( Message)), break; end

    MessageTypeName = GetMTN_by_MT( Message.msg_type);
    if( ~isempty( MessageTypeName)), break; end

    WarnUnknownType( Message.msg_type);
    Message = [];
    if( ~blocking)
        timeout = max( 0, timeout - toc( start));
        start = tic;
        if( timeout == 0), break; end
    end
end

if debug;   fprintf('done\n'); end

if( isempty( Message))
    Message = []; % Just in case MatlabRTMA returns a different kind of empty
else
    
    if debug,   fprintf('Message found...'), end
    
    % If there is data in the message, then read it
    if( Message.is_dynamic )
       Message.data = MatlabRTMA( RTMA.mex_opcode.READ_MESSAGE_DD);
    elseif( Message.num_data_bytes > 0)
        DataTemplate = GetMDF_by_MT( Message.msg_type);
        if( ischar( DataTemplate) && strncmp( 'VARIABLE_LENGTH_ARRAY', DataTemplate, 21))
            Message.data = DataTemplate;
        else
            Message.data = MatlabRTMA( RTMA.mex_opcode.READ_MESSAGE_DATA, DataTemplate);
        end
    else
        Message.data = [];
    end

    if debug,   fprintf('data transfered...'), end
    
    % Replace numeric Message Type ID with its string Message Type Name
    Message.msg_type = MessageTypeName;
    if debug,   fprintf('done\n'), end
end


function WarnUnknownType( msg_type)

persistent warned;
if( isempty( warned)), warned = []; end
if( ~any( warned == msg_type))
    warned(end+1) = msg_type;
    warning( 'ReadMessage:UnknownMessageType', ...
        ['ReadMessage: discarding a message of type %d, which the loaded ' ...
         'message definitions don''t define. Further messages of this type ' ...
         'are discarded without a warning.'], msg_type);
end
