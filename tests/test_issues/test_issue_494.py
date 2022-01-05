import unittest

from linkml_runtime.utils.schemaview import SchemaView
from linkml.utils.datautils import infer_root_class

from tests.test_issues.environment import env

SCHEMA = env.input_path('issue_494/slot_usage_example.yaml')


class AmbiguousInferredTargetClass(unittest.TestCase):
    def test_jsonschema_validation(self):
        """Test case that tries to infer the target class for a schema
           that has a local import and doesn't explicitly specify the
           target class"""
        sv = SchemaView(schema=SCHEMA)

        with self.assertRaises(RuntimeError, msg="Multiple potential target "
                                                  "classes found: ['Container', 'annotation']. "
                                                  "Please specify a target class using --target-class "
                                                  "or by adding a tree_root: true to the relevant class in the schema"):
            # infer target_class rather than explicit specification
            inferred_target_class = infer_root_class(sv)


if __name__ == '__main__':
    unittest.main()
