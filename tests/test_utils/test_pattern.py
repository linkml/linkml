import unittest

from tests.test_utils.environment import env

from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.dumpers import yaml_dumper

from linkml.utils.pattern import materialize_patterns


class PatternTestCase(unittest.TestCase):
    def test_materialize_patterns(self):
        """Test method that consolidate composite patterns."""

        sv = SchemaView(env.input_path("pattern-example.yaml"))
        materialize_patterns(sv)

        print(yaml_dumper.dumps(sv.schema))


if __name__ == "__main__":
    unittest.main()
