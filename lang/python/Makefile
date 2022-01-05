BASE_DIR   = ../..
SWIG       = swig # swig executable (add to path or include full path here)
SYMBOLS    = -DUSE_LINUX
GCC        = g++
CPPFLAGS   = -shared -Wall -Wno-deprecated -pthread -fPIC
PY2_CONFIG  = python2-config # path or command to python-config utility
PYTHON2     = python2 # path to python executable (unecessary if on path)
PY2_INC     := $(shell ${PY2_CONFIG} --includes) # path to python header files
PY2_LD_FLAGS := $(shell ${PY2_CONFIG} --ldflags) # generate commands to link to python library files
PY3_CONFIG  = python3-config # path or command to python-config utility
PYTHON3     = python3 # path to python executable (unecessary if on path)
PY3_INC     := $(shell ${PY3_CONFIG} --includes) # path to python header files
PY3_LD_FLAGS := $(shell ${PY3_CONFIG} --ldflags) # generate commands to link to python library files
LIBS       = -L${BASE_DIR}/lib -lRTMA # link rtma library
LDFLAGS_PY2   += ${LIBS} ${PY2_LD_FLAGS}
LDFLAGS_PY3   += ${LIBS} ${PY3_LD_FLAGS}
INCLUDES   = -I${BASE_DIR}/include -I${BASE_DIR}/include/internal # rtma includes
CLANG2PY   = /usr/local/lib/python3.7/site-packages/ctypeslib/clang2py.py

all:  _PyRTMA2.so _PyRTMA3.so RTMA_types.py

PyRTMA2.py: PyRTMA2.i
	${SWIG} ${SYMBOLS} ${INCLUDES} -c++ -python -threads PyRTMA2.i

PyRTMA3.py: PyRTMA3.i
	${SWIG} ${SYMBOLS} ${INCLUDES} -c++ -python -threads PyRTMA3.i

_PyRTMA2.so:  PyRTMA2.py
	${GCC} ${CPPFLAGS} ${INCLUDES} ${SYMBOLS} -I${PY2_INC} ${LDFLAGS_PY2} PyRTMA2_wrap.cxx -o _PyRTMA2.so

_PyRTMA3.so:  PyRTMA3.py
	${GCC} ${CPPFLAGS} ${INCLUDES} ${SYMBOLS} -I${PY3_INC} ${LDFLAGS_PY3} PyRTMA3_wrap.cxx -o _PyRTMA3.so

RTMA_types.py: ${BASE_DIR}/include/RTMA_types.h
	${PYTHON3} ${CLANG2PY} -c -k cdefmstu -o RTMA_types.py `pwd`/../../include/RTMA_types.h

clean:
	rm -f *.so
	rm -f *.cxx
	rm -f PyRTMA{2,3}.py
	rm -f *.pyc
	rm -f RTMA_types.xml
	rm -f RTMA_types.py

