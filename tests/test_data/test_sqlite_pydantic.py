import os
import unittest

import yaml
from linkml_runtime.dumpers import yaml_dumper
from sqlalchemy.orm import sessionmaker

from linkml.generators.pydanticgen import PydanticGenerator
from linkml.utils.sqlutils import SQLStore
from tests.test_data.environment import env
from tests.utils.dict_comparator import compare_yaml

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

    @classmethod
    def setUpClass(cls) -> None:
        cls.personinfo_module = PydanticGenerator(SCHEMA).compile_module()

    def test_enums(self):
        """
        Tests that enum objects can be constructed inlined.

        See https://github.com/linkml/linkml/issues/817
        """
        mod = self.personinfo_module
        mod.FamilialRelationship(type="SIBLING_OF", related_to="x")
        p = mod.Person(id="x", gender=mod.GenderType("cisgender_man"))
        self.assertIsInstance(p.gender, str)

    def test_sqlite_store(self):
        """
        tests a complete end-to-end example with a dump-load cycle
        """
        # step 1: setup
        # TODO: currently it is necessary to pass the actual yaml rather than a schema object
        # endpoint = SQLiteEndpoint(sv.schema, database_path=DB, include_schema_in_database=False)
        mod = self.personinfo_module
        endpoint = SQLStore(SCHEMA, database_path=DB, include_schema_in_database=False)
        endpoint.native_module = mod
        endpoint.db_exists(force=True)
        # step 2: load data from file and store in SQLStore
        # TODO: use yaml_loader once this supports pydantic
        with open(DATA) as file:
            dict_obj = yaml.safe_load(file)
        container = mod.Container(**dict_obj)
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
        [returned_container] = endpoint.load_all(target_class=mod.Container)
        # y = yaml_dumper.dumps(x[0])
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
            yaml_dumper.dumps(container_loaded)
            diff = compare_yaml(DATA, DATA_RECAP)
            self.assertEqual(diff, "")


if __name__ == "__main__":
    unittest.main()
