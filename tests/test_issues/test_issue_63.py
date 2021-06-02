import unittest

from linkml.generators.markdowngen import MarkdownGenerator
from linkml.utils.schemaloader import SchemaLoader
from linkml_runtime.utils.yamlutils import as_yaml
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env


class Issue63TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_63(self):
        """ We should get an error from this -- we have a list as an object """
        with self.assertRaises(ValueError) as error:
            SchemaLoader(env.input_path('issue_63.yaml'))
        self.assertEqual("['s3'] is not a valid URI or CURIE", str(error.exception))


if __name__ == '__main__':
    unittest.main()
