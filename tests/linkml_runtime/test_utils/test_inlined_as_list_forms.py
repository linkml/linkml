import pytest
from jsonasobj2 import JsonObj

from tests.test_utils.input.inlined_as_list import E, EInst


def test_empty_list_forms():
    """Test various empty list forms"""
    v = E()
    assert v.ev == [], "No entries, period"

    v = E({})
    assert v.ev == [], "Default is empty dictionary"

    v = E([])
    assert v.ev == [], "Empty list becomes empty dictionary"

    v = E(JsonObj())
    assert v.ev == [], "Empty JsonObj becomes empty dictionary"


def test_list_of_keys():
    """Test Form 5: list of keys"""
    v1 = JsonObj(["k1", "k2"])
    v = E(v1)
    assert v.ev == [EInst(s1="k1", s2=None, s3=None), EInst(s1="k2", s2=None, s3=None)]


def test_list_of_key_object_pairs():
    """Test Form 4: list of key/object pairs"""
    v = E([{"k1": {"s1": "k1", "s2": "v21", "s3": "v23"}}, {"k2": {"s2": "v22", "s3": "v23"}}, {"k3": {}}])
    assert v.ev == [
        EInst(s1="k1", s2="v21", s3="v23"),
        EInst(s1="k2", s2="v22", s3="v23"),
        EInst(s1="k3", s2=None, s3=None),
    ]


def test_duplicate_keys_error():
    """Test error handling for duplicate keys"""
    with pytest.raises(ValueError) as e:
        E([{"k1": None}, {"k1": "v2"}])
    assert "k1: duplicate key" in str(e.value)


def test_key_mismatch_error():
    """Test error handling for key/attribute mismatch"""
    with pytest.raises(ValueError) as e:
        E([{"k1": {"s1": "k2"}}])
    assert "Slot: ev - attribute s1 value (k2) does not match key (k1)" in str(e.value)


def test_form5_variations():
    """Test Form 5 variations with different object types"""
    v = E([{"k1": EInst(s1="k1", s2="v21", s3="v23")}, {"k2": JsonObj({"s2": "v22", "s3": "v23"})}, {"k3": None}])
    assert v.ev == [
        EInst(s1="k1", s2="v21", s3="v23"),
        EInst(s1="k2", s2="v22", s3="v23"),
        EInst(s1="k3", s2=None, s3=None),
    ]


def test_mixed_form5_variations():
    """Test more Form 5 variations with mixed types"""
    v = E(["k1", "k2", {"k3": "v3"}, ["k4", "v4"], {"s1": "k5", "s2": "v52"}])
    assert v.ev == [
        EInst(s1="k1", s2=None, s3=None),
        EInst(s1="k2", s2=None, s3=None),
        EInst(s1="k3", s2="v3", s3=None),
        EInst(s1="k4", s2="v4", s3=None),
        EInst(s1="k5", s2="v52", s3=None),
    ]


def test_positional_object_values():
    """Test Form 6: list of positional object values"""
    v = E([["k1", "v12", "v13"], ["k2", "v22"], ["k3"]])
    assert v.ev == [
        EInst(s1="k1", s2="v12", s3="v13"),
        EInst(s1="k2", s2="v22", s3=None),
        EInst(s1="k3", s2=None, s3=None),
    ]


def test_list_of_kv_dictionaries():
    """Test Form 7: list of key-value dictionaries"""
    v = E([{"s1": "v11", "s2": "v12"}, {"s1": "v21", "s2": "v22", "s3": "v23"}])
    assert v.ev == [EInst(s1="v11", s2="v12", s3=None), EInst(s1="v21", s2="v22", s3="v23")]


def test_dict_key_object_form():
    """Test Form 1: dictionary with key/object pairs"""
    v = E(
        {
            "k1": EInst(s1="k1", s2="v21", s3="v23"),
            "k2": JsonObj({"s2": "v22", "s3": "v23"}),
            "k3": {"s2": "v32", "s3": "v33"},
            "k4": {"s1": "k4"},
        }
    )
    assert v.ev == [
        EInst(s1="k1", s2="v21", s3="v23"),
        EInst(s1="k2", s2="v22", s3="v23"),
        EInst(s1="k3", s2="v32", s3="v33"),
        EInst(s1="k4", s2=None, s3=None),
    ]


def test_dict_key_value_tuples():
    """Test Form 2: dictionary with key/value tuples (max two values)"""
    v = E(ev={"k1": "v11", "k2": "v21", "k3": {}})
    assert v.ev == [
        EInst(s1="k1", s2="v11", s3=None),
        EInst(s1="k2", s2="v21", s3=None),
        EInst(s1="k3", s2=None, s3=None),
    ]


def test_single_object_dict():
    """Test Form 3: Basic single object dictionary"""
    v = E({"s1": "k1"})
    assert v.ev == [EInst(s1="k1", s2=None, s3=None)]


def test_single_object_dict_multiple_fields():
    """Test Form 3: Single object dictionary with multiple fields"""
    v = E({"s1": "k1", "s2": "v12"})
    assert v.ev == [EInst(s1="k1", s2="v12", s3=None)]
