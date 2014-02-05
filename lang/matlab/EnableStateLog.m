function EnableStateLog( max_num_states)

% EnableStateLog( max_num_states)
%
% Enable logging of states and their entry times

    global STATE_LOG;

    STATE_LOG.StateNumMap = {};
    STATE_LOG.StateNum = nan( 1, max_num_states);
    STATE_LOG.EntryTime = nan( 1, max_num_states);
    STATE_LOG.Index = 0;
