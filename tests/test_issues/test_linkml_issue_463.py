import unittest

from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


data_str = """
contains:
 - label: n1
   type:
     label: n1 label
     system: n1 system
 - label: n2
   type:
     label: n2 label
     system: n2 system
"""



class IssueJSONSchemaInlinedAsDictCase(TestEnvironmentTestCase):
    env = env

    def test_inlined(self):
        """ Ensure that inlined lists without identifiers work """
        gen = PythonGenerator(env.input_path('linkml_issue_463.yaml'))
        pystr = gen.serialize()
        #print(pystr)
        with open(env.expected_path('linkml_issue_463.py'), 'w') as stream:
            stream.write(pystr)
        module = compile_python(pystr)

        # Uncomment these two lines for debugging
        # from tests.test_issues.output.linkml_issue_463 import Container
        # obj = yaml_loader.loads(data_str, target_class=Container)
        # TODO: this currently yields "TypeError: unhashable type: 'TypeObj'"
        obj = yaml_loader.loads(data_str, target_class=module.Container)


if __name__ == '__main__':
    unittest.main()
