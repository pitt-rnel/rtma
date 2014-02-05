function DisconnectFromMMM

global RTMA;
global RTMA_runtime;

if( ~isempty( RTMA))
    MatlabRTMA( RTMA.mex_opcode.DISCONNECT_FROM_MMM);
    RTMA_runtime.Connected = false;
end
