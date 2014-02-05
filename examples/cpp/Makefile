CPP = g++
CPPFLAGS = -g -DUSE_LINUX -Wall -Wno-deprecated -pthread

LIB_DIR = ../../lib
INC_DIR = ../../include
TM_DIR = .

TM_REQS = ${INC_DIR}/RTMA.h ${TM_DIR}/CppModule.cpp

TestModule: ${TM_REQS}
	${CPP} ${CPPFLAGS} -L${LIB_DIR} -I${INC_DIR} -o ${TM_DIR}/TestModule ${TM_DIR}/CppModule.cpp -lRTMA

all: TestModule

clean:
	rm -f ${TM_DIR}/TestModule

