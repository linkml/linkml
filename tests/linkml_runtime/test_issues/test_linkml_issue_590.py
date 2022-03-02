import unittest

from linkml_runtime.utils.schemaview import SchemaView

from tests.test_issues.environment import env

SCHEMA = env.input_path('test_linkml_issue_590.yaml')


class Issue590TestCase(unittest.TestCase):
    env = env

    def test_issue_590(self):
        """get_slot() returns attribute not top level slot"""
        sv = SchemaView(SCHEMA)

        # check that multivalued is set to False as in schema
        self.assertEqual(sv.get_slot('a').multivalued, False)


if __name__ == '__main__':
    unittest.main()
