from typing import Optional, Union, Any
from dataclasses import fields

import pytest

from linkml_runtime.utils.schema_builder import SchemaBuilder
from linkml_runtime.linkml_model import (
    ClassDefinition,
    SlotDefinition,
    EnumDefinition,
    PermissibleValue,
)


# === Tests for `SchemaBuilder.add_class` ===
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
    slots: Optional[list[Union[str, SlotDefinition]]], use_attributes: bool
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


@pytest.mark.parametrize(
    ("cls", "extra_kwargs", "expected_added_class"),
    [
        ("Person", {}, ClassDefinition(name="Person")),
        (2, {}, None),  # Invalid type for `cls`
        ("Person", {"tree_root": True}, ClassDefinition(name="Person", tree_root=True)),
        ("Person", {"ijk": True}, None),  # Invalid extra kwarg
        (
            {"name": "Person", "tree_root": False},
            {"tree_root": True},
            ClassDefinition(name="Person", tree_root=True),
        ),
        (
            {"name": "Person", "tree_root": False},
            {"ijk": True},  # Invalid extra kwarg
            None,
        ),
        (
            ClassDefinition(name="Person", tree_root=False),
            {"tree_root": True},
            ClassDefinition(name="Person", tree_root=True),
        ),
        (
            ClassDefinition(name="Person", tree_root=False),
            {"ijk": True},  # Invalid extra kwarg
            ClassDefinition(name="Person", tree_root=True),
        ),
    ],
)
def test_add_class_with_extra_kwargs(
    cls: Union[ClassDefinition, dict, str],
    extra_kwargs: dict[str, Any],
    expected_added_class: Optional[ClassDefinition],
):
    """
    Test adding a class with extra kwargs
    """
    # The meta slots or fields of `ClassDefinition`
    class_meta_slots = {f.name for f in fields(ClassDefinition)}

    builder = SchemaBuilder()

    if not isinstance(cls, (str, dict, ClassDefinition)):
        with pytest.raises(TypeError, match="cls must be"):
            builder.add_class(cls, **extra_kwargs)
    elif extra_kwargs.keys() - class_meta_slots:
        # Handle the case of extra kwargs include a key that is not a meta slot of
        # `ClassDefinition`
        with pytest.raises((ValueError, TypeError)):
            builder.add_class(cls, **extra_kwargs)
    else:
        builder.add_class(cls, **extra_kwargs)

        if isinstance(cls, str):
            class_name = cls
        elif isinstance(cls, dict):
            class_name = cls["name"]
        else:
            class_name = cls.name

        added_class = builder.schema.classes[class_name]

        assert added_class == expected_added_class


# === Tests for `SchemaBuilder.add_class` end ===


# === Tests for `SchemaBuilder.add_enum` ===
@pytest.mark.parametrize(
    ("enum_def", "permissible_values", "expected_added_enum"),
    [
        (EnumDefinition(name="Color"), [], EnumDefinition(name="Color")),
        # invalid permissible values
        (EnumDefinition(name="Color"), ["RED", 3], EnumDefinition(name="Color")),
        (
            EnumDefinition(name="Color"),
            ["RED", "BLUE"],
            EnumDefinition(
                name="Color",
                permissible_values=[PermissibleValue("RED"), PermissibleValue("BLUE")],
            ),
        ),
        (
            EnumDefinition(name="Color", permissible_values=[PermissibleValue("RED")]),
            [PermissibleValue("RED", description="A bright color"), "B"],
            EnumDefinition(
                name="Color",
                permissible_values=[
                    PermissibleValue("RED", description="A bright color"),
                    PermissibleValue("B"),
                ],
            ),
        ),
    ],
)
def test_add_enum_with_extra_permissible_values(
    enum_def: EnumDefinition,
    permissible_values: list[Union[str, PermissibleValue]],
    expected_added_enum: Optional[EnumDefinition],
):
    """
    Test adding an enum with extra, overriding, permissible values
    """
    builder = SchemaBuilder()

    if any(not isinstance(pv, (str, PermissibleValue)) for pv in permissible_values):
        with pytest.raises(TypeError, match="permissible value must be"):
            builder.add_enum(enum_def, permissible_values=permissible_values)
    else:
        builder.add_enum(enum_def, permissible_values=permissible_values)
        assert builder.schema.enums[enum_def.name] == expected_added_enum


# === Tests for `SchemaBuilder.add_enum` ===
@pytest.mark.parametrize(
    ("enum_def", "extra_kwargs", "expected_added_enum"),
    [
        ("Color", {}, EnumDefinition(name="Color")),
        (42, {}, None),  # Invalid type for `enum_def`
        (
            "Color",
            {"description": "What meets the eyes"},
            EnumDefinition(name="Color", description="What meets the eyes"),
        ),
        (
            {"name": "Color", "description": "It's obvious"},
            {"description": "What meets the eyes"},
            EnumDefinition(name="Color", description="What meets the eyes"),
        ),
        (
            EnumDefinition("Color"),
            {"description": "What meets the eyes"},
            EnumDefinition(name="Color"),
        ),
        (
            "Color",
            {"description": "What meets the eyes", "ijk": True},  # Invalid extra kwarg
            None,
        ),
    ],
)
def test_add_enum_with_extra_kwargs(
    enum_def: Union[EnumDefinition, dict, str],
    extra_kwargs: dict[str, Any],
    expected_added_enum: Optional[EnumDefinition],
):
    """
    Test adding an enum with extra kwargs
    """
    enum_meta_slots = {f.name for f in fields(EnumDefinition)}

    builder = SchemaBuilder()

    if not isinstance(enum_def, (str, dict, EnumDefinition)):
        with pytest.raises(TypeError, match="enum_def must be"):
            builder.add_enum(enum_def, **extra_kwargs)
    elif extra_kwargs.keys() - enum_meta_slots:
        # Handle the case of extra kwargs include a key that is not a meta slot of
        # `EnumDefinition`
        with pytest.raises(TypeError):
            builder.add_enum(enum_def, **extra_kwargs)
    else:
        builder.add_enum(enum_def, **extra_kwargs)

        if isinstance(enum_def, str):
            enum_name = enum_def
        elif isinstance(enum_def, dict):
            enum_name = enum_def["name"]
        else:
            enum_name = enum_def.name

        added_enum = builder.schema.enums[enum_name]

        assert added_enum == expected_added_enum

# === Tests for `SchemaBuilder.add_enum` end ===