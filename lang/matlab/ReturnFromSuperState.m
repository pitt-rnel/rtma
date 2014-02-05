function ReturnFromSuperState( NextState)

global RTMA_runtime;
if( exist( 'NextState', 'var'))
    RTMA_runtime.EventMap = {'ReturnFromSuperState', NextState};
else
    RTMA_runtime.EventMap = {'ReturnFromSuperState', []};;
end
