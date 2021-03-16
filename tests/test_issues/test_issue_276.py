import unittest

import yaml.constructor

from linkml.generators.yamlgen import YAMLGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue276TestCase(TestEnvironmentTestCase):
    env = env

    def test_empty_list(self):
        """ Check the local import behavior """
        with self.assertRaises(yaml.constructor.ConstructorError) as e:
            YAMLGenerator(env.input_path('issue_276.yaml')).serialize(validateonly=True)
        self.assertIn("Empty list elements are not allowed", str(e.exception))


if __name__ == '__main__':
    unittest.main()
