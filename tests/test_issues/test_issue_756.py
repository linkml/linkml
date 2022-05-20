import unittest
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper

from tests.test_issues.environment import env
import yaml

# tests/test_issues/input/issue_756.yaml
SCHEMA = env.input_path("issue_756.yaml")


class MyTestCase(unittest.TestCase):
    def test_something(self):
        sv = SchemaView(SCHEMA)
        self.assertEqual(sv.schema.name, "test")  # add assertion here
        # print(sv.all_enums())
        test_ae = yaml_dumper.dumps(sv.all_enums())
        print(test_ae)


if __name__ == '__main__':
    unittest.main()
