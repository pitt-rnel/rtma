#!/bin/bash
#python $DRAGONFLY/tools/build_python_message_defs.py message_defs.h
H2XML=~/svn/ctypeslib/scripts/h2xml.py
XML2PY=~/svn/ctypeslib/scripts/xml2py.py
${H2XML} -c -o `pwd`/message_defs.xml `pwd`/message_defs.h
${XML2PY} -o `pwd`/message_defs.py `pwd`/message_defs.xml
rm -f `pwd`/message_defs.xml
