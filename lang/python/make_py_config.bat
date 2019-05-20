REM python C:\git\rtma\lang\python\ctypesgen/ctypesgen.py --includedir="C:\git\climber\include" -a -o RTMA_config2.py C:\git\climber\include\climber_config.h
REM python3 C:\git\ctypesgen\run.py --includedir="C:\git\climber\include" -a -o RTMA_config2.py C:\git\climber\include\climber_config.h
REM CLANG2PY works with either python2 or python3 and produces identical output, so only need to generate once
set PYTHON=python
set CLANG2PY="%PYTHON3_BASE%\Lib\site-packages\ctypeslib\clang2py.py"
%PYTHON% %CLANG2PY% -c -k cdefmstu -i -o climber_config.py D:\git\climber\include\climber_config.h