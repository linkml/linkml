import unittest

from linkml.generators.markdowngen import MarkdownGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue62TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_62(self):
        """ Make sure that types are generated as part of the output """
        env.generate_directory('issue62',
                               lambda d: MarkdownGenerator(env.input_path('issue_62.yaml')).serialize(directory=d))


if __name__ == '__main__':
    unittest.main()
