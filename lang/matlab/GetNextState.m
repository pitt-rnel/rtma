function state = GetNextState( event)

% state = GetNextState
%
% Gets the next state from a global event map

global RTMA_runtime;

try
    state = RTMA_runtime.EventMap.(event);
catch me
    error( 'Could not get next state');
end
