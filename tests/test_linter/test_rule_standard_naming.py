import unittest

from linkml_runtime import SchemaView

from linkml.linter.config.datamodel.config import RuleLevel, StandardNamingConfig
from linkml.linter.rules import StandardNamingRule
from linkml.utils.schema_builder import SchemaBuilder


class TestStandardNamingRule(unittest.TestCase):
    def setUp(self) -> None:
        builder = SchemaBuilder()

        builder.add_class("GoodClass")
        builder.add_class("bad class")
        builder.add_class("0worseclass")

        builder.add_slot("good_slot")
        builder.add_slot("fineslot")
        builder.add_slot("BadSlot")
        builder.add_slot("worse slot")

        builder.add_enum("GoodEnum", ["good_lower_pv", "great_lower_pv"])
        builder.add_enum("GoodEnumWithBadPV", ["good_lower_pv", "Bad_PV"])

        builder.add_enum("GoodEnumUpperPV", ["GOOD_UPPER_PV", "GREAT_UPPER_PV"])
        builder.add_enum("GoodEnumBadUpperPV", ["GOOD_UPPER_PV", "bad_pv"])

        builder.add_enum("bad_enum", ["good_lower_pv", "great_lower_pv"])

        self.schema_view = SchemaView(builder.schema)

    def test_standard_naming_lower_pv(self):
        config = StandardNamingConfig(level=RuleLevel.error.text, permissible_values_upper_case=False)

        rule = StandardNamingRule(config)
        problems = list(rule.check(self.schema_view))

        self.assertEqual(len(problems), 9)

        messages = [p.message for p in problems]
        self.assertIn("Class has name 'bad class'", messages)
        self.assertIn("Class has name '0worseclass'", messages)
        self.assertIn("Slot has name 'BadSlot'", messages)
        self.assertIn("Slot has name 'worse slot'", messages)
        self.assertIn("Permissible value of Enum 'GoodEnumWithBadPV' has name 'Bad_PV'", messages)
        self.assertIn(
            "Permissible value of Enum 'GoodEnumUpperPV' has name 'GOOD_UPPER_PV'",
            messages,
        )
        self.assertIn(
            "Permissible value of Enum 'GoodEnumUpperPV' has name 'GREAT_UPPER_PV'",
            messages,
        )
        self.assertIn(
            "Permissible value of Enum 'GoodEnumBadUpperPV' has name 'GOOD_UPPER_PV'",
            messages,
        )
        self.assertIn("Enum has name 'bad_enum'", messages)

    def test_standard_naming_upper_pv(self):
        config = StandardNamingConfig(level=RuleLevel.error.text, permissible_values_upper_case=True)

        rule = StandardNamingRule(config)
        problems = list(rule.check(self.schema_view))

        self.assertEqual(len(problems), 12)

        messages = [p.message for p in problems]
        self.assertIn("Class has name 'bad class'", messages)
        self.assertIn("Class has name '0worseclass'", messages)
        self.assertIn("Slot has name 'BadSlot'", messages)
        self.assertIn("Slot has name 'worse slot'", messages)
        self.assertIn("Permissible value of Enum 'GoodEnum' has name 'good_lower_pv'", messages)
        self.assertIn("Permissible value of Enum 'GoodEnum' has name 'great_lower_pv'", messages)
        self.assertIn(
            "Permissible value of Enum 'GoodEnumWithBadPV' has name 'good_lower_pv'",
            messages,
        )
        self.assertIn("Permissible value of Enum 'GoodEnumWithBadPV' has name 'Bad_PV'", messages)
        self.assertIn("Permissible value of Enum 'GoodEnumBadUpperPV' has name 'bad_pv'", messages)
        self.assertIn("Enum has name 'bad_enum'", messages)
        self.assertIn("Permissible value of Enum 'bad_enum' has name 'good_lower_pv'", messages)
        self.assertIn("Permissible value of Enum 'bad_enum' has name 'great_lower_pv'", messages)
