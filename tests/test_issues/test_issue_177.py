import unittest

import jsonasobj

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.utils.schemaloader import SchemaLoader
from linkml_runtime.utils.yamlutils import as_yaml
from tests.test_issues.environment import env
from tests.utils.filters import yaml_filter
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue18TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_177(self):
        def generator() -> str:
            gen = JsonSchemaGenerator(env.input_path('issue_177.yaml'))
            return gen.serialize()

        json_str = env.generate_single_file('issue_177.json',
                                            lambda: JsonSchemaGenerator(env.input_path('issue_177.yaml')).serialize(),
                                            value_is_returned=True)
        sobj = jsonasobj.loads(json_str)
        props = sobj['properties']
        assert props['sa']['type'] == 'string'
        assert props['sb']['type'] == 'integer'

    def test_issue_177_dup(self):
        env.generate_single_file('issue_177_error.yaml',
                                 lambda: as_yaml(SchemaLoader(env.input_path('issue_177_error.yaml')).resolve()),
                                 value_is_returned=True, filtr=yaml_filter)


if __name__ == '__main__':
    unittest.main()
