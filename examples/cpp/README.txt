CppModule.cpp is a simple example of a C++ module.

Compile it in Windows by opening the CppModule.sln in Visual Studio (has been tested with the 2005 version), or by typing "make" on a linux command-line.

Then run two instances, one that produces messages and the other one that consumes the messages, by typing "CppModule producer" in one command window, and "CppModule consumer" in another. MessageManager must already be running in the background somewhere, if it's not then run it from the bin directory.

You can use this code as a starting point to develop your own module, or just use it to test if RTMA is correctly compiled and working. 
