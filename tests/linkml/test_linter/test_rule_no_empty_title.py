from linkml_runtime import SchemaView

from linkml.linter.config.datamodel.config import NoEmptyTitleConfig, RuleConfig, RuleLevel
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
    config = NoEmptyTitleConfig(
        level=RuleLevel.error.text,
        exclude_type=["class_definition"],
    )

    rule = NoEmptyTitleRule(config)

    builder = SchemaBuilder()
    builder.add_class("MyClass")

    problems = list(rule.check(SchemaView(builder.schema)))

    assert len(problems) == 0


def test_slot_violation_allowed():
    config = NoEmptyTitleConfig(
        level=RuleLevel.error.text,
        exclude_type=["slot_definition"],
    )

    rule = NoEmptyTitleRule(config)

    builder = SchemaBuilder()
    builder.add_slot("my_slot")

    problems = list(rule.check(SchemaView(builder.schema)))

    assert len(problems) == 0


def test_enum_violation_allowed():
    config = NoEmptyTitleConfig(
        level=RuleLevel.error.text,
        exclude_type=["enum_definition"],
    )

    rule = NoEmptyTitleRule(config)

    builder = SchemaBuilder()
    builder.add_enum("MyEnum")

    problems = list(rule.check(SchemaView(builder.schema)))

    assert len(problems) == 0


# todo PVs are not checked for titles yet
