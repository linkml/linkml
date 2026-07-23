"""Tests for https://github.com/linkml/linkml/issues/1203.

Verifies that generated dataclass enumerations support intuitive equality,
hashing, stringification, and membership checks against strings, other
``EnumDefinitionImpl`` instances, and ``PermissibleValue`` objects.

Also verifies the Phase-1 structural fix (#723): bare ``PermissibleValue``
class attributes emitted by ``pythongen`` are promoted to real
``EnumDefinitionImpl`` instances at class-creation time.
"""

import pytest

import linkml_runtime  # noqa: F401
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
    """Assigning attributes on the abstract base must not raise.

    ``EnumDefinitionImpl`` has ``_defn = None``; the metaclass must not
    explode when used (e.g. for monkey-patching).
    """
    EnumDefinitionImpl._test_marker_1203 = "ok"  # noqa: SLF001
    assert EnumDefinitionImpl._test_marker_1203 == "ok"  # noqa: SLF001
    del EnumDefinitionImpl._test_marker_1203


# ---------------------------------------------------------------------------
# Phase 1 (#723): PermissibleValue -> EnumDefinitionImpl promotion


def test_member_is_enum_instance_not_permissible_value() -> None:
    """``MyEnum.A`` must be an ``EnumDefinitionImpl`` instance, not a raw PV."""
    assert isinstance(EnumValues.A, EnumValues)
    assert isinstance(EnumValues.A, EnumDefinitionImpl)
    assert type(EnumValues.A) is EnumValues
    assert not isinstance(EnumValues.A, PermissibleValue)


def test_member_identity_stable() -> None:
    """Repeated lookups return the same promoted instance (promotion runs once)."""
    assert EnumValues.A is EnumValues.A
    assert EnumValuesWrapper.A is EnumValues.A  # inherited via MRO


def test_member_text_property() -> None:
    """``EnumDefinitionImpl`` exposes ``.text`` as a delegate to the underlying PV."""
    assert EnumValues.A.text == "A"
    assert EnumValues("A").text == "A"


def test_member_code_is_underlying_pv() -> None:
    """``MyEnum.A._code`` is the original ``PermissibleValue``."""
    assert isinstance(EnumValues.A._code, PermissibleValue)
    assert EnumValues.A._code.text == "A"


def test_permissible_value_remains_clean_dataclass() -> None:
    """``PermissibleValue`` retains default dataclass equality and is unhashable.

    Phase 1 removes the runtime monkey-patch; the metamodel descriptor
    behaves like a plain dataclass again.
    """
    pv = PermissibleValue(text="A")
    assert pv == PermissibleValue(text="A")  # field-wise equality
    assert pv != PermissibleValue(text="B")
    with pytest.raises(TypeError):
        hash(pv)


# 1. Equality comparison
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("left", "right"),
    [
        (EnumValues.A, EnumValues("A")),
        (EnumValues("A"), EnumValues.A),
        (EnumValues.A, "A"),
        ("A", EnumValues.A),
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
        (EnumValues.A, "B"),
        ("B", EnumValues.A),
        (EnumValues("A"), "B"),
        ("B", EnumValues("A")),
        (EnumValues.A, EnumValues.B),
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
        EnumValues.A,
        EnumValues("A"),
    ],
)
@pytest.mark.parametrize(
    "haystack_factory",
    [
        lambda: {EnumValues.A, EnumValues.B},
        lambda: {EnumValues("A"), EnumValues("B")},
        lambda: {"A", "B"},
    ],
)
def test_enum_membership_in_set(needle, haystack_factory) -> None:
    assert needle in haystack_factory()


def test_enum_hashable() -> None:
    assert hash(EnumValues.A) == hash("A")
    assert hash(EnumValues("A")) == hash("A")
    assert hash(EnumValues.A) == hash(EnumValues("A"))


# ---------------------------------------------------------------------------
# 3. Stringification
# ---------------------------------------------------------------------------


def test_enum_stringification() -> None:
    assert str(EnumValues.A) == "A"
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
