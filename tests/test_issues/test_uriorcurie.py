import unittest

from linkml.utils.schemaloader import SchemaLoader
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class UriOrCurieTestCase(TestEnvironmentTestCase):
    env = env

    def test_uriorcurie_error(self):
        """  """
        with self.assertRaises(ValueError) as e:
            SchemaLoader(env.input_path('issue_uriorcurie.yaml')).resolve()
        self.assertIn('Slot: "s1" - subproperty_of: "homologous to" does not reference a slot definition',
                      str(e.exception))


if __name__ == '__main__':
    unittest.main()
