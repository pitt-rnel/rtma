function DumpRTMAInfo( RTMA_BaseDir, MessageConfigFile)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% DumpRTMAInfo( RTMA_BaseDir, MessageConfigFile)
%
%   Connects to MMM and dumps the entire RTMA struct as structured text
%   file
%   C modules can read the RTMA struct as DD, and make use of it
%
%   Sagi Perel
%   11/21/2006, University of Pittsburgh


%
% Initialization
%
addpath ../../MatlabCommon

RTMA = ReadRTMAConfigFiles(RTMA_BaseDir, MessageConfigFile);
SaveTextData('../RTMA_config_dump.txt', 'RTMA');
%SaveDD('../RTMA_config_dump.txt', 'RTMA');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
exit