import unittest

from linkml import LOCAL_METAMODEL_YAML_FILE
from linkml.utils.schemaloader import SchemaLoader
from tests.test_issues.environment import env
from tests.test_biolink_model.environment import env as env2


class SchemaLoaderMonotonicityTest(unittest.TestCase):
    def test_biolink(self):
        """ SchemaLoader should be monotonic - metamodel test """
        biolink_schema = SchemaLoader(LOCAL_METAMODEL_YAML_FILE).resolve()
        biolink_schema_2 = SchemaLoader(biolink_schema).resolve()
        self.assertEqual(biolink_schema, biolink_schema_2)

    def test_biolink_model(self):
        """ SchemaLoader should be monotonic - biolink-model test"""
        bm_schema = SchemaLoader(env2.input_path('biolink-model.yaml')).resolve()
        bm_schema_2 = SchemaLoader(bm_schema).resolve()
        self.assertEqual(bm_schema, bm_schema_2)

if __name__ == '__main__':
    unittest.main()
