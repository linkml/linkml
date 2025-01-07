from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import ClassDefinition

from linkml.linter.config.datamodel.config import RuleConfig, RuleLevel
from linkml.linter.rules import NoInvalidSlotUsageRule
from linkml.utils.schema_builder import SchemaBuilder


def test_invalid_slot_usage():
    builder = SchemaBuilder()
    builder.add_class("Person")
    builder.add_slot(
        {
            "name": "age_in_years",
            "range": "integer",
            "minimum_value": 0,
            "maximum_value": 999,
        },
        "Person",
    )
    builder.add_class(
        ClassDefinition(name="Adult", is_a="Person"),
        slot_usage={"age_in_days": {"minimum_value": 18}},
    )

    schema_view = SchemaView(builder.schema)
    config = RuleConfig(level=RuleLevel.error.text)

    rule = NoInvalidSlotUsageRule(config)
    problems = list(rule.check(schema_view, fix=False))

    assert len(problems) == 1
    assert problems[0].message == "Slot 'age_in_days' not found on class 'Adult'"


def test_valid_slot_usage():
    builder = SchemaBuilder()
    builder.add_class("Person")
    builder.add_slot(
        {
            "name": "age_in_years",
            "range": "integer",
            "minimum_value": 0,
            "maximum_value": 999,
        },
        "Person",
    )
    builder.add_class(
        ClassDefinition(name="Adult", is_a="Person"),
        slot_usage={"age_in_years": {"minimum_value": 18}},
    )

    schema_view = SchemaView(builder.schema)
    config = RuleConfig(level=RuleLevel.error.text)

    rule = NoInvalidSlotUsageRule(config)
    problems = list(rule.check(schema_view, fix=False))

    assert not problems
