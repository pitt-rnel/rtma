"""Checks that the C++ core type headers mirror pyrtma's core definitions.

core_types_test.cpp, which CTest compiles, asserts the values and layouts.
These tests check that it was generated from the installed pyrtma, and that
the headers define nothing the YAML files don't, apart from the legacy
definitions listed here.
"""

from __future__ import annotations

import re

import pytest

pytest.importorskip("pyrtma")

import generate  # noqa: E402

INCLUDE = generate.HERE.parents[1] / "include"

# Kept in core_types.h for existing code; not in pyrtma's definitions.
LEGACY = {
    "core_types.h": {
        "MID_QUICKLOGGER",
        "MIN_STREAM_TYPE",
        "UID",
        "RTMA_MESSAGE",
        "MT_MM_READY",
        "MT_SUBSCRIPTION_OPTION",
        "MDF_SUBSCRIPTION_OPTION",
    },
}

DEFINE = re.compile(r"^#define\s+(\w+)", re.M)
TYPEDEF = re.compile(r"^typedef\s+[\w\s]+?\s(\w+);|^}\s*(\w+);", re.M)


@pytest.fixture(scope="module")
def parser():
    return generate.parse()


def expected_names(p, src: str) -> set[str]:
    def mine(objs):
        return [o for o in objs.values() if o.src.name == src]

    names = {c.name for c in mine(p.constants)}
    names |= {a.name for a in mine(p.aliases)}
    names |= {f"HID_{h.name}" for h in mine(p.host_ids)}
    names |= {f"MID_{m.name}" for m in mine(p.module_ids)}
    names |= {s.name for s in mine(p.struct_defs)}
    for m in mine(p.message_defs):
        names |= {f"MT_{m.name}", f"HASH_{m.name}"}
        if m.fields:
            names.add(f"MDF_{m.name}")
    return names


def test_generated_test_is_current():
    committed = generate.OUTPUT.read_text(encoding="utf-8")
    assert committed == generate.generate(), (
        "core_types_test.cpp is out of date with pyrtma's core definitions; "
        "run python tests/core_types/generate.py"
    )


@pytest.mark.parametrize("src, header", list(generate.HEADERS.items()))
def test_header_defines_only_its_yaml(parser, src, header):
    text = (INCLUDE / header).read_text(encoding="utf-8")
    guard = re.search(r"^#ifndef\s+(\w+)", text, re.M).group(1)
    defined = set(DEFINE.findall(text)) - {guard}
    defined |= {a or b for a, b in TYPEDEF.findall(text)}
    expected = expected_names(parser, src)
    legacy = LEGACY.get(header, set())
    assert sorted(defined - expected - legacy) == [], f"{header} defines names not in {src}.yaml"
    assert sorted(expected - defined) == [], f"{header} is missing names from {src}.yaml"
    assert sorted(legacy - defined) == [], f"legacy names no longer in {header}"


def test_rtma_types_includes_each_header():
    text = (INCLUDE / "RTMA_types.h").read_text(encoding="utf-8")
    # Quoted includes: MATLAB's ParseHFile follows those, relative to this file.
    included = re.findall(r'^#include\s+"([^"]+)"', text, re.M)
    assert included == list(generate.HEADERS.values())
