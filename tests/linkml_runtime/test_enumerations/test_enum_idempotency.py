"""Tests for EnumDefinitionImpl constructor idempotency.

Verifies that passing an existing EnumDefinitionImpl instance into a parent
or sibling enum's constructor does not raise TypeError and correctly
re-resolves the code in the target enum's namespace.
"""

import pytest

from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue
from linkml_runtime.utils.enumerations import EnumDefinitionImpl


class _BaseEnum(EnumDefinitionImpl):
    _defn = EnumDefinition(name="_BaseEnum")

    @classmethod
    def _addvals(cls):
        cls.LOGON = PermissibleValue(text="LOGON", description="Logon event")
        cls.LOGOFF = PermissibleValue(text="LOGOFF", description="Logoff event")


class _SubEnum(EnumDefinitionImpl):
    """Simulates a slot_usage-narrowed subclass enum."""

    _defn = EnumDefinition(name="_SubEnum")

    @classmethod
    def _addvals(cls):
        cls.LOGON = PermissibleValue(text="LOGON", description="Logon (sub)")
        cls.LOGOFF = PermissibleValue(text="LOGOFF", description="Logoff (sub)")


def test_enum_idempotent_same_class():
    """Passing an instance back into its own constructor is a no-op."""
    inst = _BaseEnum("LOGON")
    inst2 = _BaseEnum(inst)
    assert str(inst2) == "LOGON"


def test_enum_idempotent_subclass_to_parent():
    """Passing a subclass enum instance into a parent enum constructor
    must not raise TypeError and must resolve against the parent's codes.
    """
    sub_inst = _SubEnum("LOGON")
    # Before the fix this raised:
    # TypeError: cannot use '_SubEnum' as a dict key (unhashable type)
    parent_inst = _BaseEnum(sub_inst)
    assert str(parent_inst) == "LOGON"


def test_enum_idempotent_parent_to_subclass():
    """Passing a parent enum instance into a subclass enum constructor works."""
    parent_inst = _BaseEnum("LOGOFF")
    sub_inst = _SubEnum(parent_inst)
    assert str(sub_inst) == "LOGOFF"


@pytest.mark.parametrize("code", ["LOGON", "LOGOFF"])
def test_enum_str_construction_still_works(code):
    """Plain string construction is unaffected by the fast-path addition."""
    inst = _BaseEnum(code)
    assert str(inst) == code


def test_enum_idempotent_preserves_code_text():
    """Re-resolved instance has _code.text equal to the original text."""
    sub_inst = _SubEnum("LOGON")
    parent_inst = _BaseEnum(sub_inst)
    assert parent_inst._code.text == "LOGON"


def test_enum_unknown_code_still_raises():
    """ValueError is still raised for unknown codes (regression guard)."""
    with pytest.raises(ValueError, match="Unknown"):
        _BaseEnum("INVALID")
