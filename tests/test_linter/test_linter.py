import unittest

import yaml

from linkml.linter.config.datamodel.config import RuleLevel
from linkml.linter.linter import Linter
from linkml.utils.schema_builder import SchemaBuilder


class TestLinter(unittest.TestCase):
    def test_rule_level_error(self):
        config = yaml.safe_load(
            """
rules:
  no_empty_title:
    level: error
"""
        )
        builder = SchemaBuilder()
        builder.add_class("MyClass")
        builder.add_slot("my slot")
        builder.add_enum("my_enum")

        linter = Linter(config)
        report = list(linter.lint(builder.schema))

        messages = [p.message for p in report]
        levels = {str(p.level) for p in report}
        rule_names = {p.rule_name for p in report}

        self.assertEqual(len(messages), 3)
        self.assertTrue(any("MyClass" in m for m in messages))
        self.assertTrue(any("my slot" in m for m in messages))
        self.assertTrue(any("my_enum" in m for m in messages))

        self.assertEqual(len(levels), 1)
        self.assertEqual(levels.pop(), RuleLevel.error.text)

        self.assertEqual(len(rule_names), 1)
        self.assertEqual(rule_names.pop(), "no_empty_title")

    def test_rule_level_warning(self):
        config = yaml.safe_load(
            """
rules:
  no_empty_title:
    level: warning
"""
        )
        builder = SchemaBuilder()
        builder.add_class("MyClass")
        builder.add_slot("my slot")
        builder.add_enum("my_enum")

        linter = Linter(config)
        report = list(linter.lint(builder.schema))

        messages = [p.message for p in report]
        levels = {str(p.level) for p in report}
        rule_names = {p.rule_name for p in report}

        self.assertEqual(len(messages), 3)
        self.assertTrue(any("MyClass" in m for m in messages))
        self.assertTrue(any("my slot" in m for m in messages))
        self.assertTrue(any("my_enum" in m for m in messages))

        self.assertEqual(len(levels), 1)
        self.assertEqual(levels.pop(), RuleLevel.warning.text)

        self.assertEqual(len(rule_names), 1)
        self.assertEqual(rule_names.pop(), "no_empty_title")

    def test_rule_level_disabled(self):
        config = yaml.safe_load(
            """
rules:
  no_empty_title:
    level: disabled
"""
        )
        builder = SchemaBuilder()
        builder.add_class("MyClass")
        builder.add_slot("my slot")
        builder.add_enum("my_enum")

        linter = Linter(config)
        report = list(linter.lint(builder.schema))

        self.assertEqual(len(report), 0)

    def test_no_extends(self):
        config = yaml.safe_load(
            """
rules:
  canonical_prefixes:
    level: error
    prefixmaps_contexts:
      - obo
      - prefixcc
  no_empty_title:
    level: warning
"""
        )
        linter = Linter(config)

        # the level is changed by the custom rules
        self.assertEqual(str(linter.config.rules.canonical_prefixes.level), RuleLevel.error.text)
        self.assertEqual(
            linter.config.rules.canonical_prefixes.prefixmaps_contexts,
            ["obo", "prefixcc"],
        )

        # this is not in the custom rules and should come from the default
        self.assertEqual(str(linter.config.rules.tree_root_class.level), RuleLevel.disabled.text)

    def test_extends_recommended(self):
        config = yaml.safe_load(
            """
extends: recommended
rules:
  canonical_prefixes:
    level: error
    prefixmaps_contexts:
      - obo
      - prefixcc
  no_empty_title:
    level: warning
"""
        )
        linter = Linter(config)

        # this rule is in the recommended set, the level is changed by the custom rules
        self.assertEqual(str(linter.config.rules.canonical_prefixes.level), RuleLevel.error.text)
        self.assertEqual(
            linter.config.rules.canonical_prefixes.prefixmaps_contexts,
            ["obo", "prefixcc"],
        )

        # this should come directly from the recommended set with no customization
        self.assertEqual(str(linter.config.rules.no_xsd_int_type.level), RuleLevel.error.text)

        # this is in the custom rules but not in the recommended set
        self.assertEqual(str(linter.config.rules.no_empty_title.level), RuleLevel.warning.text)

        # this is not in the recommended or custom rules and should come from the default
        self.assertEqual(str(linter.config.rules.tree_root_class.level), RuleLevel.disabled.text)
