function ConnectToMMM( ModuleID, Name, MessageConfig, varargin)

% ConnectToMMM( ModuleID, Name, MessageConfig, option1, option2, ...)
%
% Connects this MATLAB session to an RTMA message manager as a module.
%
% ModuleID specifies the numeric ID by which this module will be known to
% RTMA, or 0 to be given a dynamic ID. ModuleID can optionally be a string
% if a definition for that string exists in the message definitions.
%
% Name is the module's name, which the message manager announces in HELLO
% and GOODBYE messages; at most MAX_NAME_LEN - 1 (31) characters are kept.
% [] or '' gives no name. This argument used to be unused, and a number
% there is still ignored.
%
% MessageConfig gives the message definitions, the RTMA structure, as one
% of:
%   - the structure itself, such as the one returned by a definitions
%     function that pyrtma's compiler writes (python -m pyrtma.compile
%     --matlab), for example ConnectToMMM( 0, [], my_defs())
%   - such a function, as a function handle (@my_defs) or by name
%     ('my_defs', 'my_package.message_defs' or 'C:\defs\my_defs.m')
%   - the name of a MAT file containing an RTMA structure, as
%     TranslateRTMAConfigFiles2Matlab writes ('message_defs.mat')
% A name that is also a MAT file, with or without .mat, is loaded as one.
%
% Options are strings of the form '-optionname optionvalue', or the option
% name followed by its value as the next argument. The following options
% have been defined:
% '-logger' specifies that this module will receive all messages without
%           even subscribing to any of them.
% '-server_name hostname:port' specifies that the MessageManager to connect
%                              to is not on the localhost but rather on the
%                              specified IP and port.
%
% Examples:
%   ConnectToMMM( 0, [], 'message_defs.mat')
%   ConnectToMMM( 0, 'controller', my_defs(), '-server_name 192.168.1.10:7111')
%   ConnectToMMM( 'CONTROLLER', 'controller', @my_defs, '-server_name', server)

global RTMA;
global RTMA_runtime;

% Load the definitions before disconnecting, so a bad MessageConfig leaves
% the current connection as it is.
NewRTMA = LoadMessageDefinitions( MessageConfig);

% If input argument is a string, convert it to numeric Module ID
if( ischar( ModuleID) || isstring( ModuleID))
    ModuleID = char( ModuleID);
    if( isfield( NewRTMA.MID, ModuleID))
        ModuleID = NewRTMA.MID.(ModuleID);
    else
        error( ['Unrecognized ModuleID: ' ModuleID]);
    end
end

if( isstring( Name)), Name = char( Name); end
if( ischar( Name))
    ModuleName = Name;
elseif( isempty( Name) || isnumeric( Name))
    ModuleName = '';
else
    error( 'Name must be a string, or [] for no name');
end

% Process the options
logger_status = 0;
ServerName = '';
i = 1;
while( i <= length( varargin))
    option = varargin{i};
    if( isstring( option)), option = char( option); end
    if( ~ischar( option)), error( 'Option arguments must be strings'); end
    option = strtrim( option);
    [option_name, option_value] = strtok( option);
    option_value = strtrim( option_value);
    needs_value = strcmp( option_name, '-server_name');
    if( needs_value && isempty( option_value) && i < length( varargin))
        % The value is the next argument
        i = i + 1;
        option_value = varargin{i};
        if( isstring( option_value)), option_value = char( option_value); end
        if( ~ischar( option_value)), error( ['The value of ' option_name ' must be a string']); end
    end
    switch( option_name)
        case '-logger', logger_status = 1;
        case '-server_name'
            if( any( isspace( option_value)))
                error( '-server_name option must be specified with a server name in the form hostname:portnumber');
            end
            ServerName = option_value;
        otherwise, error( ['Unknown option name "' option_name '"']);
    end
    i = i + 1;
end

DisconnectFromMMM;
clear MatlabRTMA;

RTMA = NewRTMA;
RTMA_runtime = [];

status = MatlabRTMA( RTMA.mex_opcode.CONNECT_TO_MMM, ModuleID, ServerName, logger_status, ModuleName);
if( status == 0); error( 'Could not connect to MessageManager'); end

% Initialize RTMA runtime variables. The module ID is the one connected
% with, which the message manager chose if ModuleID was 0.
RTMA_runtime.ModuleID = GetModuleID();
RTMA_runtime.Name = ModuleName;
RTMA_runtime.Connected = true;
RTMA_runtime.Subscribed = {};
RTMA_runtime.Paused = {};


function defs = LoadMessageDefinitions( MessageConfig)

if( isstruct( MessageConfig))
    defs = MessageConfig;
elseif( isa( MessageConfig, 'function_handle'))
    defs = MessageConfig();
elseif( ischar( MessageConfig) || isstring( MessageConfig))
    config = char( MessageConfig);
    [folder, name, ext] = fileparts( config);
    if( strcmpi( ext, '.mat') || isfile( [config '.mat']) || ...
            (isfile( config) && ~strcmpi( ext, '.m')))
        % A MAT file containing an RTMA structure
        loaded = load( config, '-mat');
        if( ~isfield( loaded, 'RTMA'))
            error( ['ConnectToMMM: ' config ' does not contain an RTMA structure']);
        end
        defs = loaded.RTMA;
    elseif( strcmpi( ext, '.m'))
        % A definitions function file, by its path
        if( ~isempty( folder))
            previous = cd( folder);
            restore = onCleanup( @() cd( previous));
        end
        defs = feval( name);
    else
        % A definitions function on the path, such as my_defs or
        % my_package.message_defs
        defs = feval( config);
    end
else
    error( 'ConnectToMMM: MessageConfig must be an RTMA structure, a function returning one, or a MAT file name');
end

if( ~isstruct( defs) || ~isfield( defs, 'mex_opcode') || ~isfield( defs, 'MT'))
    error( 'ConnectToMMM: MessageConfig did not give an RTMA structure of message definitions');
end
