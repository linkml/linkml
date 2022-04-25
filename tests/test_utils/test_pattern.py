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
        materialize_patterns(sv)

        # create tempfile where the materializes YAML 
        # file should be saved
        new_file, filename = tempfile.mkstemp()

        path_to_yaml = filename + ".yaml"

        yaml_dumper.dump(sv.schema, path_to_yaml)

        sv = SchemaView(path_to_yaml)

        slot_patterns = []  # patterns associated with all slots
        for _, slot_defn in sv.all_slots().items():
            slot_patterns.append(slot_defn.pattern)

        # check that the expected patterns are associated with
        # at least one of the slots in the SchemaView
        self.assertIn("\\d+[\\.\\d+] (centimeter|meter|inch)", slot_patterns)
        self.assertIn("\\d+[\\.\\d+] (kg|g|lbs|stone)", slot_patterns)


if __name__ == "__main__":
    unittest.main()
