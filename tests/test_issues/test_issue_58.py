import unittest

import jsonasobj

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.utils.schemaloader import SchemaLoader
from linkml_runtime.utils.yamlutils import as_yaml
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue58TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_58(self):
        """ Reject non NSNAME model names"""
        with self.assertRaises(ValueError) as ve:
            env.generate_single_file('issue_58_error1.yaml',
                                     lambda: as_yaml(SchemaLoader(env.input_path('issue_58_error1.yaml')).resolve()),
                                     value_is_returned=True)
        self.assertIn('issue 58: Not a valid NCName', str(ve.exception))


if __name__ == '__main__':
    unittest.main()
