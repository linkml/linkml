import unittest

from linkml.generators.pydanticgen import PydanticGenerator
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator

model_txt = """
id: https://example.org/ifabsent
name: ifabsent_test

prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/ifabsent/
default_prefix: ex
default_range: string

imports:
  - linkml:types

slots:
    bool_true_slot:
        range: boolean
        ifabsent: true
    bool_false_slot:
        range: boolean
        ifabsent: False
    bnode_slot:
        ifabsent: bnode
    class_curie_slot:
        ifabsent: class_curie
    class_uri_slot:
        range: uri
        ifabsent: class_uri
    default_ns_slot:
        ifabsent: default_ns
    default_range_slot:
        ifabsent: default_range
    int_42_slot:
        range: integer
        ifabsent: int(42)
    int_0_slot:
        range: integer
        ifabsent: int(0)
    neg_int_slot:
        range: integer
        ifabsent: int(-117243)
    slot_uri_slot:
        range: uri
        ifabsent: slot_uri
    slot_curie_slot:
        ifabsent: slot_curie
    string_slot:
        ifabsent: string(s1)
    mt_string_slot:
        ifabsent: string()

classes:
    HighClass:
        slots:
            - bool_true_slot
            - bool_false_slot
            - bnode_slot
            - class_curie_slot
            - class_uri_slot
            - default_ns_slot
            - default_range_slot
            - int_42_slot
            - int_0_slot
            - neg_int_slot
            - slot_uri_slot
            - slot_curie_slot
            - string_slot
            - mt_string_slot
"""


class IfAbsentTestCase(unittest.TestCase):
    def test_ifabsent(self):
        """
        Tests pythongenerator with ifabsent_functions.

        See: https://github.com/linkml/linkml/issues/1333
        """
        # print(PythonGenerator(model_txt).serialize())
        m = compile_python(PythonGenerator(model_txt).serialize())
        sample = m.HighClass()
        self.assertEqual(sample.bool_true_slot, True)
        self.assertEqual(sample.bool_false_slot, False)
        # TODO: class_curie_slot fails
        # self.assertEqual(sample.class_curie_slot, m.HighClass.class_class_curie)
        self.assertIsNone(sample.class_curie_slot)
        # TODO: class_uri_slot fails
        # self.assertEqual(sample.class_uri_slot, m.HighClass.class_class_uri)
        self.assertIsNone(sample.class_uri_slot)

        # TODO: default_ns fails")
        # self.assertEqual(sample.default_ns_slot, 'ex')
        self.assertEqual(sample.default_ns_slot, None)
        # TODO: default_range fails
        # self.assertEqual(sample.default_range_slot, 'string')
        self.assertIsNone(sample.default_range_slot)
        # TODO: int(0) fails
        self.assertEqual(sample.int_0_slot, 0)
        self.assertEqual(sample.int_42_slot, 42)
        self.assertEqual(sample.neg_int_slot, -117243)
        # TODO: slot_curie fails
        # self.assertEqual(sample.slot_curie_slot, m.slots.slot_curie_slot.curie)
        self.assertIsNone(sample.slot_curie_slot)
        # TODO: slot_uri fails
        # self.assertEqual(sample.slot_uri_slot, m.slots.slot_uri_slot.uri)
        self.assertIsNone(sample.slot_uri_slot)
        self.assertIsNone(sample.slot_curie_slot)
        self.assertEqual(sample.string_slot, "s1")
        self.assertEqual(sample.mt_string_slot, "")

    @unittest.skip("TODO: https://github.com/linkml/linkml/issues/1334")
    def test_ifabsent_pydantic(self):
        """
        Tests pydantic generator with ifabsent_functions.

        See: https://github.com/linkml/linkml/issues/1334
        """
        m = compile_python(PydanticGenerator(model_txt).serialize())
        sample = m.HighClass()
        self.assertEqual(sample.bool_true_slot, True)
        self.assertEqual(sample.bool_false_slot, False)
        # TODO: class_curie_slot fails
        # self.assertEqual(sample.class_curie_slot, m.HighClass.class_class_curie)
        self.assertIsNone(sample.class_curie_slot)
        # TODO: class_uri_slot fails
        # self.assertEqual(sample.class_uri_slot, m.HighClass.class_class_uri)
        self.assertIsNone(sample.class_uri_slot)
        # TODO: default_ns fails
        self.assertEqual(sample.default_ns_slot, 'ex')
        # TODO: default_range fails
        # self.assertEqual(sample.default_range_slot, 'string')
        self.assertIsNone(sample.default_range_slot)
        # TODO: int(0) fails
        self.assertEqual(sample.int_0_slot, 0)
        self.assertEqual(sample.int_42_slot, 42)
        self.assertEqual(sample.neg_int_slot, -117243)
        # TODO: slot_curie fails
        # self.assertEqual(sample.slot_curie_slot, m.slots.slot_curie_slot.curie)
        self.assertIsNone(sample.slot_curie_slot)
        # TODO: slot_uri fails
        # self.assertEqual(sample.slot_uri_slot, m.slots.slot_uri_slot.uri)
        self.assertIsNone(sample.slot_uri_slot)
        self.assertIsNone(sample.slot_curie_slot)
        self.assertEqual(sample.string_slot, "s1")
        self.assertEqual(sample.mt_string_slot, "")


if __name__ == '__main__':
    unittest.main()
