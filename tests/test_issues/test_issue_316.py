import unittest

import yaml.constructor

from linkml.generators.yamlgen import YAMLGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class IssueAAATestCase(TestEnvironmentTestCase):
    env = env

    def test_alt_description(self):
        """ Check alt descriptions """
        YAMLGenerator(env.input_path('issue_326.yaml')).serialize(validateonly=True)

    def test_alt_description_2(self):
        with self.assertRaises(ValueError) as e:
            YAMLGenerator(env.input_path('issue_326a.yaml')).serialize(validateonly=True)
        self.assertIn('description must be supplied', str(e.exception))


if __name__ == '__main__':
    unittest.main()
