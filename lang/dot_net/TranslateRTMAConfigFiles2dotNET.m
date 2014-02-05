function TranslateRTMAConfigFiles2dotNET( RTMA_BaseDir, MessageConfigFile)
% TranslateRTMAConfigFiles2dotNET( RTMA_BaseDir, MessageConfigFile)
%
% Translates RTMA_config.h and associated
% h files to C# and other .NET languages.
%
% RTMA Base directory (RTMA_BaseDir) needs to be specified so that it can find the core
% definition files. MessageConfigFile specifies the application-specific
% message configuration file (e.g. '../../Source/RTMA_config.h').

    this_file_path = mfilename( 'fullpath');
    this_dir_path = fileparts( this_file_path);
    PATH = {[this_dir_path '/../matlab']};

    addpath( PATH{:});
    
    [ConfigFileDir, ConfigFileBaseName] = fileparts( MessageConfigFile);
    if(isempty(ConfigFileDir))
      ConfigFileDir='.';
    end
    ConfigFile_BasePath = [ConfigFileDir '/' ConfigFileBaseName];
    Output_Namespace = 'RTMA';
    TranslateRTMAhFiles2dotNET( RTMA_BaseDir, ConfigFile_BasePath, Output_Namespace);

    rmpath( PATH{:});
