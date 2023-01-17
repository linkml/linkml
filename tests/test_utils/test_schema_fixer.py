import unittest
from copy import deepcopy

from linkml_runtime.linkml_model import SlotDefinitionName, SlotDefinition

from linkml.utils.schema_builder import SchemaBuilder
from linkml.utils.schema_fixer import SchemaFixer

MY_CLASS = "MyClass"
MY_CLASS2 = "MyClass2"
MY_ENUM = "MyEnum"
ID = "id"
FULL_NAME = "full_name"
DESC = "description"
LIVING = "Living"
DEAD = "Dead"


class SchemaFixerTestCase(unittest.TestCase):
    """
    Tests SchemaFixer
    """

    def test_add_titles(self):
        b = SchemaBuilder()
        slots = [FULL_NAME, DESC]
        b.add_class(MY_CLASS, slots)
        b.add_enum(MY_ENUM, [LIVING, DEAD])
        s = b.schema
        fixer = SchemaFixer()
        fixer.add_titles(s)
        #print(fixer.history)
        #print(yaml_dumper.dumps(s))
        c = s.classes[MY_CLASS]
        e = s.enums[MY_ENUM]
        self.assertEqual(c.title, "my class")
        self.assertEqual(e.title, "my enum")
        self.assertEqual(s.slots[FULL_NAME].title, "full name")

    def test_add_container(self):
        b = SchemaBuilder()
        slots = [FULL_NAME, DESC]
        b.add_class(MY_CLASS, slots)
        s = b.schema
        fixer = SchemaFixer()
        container_name = "MyContainer"
        fixer.add_container(s, class_name=container_name, convert_camel_case=True)
        c = s.classes[container_name]
        index_slot_name = SlotDefinitionName("my_class_index")
        self.assertCountEqual([index_slot_name], c.slots)
        self.assertTrue(c.tree_root)
        index_slot = s.slots[index_slot_name]
        self.assertTrue(index_slot.multivalued)
        self.assertEqual(MY_CLASS, index_slot.range)
        self.assertTrue(index_slot.inlined_as_list)

    def test_attributes_to_slots(self):
        b = SchemaBuilder()
        b.add_class(MY_CLASS, [SlotDefinition(FULL_NAME), SlotDefinition(DESC)])
        s = b.schema
        fixer = SchemaFixer()
        fixer.attributes_to_slots(s, remove_redundant_slot_usage=False)
        #print(fixer.history)
        #print(yaml_dumper.dumps(s))
        c = s.classes[MY_CLASS]
        self.assertCountEqual([FULL_NAME, DESC], c.slots)
        self.assertEqual({}, c.attributes)
        self.assertEqual(s.slots[FULL_NAME].name, FULL_NAME)
        self.assertEqual(s.slots[DESC].name, DESC)

    def test_merge_slot_usage(self):
        b = SchemaBuilder()
        b.add_class(MY_CLASS)
        s = b.schema
        fixer = SchemaFixer()
        c = s.classes[MY_CLASS]
        fixer.merge_slot_usage(
            s, c, SlotDefinition(FULL_NAME, description="desc1", range="string")
        )
        #print(yaml_dumper.dumps(s))
        su = c.slot_usage[FULL_NAME]
        self.assertEqual("desc1", su.description)
        self.assertEqual("string", su.range)
        fixer.merge_slot_usage(
            s,
            c,
            SlotDefinition(
                FULL_NAME,
                # description='desc2',
                comments=["comment1"],
                is_a="foo",
                range="string",
            ),
        )
        #print(yaml_dumper.dumps(s))
        su = c.slot_usage[FULL_NAME]
        with self.assertRaises(ValueError):
            fixer.merge_slot_usage(s, c, SlotDefinition(FULL_NAME, description="desc2"))
        self.assertEqual("desc1", su.description)
        fixer.merge_slot_usage(
            s, c, SlotDefinition(FULL_NAME, description="desc2"), overwrite=True
        )
        #print(yaml_dumper.dumps(s))
        su = c.slot_usage[FULL_NAME]
        self.assertEqual("desc2", su.description)

    def test_remove_redundant(self):
        """
        Tests
        """
        b = SchemaBuilder()
        s = b.schema
        slot1 = SlotDefinition(ID, title="identifier", description="unique identifier")
        slot2 = SlotDefinition(FULL_NAME, description="full name", range="string")
        slot3 = SlotDefinition(DESC, description="used to describe")
        b.add_class(MY_CLASS, [slot1.name, slot2.name, slot3.name])
        c = s.classes[MY_CLASS]
        # add a slot usage for ID that is intentionally partially redundant with the main slot
        # here the description is redundant
        c.slot_usage[ID] = SlotDefinition(
            ID,
            identifier=True,
            comments=["my comment1"],
            description="unique identifier",
        )
        # add a slot usage for full_name that is intentionally partially redundant with the main slot
        c.slot_usage[FULL_NAME] = SlotDefinition(
            FULL_NAME, range="string", description="full name", pattern="^.*$"
        )
        # add a slot usage that is fully redundant
        c.slot_usage[DESC] = SlotDefinition(DESC, range="string")
        b.add_slot(deepcopy(slot1), replace_if_present=True).add_slot(deepcopy(slot2), replace_if_present=True)
        b.add_defaults()
        fixer = SchemaFixer()
        fixer.remove_redundant_slot_usage(s)
        # not-redundant; should be preserved
        self.assertEqual(c.slot_usage[ID].identifier, True)
        self.assertEqual(c.slot_usage[ID].comments, ["my comment1"])
        self.assertEqual(c.slot_usage[FULL_NAME].pattern, "^.*$")
        # redundant; should be removed
        self.assertNotIn(DESC, c.slot_usage)
        self.assertNotIn("description", c.slot_usage[ID])
        self.assertNotIn("range", c.slot_usage[FULL_NAME])

    def test_attributes_to_slots_remove_redundant(self):
        b = SchemaBuilder()
        b.add_class(
            MY_CLASS,
            [
                SlotDefinition(ID, identifier=True),
                SlotDefinition(FULL_NAME, description="full name", range="string"),
                SlotDefinition(DESC, description="description"),
            ],
        )
        b.add_class(
            MY_CLASS2,
            [
                SlotDefinition(FULL_NAME, description="full name2", range="string"),
                SlotDefinition(DESC, description="description"),
            ],
            replace_if_present=True,
        )
        s = b.schema
        fixer = SchemaFixer()
        fixer.attributes_to_slots(s, remove_redundant_slot_usage=True)
        #print(fixer.history)
        #print(yaml_dumper.dumps(s))
        c = s.classes[MY_CLASS]
        self.assertCountEqual([ID, FULL_NAME, DESC], c.slots)
        self.assertEqual({}, c.attributes)
        self.assertEqual(s.slots[FULL_NAME].name, FULL_NAME)
        self.assertEqual(s.slots[DESC].name, DESC)


if __name__ == "__main__":
    unittest.main()
