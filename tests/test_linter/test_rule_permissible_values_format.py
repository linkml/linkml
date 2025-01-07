import pytest
from linkml_runtime import SchemaView

from linkml.linter.config.datamodel.config import PermissibleValuesFormatRuleConfig, RuleLevel
from linkml.linter.rules import PermissibleValuesFormatRule
from linkml.utils.schema_builder import SchemaBuilder


@pytest.fixture
def schema_view():
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
    return SchemaView(schema_builder.schema)


def test_format_snake(schema_view):
    config = PermissibleValuesFormatRuleConfig(level=RuleLevel.error, format="snake")
    rule = PermissibleValuesFormatRule(config)
    problems = list(rule.check(schema_view))

    assert len(problems) == 3

    messages = [p.message for p in problems]

    assert any("BIG_MAC" in m for m in messages)
    assert any("mcChicken" in m for m in messages)
    assert any("filet-o-fish" in m for m in messages)

    assert not any("quarter_pounder_with_cheese" in m for m in messages)
    assert not any("fries" in m for m in messages)


def test_format_upper_snake(schema_view):
    config = PermissibleValuesFormatRuleConfig(level=RuleLevel.error, format="uppersnake")
    rule = PermissibleValuesFormatRule(config)
    problems = list(rule.check(schema_view))

    assert len(problems) == 4

    messages = [p.message for p in problems]

    assert any("mcChicken" in m for m in messages)
    assert any("filet-o-fish" in m for m in messages)
    assert any("quarter_pounder_with_cheese" in m for m in messages)
    assert any("fries" in m for m in messages)

    assert not any("BIG_MAC" in m for m in messages)


def test_format_camel(schema_view):
    config = PermissibleValuesFormatRuleConfig(level=RuleLevel.error, format="camel")
    rule = PermissibleValuesFormatRule(config)
    problems = list(rule.check(schema_view))

    assert len(problems) == 3

    messages = [p.message for p in problems]

    assert any("BIG_MAC" in m for m in messages)
    assert any("filet-o-fish" in m for m in messages)
    assert any("quarter_pounder_with_cheese" in m for m in messages)

    assert not any("mcChicken" in m for m in messages)
    assert not any("fries" in m for m in messages)


def test_format_kebab(schema_view):
    config = PermissibleValuesFormatRuleConfig(level=RuleLevel.error, format="kebab")
    rule = PermissibleValuesFormatRule(config)
    problems = list(rule.check(schema_view))

    assert len(problems) == 3

    messages = [p.message for p in problems]

    assert any("BIG_MAC" in m for m in messages)
    assert any("mcChicken" in m for m in messages)
    assert any("quarter_pounder_with_cheese" in m for m in messages)

    assert not any("filet-o-fish" in m for m in messages)
    assert not any("fries" in m for m in messages)


def test_format_custom_regex(schema_view):
    config = PermissibleValuesFormatRuleConfig(level=RuleLevel.error, format="[a-z]+")
    rule = PermissibleValuesFormatRule(config)
    problems = list(rule.check(schema_view))

    assert len(problems) == 4

    messages = [p.message for p in problems]

    assert any("BIG_MAC" in m for m in messages)
    assert any("mcChicken" in m for m in messages)
    assert any("quarter_pounder_with_cheese" in m for m in messages)
    assert any("filet-o-fish" in m for m in messages)

    assert not any("fries" in m for m in messages)
