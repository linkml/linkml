import unittest

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import ClassDefinition, EnumDefinition, SlotDefinition

from linkml.linter.config.datamodel.config import RecommendedRuleConfig, RuleLevel
from linkml.linter.rules import RecommendedRule
from linkml.utils.schema_builder import SchemaBuilder


class TestRecommendedRule(unittest.TestCase):
    def test_missing_descriptions(self):
        builder = SchemaBuilder()
        builder.add_class("MyClass")
        builder.add_slot("my_slot")
        builder.add_enum("MyEnum")

        schema_view = SchemaView(builder.schema)
        config = RecommendedRuleConfig(level=RuleLevel.error.text, include=[], exclude=[])

        rule = RecommendedRule(config)
        problems = list(rule.check(schema_view))
        self.assertEqual(len(problems), 3)

        messages = [p.message for p in problems]
        self.assertIn(
            "Class 'MyClass' does not have recommended slot 'description'",
            messages,
        )
        self.assertIn(
            "Slot 'my_slot' does not have recommended slot 'description'",
            messages,
        )
        self.assertIn(
            "Enum 'MyEnum' does not have recommended slot 'description'",
            messages,
        )

    def test_present_descriptions(self):
        builder = SchemaBuilder()
        builder.add_class(ClassDefinition(name="MyClass", description="this is my class"))
        builder.add_slot(SlotDefinition(name="my_slot", description="this is my slot"))
        builder.add_enum(EnumDefinition(name="MyEnum", description="this is my enum"))

        schema_view = SchemaView(builder.schema)
        config = RecommendedRuleConfig(level=RuleLevel.error.text, include=[], exclude=[])

        rule = RecommendedRule(config)
        problems = list(rule.check(schema_view))
        self.assertEqual(len(problems), 0)

    def test_include(self):
        builder = SchemaBuilder()
        builder.add_class("MyClass")
        builder.add_slot("my_slot")
        builder.add_enum("MyEnum")

        schema_view = SchemaView(builder.schema)
        config = RecommendedRuleConfig(level=RuleLevel.error.text, include=["my_slot"], exclude=[])

        rule = RecommendedRule(config)
        problems = list(rule.check(schema_view))
        self.assertEqual(len(problems), 1)

        messages = [p.message for p in problems]
        self.assertIn(
            "Slot 'my_slot' does not have recommended slot 'description'",
            messages,
        )

    def test_exclude(self):
        builder = SchemaBuilder()
        builder.add_class("MyClass")
        builder.add_slot("my_slot")
        builder.add_enum("MyEnum")

        schema_view = SchemaView(builder.schema)
        config = RecommendedRuleConfig(level=RuleLevel.error.text, include=[], exclude=["my_slot"])

        rule = RecommendedRule(config)
        problems = list(rule.check(schema_view))
        self.assertEqual(len(problems), 2)

        messages = [p.message for p in problems]
        self.assertIn(
            "Class 'MyClass' does not have recommended slot 'description'",
            messages,
        )
        self.assertIn(
            "Enum 'MyEnum' does not have recommended slot 'description'",
            messages,
        )
