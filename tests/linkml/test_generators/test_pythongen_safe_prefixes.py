"""Tests for safe Python identifier generation from CURIE prefix names.

Background
----------
CURIE prefix strings used in LinkML schemas can contain characters that are
illegal or unsafe in Python variable names:

  - Dots and hyphens         allotrope.equipment, my-prefix
  - Python hard keywords     in, for, class, not, def
  - Python builtin names     float, int, str, list, dict, set, type, id, object
  - Leading digits           2d, 3d  (not valid NCNames, unit-tested only)

Two separate code paths must produce *identical* variable names for the same
prefix, otherwise declaration and usage sites diverge and the generated module
fails at import time with a NameError:

  1. ``gen_namespaces()`` in ``pythongen.py`` — declares the namespace variable.
  2. ``curie_for(pythonform=True)`` in ``namespaces.py`` — builds every
     expression that references the namespace (class_class_uri, slot URIs, …).

The core reproduction case (from the filed issue) is:

    prefix declared:  allotrope.equipment
    gen_namespaces()  → ALLOTROPE_EQUIPMENT = CurieNamespace(...)   ✓
    curie_for()       → ALLOTROPE.EQUIPMENT["0000153"]              ✗  NameError

The fix introduces ``_safe_python_identifier`` (pythongen.py) and its twin
``_prefix_to_python_var`` (namespaces.py), which apply the same transformation
in both code paths.

Convention used (mirrors PEP 8 §Naming → trailing underscore)
--------------------------------------------------------------
  dot / hyphen         replace with '_', uppercase    allotrope.equipment → ALLOTROPE_EQUIPMENT
  keyword / builtin    append '_NS'                   float → FLOAT_NS
  leading non-alpha    prepend 'NS_'                  2d    → NS_2D
"""

from pathlib import Path
from types import ModuleType

import pytest

from linkml.generators.pythongen import PythonGenerator, _safe_python_identifier
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.namespaces import _prefix_to_python_var

# ---------------------------------------------------------------------------
# Parametrised cases shared by both helper-function tests.
#
# Each entry is (raw_prefix, expected_python_variable).  The same table is
# used to verify that _safe_python_identifier (pythongen) and
# _prefix_to_python_var (namespaces) agree on every input — because divergence
# between the two functions is exactly the bug this fix addresses.
# ---------------------------------------------------------------------------

SAFE_IDENTIFIER_CASES: list[tuple[str, str]] = [
    # --- Dot-separated prefix (the primary reproduction case) ---
    # A dot is a valid NCName character (XML spec), so these prefixes can
    # actually exist in a schema.  Without the fix, curie_for() emitted
    # ALLOTROPE.EQUIPMENT[...] which Python interprets as attribute access on
    # an undefined name ALLOTROPE, causing an immediate NameError on import.
    ("allotrope.equipment", "ALLOTROPE_EQUIPMENT"),
    # --- Hyphenated prefix ---
    # Hyphens are also valid NCName characters.  gen_namespaces() already
    # replaced them, but curie_for() did not, so usage sites were wrong.
    ("my-prefix", "MY_PREFIX"),
    # --- Python builtin names ---
    # Using a builtin name as a variable silently shadows it for the entire
    # generated module.  e.g. after `float = CurieNamespace(...)`, calling
    # float(3.14) raises TypeError instead of returning 3.14.
    ("float", "FLOAT_NS"),
    ("int", "INT_NS"),
    ("str", "STR_NS"),
    ("list", "LIST_NS"),
    ("dict", "DICT_NS"),
    ("set", "SET_NS"),
    ("type", "TYPE_NS"),  # also a soft keyword in Python 3.12+
    ("id", "ID_NS"),
    ("object", "OBJECT_NS"),
    # --- Python hard keywords ---
    # These cause a SyntaxError at parse time if used as variable names.
    # keyword.iskeyword() catches them; the check is case-insensitive because
    # the prefix is uppercased before the check.
    ("in", "IN_NS"),
    ("for", "FOR_NS"),
    ("class", "CLASS_NS"),
    ("not", "NOT_NS"),
    ("def", "DEF_NS"),
    # --- Leading-digit prefix ---
    # Not a valid NCName, so it cannot appear in an actual schema, but the
    # helper is used defensively and must still produce valid Python.
    ("2d", "NS_2D"),
    ("3d", "NS_3D"),
    # --- Safe prefixes that must pass through unchanged ---
    # Any transformation applied to already-safe names would break existing
    # schemas and change the public API of the generated module.
    ("ex", "EX"),
    ("linkml", "LINKML"),
    ("OBO", "OBO"),
]


# ---------------------------------------------------------------------------
# Unit tests: _safe_python_identifier (pythongen.py)
#
# This function is called by gen_namespaces() when emitting the LHS of every
# namespace variable declaration.  All unsafe categories must be handled here
# so that the declared variable name is always valid Python.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("prefix,expected", SAFE_IDENTIFIER_CASES)
def test_safe_python_identifier(prefix: str, expected: str) -> None:
    """_safe_python_identifier produces a valid Python identifier for every input category."""
    assert _safe_python_identifier(prefix) == expected


# ---------------------------------------------------------------------------
# Unit tests: _prefix_to_python_var (namespaces.py)
#
# This function is called inside curie_for(pythonform=True) when building
# every Python expression that references a namespace variable (class_class_uri,
# slot URIs, mapping expressions, enum code-set references, …).
#
# It must produce *exactly* the same output as _safe_python_identifier for
# every input, because a mismatch between the two is what causes the NameError
# described in the issue.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("prefix,expected", SAFE_IDENTIFIER_CASES)
def test_prefix_to_python_var_matches(prefix: str, expected: str) -> None:
    """_prefix_to_python_var agrees with _safe_python_identifier for every prefix category.

    This is the key invariant of the fix: the declaration site (pythongen.py)
    and the usage site (namespaces.py) must always produce the same name.
    """
    assert _prefix_to_python_var(prefix) == expected


# ---------------------------------------------------------------------------
# Integration tests: end-to-end code generation and compilation
#
# The fixture schema (unsafe_prefix_names.yaml) declares prefixes from every
# problematic category.  The generator is run, the output is compiled by
# Python's own compiler, and the generated source text is inspected to confirm
# that:
#   - variable declarations use the sanitised names
#   - usage expressions use the same sanitised names (no bare dot-chains)
#   - safe prefixes are left unchanged
# ---------------------------------------------------------------------------

UNSAFE_PREFIX_SCHEMA = Path(__file__).parent / "input" / "unsafe_prefix_names.yaml"


@pytest.fixture(scope="module")
def unsafe_prefix_code() -> str:
    """Generated Python source for the unsafe-prefix-names schema."""
    return PythonGenerator(str(UNSAFE_PREFIX_SCHEMA), mergeimports=True).serialize()


@pytest.fixture(scope="module")
def unsafe_prefix_module(unsafe_prefix_code: str) -> ModuleType:
    """Compiled module from the generated source — proves it is valid Python."""
    return compile_python(unsafe_prefix_code)


def test_generated_code_compiles(unsafe_prefix_module: ModuleType) -> None:
    """The generated module must import cleanly with no NameError or SyntaxError.

    Before the fix, any class whose class_uri used a dotted prefix (e.g.
    allotrope.equipment:0000153) caused a NameError at import time because the
    generated expression ALLOTROPE.EQUIPMENT[...] tried to access attribute
    EQUIPMENT on an undefined name ALLOTROPE.
    """
    assert unsafe_prefix_module is not None


def test_dotted_prefix_declaration_uses_underscore(unsafe_prefix_code: str) -> None:
    """allotrope.equipment must be declared as ALLOTROPE_EQUIPMENT.

    gen_namespaces() previously used .replace('.', '_') for the variable name,
    which was correct.  This test asserts that the fix did not regress that
    behaviour while adding the keyword/builtin guard.
    """
    assert "ALLOTROPE_EQUIPMENT = CurieNamespace" in unsafe_prefix_code


def test_dotted_prefix_no_attribute_chain_in_expressions(unsafe_prefix_code: str) -> None:
    """Generated expressions must never contain the broken ALLOTROPE.EQUIPMENT form.

    ALLOTROPE.EQUIPMENT[...] is a Python attribute-access chain.  Because
    ALLOTROPE is not defined, it raises NameError immediately.  After the fix,
    curie_for(pythonform=True) must emit ALLOTROPE_EQUIPMENT[...] instead.
    """
    assert "ALLOTROPE.EQUIPMENT" not in unsafe_prefix_code


def test_hyphen_prefix_declaration_uses_underscore(unsafe_prefix_code: str) -> None:
    """my-prefix must be declared as MY_PREFIX (hyphen → underscore).

    A hyphen is a valid NCName character but an invalid Python identifier
    character, so it must be substituted before emission.
    """
    assert "MY_PREFIX = CurieNamespace" in unsafe_prefix_code


def test_builtin_prefix_declaration_gets_ns_suffix(unsafe_prefix_code: str) -> None:
    """The 'float' prefix must be declared as FLOAT_NS, not FLOAT.

    Without the fix, `FLOAT = CurieNamespace(...)` silently shadows the
    built-in float type for every line that follows in the generated module.
    Any code in the module that subsequently calls float() would get a
    CurieNamespace object instead of the numeric type.
    """
    assert "FLOAT_NS = CurieNamespace" in unsafe_prefix_code
    assert "FLOAT = CurieNamespace" not in unsafe_prefix_code


def test_builtin_prefix_expressions_use_ns_suffix(unsafe_prefix_code: str) -> None:
    """Every usage of the float prefix in generated expressions must use FLOAT_NS.

    It is not enough to fix only the declaration; if curie_for() still emits
    FLOAT[...] in expressions, those expressions reference the shadowed (wrong)
    object and the shadowing bug is masked but not fixed.
    """
    bare_float_lines = [
        line
        for line in unsafe_prefix_code.splitlines()
        if ("FLOAT[" in line or "FLOAT." in line) and "FLOAT_NS" not in line
    ]
    assert bare_float_lines == [], "Generated code references bare FLOAT (not FLOAT_NS) in:\n" + "\n".join(
        bare_float_lines
    )


def test_keyword_prefix_declaration_gets_ns_suffix(unsafe_prefix_code: str) -> None:
    """The 'in' prefix must be declared as IN_NS, not IN.

    `IN` uppercased and checked: keyword.iskeyword('in') is True, so without
    the _NS suffix the generated file would raise a SyntaxError at parse time
    if `IN` ever appeared in a context where Python's keyword parser rejects it.
    """
    assert "IN_NS = CurieNamespace" in unsafe_prefix_code
    assert "IN = CurieNamespace" not in unsafe_prefix_code


def test_safe_prefixes_are_unchanged(unsafe_prefix_code: str) -> None:
    """Prefixes that are already safe Python identifiers must not be altered.

    The fix must only modify prefixes that are actually problematic.  Appending
    _NS to every prefix would change the public interface of all existing
    generated modules and break downstream code.
    """
    assert "EX = CurieNamespace" in unsafe_prefix_code
    assert "LINKML = CurieNamespace" in unsafe_prefix_code
