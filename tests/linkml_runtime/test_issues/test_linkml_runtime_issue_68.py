import logging
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
            - slot2
            - slot3
        slot_usage:
            slot2:
                description: induced slot2
                required: true
                range: class1
    class2:
        is_a: class1
        
    mixin1:
        mixin: true
        slot_usage:
            slot2:
                description: mixin slot2
                required: false
                range: mixin1
    class2_1:
        is_a: class2
        mixins:
          - mixin1
          
    class0:
          
slots:
    slot1:
        description: non-induced slot1
        range: class0
    slot2:
        description: non-induced slot2
        required: false
        range: class0
    slot3:
        range: class0
    
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
        assert s1.range == 'class0'

        s2 = view.get_slot("slot2")
        assert not s2.required
        assert s2.range == 'class0'

        s2_induced = view.induced_slot("slot2", "class1")
        assert s2_induced.required
        assert s2_induced.range == 'class1'

        # test description for slot2
        # this behavior is expected see: https://github.com/linkml/linkml-runtime/issues/68
        logging.info(f"s2_induced.description: {s2_induced.description}")
        assert s2_induced.description == "induced slot2"

        s2_induced_c2 = view.induced_slot('slot2', 'class2')
        assert s2_induced_c2.required
        logging.info(f"s2_induced_c2.description: {s2_induced_c2.description}")
        assert s2_induced_c2.description == "non-induced slot2"
        assert s2_induced.range == 'class1'

        s3_induced_c2 = view.induced_slot('slot3', 'class2')
        assert not s3_induced_c2.required
        assert s3_induced_c2.description == None
        assert s3_induced_c2.range == 'class0'

        # mixins take priority
        s2_induced_c2_1 = view.induced_slot('slot2', 'class2_1')
        assert not s2_induced_c2_1.required
        logging.info(f"s2_induced_c2_1.description: {s2_induced_c2_1.description}")
        assert s2_induced_c2_1.description == "non-induced slot2"
        assert s2_induced_c2_1.range == 'mixin1'



if __name__ == "__main__":
    unittest.main()
