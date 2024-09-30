from typing import Optional, List, Union

import pytest

from linkml_runtime.utils.schema_builder import SchemaBuilder
from linkml_runtime.linkml_model import ClassDefinition, SlotDefinition


@pytest.mark.parametrize("replace_if_present", [True, False])
def test_add_existing_class(replace_if_present):
    """
    Test the case of adding a class with a name that is the same as a class that already
    exists in the schema
    """
    builder = SchemaBuilder()

    cls_name = "Person"

    # Add a class to the schema
    cls = ClassDefinition(name=cls_name, slots=["name"])
    builder.add_class(cls)

    # Add another class with the same name to the schema
    cls_repeat = ClassDefinition(name=cls_name, slots=["age"])

    if replace_if_present:
        builder.add_class(cls_repeat, replace_if_present=True)
        assert builder.schema.classes[cls_name].slots == ["age"]
    else:
        with pytest.raises(ValueError, match=f"Class {cls_name} already exists"):
            builder.add_class(cls_repeat)
        assert builder.schema.classes[cls_name].slots == ["name"]


@pytest.mark.parametrize(
    "slots",
    [
        None,
        ["name", "age"],
        ["name", SlotDefinition(name="age")],
        [SlotDefinition(name="name"), SlotDefinition(name="age")],
    ],
)
@pytest.mark.parametrize("use_attributes", [True, False])
def test_add_class_with_slot_additions(
    slots: Optional[List[Union[str, SlotDefinition]]], use_attributes: bool
):
    """
    Test adding a class with separate additional slots specification
    """
    # If `slots` is None, it should be treated as if it were an empty list
    if slots is None:
        slots = []

    slot_names = {s if isinstance(s, str) else s.name for s in slots}

    builder = SchemaBuilder()

    cls_name = "Person"

    # Add a class to the schema
    cls = ClassDefinition(name=cls_name)

    if use_attributes:
        # === The case where the slots specified should be added to the `attributes`
        # meta slot of the class ===
        if any(not isinstance(s, SlotDefinition) for s in slots):
            with pytest.raises(
                ValueError,
                match="If use_attributes=True then slots must be SlotDefinitions",
            ):
                builder.add_class(cls, slots=slots, use_attributes=use_attributes)
        else:
            builder.add_class(cls, slots=slots, use_attributes=use_attributes)
            assert builder.schema.classes[cls_name].attributes.keys() == slot_names
    else:
        # === The case where the slots specified should be added to the `slots`
        # meta slot of the schema ===
        builder.add_class(cls, slots=slots, use_attributes=use_attributes)
        assert builder.schema.slots.keys() == slot_names
