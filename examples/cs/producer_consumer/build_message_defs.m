rtma_path = fileparts(fileparts(fileparts(getMyPath)));
header_file = fullfile(rtma_path,'examples','cs','producer_consumer','message_defs.h');
TranslateRTMAConfigFiles2dotNET(rtma_path,header_file);
