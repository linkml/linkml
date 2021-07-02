import unittest

import jsonasobj

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class IssueJSONSchemaEnumsTestCase(TestEnvironmentTestCase):
    env = env

    def test_enums(self):
        """ Make sure that enums are generated as part of the output """
        def generator() -> str:
            gen = JsonSchemaGenerator(env.input_path('issue_239.yaml'))
            gen.topCls = 'c'
            return gen.serialize()

        env.generate_single_file('issue_239.json', lambda: generator(), value_is_returned=True)


if __name__ == '__main__':
    unittest.main()
