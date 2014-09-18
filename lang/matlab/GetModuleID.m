function module_id = GetModuleID()

global RTMA;
module_id = MatlabRTMA( RTMA.mex_opcode.GET_MODULE_ID);
