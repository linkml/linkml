import unittest

from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue371TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_371(self):
        """Infer a model from a CSV

        Now implemented in schema-automator
        """
        pass


if __name__ == "__main__":
    unittest.main()
