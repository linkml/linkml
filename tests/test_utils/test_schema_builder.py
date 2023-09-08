import unittest

from linkml.utils.schema_builder import SchemaBuilder

MY_CLASS = "MyClass"
MY_ENUM = "MyEnum"
FULL_NAME = "full name"
DESC = "description"
AGE = "age"
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
        b = SchemaBuilder("my-schema")
        slots = [FULL_NAME, DESC]
        b.add_class(MY_CLASS, slots, description="A test class")
        b.add_enum(MY_ENUM, [LIVING, DEAD])
        s = b.schema
        self.assertEqual(s.name, "my-schema")
        c = s.classes[MY_CLASS]
        e = s.enums[MY_ENUM]
        self.assertEqual(c.name, MY_CLASS)
        self.assertEqual(c.description, "A test class")
        self.assertCountEqual(slots, c.slots)
        self.assertEqual(e.name, MY_ENUM)
        self.assertCountEqual([LIVING, DEAD], e.permissible_values)
        b.add_type("MyType", typeof="string", description="A test type")
        self.assertEqual(s.types["MyType"].description, "A test type")
        d = b.as_dict()
        self.assertEqual(d["classes"][MY_CLASS]["slots"], [FULL_NAME, DESC])
        # no defaults by default
        self.assertEqual([], s.imports)
        # defaults added
        b.add_defaults()
        self.assertEqual(["linkml:types"], s.imports)
        d = b.as_dict()

    def test_slot_overrides(self):
        """
        tests for edge cases involving overrides
        """
        b = SchemaBuilder()
        b.add_slot(AGE, range="integer")
        self.assertEqual(b.schema.slots[AGE].range, "integer")
        b.add_class(MY_CLASS, [AGE])
        # add_class will (a) add the slot name to the list of applicable slots
        # (b) add a slot definition to the top level slot definitions
        # Note that (b) should only happen if the slot is not already present
        self.assertEqual(b.schema.slots[AGE].range, "integer")
        with self.assertRaises(ValueError):
            b.add_slot(AGE, range="string")
        b.add_slot(AGE, range="string", replace_if_present=True)


if __name__ == "__main__":
    unittest.main()
