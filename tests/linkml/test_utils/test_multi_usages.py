import pytest

from linkml.utils.schemaloader import SchemaLoader
from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml_runtime.utils.yamlutils import as_yaml


def _eval_expected(
    schema: SchemaDefinition,
    slotname: str,
    alias: str | None,
    domain_of: str,
    is_a: str | None,
    usage_slot_name: str | None,
    range: str,
) -> None:
    slot = schema.slots[slotname]
    assert slotname == slot.name
    if alias:
        assert alias == slot.alias
    else:
        assert slot.alias is None
    assert [domain_of] == slot.domain_of
    if is_a:
        assert is_a == slot.is_a
    else:
        assert slot.is_a is None
    if usage_slot_name:
        assert usage_slot_name == slot.usage_slot_name
    else:
        assert slot.usage_slot_name is None
    assert range == slot.range


def test_multi_usages(input_path, snapshot):
    """Slot usage chain without starting alias"""
    schema = SchemaLoader(input_path("multi_usages.yaml")).resolve()
    _eval_expected(schema, "s1", None, "root_class", None, None, "string")
    _eval_expected(schema, "child_class1_s1", "s1", "child_class1", "s1", "s1", "boolean")
    _eval_expected(
        schema,
        "child_class2_s1",
        "s1",
        "child_class2",
        "child_class1_s1",
        "s1",
        "integer",
    )
    _eval_expected(
        schema,
        "child_class3_s1",
        "s1",
        "child_class3",
        "child_class2_s1",
        "s1",
        "integer",
    )
    assert as_yaml(schema) == snapshot("multi_usages.yaml")


def test_multi_usages_2(input_path, snapshot):
    """Slot usage chain with starting alias"""
    schema = SchemaLoader(input_path("multi_usages_2.yaml")).resolve()
    _eval_expected(schema, "s1", "value", "root_class", None, None, "string")
    _eval_expected(schema, "child_class1_s1", "value", "child_class1", "s1", "s1", "boolean")
    _eval_expected(
        schema,
        "child_class2_s1",
        "value",
        "child_class2",
        "child_class1_s1",
        "s1",
        "integer",
    )
    _eval_expected(
        schema,
        "child_class3_s1",
        "value",
        "child_class3",
        "child_class2_s1",
        "s1",
        "integer",
    )
    assert as_yaml(schema) == snapshot("multi_usages_2.yaml")


def test_multi_usages_3(input_path):
    """Illegal alias usage"""
    expected_message = 'Class: "child_class1" - alias not permitted in slot_usage slot: foo'
    with pytest.raises(ValueError, match=expected_message):
        SchemaLoader(input_path("multi_usages_3.yaml")).resolve()


def test_deep_slot_usage_no_orphan(input_path):
    """Regression test: deep slot_usage chains must not leave orphan bare slot names.

    When a leaf class (Dog) both explicitly lists a slot (sound) in its ``slots:``
    and refines it via ``slot_usage:``, and every ancestor in the chain has also
    done the same (creating Canine_sound, Mammal_sound), the proximal parent slot
    seen by process_slot_usages is already a mangled name (Canine_sound) rather
    than the bare name.  Before the fix the bare ``sound`` was never removed from
    Dog.slots, leaving a duplicate alongside the newly-crafted ``Dog_sound``.
    """
    schema = SchemaLoader(input_path("deep_slot_usage.yaml")).resolve()
    dog_cls = schema.classes["Dog"]

    # Only the mangled slot should be present; bare name must be gone.
    assert "sound" not in dog_cls.slots, (
        "Orphan bare slot 'sound' found in Dog.slots — it should have been replaced by 'Dog_sound'"
    )
    assert "Dog_sound" in dog_cls.slots

    # These three calls together assert that the full is_a chain of mangled
    # slots was built correctly
    _eval_expected(
        schema,
        "Mammal_sound",  # mangled slot name
        "sound",  # alias (inherited from original slot)
        "Mammal",  # owned by
        "sound",  # is_a (inherited from original slot)
        "sound",  # original name of the slot being refined
        "integer",  # narrowed range
    )
    _eval_expected(
        schema,
        "Canine_sound",  # mangled slot name
        "sound",  # alias (inherited from original slot)
        "Canine",  # owned by
        "Mammal_sound",  # is_a: the parent mangled slot
        "sound",  # usage_slot_name: original bare slot name
        "boolean",  # narrowed range
    )
    _eval_expected(
        schema,
        "Dog_sound",  # mangled slot name
        "sound",  # alias (inherited from original slot)
        "Dog",  # owned by
        "Canine_sound",  # is_a: the parent mangled slot
        "sound",  # usage_slot_name: original bare slot name
        "string",  # narrowed range
    )
