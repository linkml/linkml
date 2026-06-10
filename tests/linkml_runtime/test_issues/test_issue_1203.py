"""Tests for https://github.com/linkml/linkml/issues/1203.

Verifies that ``EnumDefinitionImpl`` *instances* support intuitive equality,
hashing, stringification, and membership checks against strings, other
``EnumDefinitionImpl`` instances, and ``PermissibleValue`` objects.

.. note::
    The bare class-attribute form (e.g. ``EnumValues.A``) is a raw
    ``PermissibleValue`` dataclass emitted by ``pythongen``.  Making *that*
    object compare/hash/stringify like a string is the structural fix
    tracked by https://github.com/linkml/linkml/issues/723 and delivered by
    PR https://github.com/linkml/linkml/pull/3597 (which promotes bare
    attributes to real ``EnumDefinitionImpl`` instances).  Assertions that
    exercise the bare-attribute form belong with that PR and are
    intentionally not exercised here.
"""

import pytest

from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue
from linkml_runtime.utils.enumerations import EnumDefinitionImpl, EnumDefinitionMeta


class EnumValues(EnumDefinitionImpl):
    _defn = EnumDefinition(name="EnumValues")

    A = PermissibleValue(text="A")
    B = PermissibleValue(text="B")


class EnumValuesWrapper(EnumValues):
    """Empty wrapper subclass — emitted by ``pythongen`` for identifier slots.

    Inherits permissible values from ``EnumValues`` via the MRO; the metaclass
    membership / lookup must walk it.
    """

    pass


# -------------------------------
# MRO walk in EnumDefinitionMeta
# -------------------------------


def test_wrapper_subclass_membership() -> None:
    assert "A" in EnumValuesWrapper
    assert PermissibleValue(text="A") in EnumValuesWrapper
    assert EnumValues.A in EnumValuesWrapper


def test_wrapper_subclass_getitem() -> None:
    assert EnumValuesWrapper["A"] is EnumValues.A


def test_wrapper_subclass_instantiation() -> None:
    """The empty wrapper subclass must be constructible from an inherited code."""
    inst = EnumValuesWrapper("A")
    assert str(inst) == "A"
    assert inst == "A"
    assert inst == EnumValues.A


def test_base_class_setattr_with_no_defn() -> None:
    """``EnumDefinitionMeta.__setattr__`` must tolerate ``_defn`` being ``None``.

    The abstract base ``EnumDefinitionImpl`` has ``_defn = None``; assigning
    attributes on it (e.g. during monkey-patching) must not raise.
    """
    # No exception expected.
    EnumDefinitionImpl._test_marker_1203 = "ok"  # noqa: SLF001
    assert EnumDefinitionImpl._test_marker_1203 == "ok"  # noqa: SLF001
    del EnumDefinitionImpl._test_marker_1203


# ---------------------------------------------------------------------------
# 1. Equality comparison
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("left", "right"),
    [
        (EnumValues.A, EnumValues("A")),
        (EnumValues("A"), EnumValues.A),
        (EnumValues("A"), "A"),
        ("A", EnumValues("A")),
        (EnumValues("A"), EnumValues("A")),
        (EnumValues.A, EnumValues.A),
    ],
)
def test_enum_equality(left, right) -> None:
    assert left == right


@pytest.mark.parametrize(
    ("left", "right"),
    [
        (EnumValues("A"), "B"),
        ("B", EnumValues("A")),
        (EnumValues("A"), EnumValues("B")),
    ],
)
def test_enum_inequality(left, right) -> None:
    assert left != right


# ---------------------------------------------------------------------------
# 2. Hashing support
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "needle",
    [
        "A",
        EnumValues("A"),
    ],
)
@pytest.mark.parametrize(
    "haystack_factory",
    [
        lambda: {EnumValues("A"), EnumValues("B")},
        lambda: {"A", "B"},
    ],
)
def test_enum_membership_in_set(needle, haystack_factory) -> None:
    assert needle in haystack_factory()


def test_enum_hashable() -> None:
    assert hash(EnumValues("A")) == hash("A")


# ---------------------------------------------------------------------------
# 3. Stringification
# ---------------------------------------------------------------------------


def test_enum_stringification() -> None:
    assert str(EnumValues("A")) == "A"


# ---------------------------------------------------------------------------
# 4. ``in EnumClass`` checks
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "needle",
    [
        "A",
        EnumValues.A,
        EnumValues("A"),
    ],
)
def test_membership_in_enum_class(needle) -> None:
    assert needle in EnumValues


def test_unknown_value_not_in_enum_class() -> None:
    assert "Z" not in EnumValues
    assert PermissibleValue(text="Z") not in EnumValues


# ---------------------------------------------------------------------------
# Misc sanity checks
# ---------------------------------------------------------------------------


def test_enum_class_uses_meta() -> None:
    assert isinstance(EnumValues, EnumDefinitionMeta)


def test_pattern_match_workaround_no_longer_needed() -> None:
    """The original issue noted that ``match`` statements required ``.text``.

    With ``__eq__`` against strings, a direct match on the enum value works.
    """
    value = EnumValues("A")
    matched = None
    if value == EnumValues.A:
        matched = "A"
    elif value == EnumValues.B:
        matched = "B"
    assert matched == "A"
