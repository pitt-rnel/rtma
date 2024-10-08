%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% make.m - Builds the matlab wrapper for the RTMA interface. Note that this script
%          re-compiles everything from source rather than using the pre-compiled
%          RTMA lib or dll file. This is necessary because it malloc and new 
%          calls need to be wrapped to use the Matlab memory manager (see mex_malloc.c and mex_malloc.cpp in src/core)
%
% MV 4/25/2011

if( ~ispc && ~isunix)
    error( 'Unsupported platform');
end

% base_dir = '../..';
base_dir = fullfile(fileparts(mfilename('fullpath')), '..', '..');
core_dir = fullfile(base_dir, 'src', 'core');
pipelib_dir = fullfile(core_dir, 'PipeLib');

core_sources = [fullfile(core_dir,'RTMA.cpp'), ' ' fullfile(core_dir,'MyCException.cpp'), ' ', fullfile(core_dir,'MyCString.cpp'),' ', fullfile(core_dir,'mex_hack.cpp'), ' '];
pipelib_sources = [fullfile(pipelib_dir,'UPipe.cpp'), ' ', fullfile(pipelib_dir,'SocketPipe.cpp'), ' ', fullfile(pipelib_dir,'Timing.cpp'), ' '];

sources = [fullfile(base_dir,'lang','matlab','MatlabRTMA.cpp'),' ', core_sources, pipelib_sources];
options = ['-v -D_MEX_FILE_ '];
include_dirs = ['-I' fullfile(base_dir, 'include'),' -I', fullfile(base_dir,'include','internal'), ' '];
libs = [''];

if( ispc)
    libs = [libs 'ws2_32.lib '];
elseif( isunix)
    options = [options '-DUSE_LINUX '];
end

cmd = ['mex ' options include_dirs sources libs]
eval( cmd);
