function state_name = GetCurrentState

% Get the name of current state machine state

global RTMA_runtime;

if( ~isfield( RTMA_runtime, 'EventLoop_CurrentState'))
    state_name = ''; % Make sure we always return a string (because EventLoop_CurrentState could be empty double matrix if uninitialized)
    return;
end
if( isempty( RTMA_runtime.EventLoop_CurrentState))
    state_name = '';
    return;
end

state_name = RTMA_runtime.EventLoop_CurrentState{end};
