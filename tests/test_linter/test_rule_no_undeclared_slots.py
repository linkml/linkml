"""Tests of the linter's missing slots rules."""

from linkml_runtime.utils.schemaview import SchemaView

from linkml.linter.config.datamodel.config import RuleConfig, RuleLevel
from linkml.linter.rules import NoUndeclaredSlotsRule


def test_undeclared_slots() -> None:
    """Test that slots that appear under a class but not in the main `slots` declaration throw an error."""
    test_schema = """id: http://example.org/test_undeclared_slots
name: slot_test
default_range: string
slots:
  name:

classes:
  class_1:
    slots:
      - name
      - id

  class_2:
    attributes:
      name:
      description:
"""
    schema_view = SchemaView(test_schema)
    config = RuleConfig(level=RuleLevel.error.text)

    rule = NoUndeclaredSlotsRule(config)
    problems = list(rule.check(schema_view, fix=False))

    # `id` from class_1 is not declared in `slots`
    # `description` from class_2 is an attribute so it doesn't need to be in `slots`
    assert len(problems) == 1
    assert problems[0].message == "Slot 'id' from class 'class_1' not found in schema 'slots' declaration."


def test_valid_slot_usage() -> None:
    """Test that a valid schema does not throw an error."""
    test_schema = """id: http://example.org/test_undeclared_slots
name: slot_test
default_range: string
slots:
  name:
  id:

classes:
  class_1:
    slots:
      - name
      - id

  class_2:
    attributes:
      name:
      description:
"""
    schema_view = SchemaView(test_schema)
    config = RuleConfig(level=RuleLevel.error.text)

    rule = NoUndeclaredSlotsRule(config)
    problems = list(rule.check(schema_view, fix=False))

    assert not problems
