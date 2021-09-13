import unittest

from jsonasobj2 import loads

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue202TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_202(self):
        json_str = env.generate_single_file('issue_202.json.schema',
                                            lambda: JsonSchemaGenerator(env.input_path('issue_202.yaml')).serialize(),
                                            value_is_returned=True)
        json_schema = loads(json_str)
        self.assertEqual(json_schema["$defs"].GeospatialDDCoordLocation.properties.latitude.type, "number")


if __name__ == '__main__':
    unittest.main()
