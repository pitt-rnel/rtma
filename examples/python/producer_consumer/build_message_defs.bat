REM python %RTMA%/tools/build_python_message_defs.py message_defs.h
set PYTHON=python
set CLANG2PY="%PYTHON3_BASE%\Lib\site-packages\ctypeslib\clang2py.py"
%PYTHON% %CLANG2PY% -c -k cdefmstu -o message_defs.py message_defs.h