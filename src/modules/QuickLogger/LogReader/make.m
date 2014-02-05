function make()
% make
%
% Builds mex file for reading binary message logs.
base_dir = '../../../../..'
if( isunix)
    options = '-D_MEX_FILE_ -DUSE_LINUX';
else
    options = '-D_MEX_FILE_';
end
options = [options ' -I' base_dir '/include' ' -I' base_dir '/src' ' -I' base_dir ' -I..'];

aFiles = [base_dir '/Util/MyCException.cpp ' base_dir '/Util/MyCString.cpp'];

cmd = ['mex ' options ' LogReader.cpp ' aFiles]
eval( cmd);
