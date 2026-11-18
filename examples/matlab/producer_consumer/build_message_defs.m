scriptDir = fileparts(mfilename('fullpath'));
rtma_path = fileparts(fileparts(fileparts(scriptDir)));
TranslateRTMAConfigFiles2Matlab(rtma_path,[ rtma_path '/examples/matlab/producer_consumer/message_defs.h'],'message_defs');
