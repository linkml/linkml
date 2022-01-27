import unittest
from linkml_runtime.linkml_model import SchemaDefinition, SlotDefinition, ClassDefinition
from linkml_runtime.dumpers import yaml_dumper
from linkml.generators.yamlgen import YAMLGenerator
from linkml.generators.sqlddlgen import SQLDDLGenerator


class BasicExample(unittest.TestCase):
    """An illustration of failed java generation will go here.
    Right now I'm just getting used to unittest"""

    def test_valid_math(self):
        self.assertEqual(1, 2 / 2)

    # def test_bogus_math(self):
    #     self.assertEqual(1, 0.5 + 0.501)

    def test_sql_ddl_gen(self):
        schema_id = 'http://example.com/test_schema'
        test_schema = SchemaDefinition(name="test_schema", id=schema_id)
        test_schema.imports.append("https://w3id.org/linkml/types")
        test_class1 = ClassDefinition(name="test_class1", from_schema=schema_id)
        test_class2 = ClassDefinition(name="test_class2", from_schema=schema_id)
        test_slot = SlotDefinition(name="test_slot", range='test_class2')
        test_id = SlotDefinition(name="test_id", range='string', identifier=True)
        test_schema.slots['test_slot'] = test_slot
        test_schema.slots['test_id'] = test_id
        test_class1.slots.append('test_slot')
        test_class1.slots.append('test_id')
        test_class2.slots.append('test_id')
        test_schema.classes['test_class1'] = test_class1
        test_schema.classes['test_class2'] = test_class2
        dumped_yaml = yaml_dumper.dumps(test_schema)
        print(dumped_yaml)
        ts_type = type(test_schema)
        # PREVIOUSLY
        # Exception: Class has no from_schema
        generated_yaml = YAMLGenerator(test_schema).serialize()
        print(generated_yaml)
        # PREVIOUSLY
        # ERROR:root:No PK for test_class1
        generated_sql = SQLDDLGenerator(test_schema).serialize()
        print(generated_sql)
        self.assertEqual(ts_type, SchemaDefinition)


if __name__ == "__main__":
    unittest.main()
