import os
import unittest

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue44UnitTest(TestEnvironmentTestCase):
    env = env

    def test_multiple_postinit(self):
        """ Generate postinit code for a multi-occurring element """
        env.generate_single_file('issue_44.py',
                                 lambda: PythonGenerator(env.input_path('issue_44.yaml'),
                                                         emit_metadata=False).serialize(), value_is_returned=True)



if __name__ == '__main__':
    unittest.main()
