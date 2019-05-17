REM python %RTMA%/tools/build_python_message_defs.py message_defs.h
set CLANG2PY="C:\Program Files\Python37\Lib\site-packages\ctypeslib\clang2py.py"
python3 %CLANG2PY% -c -k cdefmstu -o message_defs.py message_defs.h