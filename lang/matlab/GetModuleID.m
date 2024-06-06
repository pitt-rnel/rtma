function module_id = GetModuleID()

global RTMA;
global RTMA_runtime;
module_id = MatlabRTMA( RTMA.mex_opcode.GET_MODULE_ID);
RTMA_runtime.ModuleID = module_id;