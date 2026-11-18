# MATLAB message definition comparison

The MATLAB bindings can load message definitions two ways: a MAT file that
`TranslateRTMAConfigFiles2Matlab` writes from C headers (the legacy
translator), or the function that pyrtma's compiler writes
(`python -m pyrtma.compile --matlab`). `compare_message_defs.m` checks that
both give the bindings the same structure for the same definitions.

To compare them for pyrtma's own test definitions, which cover struct
fields, arrays and aliases, from the repository root:

```
python -m pyrtma.compile -i PYRTMA/tests/test_msg_defs/test_defs.defs --c --matlab -o build/defs_compare -n test_defs
```

where `PYRTMA` is a pyrtma checkout. Then in MATLAB, from the repository
root:

```
addpath lang/matlab tests/matlab
TranslateRTMAConfigFiles2Matlab(pwd, fullfile(pwd, 'build', 'defs_compare', 'test_defs.h'), 'test_defs_legacy')
compare_message_defs(fullfile('build', 'defs_compare', 'test_defs_legacy.mat'), fullfile(pwd, 'build', 'defs_compare', 'test_defs.m'))
```

It prints each difference, then their number; for equivalent definitions,
0. Names only the legacy core headers define are listed as expected and not
counted. With a pyrtma whose MATLAB compiler still adds the old text messages
`MM_ERROR`, `MM_INFO` and `DEBUG_TEXT`, from before its change "drop obsolete
opcodes and text messages", those are reported as only in the compiled
definitions.
