import unittest

from linkml.generators.pythongen import PythonGenerator
from tests.test_base.environment import env
from tests.utils.filters import metadata_filter
from tests.utils.python_comparator import compare_python
from tests.utils.test_environment import TestEnvironmentTestCase


class PythonTestCase(TestEnvironmentTestCase):
    """ Generate python for all of the models, compare them against what has been published
     and verify that they compile"""
    env = env

    @classmethod
    def setUpClass(cls) -> None:
        env.make_testing_directory(env.root_temp_file_path('includes'))

    def test_types_python(self):
        """ Build includes/types.py """
        env.generate_single_file('includes/types.py',
                                 lambda: PythonGenerator(env.types_yaml, importmap=env.import_map, genmeta=True).serialize(),
                                 value_is_returned=True, filtr=metadata_filter,
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('includes/types.py')),
                                 use_testing_root=True)

    def test_mapping_python(self):
        """ Build includes/mappings.py """
        env.generate_single_file('includes/mappings.py',
                                 lambda: PythonGenerator(env.mapping_yaml, importmap=env.import_map, genmeta=True).serialize(),
                                 value_is_returned=True, filtr=metadata_filter,
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('includes/mappings.py')),
                                 use_testing_root=True)

    def test_extensions_python(self):
        """ Build includes/extensions.py """
        env.generate_single_file('includes/extensions.py',
                                 lambda: PythonGenerator(env.input_path('includes', 'extensions.yaml'),
                                                         importmap=env.import_map, genmeta=True).serialize(),
                                 value_is_returned=True, filtr=metadata_filter,
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('includes/extensions.py')),
                                 use_testing_root=True)

    def test_annotations_python(self):
        """ Build includes/annotations.py """
        env.generate_single_file('includes/annotations.py',
                                 lambda: PythonGenerator(env.input_path('includes', 'annotations.yaml'),
                                                         importmap=env.import_map, genmeta=True).serialize(),
                                 value_is_returned=True, filtr=metadata_filter,
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('includes/annotations.py')),
                                 use_testing_root=True)

    def test_metamodel_python(self):
        """ Build meta.py """
        env.generate_single_file('meta.py',
                                 lambda: PythonGenerator(env.meta_yaml, importmap=env.import_map, genmeta=True).serialize(),
                                 value_is_returned=True, filtr=metadata_filter,
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('meta.py')),
                                 use_testing_root=True)


if __name__ == '__main__':
    unittest.main()
