import os
import unittest

from jsonasobj2 import as_json

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.python_comparator import compare_python
from linkml_runtime.utils.compile_python import compile_python
from tests.utils.test_environment import TestEnvironmentTestCase


class IssuePythonOrderingTestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_python_ordering(self):
        """ Make sure that types are generated as part of the output """
        env.generate_single_file('issue_134.py',
                                 lambda: PythonGenerator(env.input_path('issue_134.yaml')).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('issue_134.py')),
                                 value_is_returned=True)
        module = compile_python(env.expected_path('issue_134.py'))
        e = module.E('id:1')
        b = module.B('id:2')
        e.has_b = b

        def output_generator(dirname) -> None:
            with open(os.path.join(dirname, 'issue_134.json'), 'w') as f:
                f.write(as_json(e))

        env.generate_directory('issue_134', lambda dirname: output_generator(dirname) )


if __name__ == '__main__':
    unittest.main()
