import unittest
from unittest import TestCase
from linkml_runtime.utils.schemaview import SchemaView

schema_str = """
id: https://example.com/test-induced
name: test-induced
title: test induced

description: >-
    test schema view's finding of induced slot information.

classes:
    class1:
        slots:
            - slot1
        slot_usage:
            slot2:
                description: induced slot2
                required: true
slots:
    slot1:
        description: non-induced slot1
    slot2:
        description: non-induced slot2
        required: false
    
"""


class Issue68TestCase(TestCase):
    """
    Note: linkml-runtime issue 68 was moved to https://github.com/linkml/linkml/issues/479
    """
    def test_issue_68(self):
        view = SchemaView(schema_str)

        # test descripton for slot1
        s1 = view.get_slot("slot1")
        assert s1.description == "non-induced slot1"

        s2 = view.get_slot("slot2")
        assert s2.required == False

        s2_induced = view.induced_slot("slot2", "class1")
        assert s2_induced.required == True

        # test description for slot2
        # this behavior is expected see: https://github.com/linkml/linkml-runtime/issues/68
        s2_induced = view.induced_slot("slot2", "class1")
        print("s2_induced.description:", s2_induced.description)
        assert s2_induced.description == "induced slot2"


if __name__ == "__main__":
    unittest.main()
