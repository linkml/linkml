import logging
import unittest
from unittest import TestCase
from linkml_runtime.utils.schemaview import SchemaView

from tests.test_issues.environment import env


class Issue998TestCase(TestCase):
    """
    https://github.com/linkml/linkml/issues/998
    """
    env = env

    def test_issue_998_schema_slot(self):
        view = SchemaView(env.input_path('linkml_issue_998.yaml'))
        enum_slots = view.get_slots_by_enum("PersonStatusEnum")
        # assert type(enum_slots) is List[SlotDefinition]
        assert len(enum_slots) == 1
        assert enum_slots[0].name == "status"

    def test_issue_998_attribute_slot(self):
        view = SchemaView(env.input_path('linkml_issue_998.yaml'))
        enum_slots = view.get_slots_by_enum("EmploymentStatusEnum")
        assert len(enum_slots) == 1
        assert enum_slots[0].name == "employed"

    def test_issue_998_schema_and_atribute_slots(self):
        view = SchemaView(env.input_path('linkml_issue_998.yaml'))
        enum_slots = view.get_slots_by_enum("RelationshipStatusEnum")
        assert len(enum_slots) == 2
        assert enum_slots[0].name == "relationship"
        assert enum_slots[1].name == "past_relationship"

    def test_issue_998_slot_usage_range(self):
        view = SchemaView(env.input_path('linkml_issue_998.yaml'))
        enum_slots = view.get_slots_by_enum("TypeEnum")
        assert len(enum_slots) == 1
        assert enum_slots[0].name == "type"


if __name__ == "__main__":
    unittest.main()
