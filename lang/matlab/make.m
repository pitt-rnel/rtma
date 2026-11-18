%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% make.m - Builds the matlab wrapper for the RTMA interface. Note that this script
%          re-compiles everything from source rather than using the pre-compiled
%          RTMA lib or dll file. This is necessary because it malloc and new 
%          calls need to be wrapped to use the Matlab memory manager (see mex_malloc.c and mex_malloc.cpp in src/core)
%
%          The client logger uses the fmt library, compiled here header-only.
%          CMake downloads fmt into build/cmake/_deps/fmt-src when it builds
%          the repository (make.sh or build_msvc_2026.bat), and this script
%          uses that copy, so build the repository first. To use another copy,
%          set the environment variable RTMA_FMT_INCLUDE to its include folder,
%          the one that contains fmt/format.h.
%
%          The mex file is written to lang/matlab, wherever this is run from.
%
% MV 4/25/2011

if( ~ispc && ~isunix)
    error( 'Unsupported platform');
end

base_dir = fullfile(fileparts(mfilename('fullpath')), '..', '..');
core_dir = fullfile(base_dir, 'src', 'core');
pipelib_dir = fullfile(core_dir, 'PipeLib');

fmt_include = getenv('RTMA_FMT_INCLUDE');
if( isempty( fmt_include))
    fmt_include = fullfile(base_dir, 'build', 'cmake', '_deps', 'fmt-src', 'include');
end
if( ~isfile( fullfile( fmt_include, 'fmt', 'format.h')))
    error( ['fmt not found in ' fmt_include '. Build the repository with make.sh ' ...
        'or build_msvc_2026.bat first, which downloads it, or set RTMA_FMT_INCLUDE ' ...
        'to the include folder of a copy of fmt.']);
end

sources = { ...
    fullfile(base_dir, 'lang', 'matlab', 'MatlabRTMA.cpp'), ...
    fullfile(core_dir, 'RTMA.cpp'), ...
    fullfile(core_dir, 'RTMA_Logger.cpp'), ...
    fullfile(core_dir, 'MyCException.cpp'), ...
    fullfile(core_dir, 'MyCString.cpp'), ...
    fullfile(core_dir, 'mex_hack.cpp'), ...
    fullfile(pipelib_dir, 'UPipe.cpp'), ...
    fullfile(pipelib_dir, 'SocketPipe.cpp'), ...
    fullfile(pipelib_dir, 'Timing.cpp')};
options = {'-v', '-D_MEX_FILE_', '-DFMT_HEADER_ONLY', ...
    '-outdir', fullfile(base_dir, 'lang', 'matlab')};
include_dirs = {['-I' fullfile(base_dir, 'include')], ...
    ['-I' fullfile(base_dir, 'include', 'internal')], ['-I' fmt_include]};
libs = {};

if( ispc)
    libs{end+1} = 'ws2_32.lib';
    % Since Visual Studio 2022 17.10, std::mutex's constructor is constexpr
    % and needs an msvcp140.dll at least as new. MATLAB loads its own, older
    % one, and the mex crashed (access violation in msvcp140.dll) on the
    % logger's first lock. This makes std::mutex work with any msvcp140.dll.
    options{end+1} = '-D_DISABLE_CONSTEXPR_MUTEX_CONSTRUCTOR';
    % fmt requires MSVC to compile with /utf-8, which fmt's CMake target
    % adds for the C++ library; mex needs it added to its own flags.
    compiler = mex.getCompilerConfigurations( 'C++', 'Selected');
    if( ~isempty( compiler) && strncmpi( compiler(1).ShortName, 'MSVC', 4))
        options{end+1} = 'COMPFLAGS=$COMPFLAGS /utf-8';
    end
elseif( isunix)
    options{end+1} = '-DUSE_LINUX';
end

% The function form of mex passes each argument as is, so paths with
% spaces work.
mex( options{:}, include_dirs{:}, sources{:}, libs{:});
