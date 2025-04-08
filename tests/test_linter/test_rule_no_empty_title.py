import yaml
from linkml_runtime import SchemaView

from linkml.linter.config.datamodel.config import RuleConfig, RuleLevel
from linkml.linter.linter import Linter
from linkml.linter.rules import NoEmptyTitleRule
from linkml.utils.schema_builder import SchemaBuilder


def test_elements_with_empty_title():
    builder = SchemaBuilder()
    builder.add_class("AClass")
    builder.add_slot("a_slot")
    builder.add_enum("AnEnum")
    builder.add_type("a_type")
    builder.add_class("WithTitle", title="With title")

    schema_view = SchemaView(builder.schema)
    config = RuleConfig(level=RuleLevel.error.text)

    rule = NoEmptyTitleRule(config)
    problems = list(rule.check(schema_view))

    assert len(problems) == 4

    messages = [p.message for p in problems]
    assert "Class 'AClass' has no title" in messages
    assert "Slot 'a_slot' has no title" in messages
    assert "Enum 'AnEnum' has no title" in messages
    assert "Type 'a_type' has no title" in messages


def test_class_violation_allowed():
    config = yaml.safe_load(
        """
rules:
  no_empty_title:
    level: error
    exclude_type:
      - class_definition
"""
    )

    builder = SchemaBuilder()
    builder.add_class("MyClass")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    assert len(messages) == 0


def test_slot_violation_allowed():
    config = yaml.safe_load(
        """
rules:
  no_empty_title:
    level: error
    exclude_type:
      - slot_definition
"""
    )

    builder = SchemaBuilder()
    builder.add_slot("my_slot")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    assert len(messages) == 0


def test_enum_violation_allowed():
    config = yaml.safe_load(
        """
rules:
  no_empty_title:
    level: error
    exclude_type:
      - enum_definition
"""
    )

    builder = SchemaBuilder()
    builder.add_enum("MyEnum")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    assert len(messages) == 0


# todo PVs are not checked for titles yet
