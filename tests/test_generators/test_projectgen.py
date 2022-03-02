import os
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from linkml.generators.projectgen import ProjectGenerator, ProjectConfiguration
from tests.test_generators.environment import env

SCHEMA = env.input_path('kitchen_sink.yaml')
PROJECT_DIR = env.expected_path('ks')

class ProjectGeneratorTestCase(unittest.TestCase):

    def check_contains(self, v: str, folder: str, local_path: str):
        with open(Path(PROJECT_DIR) / folder / local_path, encoding='UTF-8') as stream:
            assert v in stream.read()

    def test_projectgen(self):
        """ Generate whole project  """
        config = ProjectConfiguration()
        config.directory = PROJECT_DIR
        config.generator_args['jsonschema'] = {"top_class": "Dataset", "not_closed": False}
        config.generator_args['owl'] = {"metaclasses": False, "type_objects": False}
        gen = ProjectGenerator()
        gen.generate(SCHEMA, config)
        # some of these tests may be quite rigid as they make assumptions about formatting
        self.check_contains("CREATE TABLE", "sqlschema", "kitchen_sink.sql")
        self.check_contains("ks:age_in_years a owl:DatatypeProperty", "owl", "kitchen_sink.owl.ttl")
        # TODO: restore this test
        #self.check_contains("Address.md", "docs", "index.md")
        self.check_contains("ks:Address", "docs", "Address.md")
        self.check_contains('"additionalProperties": false', "jsonschema", "kitchen_sink.schema.json")


if __name__ == '__main__':
    unittest.main()
