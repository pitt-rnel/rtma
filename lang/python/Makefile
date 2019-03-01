BASE_DIR   = ../..
SWIG       = swig # swig executable (add to path or include full path here)
SYMBOLS    = -DUSE_LINUX
GCC        = g++
CPPFLAGS   = -shared -Wall -Wno-deprecated -pthread -fPIC
PY_INC     = $(shell python3-config --includes)
PYTHON     = /usr/local/bin/python3 # path to python executable (might be unecessary? Some systems may need to reference this var to run H2XML and XML2PY)
PY_LD_FLAGS := $(shell python3-config --ldflags) # generate commands to link to python library files
LIBS       = -L${BASE_DIR}/lib -lRTMA # link rtma library
LDFLAGS   += ${LIBS} ${PY_LD_FLAGS}
INCLUDES   = -I${BASE_DIR}/include -I${BASE_DIR}/include/internal # rtma includes
CLANG2PY   = /usr/local/lib/python3.7/site-packages/ctypeslib/clang2py.py

all:  _PyRTMA.so RTMA_types.py

PyRTMA.py: PyRTMA.i
	${SWIG} ${SYMBOLS} ${INCLUDES} -c++ -python PyRTMA.i

_PyRTMA.so:  PyRTMA.py
	${GCC} ${CPPFLAGS} ${INCLUDES} ${SYMBOLS} -I${PY_INC} ${LDFLAGS} PyRTMA_wrap.cxx -o _PyRTMA.so

RTMA_types.py: ${BASE_DIR}/include/RTMA_types.h
	${PYTHON} ${CLANG2PY} -c -o RTMA_types.py `pwd`/../../include/RTMA_types.h

clean:
	rm -f *.so
	rm -f *.cxx
	rm -f PyRTMA.py
	rm -f *.pyc
	rm -f RTMA_types.xml
	rm -f RTMA_types.py

