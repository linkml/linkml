import unittest
from linkml_runtime.linkml_model import SchemaDefinition, SlotDefinition, ClassDefinition
from linkml_runtime.dumpers import yaml_dumper
from linkml.generators.yamlgen import YAMLGenerator
from linkml.generators.sqlddlgen import SQLDDLGenerator
from linkml.generators.javagen import JavaGenerator
from linkml.generators.projectgen import ProjectGenerator

# import os
# from contextlib import redirect_stdout
# from tests.test_generators.environment import env

# SCHEMA = env.input_path('kitchen_sink.yaml')
# JAVA_DIR = env.expected_path('kitchen_sink_java')
PACKAGE = 'org.sink.kitchen'


class BasicExample(unittest.TestCase):
    """An illustration of failed java generation will go here.
    Right now I'm just getting used to unittest"""

    # def test_valid_math(self):
    #     self.assertEqual(1, 2 / 2)

    # def test_bogus_math(self):
    #     self.assertEqual(1, 0.5 + 0.501)

    def test_sql_ddl_gen(self):
        # todo make the schema creation a fixture and split out the different generations
        schema_id = 'http://example.com/issue_571_schema'
        issue_571_schema = SchemaDefinition(name="issue_571_schema", id=schema_id)
        issue_571_schema.imports.append("https://w3id.org/linkml/types")
        issue_571_class1 = ClassDefinition(name="issue_571_class1", from_schema=schema_id)
        issue_571_class2 = ClassDefinition(name="issue_571_class2", from_schema=schema_id)
        test_slot = SlotDefinition(name="test_slot", range='issue_571_class2')
        test_id = SlotDefinition(name="test_id", range='string', identifier=True)
        issue_571_schema.slots['test_slot'] = test_slot
        issue_571_schema.slots['test_id'] = test_id
        issue_571_class1.slots.append('test_slot')
        issue_571_class1.slots.append('test_id')
        issue_571_class2.slots.append('test_id')
        issue_571_schema.classes['issue_571_class1'] = issue_571_class1
        issue_571_schema.classes['issue_571_class2'] = issue_571_class2
        # dumped_yaml = yaml_dumper.dumps(issue_571_schema)
        # print(dumped_yaml)
        # PREVIOUSLY
        # Exception: Class has no from_schema
        # generated_yaml = YAMLGenerator(issue_571_schema).serialize()
        # print(generated_yaml)
        # PREVIOUSLY
        # ERROR:root:No PK for issue_571_class1
        generated_sql = SQLDDLGenerator(issue_571_schema).serialize()
        print(generated_sql)
        gen = JavaGenerator(issue_571_schema, package=PACKAGE)
        # md =
        gen.serialize(directory='output/issue_571')
        ts_type = type(issue_571_schema)
        self.assertEqual(ts_type, SchemaDefinition)


if __name__ == "__main__":
    unittest.main()
