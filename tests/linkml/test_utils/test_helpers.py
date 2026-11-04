import jsonschema
import pytest

from linkml.utils.helpers import format_checker_for, is_simple_dict
from linkml_runtime.linkml_model import ClassDefinition, SchemaDefinition, SlotDefinition
from linkml_runtime.utils.schema_builder import SchemaBuilder
from linkml_runtime.utils.schemaview import SchemaView

SCHEMA = SchemaDefinition(
    id="testschema",
    name="testschema",
    classes=[
        ClassDefinition(name="MyClass"),
    ],
)


def test_is_simple_dict():
    sb = SchemaBuilder()
    sb.add_class(
        "SimpleDictItem",
        [
            SlotDefinition("id", identifier=True),
            SlotDefinition("value", range="string"),
        ],
        use_attributes=True,
    )
    sb.add_class(
        "DictionaryItem1",
        [
            SlotDefinition("id", identifier=True),
            SlotDefinition("value", range="string"),
            SlotDefinition("another_value", range="string"),
        ],
        use_attributes=True,
    )
    sb.add_class(
        "DictionaryItem2",
        [
            SlotDefinition("id", range="string"),
            SlotDefinition("value", range="string"),
            SlotDefinition("another_value", range="string"),
        ],
        use_attributes=True,
    )
    simple_dict_slot = SlotDefinition(
        "simple_dict", inlined=True, inlined_as_list=False, multivalued=True, range="SimpleDictItem"
    )
    no_simple_dict_slot_1 = SlotDefinition(
        "no_simple_dict1", inlined=True, inlined_as_list=False, multivalued=True, range="DictionaryItem1"
    )
    no_simple_dict_slot_2 = SlotDefinition(
        "no_simple_dict2", inlined=True, inlined_as_list=False, multivalued=True, range="DictionaryItem2"
    )
    sb.add_class("C", [simple_dict_slot, no_simple_dict_slot_1, no_simple_dict_slot_2])

    sv = SchemaView(sb.schema)

    assert is_simple_dict(sv, simple_dict_slot)
    assert not is_simple_dict(sv, no_simple_dict_slot_1)
    assert not is_simple_dict(sv, no_simple_dict_slot_2)


@pytest.mark.parametrize(
    ("format_name", "value"),
    [("uri", "https://example.org/x"), ("date-time", "2020-01-01T00:00:00Z"), ("time", "00:00:00Z")],
)
def test_format_checker_refuses_a_final_newline(format_name, value):
    """A value conforms to its format without a final newline and does not with one."""
    checker = format_checker_for(jsonschema.Draft201909Validator)
    assert checker.conforms(value, format_name)
    assert not checker.conforms(value + "\n", format_name)
