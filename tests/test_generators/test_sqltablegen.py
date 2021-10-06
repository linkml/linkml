import os
import sqlite3
import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.schemaview import SchemaView

from linkml.generators.yamlgen import YAMLGenerator
from linkml.generators.sqltablegen import SQLTableGenerator, SqlNamingPolicy
from linkml.transformers.relmodel_transformer import RelationalModelTransformer
from tests.test_generators.environment import env

SCHEMA = env.input_path('personinfo.yaml')
OUT_PATH = env.expected_path('personinfo.relational.yaml')
RSCHEMA_EXPANDED = env.expected_path('personinfo.relational.expanded.yaml')
OUT_DDL = env.expected_path('personinfo.ddl.sql')
SQLDDLLOG = env.expected_path('personinfo.sql.log')
DB = env.expected_path('personinfo.db')


class SQLTableGeneratorTestCase(unittest.TestCase):
    """
    Tests the (new) SQLTableGenerator
    """

    def test_sqlddl_basic(self):
        #sv = SchemaView(SCHEMA)
        #sqltr = RelationalModelTransformer(sv)
        gen = SQLTableGenerator(SCHEMA)
        #ddl = gen.generate_ddl(naming_policy=SqlNamingPolicy.underscore)
        ddl = gen.generate_ddl()
        with open(OUT_DDL, 'w') as stream:
            stream.write(ddl)

        with open(SQLDDLLOG, 'w') as log:
            # with open(DDL_PATH, 'w') as stream:
            #     stream.write(ddl)
            #print(ddl)
            try:
                os.remove(DB)
            except OSError:
                pass
            con = sqlite3.connect(DB)
            cur = con.cursor()
            cur.executescript(ddl)
            NAME = 'fred'
            cur.execute("INSERT INTO Person (id, name, age_in_years) VALUES (?,?,?)", ('P1', NAME, 33))
            cur.execute("INSERT INTO Person_alias (Person_id, alias) VALUES (?,?)", ('P1', 'wibble'))
            cur.execute("INSERT INTO FamilialRelationship (Person_id, type, related_to) VALUES (?,?,?)", ('P1', 'P2', 'BROTHER_OF'))
            cur.execute("select * from Person where name=:name", {"name": NAME})
            rows = cur.fetchall()
            log.write(f"{rows}\n")
            assert len(rows) == 1
            con.commit()
            with self.assertRaises(Exception):
                # PK violation
                cur.execute("INSERT INTO Person (id, name, age_in_years) VALUES (?,?,?)", ('P1', 'other person', 22))
            with self.assertRaises(Exception):
                cur.execute("INSERT INTO Person_alias (Person_id, alias) VALUES (?,?)", ('P1', 'wibble'))

            con.close()




if __name__ == '__main__':
    unittest.main()
