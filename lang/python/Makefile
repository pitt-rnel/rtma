BASE_DIR   = ../..
SWIG       = swig # swig executable (add to path or include full path here)
SYMBOLS    = -DUSE_LINUX
GCC        = g++
CPPFLAGS   = -shared -Wall -Wno-deprecated -pthread -fPIC
PY_INC     = /usr/local/Cellar/python@2/2.7.15_3/Frameworks/Python.framework/Versions/2.7/include/python2.7 # path to python header files
PYTHON     = /usr/local/bin/python # path to python executable (might be unecessary? Some systems may need to reference this var to run H2XML and XML2PY)
PY_LD_FLAGS := $(shell python-config --ldflags) # generate commands to link to python library files
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
	${H2XML} -c -o RTMA_types.xml `pwd`/../../include/RTMA_types.h

RTMA_types.py: RTMA_types.xml
	${XML2PY} -o RTMA_types.py RTMA_types.xml

clean:
	rm -f *.so
	rm -f *.cxx
	rm -f PyRTMA.py
	rm -f *.pyc
	rm -f RTMA_types.xml
	rm -f RTMA_types.py

