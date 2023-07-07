import unittest

from linkml_runtime import SchemaView

from linkml.linter.config.datamodel.config import PermissibleValuesFormatRuleConfig, RuleLevel
from linkml.linter.rules import PermissibleValuesFormatRule
from linkml.utils.schema_builder import SchemaBuilder


class TestRulePermissibleValuesFormat(unittest.TestCase):
    def setUp(self) -> None:
        schema_builder = SchemaBuilder()
        schema_builder.add_enum(
            "MENU",
            [
                "BIG_MAC",
                "quarter_pounder_with_cheese",
                "mcChicken",
                "filet-o-fish",
                "fries",
            ],
        )
        self.schema_view = SchemaView(schema_builder.schema)

    def test_format_snake(self):
        config = PermissibleValuesFormatRuleConfig(level=RuleLevel.error, format="snake")
        rule = PermissibleValuesFormatRule(config)
        problems = list(rule.check(self.schema_view))

        self.assertEqual(len(problems), 3)

        messages = [p.message for p in problems]

        self.assertTrue(any("BIG_MAC" in m for m in messages))
        self.assertTrue(any("mcChicken" in m for m in messages))
        self.assertTrue(any("filet-o-fish" in m for m in messages))

        self.assertFalse(any("quarter_pounder_with_cheese" in m for m in messages))
        self.assertFalse(any("fries" in m for m in messages))

    def test_format_upper_snake(self):
        config = PermissibleValuesFormatRuleConfig(level=RuleLevel.error, format="uppersnake")
        rule = PermissibleValuesFormatRule(config)
        problems = list(rule.check(self.schema_view))

        self.assertEqual(len(problems), 4)

        messages = [p.message for p in problems]

        self.assertTrue(any("mcChicken" in m for m in messages))
        self.assertTrue(any("filet-o-fish" in m for m in messages))
        self.assertTrue(any("quarter_pounder_with_cheese" in m for m in messages))
        self.assertTrue(any("fries" in m for m in messages))

        self.assertFalse(any("BIG_MAC" in m for m in messages))

    def test_format_camel(self):
        config = PermissibleValuesFormatRuleConfig(level=RuleLevel.error, format="camel")
        rule = PermissibleValuesFormatRule(config)
        problems = list(rule.check(self.schema_view))

        self.assertEqual(len(problems), 3)

        messages = [p.message for p in problems]

        self.assertTrue(any("BIG_MAC" in m for m in messages))
        self.assertTrue(any("filet-o-fish" in m for m in messages))
        self.assertTrue(any("quarter_pounder_with_cheese" in m for m in messages))

        self.assertFalse(any("mcChicken" in m for m in messages))
        self.assertFalse(any("fries" in m for m in messages))

    def test_format_kebab(self):
        config = PermissibleValuesFormatRuleConfig(level=RuleLevel.error, format="kebab")
        rule = PermissibleValuesFormatRule(config)
        problems = list(rule.check(self.schema_view))

        self.assertEqual(len(problems), 3)

        messages = [p.message for p in problems]

        self.assertTrue(any("BIG_MAC" in m for m in messages))
        self.assertTrue(any("mcChicken" in m for m in messages))
        self.assertTrue(any("quarter_pounder_with_cheese" in m for m in messages))

        self.assertFalse(any("filet-o-fish" in m for m in messages))
        self.assertFalse(any("fries" in m for m in messages))

    def test_format_custom_regex(self):
        config = PermissibleValuesFormatRuleConfig(level=RuleLevel.error, format="[a-z]+")
        rule = PermissibleValuesFormatRule(config)
        problems = list(rule.check(self.schema_view))

        self.assertEqual(len(problems), 4)

        messages = [p.message for p in problems]

        self.assertTrue(any("BIG_MAC" in m for m in messages))
        self.assertTrue(any("mcChicken" in m for m in messages))
        self.assertTrue(any("quarter_pounder_with_cheese" in m for m in messages))
        self.assertTrue(any("filet-o-fish" in m for m in messages))

        self.assertFalse(any("fries" in m for m in messages))
