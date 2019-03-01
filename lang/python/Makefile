BASE_DIR   = ../..
SWIG       = swig # swig executable (add to path or include full path here)
SYMBOLS    = -DUSE_LINUX
GCC        = g++
CPPFLAGS   = -shared -Wall -Wno-deprecated -pthread -fPIC
PY_CONFIG = python-config # path or command to python-config utility
PYTHON     = python # path to python executable (unecessary if on path)
PY_INC     := $(shell ${PY_CONFIG} --includes) # path to python header files
PY_LD_FLAGS := $(shell ${PY_CONFIG} --ldflags) # generate commands to link to python library files
LIBS       = -L${BASE_DIR}/lib -lRTMA # link rtma library
LDFLAGS   += ${LIBS} ${PY_LD_FLAGS}
INCLUDES   = -I${BASE_DIR}/include -I${BASE_DIR}/include/internal # rtma includes
H2XML      = ~/svn/ctypeslib/scripts/h2xml.py
XML2PY     = ~/svn/ctypeslib/scripts/xml2py.py

all:  _PyRTMA.so RTMA_types.py

PyRTMA.py: PyRTMA.i
	${SWIG} ${SYMBOLS} ${INCLUDES} -c++ -python PyRTMA.i

_PyRTMA.so:  PyRTMA.py
	${GCC} ${CPPFLAGS} ${INCLUDES} ${SYMBOLS} -I${PY_INC} ${LDFLAGS} PyRTMA_wrap.cxx -o _PyRTMA.so

RTMA_types.xml: ${BASE_DIR}/include/RTMA_types.h
	${PYTHON} ${H2XML} -c -o RTMA_types.xml `pwd`/../../include/RTMA_types.h

RTMA_types.py: RTMA_types.xml
	${PYTHON} ${XML2PY} -o RTMA_types.py RTMA_types.xml

clean:
	rm -f *.so
	rm -f *.cxx
	rm -f PyRTMA.py
	rm -f *.pyc
	rm -f RTMA_types.xml
	rm -f RTMA_types.py

