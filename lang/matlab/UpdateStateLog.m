function UpdateStateLog( StateName, EntryTime)

% UpdateStateLog( StateName, EntryTime)
%
% Called by EventLoop. Adds StateName, and the time when the state starts
% to a global log that can be saved later.
% 
% MV & SP 2/13/2007

    global STATE_LOG;

    if( ~isempty( STATE_LOG))
        if( STATE_LOG.Index < length( STATE_LOG.StateNum))
            state_num = strmatch( StateName, STATE_LOG.StateNumMap);
            if( isempty( state_num))
                STATE_LOG.StateNumMap(end+1,1) = {StateName};
                state_num = length( STATE_LOG.StateNumMap);
            end
            STATE_LOG.Index = STATE_LOG.Index + 1;
            STATE_LOG.StateNum(1,STATE_LOG.Index) = state_num;
            STATE_LOG.EntryTime(1,STATE_LOG.Index) = EntryTime;
        end
    end
    