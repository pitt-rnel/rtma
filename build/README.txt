This directory contains the top-level build-scripts for RTMA.
To build RTMA:

On Windows, open RTMA.sln in Visual Studio (tested with version 2005), 
select the "Release" configuration and run Build All. This will build
the C++ API (lib/RTMA.lib), the .NET API (lang/dot_net/RTMA.NET.dll), 
and the executable modules (bin/MessageManager.exe and bin/QuickLogger.exe).

On Linux, make sure you have qmake installed in addition to regular make,
the run "make" within this build directory. This will build the C++ API
(lib/libRTMA.so), the Python API (lang/python/PyRTMA.?), and the
executable modules (bin/MessageManager and bin/QuickLogger).

The Matlab API needs to be compiled separately by starting matlab, changing current
directory to lang/matlab and running the make.m script. It works the same on
Windows or Linux.
