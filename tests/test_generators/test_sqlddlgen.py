import unittest

from linkml.generators.sqlddlgen import SQLDDLGenerator
from tests.test_generators.environment import env
import sqlite3
from sqlalchemy.orm import relationship, sessionmaker, aliased
from sqlalchemy import create_engine
from io import StringIO
from contextlib import redirect_stdout

from linkml_runtime.utils.compile_python import compile_python

import os
from output.kitchen_sink import *
#from kitchen_sink_db_mapping import *
from output.kitchen_sink_db_mapping import *

SCHEMA = env.input_path('kitchen_sink.yaml')
DB = env.expected_path('kitchen_sink.db')
SQLA_CODE = env.expected_path('kitchen_sink_db_mapping.py')
DDL_PATH = env.expected_path('kitchen_sink.ddl.sql')
BASIC_DDL_PATH = env.expected_path('kitchen_sink.basic.ddl.sql')
BASIC_SQLA_CODE = env.expected_path('kitchen_sink_basic_db_mapping.py')

NAME = 'fred'
CITY = 'Gotham city'

def create_and_compile_sqla_bindings(gen: SQLDDLGenerator, path: str = SQLA_CODE):
    with open(path, 'w') as stream:
        with redirect_stdout(stream):
            gen.write_sqla_python_imperative('output.kitchen_sink')
            module = compile_python(path)
            return module

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
                # don't load this - will conflict
                #create_and_compile_sqla_bindings(gen, BASIC_SQLA_CODE)

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
        cur.execute("INSERT INTO Person_aliases (backref_id, aliases) VALUES (?,?)", ('P1', 'wibble'))
        cur.execute("INSERT INTO Address (Person_id, street, city) VALUES (?,?,?)", ('P1', '99 foo street', 'SF'))
        cur.execute("select * from Person where name=:name", {"name": NAME})
        print(cur.fetchall())
        con.commit()
        con.close()
        #print(gen.to_sqla_python())
        #output = StringIO()
        #with redirect_stdout(output):
        #    gen.write_sqla_python_imperative('output.kitchen_sink')
        #print(output.getvalue())
        #with open(SQLA_CODE, 'w') as stream:
        #    stream.write(output.getvalue())
        create_and_compile_sqla_bindings(gen, SQLA_CODE)

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
        #person = Person(id='P22', name='joe', addresses=[Address(street='1 Acacia Ave', city='treetown')])
        person = Person(id='P22', name='joe',
                        aliases=['foo'],
                        addresses=[Address(street='1 random streer', city=CITY)],
                        has_employment_history=[EmploymentEvent(started_at_time='2020-01-01', is_current=True)],
                        has_familial_relationships=[],
                        has_medical_history=[])
        person = Person(id='P22', name='joe')
        print(f'Aliases={person.aliases}')
        session.flush()
        #todo: fix this
        #session.add(person)
        org = Organization(id='org1', name='foo org', aliases=['bar org'])
        org.aliases = ['abc def']
        session.add(org)
        session.flush()
        for o in session.query(Organization).all():
            print(f'org = {o}')
        q = session.query(Person)
        p: Person
        is_found_address = False
        for p in q.all():
            print(f'Person={p.id} {p.name}')
            for a in p.addresses:
                print(f'  Address={a}')
                #if a.city == CITY:
                #    is_found_address = True
            #for alias in p.aliases:
            #    print(f'  AKA={a}')
        #assert is_found_address
        session.commit()


if __name__ == '__main__':
    unittest.main()
