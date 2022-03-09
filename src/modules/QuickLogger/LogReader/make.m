function make()
% make
%
% Builds mex file for reading binary message logs.
base_dir = getenv('RTMA');
if( isunix)
    options = '-D_MEX_FILE_ -DUSE_LINUX';
else
    options = '-D_MEX_FILE_';
end
options = [options ' -I' base_dir '/include' ' -I' base_dir '/include/internal' ' -I' base_dir '/src' ' -I' base_dir '/src/core' ' -I' base_dir ' -I..'];

aFiles = [base_dir '/src/core/MyCException.cpp ' base_dir '/src/core/MyCString.cpp ' base_dir '/src/core/mex_hack.cpp'];

cmd = ['mex ' options ' LogReader.cpp ' aFiles]
eval( cmd);
