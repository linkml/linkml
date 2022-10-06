import unittest

from linkml_runtime import SchemaView

from linkml.linter.config.datamodel.config import RuleConfig, RuleLevel
from linkml.linter.rules import NoEmptyTitleRule
from linkml.utils.schema_builder import SchemaBuilder


class TestRuleNoEmptyTitle(unittest.TestCase):
    def test_elements_with_empty_title(self):
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

        self.assertEqual(len(problems), 4)

        messages = [p.message for p in problems]
        self.assertIn("Class 'AClass' has no title", messages)
        self.assertIn("Slot 'a_slot' has no title", messages)
        self.assertIn("Enum 'AnEnum' has no title", messages)
        self.assertIn("Type 'a_type' has no title", messages)
