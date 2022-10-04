import unittest

from tests.test_utils.environment import env

from linkml_runtime.utils.schemaview import SchemaView

from linkml_runtime.utils.pattern import PatternResolver, generate_patterns


class PatternTestCase(unittest.TestCase):
    def test_generate_patterns(self):
        """Test method that consolidates composite patterns."""
        sv = SchemaView(env.input_path("pattern-example.yaml"))

        # actual result returned from call to generate_patterns()
        actual_dict = generate_patterns(sv)

        expected_dict = {
            "{float} {unit.length}": "\\d+[\\.\\d+] (centimeter|meter|inch)",
            "{float} {unit.weight}": "\\d+[\\.\\d+] (kg|g|lbs|stone)",
        }

        self.assertDictEqual(actual_dict, expected_dict)


    def test_pattern_resolver(self):
        sv = SchemaView(env.input_path("pattern-example.yaml"))

        resolver = PatternResolver(sv)

        self.assertEqual(resolver.resolve("{float} {unit.length}"), "\\d+[\\.\\d+] (centimeter|meter|inch)")
        self.assertEqual(resolver.resolve("{float} {unit.weight}"), "\\d+[\\.\\d+] (kg|g|lbs|stone)")


if __name__ == "__main__":
    unittest.main()
