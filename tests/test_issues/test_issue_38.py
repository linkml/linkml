import unittest

from linkml.generators.csvgen import CsvGenerator
from tests import DEFAULT_LOG_LEVEL
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env


class Issue38UnitTest(TestEnvironmentTestCase):
    env = env

    @unittest.skip("issue_38.yaml clinical profile conflicts with latest Biolink Model")
    def test_domain_slots(self):
        """ Subsets need to be imported as well """
        CsvGenerator(env.input_path('issue_38.yaml'), log_level=DEFAULT_LOG_LEVEL,
                     importmap=env.input_path('biolink-model-importmap.json')).serialize()
        # We never get here if the imports fails
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
