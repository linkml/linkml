import unittest

from linkml_runtime.dumpers import yaml_dumper

from linkml.utils.schema_builder import SchemaBuilder

MY_CLASS = "MyClass"
MY_ENUM = "MyEnum"
FULL_NAME = "full name"
DESC = "description"
LIVING = "Living"
DEAD = "Dead"


class SchemaBuilderTestCase(unittest.TestCase):
    """
    Tests SchemaBuilder
    """

    def test_build_schema(self):
        """
        test a minimal schema with no primary names declared
        """
        b = SchemaBuilder()
        slots = [FULL_NAME, DESC]
        b.add_class(MY_CLASS, slots)
        b.add_enum(MY_ENUM, [LIVING, DEAD])
        s = b.schema
        c = s.classes[MY_CLASS]
        e = s.enums[MY_ENUM]
        self.assertEqual(c.name, MY_CLASS)
        self.assertCountEqual(slots, c.slots)
        self.assertEqual(e.name, MY_ENUM)
        self.assertCountEqual([LIVING, DEAD], e.permissible_values)


if __name__ == "__main__":
    unittest.main()
