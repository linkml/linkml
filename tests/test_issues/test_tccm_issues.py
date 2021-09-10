import logging
import unittest
import inspect

from linkml.generators import *
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.yamlgen import YAMLGenerator
from linkml.utils.generator import Generator
from linkml.utils.schemaloader import SchemaLoader
from tests.utils.python_comparator import compare_python
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env


class TCCMTestCase(TestEnvironmentTestCase):
    env = env

    """ Unit tests for issues encountered in the TCCM model generation """
    def test_references_typeerror(self):
        """  TypeError: sequence item 0: expected str instance, NoneType found is generated from schemasynopsis """
        SchemaLoader(env.input_path('issue_tccm', 'resourcedescription.yaml'), mergeimports=False).resolve()

    def test_slot_usage_only(self):
        """ Slot_usages without parents don't generate slots period. """
        env.generate_single_file('issue_ttcm_1.py',
                                 lambda: PythonGenerator(env.input_path('issue_tccm', 'resourcedescription.yaml'),
                                                         importmap=env.import_map, mergeimports=True).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, env.expected_path('issue_ttcm_1.py')),
                                 value_is_returned=True)

    def test_mapping_prefix(self):
        """ Prefix validation fails in  """
        with self.redirect_logstream() as logger:
            YAMLGenerator(env.input_path('issue_tccm', 'illegal_mapping_prefix.yaml'),
                          mergeimports=False, logger=logger).serialize(validateonly=True)
        self.assertIn('Unrecognized prefix: DO', logger.result, "Basic slot mapping validation failure")
        self.assertIn('Unrecognized prefix: RE', logger.result, "Basic class mapping validation failure")
        self.assertIn('Unrecognized prefix: MI', logger.result, "Solo slot usage mapping validation failure")
        self.assertIn('Unrecognized prefix: FA', logger.result, "Slot usage specialization validation failure")
        self.assertIn('Unrecognized prefix: SO', logger.result, "Slot usage variant validation failure")
        self.assertIn('Unrecognized prefix: LA', logger.result, "Inherited slot mapping validation failure")
        self.assertIn('Unrecognized prefix: TI', logger.result, "Inherited class mapping mapping validation failure")

    def test_local_imports(self):
        """ Make sure there is a '.' on a local import in python """
        env.generate_single_file('importee.py',
                                 lambda: PythonGenerator(env.input_path('issue_tccm', 'importee.yaml'),
                                                         importmap=env.import_map, mergeimports=False).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, env.expected_path('importee.py')),
                                 value_is_returned=True)
        env.generate_single_file('importer.py',
                                 lambda: PythonGenerator(env.input_path('issue_tccm', 'importer.yaml'),
                                                         importmap=env.import_map, mergeimports=False).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, env.expected_path('importer.py')),
                                 value_is_returned=True)

    def test_minimal_model(self):
        """ Test to make the absolute minimal model work """
        YAMLGenerator(env.input_path('issue_tccm', 'minimalmodel.yaml'),
                      mergeimports=False, log_level=logging.INFO).serialize(validateonly=True)

        env.make_testing_directory(env.expected_path('issue_tccm'))
        for generator in Generator.__subclasses__():
            if not generator.__module__.startswith('linkml.generators') \
                    or generator.__name__ == 'SQLDDLGenerator'\
                    or getattr(generator.serialize, '__isabstractmethod__', True):
                pass
            elif not generator.directory_output:
                env.generate_single_file(['issue_tccm', 'minimalmodel.' + generator.valid_formats[0]],
                                         lambda: generator(env.input_path('issue_tccm', 'minimalmodel.yaml'),
                                                           importmap=env.import_map, mergeimports=False,
                                                           emit_metadata=False).serialize(),
                                         value_is_returned=True)
            else:
                env.generate_directory(['issue_tccm', generator.__name__],
                                        lambda d: generator(env.input_path('issue_tccm', 'minimalmodel.yaml'),
                                                           importmap=env.import_map, mergeimports=False,
                                                           emit_metadata=False).serialize(directory=d))


    @unittest.skipIf(True, "Outstanding issue")
    def test_dictionary_name(self):
        """ Allow dictionaries w/ explicit keys or identifiers through as long as they match """
        yaml = env.generate_single_file(['issue_tccm', 'explicit_key_id.yaml'],
                                        lambda: YAMLGenerator(env.input_path('issue_tccm', 'explicit_key_id.yaml'),
                                        importmap=env.import_map, mergeimports=False,
                                        emit_metadata=False).serialize(),
                                        value_is_returned = True)
        print(yaml)

if __name__ == '__main__':
    unittest.main()
