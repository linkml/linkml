"""Tests of the linter's slot_group integrity rule."""

from linkml.linter.config.datamodel.config import RuleConfig, RuleLevel
from linkml.linter.linter import LinterProblem
from linkml.linter.rules import NoInvalidSlotGroupRule
from linkml_runtime.utils.schemaview import SchemaView


def check_schema(test_schema: str) -> list[LinterProblem]:
    """Check a schema using the NoInvalidSlotGroupRule linter.

    :param test_schema: schema to test, as a string
    :type test_schema: str
    :return: list of linting problems discovered
    :rtype: list[LinterProblem]
    """
    schema_view = SchemaView(test_schema)
    config = RuleConfig(level=RuleLevel.error.text)

    rule = NoInvalidSlotGroupRule(config)
    return list(rule.check(schema_view, fix=False))


def test_valid_slot_group() -> None:
    """A slot_group that names a slot marked is_grouping_slot: true is valid."""
    test_schema = """id: http://example.org/test_slot_group
name: test_slot_group
slots:
  section_header:
    is_grouping_slot: true
  member_slot:
    slot_group: section_header
"""
    assert not check_schema(test_schema)


def test_no_slot_group() -> None:
    """A slot with no slot_group produces no problems."""
    test_schema = """id: http://example.org/test_slot_group
name: test_slot_group
slots:
  plain_slot:
"""
    assert not check_schema(test_schema)


def test_undefined_slot_group() -> None:
    """A slot_group naming something that is not a defined slot is an error."""
    test_schema = """id: http://example.org/test_slot_group
name: test_slot_group
slots:
  member_slot:
    slot_group: Not A Slot
"""
    problems = check_schema(test_schema)
    assert len(problems) == 1
    assert problems[0].message == "Slot 'member_slot' has slot_group 'Not A Slot' which is not a defined slot."


def test_non_grouping_slot_group() -> None:
    """A slot_group naming a defined slot that is not a grouping slot is an error."""
    test_schema = """id: http://example.org/test_slot_group
name: test_slot_group
slots:
  ordinary_slot:
  member_slot:
    slot_group: ordinary_slot
"""
    problems = check_schema(test_schema)
    assert len(problems) == 1
    assert (
        problems[0].message
        == "Slot 'member_slot' has slot_group 'ordinary_slot' which is not marked 'is_grouping_slot: true'."
    )


def test_slot_group_in_slot_usage() -> None:
    """slot_group asserted in a class's slot_usage is also checked."""
    test_schema = """id: http://example.org/test_slot_group
name: test_slot_group
slots:
  member_slot:
classes:
  SomeClass:
    slots:
      - member_slot
    slot_usage:
      member_slot:
        slot_group: Not A Slot
"""
    problems = check_schema(test_schema)
    assert len(problems) == 1
    assert (
        problems[0].message
        == "Class 'SomeClass' slot_usage 'member_slot' has slot_group 'Not A Slot' which is not a defined slot."
    )
