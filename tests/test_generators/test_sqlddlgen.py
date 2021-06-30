import unittest

from linkml_runtime.loaders import yaml_loader, json_loader, rdf_loader
from linkml_runtime.dumpers import rdf_dumper, json_dumper
from linkml.generators.sqlddlgen import SQLDDLGenerator
from linkml.generators.jsonldcontextgen import ContextGenerator
from tests.test_generators.environment import env
import sqlite3
from sqlalchemy.orm import relationship, sessionmaker, aliased
from sqlalchemy import create_engine
from io import StringIO
from contextlib import redirect_stdout

from pyshex.evaluate import evaluate
from rdflib.namespace import RDF
from importlib import import_module
import json
import yaml
import os
from output.kitchen_sink import *
from output.kitchen_sink_db_mapping import *

SCHEMA = env.input_path('kitchen_sink.yaml')
DB = env.expected_path('kitchen_sink.db')
SQLA_CODE = env.expected_path('kitchen_sink_db_mapping.py')
DDL_PATH = env.expected_path('kitchen_sink.ddl.sql')
BASIC_DDL_PATH = env.expected_path('kitchen_sink.basic.ddl.sql')
BASIC_SQLA_CODE = env.expected_path('kitchen_sink_basic_db_mapping.py')
NAME = 'fred'

class SQLDDLTestCase(unittest.TestCase):

    def test_sqlddl_basic(self):
        """ DDL  """
        gen = SQLDDLGenerator(SCHEMA, mergeimports=True, direct_mapping=True)
        ddl = gen.serialize()
        with open(BASIC_DDL_PATH, 'w') as stream:
            stream.write(ddl)
        with open(BASIC_SQLA_CODE, 'w') as stream:
            with redirect_stdout(stream):
                gen.write_sqla_python_imperative('output.kitchen_sink')

    def test_sqlddl(self):
        """ DDL  """
        gen = SQLDDLGenerator(SCHEMA, mergeimports=True, rename_foreign_keys=True)
        ddl = gen.serialize()
        with open(DDL_PATH, 'w') as stream:
            stream.write(ddl)
        #print(ddl)
        try:
            os.remove(DB)
        except OSError:
            pass
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.executescript(ddl)
        cur.execute("INSERT INTO Person (id, name, age_in_years) VALUES (?,?,?)", ('P1', NAME, 33))
        cur.execute("select * from Person where name=:name", {"name": NAME})
        print(cur.fetchall())
        con.commit()
        con.close()
        #print(gen.to_sqla_python())
        output = StringIO()
        with redirect_stdout(output):
            gen.write_sqla_python_imperative('output.kitchen_sink')
        #print(output.getvalue())
        with open(SQLA_CODE, 'w') as stream:
            stream.write(output.getvalue())

        # test SQLA
        engine = create_engine(f'sqlite:///{DB}')
        Session = sessionmaker(bind=engine)
        session = Session()
        q = session.query(Person).where(Person.name == NAME)
        print(f'Q={q}')
        #for row in q.all():
        #    print(f'Row={row}')
        agent = Agent(id='Agent03')
        print(f'Agent={agent}')
        activity = Activity(id='Act01', was_associated_with=agent)
        session.add(agent)
        session.add(activity)
        session.flush()
        q = session.query(Activity)
        for row in q.all():
            print(f'Row={row}')
        session.commit()


if __name__ == '__main__':
    unittest.main()
