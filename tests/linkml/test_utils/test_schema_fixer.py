"""
Tests SchemaFixer
"""

from copy import deepcopy

import pytest
from linkml_runtime.linkml_model import SlotDefinition, SlotDefinitionName

from linkml.utils.schema_builder import SchemaBuilder
from linkml.utils.schema_fixer import SchemaFixer

MY_CLASS = "MyClass"
MY_CLASS2 = "MyClass2"
MY_ENUM = "MyEnum"
ID = "id"
FULL_NAME = "full_name"
DESC = "description"
LIVING = "Living"
DEAD = "Dead"


def test_add_titles():
    b = SchemaBuilder()
    slots = [FULL_NAME, DESC]
    b.add_class(MY_CLASS, slots)
    b.add_enum(MY_ENUM, [LIVING, DEAD])
    s = b.schema
    fixer = SchemaFixer()
    fixer.add_titles(s)
    c = s.classes[MY_CLASS]
    e = s.enums[MY_ENUM]
    assert c.title == "my class"
    assert e.title == "my enum"
    assert s.slots[FULL_NAME].title == "full name"


def test_add_container():
    b = SchemaBuilder()
    slots = [FULL_NAME, DESC]
    b.add_class(MY_CLASS, slots)
    s = b.schema
    fixer = SchemaFixer()
    container_name = "MyContainer"
    fixer.add_container(s, class_name=container_name, convert_camel_case=True)
    c = s.classes[container_name]
    index_slot_name = SlotDefinitionName("my_class_index")
    assert [index_slot_name] == c.slots
    assert c.tree_root
    index_slot = s.slots[index_slot_name]
    assert index_slot.multivalued
    assert MY_CLASS == index_slot.range
    assert index_slot.inlined_as_list


def test_attributes_to_slots():
    b = SchemaBuilder()
    b.add_class(MY_CLASS, [SlotDefinition(FULL_NAME), SlotDefinition(DESC)])
    s = b.schema
    fixer = SchemaFixer()
    fixer.attributes_to_slots(s, remove_redundant_slot_usage=False)
    c = s.classes[MY_CLASS]
    assert [DESC, FULL_NAME] == sorted(c.slots)
    assert {} == c.attributes
    assert s.slots[FULL_NAME].name == FULL_NAME
    assert s.slots[DESC].name == DESC


def test_merge_slot_usage():
    b = SchemaBuilder()
    b.add_class(MY_CLASS)
    s = b.schema
    fixer = SchemaFixer()
    c = s.classes[MY_CLASS]
    fixer.merge_slot_usage(s, c, SlotDefinition(FULL_NAME, description="desc1", range="string"))
    su = c.slot_usage[FULL_NAME]
    assert "desc1" == su.description
    assert "string" == su.range
    fixer.merge_slot_usage(
        s,
        c,
        SlotDefinition(
            FULL_NAME,
            # description='desc2',
            comments=["comment1"],
            is_a="foo",
            range="string",
        ),
    )
    su = c.slot_usage[FULL_NAME]
    with pytest.raises(ValueError):
        fixer.merge_slot_usage(s, c, SlotDefinition(FULL_NAME, description="desc2"))
    assert "desc1" == su.description
    fixer.merge_slot_usage(s, c, SlotDefinition(FULL_NAME, description="desc2"), overwrite=True)
    su = c.slot_usage[FULL_NAME]
    assert "desc2" == su.description


def test_remove_redundant():
    """
    Tests
    """
    b = SchemaBuilder()
    s = b.schema
    slot1 = SlotDefinition(ID, title="identifier", description="unique identifier")
    slot2 = SlotDefinition(FULL_NAME, description="full name", range="string")
    slot3 = SlotDefinition(DESC, description="used to describe")
    b.add_class(MY_CLASS, [slot1.name, slot2.name, slot3.name])
    c = s.classes[MY_CLASS]
    # add a slot usage for ID that is intentionally partially redundant with the main slot
    # here the description is redundant
    c.slot_usage[ID] = SlotDefinition(
        ID,
        identifier=True,
        comments=["my comment1"],
        description="unique identifier",
    )
    # add a slot usage for full_name that is intentionally partially redundant with the main slot
    c.slot_usage[FULL_NAME] = SlotDefinition(FULL_NAME, range="string", description="full name", pattern="^.*$")
    # add a slot usage that is fully redundant
    c.slot_usage[DESC] = SlotDefinition(DESC, range="string")
    b.add_slot(deepcopy(slot1), replace_if_present=True).add_slot(deepcopy(slot2), replace_if_present=True)
    b.add_defaults()
    fixer = SchemaFixer()
    fixer.remove_redundant_slot_usage(s)
    # not-redundant; should be preserved
    assert c.slot_usage[ID].identifier is True
    assert c.slot_usage[ID].comments == ["my comment1"]
    assert c.slot_usage[FULL_NAME].pattern == "^.*$"
    # redundant; should be removed
    assert DESC not in c.slot_usage
    assert "description" not in c.slot_usage[ID]
    assert "range" not in c.slot_usage[FULL_NAME]


def test_attributes_to_slots_remove_redundant():
    b = SchemaBuilder()
    b.add_class(
        MY_CLASS,
        [
            SlotDefinition(ID, identifier=True),
            SlotDefinition(FULL_NAME, description="full name", range="string"),
            SlotDefinition(DESC, description="description"),
        ],
    )
    b.add_class(
        MY_CLASS2,
        [
            SlotDefinition(FULL_NAME, description="full name2", range="string"),
            SlotDefinition(DESC, description="description"),
        ],
        replace_if_present=True,
    )
    s = b.schema
    fixer = SchemaFixer()
    fixer.attributes_to_slots(s, remove_redundant_slot_usage=True)
    c = s.classes[MY_CLASS]
    assert [DESC, FULL_NAME, ID] == sorted(c.slots)
    assert {} == c.attributes
    assert s.slots[FULL_NAME].name == FULL_NAME
    assert s.slots[DESC].name == DESC


@pytest.mark.parametrize("preserve_original_using", [None, "title"])
def test_fix_element_names(preserve_original_using):
    b = SchemaBuilder()
    slots = {
        "a b": "a_b",
        "xyz": "xyz",
        "CamelSlot": "CamelSlot",
    }
    classes = {
        "foo_bar": "FooBar",
        "class with space": "ClassWithSpace",
    }
    for k in slots.keys():
        b.add_slot(k)
    for k in classes.keys():
        b.add_class(k)
    b.add_slot("foo bar ref", range="foo_bar")
    b.add_defaults()
    fixer = SchemaFixer()
    schema = b.schema
    fixed_schema = fixer.fix_element_names(schema, preserve_original_using=preserve_original_using)
    for v in slots.values():
        assert v in fixed_schema.slots
    for v in classes.values():
        assert v in fixed_schema.classes
        cls = fixed_schema.classes[v]
        if preserve_original_using:
            orig = getattr(cls, preserve_original_using)
            # print(cls.name, preserve_original_using, orig)
            assert classes[orig] == cls.name
    assert "FooBar" == fixed_schema.slots["foo_bar_ref"].range


def test_remove_redundant_slot_usage_issue_954(input_path):
    """
    Tests https://github.com/linkml/linkml/issues/954

    This test verifies that SchemaFixer.remove_redundant_slot_usage() correctly
    identifies and removes slot_usage entries that duplicate information already
    present in the slot definition.
    """
    # Using a minimal schema that demonstrates the redundant slot usage pattern
    from linkml_runtime import SchemaView

    schema_path = input_path("redundant_slot_usage.yaml")
    view = SchemaView(schema_path)
    s = view.schema
    fixer = SchemaFixer()
    fixer.remove_redundant_slot_usage(s)

    # Verify that many redundant fields were removed
    assert len(fixer.history) > 50

    # Check specific slot_usage to ensure correct behavior
    jgi = s.classes["soil_jgi_mg"].slot_usage
    jgi_ecosystem = jgi["ecosystem"]

    # These should remain because they're not in the base slot definition
    assert "slot_group" in jgi_ecosystem
    assert "required" in jgi_ecosystem
    assert "range" in jgi_ecosystem

    # These should be removed because they're redundant with the base slot
    assert "description" not in jgi_ecosystem
    assert "name" not in jgi_ecosystem
    assert "owner" not in jgi_ecosystem
