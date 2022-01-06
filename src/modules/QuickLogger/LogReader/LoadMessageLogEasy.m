function Log = LoadMessageLogEasy( Filename)

% Log = LoadMessageLog( Filename, RTMA)
%
% Loads the binary RTMA message log in Filename and converts it to a matlab 
% data structure, organized by message type, so it is easy to look at
% data associated with any particular message type.
% RTMA is a structure containing RTMA message definitions (saved from a
% matlab module at runtime when Filename was recorded.

% Meel Velliste 12/29/2008
%App_Basedir= getenv('ROBOTAPP');


%load([App_Basedir '/Common/include/RTMA_config.mat']);
RTMA = LoadRtmaConfig; % This is a CLIMBER dependency

[RawLog, ignorelist] = LoadRawMessageLog( Filename, RTMA, true);
Log = OrganizeLogByMsgType( RawLog, RTMA, ignorelist);
