import unittest

from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml_runtime.loaders import yaml_loader
from tests.test_issues.environment import env


class IncludeSchemaTestCase(unittest.TestCase):
    """ include_schema.yaml produces a Python exception on an uncaught error"""
    # "Awaiting fix for issue #3"
    def test_include_schema(self):
        inp = yaml_loader.load(env.input_path('include_schema.yaml'), SchemaDefinition)



if __name__ == '__main__':
    unittest.main()
