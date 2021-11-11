function OrganizedLog = OrganizeLogByMsgType(LinearLog, RTMA, get_full_log)

% OrganizedLog = OrganizeLogByMsgType( LinearLog, RTMA)
%
% Organizes the linear message log LinearLog into a structure by message
% type.

% Meel Velliste 12/23/2008
    
    % CMG 11/11/21 Use same ignorelist function as LoadMessageLog
    if ~exist('get_full_log','var')
        get_full_log = true;
    elseif iscell(get_full_log) % CMG 11/11/21 Allow custom ignore lists
        ignorelist = get_full_log;
        get_full_log = false;
    elseif islogical(get_full_log)
        if ~get_full_log
            ignorelist = {'SPIKE_SNIPPET','REJECTED_SNIPPET','RAW_DIGITAL_EVENT','RAW_SPIKECOUNT','PLAYSOUND','TIMING_MESSAGE'};
        end
    end

    %IGNORE LARGE FIELDS WE DON'T OFTEN NEED: Prep ignore list
    ignorenums = [];
    if ~get_full_log
        badentries = cellfun(@isempty,RTMA.MTN_by_MT);
        badentries = find(~badentries);
        for a = 1:length(ignorelist)
           t = find(ismember(RTMA.MTN_by_MT(badentries),ignorelist{a}));
           if ~isempty(t)
               ignorenums(end+1) = badentries(t)-1;
           end
        end
    end

    % Initialize the output structure
    OrganizedLog = [];
    OrganizedLog.Headers = [];
    OrganizedLog.Data    = [];
    OrganizedLog.SequenceNo = [];
    % Find the unique message types present in the log
    MT = [LinearLog.Headers.msg_type];
    unique_MT = unique( MT);
    % Iterate over message types
    for i = 1 : length( unique_MT)
        % For each message type, gather all the data for that type into a
        % field in the output struct
        mt = unique_MT(i);
        if ismember(mt, ignorenums)
           continue 
        end
        mt_name = RTMA.MTN_by_MT{mt+1};
        mt_data_format = RTMA.MDF_by_MT{mt+1};
        mt_mask = (MT == mt);
        OrganizedLog.Headers.(mt_name) = CatStructFields( LinearLog.Headers(mt_mask), 'horizontal');
        OrganizedLog.Data.(mt_name)    = GatherData( LinearLog.Data(mt_mask), mt_data_format, mt_name);
        OrganizedLog.SequenceNo.(mt_name) = find( mt_mask);
    end
    

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Gather data from cell array where each element is known to be data from
% a certain type of message, into a:
% 1) numeric array, if data is numeric
% 2) a single struct if data elements are struct
function DataOut = GatherData( DataIn, MessageDataFormat, MessageTypeName)

    % If there is no message data format defined, then there should not be
    % any data. If there is data, issue a warning and treat it as variable
    % length data, i.e. put it in a cell array
    if( isempty( MessageDataFormat))
        % Check if all elements are empty
        all_empty = true;
        for i = 1 : length( DataIn)
            if( ~isempty(DataIn{i})), all_empty = false; break; end
        end
        if( all_empty)
            DataOut = zeros( 0, length(DataIn)); % An empty matrix with the size of the second dimension representing the number of messages
        else
            DataOut = DataIn;
            warning( 'OrganizeLogByMsgType:MessageShouldNotHaveData', ['Found data in a ' MessageTypeName ' message whose format definition says there should not be any']);
        end
        return
    end
    
    % If the message data format specifies a variable length array, then
    % leave the data as is
    if( ischar( MessageDataFormat) && strmatch( 'VARIABLE_LENGTH_ARRAY', MessageDataFormat))
        DataOut = DataIn;
        return
    end
    
    % If it is regular data with a fixed format definition, then
    % concatenate to a regular array, or if a struct, then concatenate
    % fields recursively
    element = DataIn{1};
    switch( class( element))
        case 'struct'
            % If elements are struct, presumably they are all exactly the
            % same, so try concatenating to struct array
            try
                StructArray = [DataIn{:}];
            catch
            me = lasterror();
                switch me.identifier
                    case 'MATLAB:catenate:structFieldBad', throw( MException( 'OrganizeLogByMsgType:StructFieldMismatch', 'Structure fields inconsistent while concatenating data across messages'));
                    otherwise, rethrow( me);
                end
            end
            DataOut = CatStructFields( StructArray, 'vertical', 'transpose');
        otherwise
            % Otherwise elements must be numeric or character matrices or
            % something.
            try
                DataOut = cat( 1, DataIn{:})';
            catch
            me = lasterror();
                switch me.identifier
                    case 'MATLAB:catenate:dimensionMismatch', throw( MException( 'OrganizeLogByMsgType:DimensionMismatch', 'Dimension mismatch in concatenating data across messages'));
                    otherwise, rethrow( me);
                end
            end
    end
