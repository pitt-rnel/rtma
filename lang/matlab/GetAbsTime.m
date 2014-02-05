function timestamp = GetAbsTime

global RTMA;
timestamp = MatlabRTMA( RTMA.mex_opcode.GET_TIME);
