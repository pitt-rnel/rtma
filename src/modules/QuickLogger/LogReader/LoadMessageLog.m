function Log = LoadMessageLog( Filename, RTMA, get_full_log)

% Log = LoadMessageLog( Filename, RTMA)
%
% Loads the binary RTMA message log in Filename and converts it to a matlab 
% data structure, organized by message type, so it is easy to look at
% data associated with any particular message type.
% RTMA is a structure containing RTMA message definitions (saved from a
% matlab module at runtime when Filename was recorded.

% Meel Velliste 12/29/2008

if ~exist('get_full_log','var')
    get_full_log = true;
end

RawLog = LoadRawMessageLog( Filename, RTMA, get_full_log);
Log = OrganizeLogByMsgType( RawLog, RTMA, get_full_log);
