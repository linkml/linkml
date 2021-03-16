import unittest

from linkml.generators.markdowngen import MarkdownGenerator
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env


class Issue65TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_65(self):
        """ Make sure that types are generated as part of the output """
        env.generate_directory('issue65',
                               lambda d: MarkdownGenerator(env.input_path('issue_65.yaml')).serialize(directory=d))


if __name__ == '__main__':
    unittest.main()
