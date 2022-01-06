function [Log, IgnoreList] = LoadMessageLog( Filename, RTMA, get_full_log)

% [Log, IgnoreList] = LoadMessageLog( Filename, RTMA, [get_full_log])
%
% Loads the binary RTMA message log in Filename and converts it to a matlab 
% data structure, organized by message type, so it is easy to look at
% data associated with any particular message type.
% RTMA is a structure containing RTMA message definitions (saved from a
% matlab module at runtime when Filename was recorded.
%
% optional input get_full_log: logical value will skip loading from a
% default set of messages to ignore when set to false. Can also be a cell
% array of message types to ignore.

% Meel Velliste 12/29/2008
% CG and JW 2022

if ~exist('get_full_log','var')
    get_full_log = true;
end

[RawLog, IgnoreList] = LoadRawMessageLog(Filename, RTMA, get_full_log);
Log = OrganizeLogByMsgType( RawLog, RTMA, IgnoreList);
