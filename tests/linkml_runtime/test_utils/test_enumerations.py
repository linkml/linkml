"""Tests for ``EnumDefinitionMeta`` MRO behaviour.

Regression for https://github.com/linkml/linkml/issues/3591: the metaclass
operators ``__contains__`` and ``__getitem__`` previously only inspected
``cls.__dict__`` and so failed to find permissible values inherited from a
parent enumeration class.  ``pythongen`` emits empty wrapper subclasses for
identifier slots whose range is an enum, which triggered the failure as
``ValueError: Unknown <Wrapper> enumeration code: <X>``.
"""

import pytest

from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue
from linkml_runtime.utils.enumerations import EnumDefinitionImpl


class _ParentEnum(EnumDefinitionImpl):
    _defn = EnumDefinition(name="_ParentEnum")
    A = PermissibleValue(text="A")
    B = PermissibleValue(text="B")


class _WrapperEnum(_ParentEnum):
    """Empty subclass, mirroring ``pythongen`` wrapper output."""

    _defn = EnumDefinition(name="_WrapperEnum")


class _GrandchildEnum(_WrapperEnum):
    _defn = EnumDefinition(name="_GrandchildEnum")
    C = PermissibleValue(text="C")


@pytest.mark.parametrize("cls", [_ParentEnum, _WrapperEnum, _GrandchildEnum])
def test_contains_walks_mro(cls):
    """``key in cls`` must find values from any ancestor in the MRO."""
    assert "A" in cls
    assert "B" in cls


@pytest.mark.parametrize("cls", [_ParentEnum, _WrapperEnum, _GrandchildEnum])
def test_contains_false_for_missing_key(cls):
    assert "DOES_NOT_EXIST" not in cls


def test_grandchild_sees_own_values():
    assert "C" in _GrandchildEnum
    assert "C" not in _WrapperEnum
    assert "C" not in _ParentEnum


@pytest.mark.parametrize("cls", [_ParentEnum, _WrapperEnum, _GrandchildEnum])
def test_getitem_walks_mro(cls):
    """``cls[key]`` must return the ancestor's ``PermissibleValue``."""
    assert cls["A"] is _ParentEnum.__dict__["A"]
    assert cls["B"] is _ParentEnum.__dict__["B"]


def test_getitem_returns_nearest_definition():
    assert _GrandchildEnum["C"] is _GrandchildEnum.__dict__["C"]


@pytest.mark.parametrize("cls", [_ParentEnum, _WrapperEnum, _GrandchildEnum])
def test_getitem_raises_keyerror_for_missing(cls):
    with pytest.raises(KeyError):
        cls["DOES_NOT_EXIST"]


@pytest.mark.parametrize("cls", [_ParentEnum, _WrapperEnum, _GrandchildEnum])
def test_construct_with_inherited_code(cls):
    """The full reporter repro: instantiating a wrapper with a parent's code."""
    instance = cls("A")
    assert str(instance) == "A"


def test_construct_with_own_code_on_grandchild():
    instance = _GrandchildEnum("C")
    assert str(instance) == "C"
