import logging
import unittest
from unittest import TestCase
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.linkml_model import ClassDefinition

from tests.test_issues.environment import env


class Issue998TestCase(TestCase):
    """
    https://github.com/linkml/linkml/issues/1126
    Test getting classes that modify a slot
    """
    env = env

    def test_issue_1126_slot_classes(self):
        view = SchemaView(env.input_path('linkml_issue_1126.yaml'))
        slot_classes = view.get_classes_modifying_slot("type")
        assert len(slot_classes) == 2
        for element in slot_classes:
            assert type(element) is ClassDefinition
        assert slot_classes[0].name == "Programmer"
        assert slot_classes[1].name == "Administrator"


if __name__ == "__main__":
    unittest.main()
