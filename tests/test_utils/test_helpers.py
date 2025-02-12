from linkml_runtime.linkml_model import ClassDefinition, SchemaDefinition, SlotDefinition
from linkml_runtime.utils.schemaview import SchemaView

from linkml.utils.helpers import is_simple_dict
from linkml.utils.schema_builder import SchemaBuilder

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
