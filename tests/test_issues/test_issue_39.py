import unittest

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.python_comparator import validate_python


class Issue39UnitTest(unittest.TestCase):

    @unittest.skip("issue_38.yaml clinical profile conflicts with latest Biolink Model")
    def test_python_import(self):
        """ Import generates for biolink-model """
        python = PythonGenerator(env.input_path('issue_38.yaml'),
                                 importmap=env.input_path('biolink-model-importmap.json')).serialize()
        msg = validate_python(python, expected_path=env.expected_path('foo.py'))
        if msg:
            self.fail(msg)


if __name__ == '__main__':
    unittest.main()
