#!/bin/bash
#python $DRAGONFLY/tools/build_python_message_defs.py message_defs.h
CLANG2PY=/usr/local/lib/python3.7/site-packages/ctypeslib/clang2py.py
python3 ${CLANG2PY} -c -k cdefmstu -o `pwd`/message_defs.py `pwd`/message_defs.h