from typing import Optional

import pytest
from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml_runtime.utils.yamlutils import as_yaml

from linkml.utils.schemaloader import SchemaLoader


def _eval_expected(
    schema: SchemaDefinition,
    slotname: str,
    alias: Optional[str],
    domain_of: str,
    is_a: Optional[str],
    usage_slot_name: Optional[str],
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
