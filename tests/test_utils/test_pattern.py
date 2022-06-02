import tempfile
import unittest

from tests.test_utils.environment import env

from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.dumpers import yaml_dumper

from linkml.utils.pattern import materialize_patterns


class PatternTestCase(unittest.TestCase):
    def test_materialize_patterns(self):
        """Test method that consolidate composite patterns."""

        sv = SchemaView(env.input_path("pattern-example.yaml"))

        # actual result returned from call to materialize_patterns()
        actual_dict = materialize_patterns(sv)

        expected_dict = {
            "{float} {unit.length}": "\\d+[\\.\\d+] (centimeter|meter|inch)",
            "{float} {unit.weight}": "\\d+[\\.\\d+] (kg|g|lbs|stone)",
        }

        self.assertDictEqual(actual_dict, expected_dict)


if __name__ == "__main__":
    unittest.main()
