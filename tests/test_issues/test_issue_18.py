import unittest

from linkml.utils.schemaloader import SchemaLoader
from linkml_runtime.utils.yamlutils import as_yaml
from tests.test_issues.environment import env
from tests.utils.filters import yaml_filter
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue18TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_18(self):
        """ Make sure that inverses are automatically generated """
        env.generate_single_file('issue_18.yaml',
                                 lambda: as_yaml(SchemaLoader(env.input_path('issue_18.yaml')).resolve()),
                                 filtr=yaml_filter, value_is_returned=True)

    def test_inverse_mismatch(self):
        """ Test error detection when inverses don't match """
        with self.assertRaises(ValueError) as e:
            env.generate_single_file('issue_18_error1.yaml',
                                     lambda: as_yaml(SchemaLoader(env.input_path('issue_18_error1.yaml')).resolve()),
                                     value_is_returned=True)
        self.assertEqual('Slot s1.inverse (s2) does not match slot s2.inverse (s3)', str(e.exception).strip())

    def test_missing_inverse(self):
        with self.assertRaises(ValueError) as e:
            env.generate_single_file('issue_18_error2.yaml',
                                     lambda: as_yaml(SchemaLoader(env.input_path('issue_18_error2.yaml')).resolve()),
                                     value_is_returned=True)
        self.assertEqual('Slot s1.inverse (s2) is not defined', str(e.exception).strip())

    def test_no_inverse_domain(self):
        with self.assertRaises(ValueError) as e:
            env.generate_single_file('issue_18_error3.yaml',
                                     lambda: as_yaml(SchemaLoader(env.input_path('issue_18_error3.yaml')).resolve()),
                                     value_is_returned=True)
        self.assertEqual("Unable to determine the range of slot `s1'. Its inverse (s2) has no declared domain",
                         str(e.exception).strip())

    def test_multi_domains(self):
        with self.redirect_logstream() as logger:
            env.generate_single_file('issue_18_warning1.yaml',
                                     lambda: as_yaml(SchemaLoader(env.input_path('issue_18_warning1.yaml'),
                                                                  logger=logger).resolve()),
                                     filtr=yaml_filter, value_is_returned=True)
        self.assertIn('Slot s2.inverse (s1), has multi domains (c1, c2)  Multi ranges not yet implemented',
                      logger.result)




if __name__ == '__main__':
    unittest.main()
