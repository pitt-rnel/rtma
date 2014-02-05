function ConnectToMMM( ModuleID, Reserved, MessageConfigFile, varargin)

% ConnectToMMM( ModuleID, Reserved, MessageConfigFile, option1, option2, ...)
%
% ModuleID specifies the numeric ID by which this module will be know to
% RTMA. ModuleID can optionally be a string if a definition for that
% string exists in the MessageConfigFile. MessageConfigFile specifies the
% name of a MAT file that contains an RTMA structure containing message
% definitions, module ID definitions etc. Reserved is an argument that
% is there for backward compatibility. Its value does not matter. Options
% are strings of the form '-optionname optionvalue'. The following options
% have been defined:
% '-logger' specifies that this module will receive all messages without
%           even subscribing to any of them.
% '-server_name hostname:port' specifies that the MessageManager to connect
%                              to is not on the localhost but rather on the
%                              specified IP and port.

DisconnectFromMMM;
clear MatlabRTMA;

global RTMA;
global RTMA_runtime;
RTMA = [];
RTMA_runtime = [];

load( MessageConfigFile, '-mat'); % MessageConfigFile is expected to contain an RTMA structure

% Need an IsConnected function
% Then we can give a proper error message when you try to connect
% again if already connected

% If input argument is a string, convert it to numeric Module ID

if( ischar( ModuleID))
    if( isfield( RTMA.MID, ModuleID))
        ModuleID = getfield( RTMA.MID, ModuleID);
    else
        error( ['Unrecognized ModuleID: ' ModuleID]);
    end
end

% Process the options
logger_status = 0;
ServerName = '';
for i = 1 : length( varargin)
    option = varargin{i};
    if( ~ischar( option)), error( 'Option arguments must be strings'); end
    [starts,ends,extents,matches] = regexp( option, '\S+');
    option_name = matches{1};
    option_values = matches(2:end);
    switch( option_name)
        case '-logger', logger_status = 1;
        case '-server_name'
            if( length( option_values) ~= 1), error( '-server_name option must be specified with a server name in the form hostname:portnumber'); end
            ServerName = option_values{1};
        otherwise, error( ['Unknown option name "' option_name '"']);
    end
end

status = MatlabRTMA( RTMA.mex_opcode.CONNECT_TO_MMM, ModuleID, ServerName, logger_status);
if( status == 0) error( 'Could not connect to MessageManager'); end

% Initialize RTMA runtime variables
RTMA_runtime.ModuleID = ModuleID;
RTMA_runtime.Connected = true;
RTMA_runtime.EventLoop_CurrentState = {};
RTMA_runtime.StateTimeout_TimerID = [];
RTMA_runtime.Subscribed = {};
RTMA_runtime.Paused = {};
%RTMA_runtime.EventMap = [];
