from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import ClassDefinition, EnumDefinition, SlotDefinition

from linkml.linter.config.datamodel.config import RecommendedRuleConfig, RuleLevel
from linkml.linter.rules import RecommendedRule
from linkml.utils.schema_builder import SchemaBuilder


def test_missing_descriptions():
    builder = SchemaBuilder()
    builder.add_class("MyClass")
    builder.add_slot("my_slot")
    builder.add_enum("MyEnum")

    schema_view = SchemaView(builder.schema)
    config = RecommendedRuleConfig(level=RuleLevel.error.text, include=[], exclude=[])

    rule = RecommendedRule(config)
    problems = list(rule.check(schema_view))
    assert len(problems) == 3

    messages = [p.message for p in problems]
    assert "Class 'MyClass' does not have recommended slot 'description'" in messages
    assert "Slot 'my_slot' does not have recommended slot 'description'" in messages
    assert "Enum 'MyEnum' does not have recommended slot 'description'" in messages


def test_present_descriptions():
    builder = SchemaBuilder()
    builder.add_class(ClassDefinition(name="MyClass", description="this is my class"))
    builder.add_slot(SlotDefinition(name="my_slot", description="this is my slot"))
    builder.add_enum(EnumDefinition(name="MyEnum", description="this is my enum"))

    schema_view = SchemaView(builder.schema)
    config = RecommendedRuleConfig(level=RuleLevel.error.text, include=[], exclude=[])

    rule = RecommendedRule(config)
    problems = list(rule.check(schema_view))
    assert len(problems) == 0


def test_include():
    builder = SchemaBuilder()
    builder.add_class("MyClass")
    builder.add_slot("my_slot")
    builder.add_enum("MyEnum")

    schema_view = SchemaView(builder.schema)
    config = RecommendedRuleConfig(level=RuleLevel.error.text, include=["my_slot"], exclude=[])

    rule = RecommendedRule(config)
    problems = list(rule.check(schema_view))
    assert len(problems) == 1

    messages = [p.message for p in problems]
    assert "Slot 'my_slot' does not have recommended slot 'description'" in messages


def test_exclude():
    builder = SchemaBuilder()
    builder.add_class("MyClass")
    builder.add_slot("my_slot")
    builder.add_enum("MyEnum")

    schema_view = SchemaView(builder.schema)
    config = RecommendedRuleConfig(level=RuleLevel.error.text, include=[], exclude=["my_slot"])

    rule = RecommendedRule(config)
    problems = list(rule.check(schema_view))
    assert len(problems) == 2

    messages = [p.message for p in problems]
    assert "Class 'MyClass' does not have recommended slot 'description'" in messages
    assert "Enum 'MyEnum' does not have recommended slot 'description'" in messages


def test_class_violation_allowed():
    config = RecommendedRuleConfig(
        level=RuleLevel.error.text,
        exclude_type=["class_definition"],
    )

    builder = SchemaBuilder()
    builder.add_class("MyClass")

    rule = RecommendedRule(config)

    problems = list(rule.check(SchemaView(builder.schema)))

    assert len(problems) == 0


def test_slot_violation_allowed():
    config = RecommendedRuleConfig(
        level=RuleLevel.error.text,
        exclude_type=["slot_definition"],
    )

    builder = SchemaBuilder()
    builder.add_slot("my_slot")

    rule = RecommendedRule(config)

    problems = list(rule.check(SchemaView(builder.schema)))

    assert len(problems) == 0


def test_enum_violation_allowed():
    config = RecommendedRuleConfig(
        level=RuleLevel.error.text,
        exclude_type=["enum_definition"],
    )

    builder = SchemaBuilder()
    builder.add_enum("MyEnum")

    rule = RecommendedRule(config)

    problems = list(rule.check(SchemaView(builder.schema)))

    assert len(problems) == 0


# todo PVs are not checked for recommended fields yet
