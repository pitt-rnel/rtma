BASE_DIR   = ../..
SWIG       = swig
SYMBOLS    = -DUSE_LINUX
GCC        = g++
CPPFLAGS   = -shared -Wall -Wno-deprecated -pthread -fPIC
LIBS       = -L${BASE_DIR}/lib -lRTMA
PY_INC     = /usr/local/Cellar/python@2/2.7.15_3/Frameworks/Python.framework/Versions/2.7/include/python2.7
PYTHON     = /usr/local/bin/python
INCLUDES   = -I${BASE_DIR}/include -I${BASE_DIR}/include/internal
H2XML      = ~/svn/ctypeslib/scripts/h2xml.py
XML2PY     = ~/svn/ctypeslib/scripts/xml2py.py

all:  _PyRTMA.so RTMA_types.py

PyRTMA.py: PyRTMA.i
	${SWIG} ${SYMBOLS} ${INCLUDES} -c++ -python PyRTMA.i

_PyRTMA.so:  PyRTMA.py
	${GCC} ${CPPFLAGS} ${INCLUDES} ${SYMBOLS} -I${PY_INC} ${LIBS} PyRTMA_wrap.cxx -o _PyRTMA.so -lpython2.7 -lRTMA

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

