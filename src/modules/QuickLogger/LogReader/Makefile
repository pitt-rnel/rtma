# defines
CPP = mex
INCLUDES  = -I../../../src -I.. -I../../../include -I../../..
REQS = LogReader.cpp
LIBPATH = -L../../../lib
LIBS = -lRTMA
DEFINES =  -D_MEX_FILE_ -DUSE_LINUX
#rules
# this should depend on rtma lib---
default: LogReader.mexa64

LogReader.mexa64: LogReader.cpp
	${CPP} ${DEFINES} ${INCLUDES} ${LIBPATH} ${LIBS} LogReader.cpp

clean:
	rm -rf *.o
	rm -rf *.mex*
