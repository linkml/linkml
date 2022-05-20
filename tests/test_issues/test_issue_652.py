import json
import os
import unittest

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env


class Issue652TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_652_scenario1(self):
        """
        Generate JSON Schema in default mode, where range class
        descendants are not included
        """
        x = env.generate_single_file('issue_652_scenario1.schema.json',
                                 lambda: JsonSchemaGenerator(env.input_path('issue_652.yaml'),
                                 include_range_class_descendants=False).serialize(), value_is_returned=True)
        with open(os.path.join(env.outdir, 'issue_652_scenario1.schema.json')) as f:
            issue_jsonschema = json.load(f)
        prop4_def = issue_jsonschema["$defs"]["NamedThing"]["properties"]["prop4"]
        self.assertEqual(prop4_def["$ref"], "#/$defs/C1")

    def test_issue_652_scenario2(self):
        """
        Generate JSON Schema where descendants of range class
        are included for the type of a property
        """
        x = env.generate_single_file('issue_652_scenario2.schema.json',
                                 lambda: JsonSchemaGenerator(env.input_path('issue_652.yaml'),
                                 include_range_class_descendants=True).serialize(), value_is_returned=True)
        with open(os.path.join(env.outdir, 'issue_652_scenario2.schema.json')) as f:
            issue_jsonschema = json.load(f)
        prop4_def = issue_jsonschema["$defs"]["NamedThing"]["properties"]["prop4"]
        self.assertIn("oneOf", prop4_def)
        self.assertEqual(len(prop4_def["oneOf"]), 3)
        self.assertIn({"$ref": "#/$defs/C1"}, prop4_def["oneOf"])
        self.assertIn({"$ref": "#/$defs/C2"}, prop4_def["oneOf"])
        self.assertIn({"$ref": "#/$defs/C3"}, prop4_def["oneOf"])

if __name__ == '__main__':
    unittest.main()
