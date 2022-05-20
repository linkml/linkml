import unittest

import yaml

from tests.test_issues.environment import env

# load any random input YAML files from previous tests
SCHEMA = env.input_path("issue_494/testme.yaml")


class PyyamlLoadSignatureUpdate(unittest.TestCase):
    def test_yaml_load(self):
        """Test case to ensure that we are using the right
        signature for the yaml.load() method."""
        
        # negative test case to check TypeError is raised 
        # when we don't pass value to Loader argument
        with open(SCHEMA) as f:
            with self.assertRaises(TypeError):
                yaml.load(stream=f)

        # compare results when we pass a value to the Loader
        # argument as expected
        expected_dict = {
            "id": "file://testmodel",
            "classes": {"annotation": {"description": "dummy", "abstract": True}},
        }
        with open(SCHEMA) as f:
            actual_dict = yaml.load(stream=f, Loader=yaml.Loader)

        self.assertDictEqual(actual_dict, expected_dict)


if __name__ == "__main__":
    unittest.main()
