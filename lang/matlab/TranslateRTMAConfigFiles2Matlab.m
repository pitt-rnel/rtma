function TranslateRTMAConfigFiles2Matlab( RTMA_BaseDir, MessageConfigFile, OutputFileName)
% TranslateRTMAConfigFiles2Matlab( RTMA_BaseDir, MessageConfigFile)
%
% Translates RTMA_config.h and associated
% h files to Matlab saves the result in a mat file
% with the same base file name as the input MessageConfigFile.
%
% RTMA Base directory (RTMA_BaseDir) needs to be specified so that it can find the core
% definition files. MessageConfigFile specifies the application-specific
% message configuration file (e.g. '../../Source/RTMA_config.h').

[ConfigFileDir, ConfigFileBaseName] = fileparts( MessageConfigFile);

if(isempty(ConfigFileDir))
  ConfigFileDir = '.';
end

% OutputFile = [ConfigFileDir '/' ConfigFileBaseName '.mat'];
%OutputFile = [ConfigFileDir '\..\..\..\include\RTMA_config.mat'];
if exist('OutputFileName','var') && ~isempty(OutputFileName)
    OutputFile = fullfile(ConfigFileDir,[OutputFileName '.mat']);
else
    OutputFile = fullfile(ConfigFileDir,'RTMA_config.mat');
end
RTMA = ReadRTMAConfigFiles( RTMA_BaseDir, MessageConfigFile);
save( OutputFile, 'RTMA');
