import unittest

import yaml
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader

from linkml.utils.sqlutils import SQLStore
from tests.test_issues.environment import env
import tests.test_issues.model.issue_1160_datamodel
from tests.test_issues.model.issue_1160_datamodel import DataListCollection

SCHEMA = env.input_path("issue_1160_schema.yaml")
DATA = env.input_path("issue_1160_data.yaml")
DB = env.expected_path("issue_1160_data.db")


class SchemaNameTest(unittest.TestCase):
    def test_schema_name(self):
        sv = SchemaView(SCHEMA)
        self.assertEqual(sv.schema.name, "cleanroom-schema")  # add assertion here

    def test_data(self):
        obj = yaml_loader.load(DATA, target_class=DataListCollection)
        bs0_id = obj['biosample_list'][0]['id']
        self.assertEqual(bs0_id, 'GOLD:Gb0305833')

    def test_prepare_dump_sqlite(self):
        endpoint = SQLStore(SCHEMA, database_path=DB, include_schema_in_database=False)
        endpoint.native_module = tests.test_issues.model.issue_1160_datamodel
        endpoint.db_exists(force=True)
        endpoint.compile()
        dlc: DataListCollection = yaml_loader.load(DATA, target_class=DataListCollection)

    def test_do_dump_sqlite(self):
        endpoint = SQLStore(SCHEMA, database_path=DB, include_schema_in_database=False)
        endpoint.native_module = tests.test_issues.model.issue_1160_datamodel
        endpoint.db_exists(force=True)
        endpoint.compile()
        dlc: DataListCollection = yaml_loader.load(DATA, target_class=DataListCollection)
        endpoint.dump(dlc)

if __name__ == "__main__":
    unittest.main()
