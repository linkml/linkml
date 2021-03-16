import unittest

from linkml.generators.markdowngen import MarkdownGenerator
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env


class Issue179TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_179(self):
        """ Make sure that inheritence isn't implied by reference slots """
        env.generate_directory('issue179',
                               lambda d: MarkdownGenerator(env.input_path('issue_179.yaml')).serialize(directory=d))


if __name__ == '__main__':
    unittest.main()
