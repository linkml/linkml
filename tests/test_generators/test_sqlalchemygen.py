import os
import re
import sqlite3
import unittest
import tempfile
from pathlib import Path

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.schemaview import SchemaView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from linkml.generators.sqltablegen import SQLTableGenerator
from linkml.generators.yamlgen import YAMLGenerator
from linkml.generators.sqlalchemygen import SQLAlchemyGenerator, TemplateEnum
from linkml.transformers.relmodel_transformer import RelationalModelTransformer
from tests.test_generators.environment import env

SCHEMA = env.input_path('personinfo.yaml')
OUT_PATH = env.expected_path('personinfo_sqla.py')
OUT_PATH_DECLARATIVE = env.expected_path('personinfo_sqla_decl.py')
RSCHEMA_EXPANDED = env.expected_path('personinfo.relational.expanded.yaml')
OUT_DDL = env.expected_path('personinfo.ddl.sql')
SQLDDLLOG = env.expected_path('personinfo.sql.log')
DB = env.expected_path('personinfo.db')
DB_DECLARATIVE = env.expected_path('personinfo-decl.db')



class SQLAlchemyGeneratorTestCase(unittest.TestCase):
    """
    Test compilation to SQL Alchemy python code
    """

    def test_sqla_basic_imperative(self):
        """
        Test generation of DDL for imperative mode (mappings only)
        """
        gen = SQLAlchemyGenerator(SCHEMA)
        code = gen.generate_sqla()

        new_file, filename = tempfile.mkstemp()
        temp_py_filepath = filename + ".py"
        
        with open(temp_py_filepath, 'w') as stream:
            stream.write(code)
        
        py_file_list = []
        with open(temp_py_filepath) as file:
            lines = file.readlines()
            py_file_list = [line.rstrip() for line in lines]

        tbl_list = []
        for item in py_file_list:
            res = re.search(r"Table\('(.*?)',", item)
            if res:
                tbl_list.append(res.group(1))
                
        self.assertTrue(all(x in tbl_list for x in ["NamedThing",
                                                    "Person",
                                                    "Organization",
                                                    "Place",
                                                    "Address",
                                                    "Event",
                                                    "Concept",
                                                    "DiagnosisConcept",
                                                    "ProcedureConcept",
                                                    "Relationship",
                                                    "FamilialRelationship",
                                                    "EmploymentEvent",
                                                    "MedicalEvent"]),
                        f"Expected classes from personinfo schema not written to {temp_py_filepath}")

    def test_sqla_basic_declatative(self):
        """
        Test generation of DDL for declarative mode (alternative to generated dataclasses)
        """
        gen = SQLAlchemyGenerator(SCHEMA)
        code = gen.generate_sqla(template=TemplateEnum.DECLARATIVE)

        new_file, filename = tempfile.mkstemp()
        temp_py_filepath = filename + ".py"
        
        with open(temp_py_filepath, 'w') as stream:
            stream.write(code)
        
        py_file_list = []
        with open(temp_py_filepath) as file:
            lines = file.readlines()
            py_file_list = [line.rstrip() for line in lines]

        tbl_list = []
        for item in py_file_list:
            res = re.search(r"class\s(.*?)\(", item)
            if res:
                tbl_list.append(res.group(1))

        self.assertTrue(all(x in tbl_list for x in ["NamedThing",
                                                    "Person",
                                                    "Organization",
                                                    "Place",
                                                    "Address",
                                                    "Event",
                                                    "Concept",
                                                    "DiagnosisConcept",
                                                    "ProcedureConcept",
                                                    "Relationship",
                                                    "FamilialRelationship",
                                                    "EmploymentEvent",
                                                    "MedicalEvent"]),
                        f"Expected classes from personinfo schema not written to {temp_py_filepath}")

    def test_sqla_compile(self):
        gen = SQLAlchemyGenerator(SCHEMA)
        personinfo_module = gen.compile_sqla(compile_python_dataclasses=True)
        p1 = personinfo_module.Person(id='P1', name='John Doe', age_in_years=22)

        # test three attributes with values supplied above
        self.assertTrue(hasattr(p1, "id"), f"'id' attribute not found in {p1}")
        self.assertTrue(hasattr(p1, "name"), f"'name' attribute not found in {p1}")
        self.assertTrue(hasattr(p1, "age_in_years"), f"'age_in_years' attribute not found in {p1}")

        # test one or more attributes without values supplied during initialization
        self.assertTrue(hasattr(p1, "description"), f"'description' attribute not found in {p1}")

    def test_sqla_imperative_exec(self):
        Path(DB).unlink(missing_ok=True)
        engine = create_engine(f'sqlite:///{DB}')
        con = sqlite3.connect(DB)
        cur = con.cursor()
        ddl = SQLTableGenerator(SCHEMA).generate_ddl()
        cur.executescript(ddl)
        Session = sessionmaker(bind=engine)
        session = Session()
        gen = SQLAlchemyGenerator(SCHEMA)
        mod = gen.compile_sqla(compile_python_dataclasses=True)
        p1 = mod.Person(id='P1', name='a b', age_in_years=22)
        session.add(p1)
        q = session.query(mod.Person).where(mod.Person.name == p1.name)
        persons = q.all()
        for person in persons:
            print(f'Person={person}')
        assert p1 in persons
        session.commit()
        e1 = mod.MedicalEvent(duration=100.0)
        p2 = mod.Person(id='P2', name='a b', aliases=['foo'], has_medical_history=[e1])
        session.add(p2)
        session.commit()

    def test_sqla_declarative_exec(self):
        Path(DB_DECLARATIVE).unlink(missing_ok=True)
        engine = create_engine(f'sqlite:///{DB_DECLARATIVE}')
        con = sqlite3.connect(DB_DECLARATIVE)
        cur = con.cursor()
        ddl = SQLTableGenerator(SCHEMA).generate_ddl()
        cur.executescript(ddl)
        Session = sessionmaker(bind=engine)
        session = Session()
        gen = SQLAlchemyGenerator(SCHEMA)
        mod = gen.compile_sqla(template=TemplateEnum.DECLARATIVE)
        dc = mod.DiagnosisConcept(id='C001', name='cough')
        #e1 = mod.MedicalEvent(duration=100.0, diagnosis=dc)
        e1 = mod.MedicalEvent(duration=100.0, diagnosis_id='C999')
        session.add(mod.DiagnosisConcept(id='C999', name='rash'))
        e2 = mod.MedicalEvent(duration=200.0, diagnosis=dc)
        #e1 = mod.MedicalEvent(duration=100.0)
        p1 = mod.Person(id='P1', name='a b', age_in_years=22, has_medical_history=[e1, e2])
        session.add(p1)
        q = session.query(mod.Person).where(mod.Person.name == p1.name)
        persons = q.all()
        for person in persons:
            print(f'Person={person}')
            for e in person.has_medical_history:
                print(f'  MEDICAL EVENT={e}')
                assert e.duration > 0
                #assert e.diagnosis.id is not None
        assert p1 in persons
        #assert any(e for e in persons[0].has_medical_history if e.diagnosis.id == 'C999')
        assert any(e for e in persons[0].has_medical_history if e.diagnosis_id == 'C999')
        assert any(e for e in persons[0].has_medical_history if e.diagnosis is not None and e.diagnosis.id == 'C001')
        assert any(e for e in persons[0].has_medical_history if e.diagnosis is not None and e.diagnosis.name == 'cough')
        #q = session.query(mod.Person).where(mod.Person.diagnosis.id == 'C999')
        #persons = q.all()
        #for person in persons:
        #    print(f'Person[C999]={person}')
        session.commit()


if __name__ == '__main__':
    unittest.main()
