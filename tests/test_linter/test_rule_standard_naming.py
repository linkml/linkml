import pytest
from linkml_runtime import SchemaView

from linkml.linter.config.datamodel.config import RuleLevel, StandardNamingConfig
from linkml.linter.rules import StandardNamingRule
from linkml.utils.schema_builder import SchemaBuilder


@pytest.fixture
def schema_view():
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

    return SchemaView(builder.schema)


def test_standard_naming_lower_pv(schema_view):
    config = StandardNamingConfig(level=RuleLevel.error.text, permissible_values_upper_case=False)

    rule = StandardNamingRule(config)
    problems = list(rule.check(schema_view))

    assert len(problems) == 9

    messages = [p.message for p in problems]
    assert "Class has name 'bad class'" in messages
    assert "Class has name '0worseclass'" in messages
    assert "Slot has name 'BadSlot'" in messages
    assert "Slot has name 'worse slot'" in messages
    assert "Permissible value of Enum 'GoodEnumWithBadPV' has name 'Bad_PV'" in messages
    assert "Permissible value of Enum 'GoodEnumUpperPV' has name 'GOOD_UPPER_PV'" in messages
    assert "Permissible value of Enum 'GoodEnumUpperPV' has name 'GREAT_UPPER_PV'" in messages
    assert "Permissible value of Enum 'GoodEnumBadUpperPV' has name 'GOOD_UPPER_PV'" in messages
    assert "Enum has name 'bad_enum'" in messages


def test_standard_naming_upper_pv(schema_view):
    config = StandardNamingConfig(level=RuleLevel.error.text, permissible_values_upper_case=True)

    rule = StandardNamingRule(config)
    problems = list(rule.check(schema_view))

    assert len(problems) == 12

    messages = [p.message for p in problems]
    assert "Class has name 'bad class'" in messages
    assert "Class has name '0worseclass'" in messages
    assert "Slot has name 'BadSlot'" in messages
    assert "Slot has name 'worse slot'" in messages
    assert "Permissible value of Enum 'GoodEnum' has name 'good_lower_pv'" in messages
    assert "Permissible value of Enum 'GoodEnum' has name 'great_lower_pv'" in messages
    assert "Permissible value of Enum 'GoodEnumWithBadPV' has name 'good_lower_pv'" in messages
    assert "Permissible value of Enum 'GoodEnumWithBadPV' has name 'Bad_PV'" in messages
    assert "Permissible value of Enum 'GoodEnumBadUpperPV' has name 'bad_pv'" in messages
    assert "Enum has name 'bad_enum'" in messages
    assert "Permissible value of Enum 'bad_enum' has name 'good_lower_pv'" in messages
    assert "Permissible value of Enum 'bad_enum' has name 'great_lower_pv'" in messages


def test_standard_naming_slot_pattern(schema_view):
    config = StandardNamingConfig(level=RuleLevel.error.text, slot_pattern="uppercamel")

    rule = StandardNamingRule(config)
    problems = list(rule.check(schema_view))

    assert len(problems) == 10

    messages = [p.message for p in problems]
    assert "Class has name 'bad class'" in messages
    assert "Class has name '0worseclass'" in messages
    # BadSlot no longer bad
    assert "Slot has name 'worse slot'" in messages
    assert "Permissible value of Enum 'GoodEnumWithBadPV' has name 'Bad_PV'" in messages
    assert "Permissible value of Enum 'GoodEnumUpperPV' has name 'GOOD_UPPER_PV'" in messages
    assert "Permissible value of Enum 'GoodEnumUpperPV' has name 'GREAT_UPPER_PV'" in messages
    assert "Permissible value of Enum 'GoodEnumBadUpperPV' has name 'GOOD_UPPER_PV'" in messages
    assert "Enum has name 'bad_enum'" in messages


def test_standard_naming_class_pattern(schema_view):
    config = StandardNamingConfig(level=RuleLevel.error.text, class_pattern=r"[_a-z0-9]+")

    rule = StandardNamingRule(config)
    problems = list(rule.check(schema_view))

    assert len(problems) == 9

    messages = [p.message for p in problems]
    print(messages)
    assert "Class has name 'GoodClass'" in messages
    assert "Class has name 'bad class'" in messages
    # '0worseclass' now longer bad in the context of the given regular expression
    assert "Slot has name 'BadSlot'" in messages
    assert "Slot has name 'worse slot'" in messages
    assert "Permissible value of Enum 'GoodEnumWithBadPV' has name 'Bad_PV'" in messages
    assert "Permissible value of Enum 'GoodEnumUpperPV' has name 'GOOD_UPPER_PV'" in messages
    assert "Permissible value of Enum 'GoodEnumUpperPV' has name 'GREAT_UPPER_PV'" in messages
    assert "Permissible value of Enum 'GoodEnumBadUpperPV' has name 'GOOD_UPPER_PV'" in messages
    assert "Enum has name 'bad_enum'" in messages
