function StateLog = GetStateLog

% StateLog = GetStateLog()
%
% Returns the internal Matlab RTMA state log that keeps state transitions
% and times.
%
% MV & SP 2/13/2007

    global STATE_LOG;

    if( isempty( STATE_LOG))
        error( 'GetStateLog: State log has not been initialized');
    end

    StateLog = STATE_LOG;
    StateLog.StateNum(STATE_LOG.Index+1:end) = [];
    StateLog.EntryTime(STATE_LOG.Index+1:end) = [];
