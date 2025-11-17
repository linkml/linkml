import yaml

from linkml.linter.config.datamodel.config import RuleLevel
from linkml.linter.linter import Linter
from linkml.utils.schema_builder import SchemaBuilder


def test_rule_level_error():
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

    assert len(messages) == 3
    assert any("MyClass" in m for m in messages)
    assert any("my slot" in m for m in messages)
    assert any("my_enum" in m for m in messages)

    assert len(levels) == 1
    assert levels.pop() == RuleLevel.error.text

    assert len(rule_names) == 1
    assert rule_names.pop() == "no_empty_title"


def test_rule_level_warning():
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

    assert len(messages) == 3
    assert any("MyClass" in m for m in messages)
    assert any("my slot" in m for m in messages)
    assert any("my_enum" in m for m in messages)

    assert len(levels) == 1
    assert levels.pop() == RuleLevel.warning.text

    assert len(rule_names) == 1
    assert rule_names.pop() == "no_empty_title"


def test_rule_level_disabled():
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

    assert len(report) == 0


def test_no_extends():
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
    assert str(linter.config.rules.canonical_prefixes.level) == RuleLevel.error.text
    assert linter.config.rules.canonical_prefixes.prefixmaps_contexts == ["obo", "prefixcc"]

    assert str(linter.config.rules.tree_root_class.level) == RuleLevel.disabled.text


def test_extends_recommended():
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
    assert str(linter.config.rules.canonical_prefixes.level) == RuleLevel.error.text
    assert linter.config.rules.canonical_prefixes.prefixmaps_contexts == ["obo", "prefixcc"]

    # this should come directly from the recommended set with no customization
    assert str(linter.config.rules.no_xsd_int_type.level) == RuleLevel.error.text

    # this is in the custom rules but not in the recommended set
    assert str(linter.config.rules.no_empty_title.level) == RuleLevel.warning.text

    # this is not in the recommended or custom rules and should come from the default
    assert str(linter.config.rules.tree_root_class.level) == RuleLevel.disabled.text
