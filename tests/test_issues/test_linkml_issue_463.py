import json
import unittest

import jsonasobj
import jsonschema

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env

data_str = """
TODO
"""



class IssueJSONSchemaInlinedAsDictCase(TestEnvironmentTestCase):
    env = env

    def test_inlined(self):
        """ Make sure that enums are generated as part of the output """
        TODO


if __name__ == '__main__':
    unittest.main()
