from linkml_runtime import SchemaView

from linkml.linter.config.datamodel.config import RuleConfig, RuleLevel
from linkml.linter.rules import NoEmptyTitleRule
from linkml.utils.schema_builder import SchemaBuilder


def test_elements_with_empty_title():
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

    assert len(problems) == 4

    messages = [p.message for p in problems]
    assert "Class 'AClass' has no title" in messages
    assert "Slot 'a_slot' has no title" in messages
    assert "Enum 'AnEnum' has no title" in messages
    assert "Type 'a_type' has no title" in messages
