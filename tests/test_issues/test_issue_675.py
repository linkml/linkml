import pytest
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pydanticgen import PydanticGenerator
from linkml.generators.pythongen import PythonGenerator

model_txt = """
id: https://example.org/ifabsent
name: ifabsent_test

prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/ifabsent/
default_prefix: ex
default_range: string

imports:
  - linkml:types

slots:
    bool_true_slot:
        range: boolean
        ifabsent: true
    bool_false_slot:
        range: boolean
        ifabsent: False
    bnode_slot:
        ifabsent: bnode
    class_curie_slot:
        ifabsent: class_curie
    class_uri_slot:
        range: uri
        ifabsent: class_uri
    default_ns_slot:
        ifabsent: default_ns
    default_range_slot:
        ifabsent: default_range
    int_42_slot:
        range: integer
        ifabsent: int(42)
    int_0_slot:
        range: integer
        ifabsent: int(0)
    neg_int_slot:
        range: integer
        ifabsent: int(-117243)
    slot_uri_slot:
        range: uri
        ifabsent: slot_uri
    slot_curie_slot:
        ifabsent: slot_curie
    string_slot:
        ifabsent: string(s1)
    mt_string_slot:
        ifabsent: string()

classes:
    HighClass:
        slots:
            - bool_true_slot
            - bool_false_slot
            - bnode_slot
            - class_curie_slot
            - class_uri_slot
            - default_ns_slot
            - default_range_slot
            - int_42_slot
            - int_0_slot
            - neg_int_slot
            - slot_uri_slot
            - slot_curie_slot
            - string_slot
            - mt_string_slot
"""


def test_ifabsent():
    """
    Tests pythongenerator

    See: https://github.com/linkml/linkml/issues/1333
    """
    m = compile_python(PythonGenerator(model_txt).serialize())
    sample = m.HighClass()
    assert sample.bool_true_slot is True
    assert sample.bool_false_slot is False
    # TODO: class_curie_slot fails
    # assert sample.class_curie_slot, m.HighClass.class_class_curie)
    assert sample.class_curie_slot is None
    # TODO: class_uri_slot fails
    # assert sample.class_uri_slot, m.HighClass.class_class_uri)
    assert sample.class_uri_slot is None

    # TODO: default_ns fails")
    # assert sample.default_ns_slot, 'ex')
    assert sample.default_ns_slot is None
    # TODO: default_range fails
    # assert sample.default_range_slot, 'string')
    assert sample.default_range_slot is None
    # TODO: int(0) fails
    assert sample.int_0_slot == 0
    assert sample.int_42_slot == 42
    assert sample.neg_int_slot == -117243
    # TODO: slot_curie fails
    # assert sample.slot_curie_slot, m.slots.slot_curie_slot.curie)
    assert sample.slot_curie_slot is None
    # TODO: slot_uri fails
    # assert sample.slot_uri_slot, m.slots.slot_uri_slot.uri)
    assert sample.slot_uri_slot is None
    assert sample.slot_curie_slot is None
    assert sample.string_slot == "s1"
    assert sample.mt_string_slot == ""


@pytest.mark.skip("TODO: https://github.com/linkml/linkml/issues/1334")
def test_ifabsent_pydantic():
    """
    Tests pydantic generator.

    See: https://github.com/linkml/linkml/issues/1334
    """
    m = compile_python(PydanticGenerator(model_txt).serialize())
    sample = m.HighClass()
    assert sample.bool_true_slot is True
    assert sample.bool_false_slot is False
    # TODO: class_curie_slot fails
    # assert sample.class_curie_slot, m.HighClass.class_class_curie)
    assert sample.class_curie_slot is None
    # TODO: class_uri_slot fails
    # assert sample.class_uri_slot, m.HighClass.class_class_uri)
    assert sample.class_uri_slot is None
    # TODO: default_ns fails
    assert sample.default_ns_slot == "ex"
    # TODO: default_range fails
    # assert sample.default_range_slot, 'string')
    assert sample.default_range_slot is None
    # TODO: int(0) fails
    assert sample.int_0_slot == 0
    assert sample.int_42_slot == 42
    assert sample.neg_int_slot == -117243
    # TODO: slot_curie fails
    # assert sample.slot_curie_slot, m.slots.slot_curie_slot.curie)
    assert sample.slot_curie_slot is None
    # TODO: slot_uri fails
    # assert sample.slot_uri_slot, m.slots.slot_uri_slot.uri)
    assert sample.slot_uri_slot is None
    assert sample.slot_curie_slot is None
    assert sample.string_slot == "s1"
    assert sample.mt_string_slot == ""
