import unittest

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition

from linkml.utils.schema_builder import SchemaBuilder


class UniqueKeyTestCase(unittest.TestCase):
    def test_range_is_built(self):
        asserted_person_range = "Person"
        scrutinized_slot = "person_set"
        b = SchemaBuilder()
        b.add_defaults()
        b.add_slot(SlotDefinition("id", range="str"))
        b.add_slot(SlotDefinition("name", range="str"))
        # , multivalued=True, inlined_as_list=True
        b.add_slot(SlotDefinition(scrutinized_slot, range=asserted_person_range))
        b.add_class("Person", slots=["id", "name"])
        b.add_class("Database", slots=[scrutinized_slot])
        schema = b.schema
        view = SchemaView(schema)
        built_person_set_range = view.get_slot(scrutinized_slot).range
        self.assertEqual(built_person_set_range, asserted_person_range)
