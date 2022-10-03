import unittest

from linkml_runtime import SchemaView

from linkml.linter.config.datamodel.config import RuleConfig, RuleLevel
from linkml.linter.rules import NoXsdIntTypeRule
from linkml.utils.schema_builder import SchemaBuilder


class TestNoXsdIntTypeRule(unittest.TestCase):
    def test_xsd_int_type_no_fix(self):
        builder = SchemaBuilder()
        builder.add_type({"name": "a_type", "uri": "xsd:int"})
        builder.add_type({"name": "b_type", "uri": "xsd:integer"})
        builder.add_type({"name": "c_type", "uri": "xsd:string"})

        schema_view = SchemaView(builder.schema)
        config = RuleConfig(level=RuleLevel.error.text)

        rule = NoXsdIntTypeRule(config)
        problems = list(rule.check(schema_view, fix=False))

        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0].message, "Type 'a_type' has uri xsd:int")

    def test_xsd_int_type_fix(self):
        builder = SchemaBuilder()
        builder.add_type({"name": "a_type", "uri": "xsd:int"})
        builder.add_type({"name": "b_type", "uri": "xsd:integer"})
        builder.add_type({"name": "c_type", "uri": "xsd:string"})

        schema_view = SchemaView(builder.schema)
        config = RuleConfig(level=RuleLevel.error.text)

        rule = NoXsdIntTypeRule(config)
        problems = list(rule.check(schema_view, fix=True))

        self.assertEqual(len(problems), 0)
        self.assertEqual(schema_view.get_type("a_type").uri, "xsd:integer")

        problems = list(rule.check(schema_view, fix=False))

        self.assertEqual(len(problems), 0)
