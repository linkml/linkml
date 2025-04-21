from unittest import TestCase

import yaml.constructor

from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader
from tests.test_issues.environment import env


class Issue1040TestCase(TestCase):
    """
    https://github.com/linkml/linkml/issues/1040
    """
    env = env

    def test_issue_1040_file_name(self):
        """ issue_1040.yaml has a parsing error is confusing as all getout when accompanied by a stack
            trace.  We use this to make sure that the file name gets in correctly.  """
        with self.assertRaises(yaml.constructor.ConstructorError) as e:
            yaml_loader.load(env.input_path('issue_1040.yaml'), SchemaDefinition)
        self.assertIn('"issue_1040.yaml"', str(e.exception))
