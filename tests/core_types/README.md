# Core type tests

The core type headers mirror pyrtma's core message definitions, one header
per YAML file:

| Header | pyrtma YAML |
|---|---|
| `include/core_types.h` | `core_defs/rtma_core.yaml` |
| `include/quick_logger_types.h` | `core_defs/quick_logger.yaml` |
| `include/data_logger_types.h` | `core_defs/data_logger.yaml` |

`include/RTMA_types.h` includes all three.

`core_types_test.cpp` is generated from the YAML files. It holds a
`static_assert` for every constant, alias, ID and hash, and for the size of
every struct and message and the offset, type and length of every field.
CTest builds it as `rtma_core_types_test`, so a header that drifts from the
YAML fails the build.

After changing a header or updating pyrtma, regenerate it with the pyrtma
whose definitions the headers should match, and rebuild:

```
python tests/core_types/generate.py
```

`test_core_types.py` checks that the committed file is current, and that
each header defines nothing its YAML file doesn't, apart from the legacy
names it lists:

```
python -m pytest tests/core_types
```
