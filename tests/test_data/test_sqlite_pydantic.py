import csv
import os
import unittest

import _csv

import yaml
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.loaders import csv_loader, yaml_loader
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schemaview import SchemaDefinition, SchemaView
from sqlalchemy.orm import sessionmaker

import tests.test_data.model.personinfo
from linkml.utils.schema_builder import SchemaBuilder
from linkml.utils.schema_fixer import SchemaFixer
from linkml.utils.sqlutils import SQLStore
from tests.test_data.environment import env
from tests.test_data.model.personinfo_pydantic import (Container, FamilialRelationship, Person, GenderType)
from tests.utils.dict_comparator import compare_objs, compare_yaml

SCHEMA = env.input_path("personinfo.yaml")
METAMODEL_SCHEMA = env.input_path(os.path.join("meta", "meta.yaml"))
DATA = env.input_path("personinfo_data01.yaml")
DATA_RECAP = env.expected_path("personinfo_data01.recap.yaml")
DB = env.expected_path("personinfo.db")
TMP_DB = env.expected_path("tmp.db")
TMP_TSV = env.expected_path("tmp.tsv")
METAMODEL_DB = env.expected_path("meta.db")


class SQLiteStoreTest(unittest.TestCase):
    """
    Tests :class:`SQLStore`

    - :meth:`SQLStore.dump`
    - :meth:`SQLStore.load`
    """

    def test_enums(self):
        """
        Tests that enum objects can be constructed inlined.

        See https://github.com/linkml/linkml/issues/817
        """
        r = FamilialRelationship(type="SIBLING_OF", related_to="x")
        p = Person(id="x", gender=GenderType("cisgender_man"))
        self.assertIsInstance(p.gender, GenderType)

    def test_sqlite_store(self):
        """
        tests a complete end-to-end example with a dump-load cycle
        """
        # step 1: setup
        sv = SchemaView(SCHEMA)
        # TODO: currently it is necessary to pass the actual yaml rather than a schema object
        # endpoint = SQLiteEndpoint(sv.schema, database_path=DB, include_schema_in_database=False)
        endpoint = SQLStore(SCHEMA, database_path=DB, include_schema_in_database=False)
        endpoint.native_module = tests.test_data.model.personinfo_pydantic
        endpoint.db_exists(force=True)
        # step 2: load data from file and store in SQLStore
        # TODO: use yaml_loader once this supports pydantic
        with open(DATA) as file:
            dict_obj = yaml.safe_load(file)
        container = Container(**dict_obj)
        endpoint.dump(container)
        # step 3: test query using SQL Alchemy
        session_class = sessionmaker(bind=endpoint.engine)
        session = session_class()
        q = session.query(endpoint.module.Person)
        all_objs = q.all()
        self.assertEqual(2, len(all_objs))
        q = session.query(endpoint.module.FamilialRelationship)
        # step 4: test loading from SQLStore
        # 4a: first test load_all, diff to original data should be empty
        [returned_container] = endpoint.load_all(target_class=Container)
        #y = yaml_dumper.dumps(x[0])
        returned_dict = returned_container.dict(exclude_none=True)
        if False:
            # Fix when this is fixed https://github.com/linkml/linkml/issues/999
            print(returned_dict)
            with open(DATA_RECAP, "w") as stream:
                yaml.dump(returned_dict, stream)
            diff = compare_yaml(DATA, DATA_RECAP)
            self.assertEqual(diff, "")
            # 4b: next test load implicit object, diff to original data should be empty
            container_loaded = endpoint.load()
            yaml_dumper.dump(container_loaded, to_file=DATA_RECAP)
            y = yaml_dumper.dumps(container_loaded)
            diff = compare_yaml(DATA, DATA_RECAP)
            self.assertEqual(diff, "")



if __name__ == "__main__":
    unittest.main()
