import unittest

from linkml.utils.schemaloader import SchemaLoader
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue63TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_63(self):
        """We should get an error from this -- we have a list as an object"""
        with self.assertRaises(ValueError) as error:
            SchemaLoader(env.input_path("issue_63.yaml"))
        self.assertEqual("['s3'] is not a valid URI or CURIE", str(error.exception))


if __name__ == "__main__":
    unittest.main()
