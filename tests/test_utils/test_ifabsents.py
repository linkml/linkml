import os
import unittest

from linkml.generators.pythongen import PythonGenerator
from tests.test_utils.environment import env
from tests.utils.generatortestcase import GeneratorTestCase
from tests.utils.filters import metadata_filter
from tests.utils.python_comparator import compare_python


class IfAbsentTestCase(GeneratorTestCase):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env = env

    model_name: str = None
    output_name: str = None

    def do_test(self):
        """ Test the metadata options"""
        self.single_file_generator('py', PythonGenerator,
                                   comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('x.py')))

    def test_good_ifabsent(self):
        """ Test isabsent with no default_prefix """
        IfAbsentTestCase.model_name = "ifabsents"
        self.do_test()

    def test_good_ifabsent2(self):
        """ Test isabsents with default_prefix specified """
        IfAbsentTestCase.model_name = "ifabsents2"
        self.do_test()

    def test_good_ifabsent3(self):
        """ Test isabsent with no default_prefix, but prefix specified that matches the module id """
        IfAbsentTestCase.model_name = "ifabsents3"
        self.do_test()

    def test_bad_ifabsent(self):
        IfAbsentTestCase.model_name = "ifabsents_error"
        with self.assertRaises(ValueError):
            self.single_file_generator('py', PythonGenerator, filtr=metadata_filter)

    def test_ifabsent_uri(self):
        IfAbsentTestCase.model_name = "ifabsent_uri"
        self.do_test()


if __name__ == '__main__':
    unittest.main()
