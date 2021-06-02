import unittest

from linkml.generators.pythongen import PythonGenerator
from tests.utils.python_comparator import compare_python
from linkml_runtime.utils.compile_python import compile_python
from tests.utils.filters import metadata_filter

from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env
# from tests.test_issues.output.issue_14 import MixinOwner, SubjectRange1, NamedThing


class InheritedPhenotypicFeatureTestCase(TestEnvironmentTestCase):
    env = env

    def test_inheritence(self):
        env.generate_single_file('issue_14.py',
                                 lambda: PythonGenerator(env.input_path('issue_14.yaml')).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('issue_14.py')),
                                 filtr=metadata_filter, value_is_returned=True)

        # Added test for issue #183, where sex_qualifier disappeared from MixinOwner class
        module = compile_python(env.expected_path('issue_14.py'))
        subject = module.SubjectRange1(id='sr1',name="SubjectRange1", subject='thing1', object='thing2')
        mixin_owner = module.MixinOwner(id='mo1', subject='sr1', name='MixinOwner1', object='thing2', sex_qualifier="ntx")



if __name__ == '__main__':
    unittest.main()
