import unittest

import yaml

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.utils.yamlutils import as_yaml
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class IssueYamlSerializerTestCase(TestEnvironmentTestCase):
    env = env

    def test_roundtrip(self):
        """ Test as_yaml emitter """
        # env.generate_single_file('issue_154.py',
        #                          lambda: PythonGenerator(env.input_path('issue_134.yaml')).serialize(),
        #                          comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('issue_154.py')),
        #                          value_is_returned=True)
        # yaml_fname = env.input_path('issue_134.yaml')

        # We use the PythonGenerator as a generic generator instance.  We don't actually serialize

        yaml_fname = env.input_path('issue_134.yaml')
        gen = PythonGenerator(yaml_fname)
        yaml_str = as_yaml(gen.schema)
        generated = yaml.safe_load(yaml_str)
        with open(yaml_fname) as yaml_file:
            original = yaml.safe_load(yaml_file)

        # The generated YAML contains many added fields. Some with default values. Therefore, we can't directly
        # compare it to the original.
        for key in original:
            self.assertEqual(len(original[key]), len(generated[key]))
            if isinstance(original[key], dict):
                for subkey in original[key]:
                    self.assertTrue(subkey in generated[key])


if __name__ == '__main__':
    unittest.main()
