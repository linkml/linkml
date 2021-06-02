import unittest

from linkml.utils.schemaloader import SchemaLoader
from tests.test_issues.environment import env


class ClassListIssueTest(unittest.TestCase):
    "Issue #206 - SchemaLoader needs to do a yaml_loader.load early on"
    @unittest.expectedFailure
    def test_class_list(self):
        """ SchemaLoader should be monotonic - metamodel test """
        biolink_schema = SchemaLoader(env.input_path('issue_206.yaml')).resolve()


if __name__ == '__main__':
    unittest.main()
