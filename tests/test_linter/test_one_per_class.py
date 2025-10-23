"""Tests of the linter's one per class checks."""

import pytest
from linkml_runtime import SchemaView

from linkml.linter.config.datamodel.config import RuleConfig, RuleLevel
from linkml.linter.linter import LinterProblem
from linkml.linter.rules import OneIdentifierPerClass, OneKeyPerClass

EMPTY = ""
ID = "identifier"
KEY = "key"


def check_schema(test_schema: str, check_identifier: bool) -> list[LinterProblem]:  # noqa: FBT001
    """Check a schema using a OnePerClass linter.

    :param test_schema: schema to test, as a string
    :type test_schema: str
    :param check_identifier: whether to check the `identifier` field or the `key` field
    :type check_identifier: bool
    :return: list of linting problems discovered
    :rtype: list[LinterProblem]
    """
    schema_view = SchemaView(test_schema)
    config = RuleConfig(level=RuleLevel.error.text)

    rule = OneIdentifierPerClass(config) if check_identifier else OneKeyPerClass(config)
    return list(rule.check(schema_view, fix=False))


@pytest.fixture(scope="module")
def identifier_key_schema() -> str:
    """Return a schema that defines a set of slots with identifiers and keys, and a test class to populate."""
    return """
# yaml-language-server: $schema=https://linkml.io/linkml-model/linkml_model/jsonschema/meta.schema.json
id: https://w3id.org/linkml/examples/identifiers
title: Identifiers, Keys, Primary Keys, and More!
name: identifiers
description: Schema for testing identifiers, keys, primary keys, and much, much more.

prefixes:
  ex: https://w3id.org/linkml/examples/patterns/

default_prefix: ex

slots:
  slot_a:
  slot_b:
  id_slot_a:
    identifier: true
  id_slot_b:
    identifier: true
  id_slot_false:
    identifier: false
  key_slot_a:
    key: true
  key_slot_b:
    key: true
  key_slot_false:
    key: false
  pk_slot_a:
    annotations:
      primary_key: true
  pk_slot_b:
    annotations:
      primary_key: true
  pk_slot_false:
    annotations:
      primary_key: false

classes:
  TestClass:
    slots:
      - slot_a
      - slot_b
"""


@pytest.mark.parametrize("id_slot_a", [EMPTY, "id_slot_a"])
@pytest.mark.parametrize("id_slot_b", [EMPTY, "id_slot_b"])
@pytest.mark.parametrize("id_slot_false", [EMPTY, "id_slot_false"])
@pytest.mark.parametrize("key_slot_a", [EMPTY, "key_slot_a"])
@pytest.mark.parametrize("key_slot_b", [EMPTY, "key_slot_b"])
@pytest.mark.parametrize("key_slot_false", [EMPTY, "key_slot_false"])
def test_get_identifier_get_key_slot(
    identifier_key_schema: str,
    id_slot_a: str,
    id_slot_b: str,
    id_slot_false: str,
    key_slot_a: str,
    key_slot_b: str,
    key_slot_false: str,
) -> None:
    """Test the detection of multiple "identifier" and "key" slots in classes in the schema.

    The parameters represent the slots to be added to the test class; if the value of the parameter is EMPTY,
    the slot is not added. If the parameter is a string, that slot is added to the test class.

    For example, given the following set of parameters:

    id_slot_a: "id_slot_a"
    id_slot_b: EMPTY
    id_slot_false: "id_slot_false"
    key_slot_a: EMPTY
    key_slot_b: EMPTY
    key_slot_false: "key_slot_false"

    The following lines would be added to the bottom of the identifier_key_schema:

          - id_slot_a
          - id_slot_false
          - key_slot_false

    resulting in the following structure for `TestClass`:

    classes:
      TestClass:
        slots:
          - slot_a
          - slot_b
          - id_slot_a
          - id_slot_false
          - key_slot_false

    This allows the testing of a large number of combinations without having to generate them all manually.
    """
    all_id_slots = [id_slot_a, id_slot_b, id_slot_false]
    all_key_slots = [key_slot_a, key_slot_b, key_slot_false]

    for k in [*all_id_slots, *all_key_slots]:
        if k:
            identifier_key_schema += f"      - {k}\n"

    sv = SchemaView(identifier_key_schema)
    test_class_slots = sv.class_slots("TestClass")
    # ensure that the correct slots are in the schema
    assert set(test_class_slots) == {"slot_a", "slot_b", *[s for s in [*all_id_slots, *all_key_slots] if s]}

    # Collect the expected slots to be returned by `get_***_slot` for identifiers and keys.
    # Note that id_slot_false and key_slot_false have `identifier` and `key` set to `false`,
    # so we would not expect `get_identifier_slot` or `get_key_slot` to return these slots.
    # If the value from the parameters is EMPTY, the attribute is not present and should be deleted.
    exp_slots = {ID: {id_slot_a, id_slot_b}, KEY: {key_slot_a, key_slot_b}}
    for slot_set in exp_slots.values():
        slot_set.discard(EMPTY)

    problems = {
        ID: check_schema(identifier_key_schema, check_identifier=True),
        KEY: check_schema(identifier_key_schema, check_identifier=False),
    }

    for attr_type, val in exp_slots.items():
        # if there is more than one slot of the identifier or key type present, we expect an error
        if len(val) > 1:
            assert len(problems[attr_type]) == 1
            msg = f"Class 'TestClass' has more than one '{attr_type}' slot: "
            msg += ", ".join(sorted(val))
            assert {p.message for p in problems[attr_type]} == {msg}
        else:
            assert problems[attr_type] == []
