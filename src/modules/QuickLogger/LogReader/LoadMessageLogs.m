function BigLog = LoadMessageLogs( DirName, FileNames, RTMA, get_full_log)

% BigLog = LoadMessageLogs( DirName, FileNames, RTMA)
%
% Loads the binary RTMA message logs for each file name in the FileNames
% cell array (where these files are in the directory DirName) and converts
% them to a matlab data structure, organized by message type, so it is easy
% to look at data associated with any particular message type.
% RTMA is a structure containing RTMA message definitions (saved from a
% matlab module at runtime when message logs were recorded.

% Meel Velliste 12/29/2008

if ~exist('get_full_log','var')
    get_full_log = true;
end

    % If there is a slash at the end of DirName, remove it, so that the
    % code below can treat the directory name in a uniform manner
    if( DirName(end) == '/' || DirName(end) == '\')
        DirName(end) = [];
    end

    %BW: Arrange in chronological order first:
    for a = 1:length(FileNames)
        f = dir(fullfile(DirName,FileNames{a}));
        timestamp(a) = f.datenum;
    end
    [v idx] = sort(timestamp);
    FileNames = FileNames(idx);
    
    % Process all input files and gather individual message logs
    % into an array of message logs
    Logs = [];
    LastSequenceNo = 0;
    for i = 1 : length( FileNames)
        % Show progress indicator
        counter('%d/%d',i,length(FileNames));
        % Load message log from the binary file
        input_file = FileNames{i};
        input_file_path = [DirName '/' input_file];
        Log = LoadMessageLog(input_file_path, RTMA, get_full_log);
        % Offset message sequence numbers so that they form one continuous
        % sequence in the concatenated log (instead of starting over from 1
        % for each file)
        PrevLastSequenceNo = LastSequenceNo;
        [Log.SequenceNo, LastSequenceNo] = OffsetSequenceNos( Log.SequenceNo, LastSequenceNo);
        % Create an index that allows us to track which file each message
        % came from
        Log.FileIndex = CreateFileIndex( Log.SequenceNo, i);
        Log.FileName = {[DirName '/' input_file]};
        Log.SequenceNumRange = [PrevLastSequenceNo+1 LastSequenceNo]';  
        
        %IGNORE LARGE FIELDS WE DON'T OFTEN NEED:
%         if ~get_full_log
%             ignorelist = {'SPIKE_SNIPPET','RAW_SPIKECOUNT','RAW_CTSDATA','PLAYSOUND','TIMING_MESSAGE'};
%             fields = fieldnames(Log.Data);
%             has = find(ismember(ignorelist,fields));
%             for b = has
%                 Log.Data = rmfield(Log.Data,ignorelist(b));
%             end
%         end
        
        % Put log into a big array of logs
        Logs = [Logs Log];
    end

    % Concatenate the fields in all the logs, so it becomes
    % a single log (a single struct where the fields at the
    % deepest level are concatenated)


    
    if ~isempty(Logs)
        BigLog = CatStructFields( Logs, 'horizontal', 'merge-fields');
    end
      

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function Index = CreateFileIndex( Template, FileNo)

    Index = Template;
    MsgNames = fieldnames( Index);
    for i = 1 : length( MsgNames)
        Index.(MsgNames{i})(:) = FileNo;
    end
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [SeqNos, LastSeqNo] = OffsetSequenceNos( SeqNos, LastSeqNo)
    
    MsgNames = fieldnames( SeqNos);
    last_seq_no = 0;
    for i = 1 : length( MsgNames)
        msg_name = MsgNames{i};
        lsn = SeqNos.(msg_name)(end); % Last sequence number of current message type
        % Look for the last sequence number locally in the current log
        if( lsn > last_seq_no)
            last_seq_no = lsn;
        end
        % Increment sequence numbers by the global last sequence number, so
        % that the current log continues where the previous one left off
        SeqNos.(msg_name) = SeqNos.(msg_name) + LastSeqNo;
    end
    % Increment the global last sequence number by the local one, so that
    % the next log may continue where this one left off
    LastSeqNo = LastSeqNo + last_seq_no;
    