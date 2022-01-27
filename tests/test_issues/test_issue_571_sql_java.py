from linkml.generators.projectgen import ProjectGenerator, ProjectConfiguration
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SchemaDefinition, SlotDefinition, ClassDefinition
from tests.test_generators.environment import env
import filecmp
import os
import unittest

SCHEMA = env.input_path('kitchen_sink.yaml')

PACKAGE = 'org.sink.kitchen'

OUT_DIR = 'output/issue_571'
OUT_SUFFIX = 'issue_571'
YAML_FILE = 'issue_571.yaml'
SQL_FILE = 'issue_571.sql'
SQL_DIR = 'sqlschema'
JAVA_DIR = 'java'

OUTDIR = env.outdir
DEEPER_OUT = os.path.join(env.outdir, OUT_SUFFIX)
YAML_PATH = os.path.join(DEEPER_OUT, YAML_FILE)
SQL_PATH = os.path.join(DEEPER_OUT, SQL_DIR, SQL_FILE)
JAVA_PATH = os.path.join(DEEPER_OUT, JAVA_DIR, SQL_FILE)


class SqlVsJava(unittest.TestCase):
    """Is there a SQL DDL file in the Java output dir?
    Does it match the SQL DDL file in the SQL output dir?"""

    def test_sql_vs_java(self):

        # todo make the schema creation a fixture and split out the different generations ?
        # todo switch to kitchen sink instead of crating my own schema?
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

        yaml_dumper.dump(issue_571_schema, YAML_PATH)

        # yaml_dumper.dump(SCHEMA, YAML_PATH)

        config = ProjectConfiguration()
        config.directory = DEEPER_OUT
        config.generator_args['jsonschema'] = {"top_class": "issue_571_class1"}
        pgen = ProjectGenerator()
        pgen.generate(YAML_PATH, config)

        if os.path.isfile(SQL_PATH):
            if os.path.isfile(JAVA_PATH):
                identical_files = filecmp.cmp(SQL_PATH, JAVA_PATH)
                self.assertFalse(identical_files, msg=f"""There's a SQL DDL file {JAVA_PATH} 
                that's identical with the expected {SQL_PATH}""")
            else:
                print(f"{JAVA_PATH} is not accessible")
        else:
            print(f"{SQL_PATH} is not accessible")


if __name__ == "__main__":
    unittest.main()

# from contextlib import redirect_stdout

# dumped_yaml = yaml_dumper.dumps(issue_571_schema)
# print(dumped_yaml)
# PREVIOUSLY
# Exception: Class has no from_schema
# generated_yaml = YAMLGenerator(issue_571_schema).serialize()
# print(generated_yaml)
# PREVIOUSLY
# ERROR:root:No PK for issue_571_class1
# generated_sql = SQLDDLGenerator(issue_571_schema).serialize()
# print(generated_sql)
# jgen = JavaGenerator(issue_571_schema, package=PACKAGE)
# jgen.serialize(directory=OUT_DIR)
