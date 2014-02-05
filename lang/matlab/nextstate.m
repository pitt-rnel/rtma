function nextstate( state, message)

% nextstate( state)
%
% Sets the next state to STATE unconditionally, so that the next call
% to GetNextState will return this state.

global RTMA_runtime;

try

    if( ~exist( 'message', 'var'))
        message = [];
    end
    
    if( ischar( state))
        RTMA_runtime.EventMap = {state, message};
    else
        error( 'The input argument to nextstate should be a string');
    end

catch 
    error( 'Error in setting next state');
end
