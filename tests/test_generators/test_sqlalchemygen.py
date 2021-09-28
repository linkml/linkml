import os
import sqlite3
import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.schemaview import SchemaView

from linkml.generators.yamlgen import YAMLGenerator
from linkml.generators.sqlalchemygen import SQLAlchemyGenerator
from linkml.transformers.relmodel_transformer import RelationalModelTransformer
from tests.test_generators.environment import env

SCHEMA = env.input_path('personinfo.yaml')
OUT_PATH = env.expected_path('personinfo_sqla.py')
RSCHEMA_EXPANDED = env.expected_path('personinfo.relational.expanded.yaml')
OUT_DDL = env.expected_path('personinfo.ddl.sql')
SQLDDLLOG = env.expected_path('personinfo.sql.log')
DB = env.expected_path('personinfo.db')



class SQLAlchemyGeneratorTestCase(unittest.TestCase):



    def test_sqla_basic(self):
        gen = SQLAlchemyGenerator(SCHEMA)
        code = gen.generate_sqla()
        print(code)
        with open(OUT_PATH, 'w') as stream:
            stream.write(code)



if __name__ == '__main__':
    unittest.main()
