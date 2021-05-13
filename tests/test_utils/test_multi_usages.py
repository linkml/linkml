import unittest
from typing import Optional

from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml.utils.schemaloader import SchemaLoader
from linkml_runtime.utils.yamlutils import as_yaml
from tests.utils.filters import yaml_filter
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_utils.environment import env


class SlotUsageTestCase(TestEnvironmentTestCase):
    env = env

    def _eval_expected(self, schema: SchemaDefinition, slotname: str, alias: Optional[str], domain_of: str,
                       is_a: Optional[str], usage_slot_name: Optional[str], range: str) -> None:
        slot = schema.slots[slotname]
        self.assertEqual(slotname, slot.name)
        self.assertEqual(alias, slot.alias) if alias else self.assertIsNone(slot.alias)
        self.assertEqual([domain_of], slot.domain_of)
        self.assertEqual(is_a, slot.is_a) if is_a else self.assertIsNone(slot.is_a)
        self.assertEqual(usage_slot_name, slot.usage_slot_name) if usage_slot_name else\
            self.assertIsNone(slot.usage_slot_name)
        self.assertEqual(range, slot.range)

    def test_multi_usages(self):
        """ Slot usage chain without starting alias """
        schema = SchemaLoader(env.input_path('multi_usages.yaml')).resolve()
        self._eval_expected(schema, 's1', None, 'root_class', None, None, 'string')
        self._eval_expected(schema, 'child_class1_s1', 's1', 'child_class1', 's1', 's1', 'boolean')
        self._eval_expected(schema, 'child_class2_s1', 's1', 'child_class2', 'child_class1_s1', 's1', 'integer')
        self._eval_expected(schema, 'child_class3_s1', 's1', 'child_class3', 'child_class2_s1', 's1', 'integer')
        env.eval_single_file(env.expected_path('multi_usages.yaml'), as_yaml(schema), filtr=yaml_filter)

    def test_multi_usages_2(self):
        """ Slot usage chain with starting alias """
        schema = SchemaLoader(env.input_path('multi_usages_2.yaml')).resolve()
        self._eval_expected(schema, 's1', 'value', 'root_class', None, None, 'string')
        self._eval_expected(schema, 'child_class1_s1', 'value', 'child_class1', 's1', 's1', 'boolean')
        self._eval_expected(schema, 'child_class2_s1', 'value', 'child_class2', 'child_class1_s1', 's1', 'integer')
        self._eval_expected(schema, 'child_class3_s1', 'value', 'child_class3', 'child_class2_s1', 's1', 'integer')
        env.eval_single_file(env.expected_path('multi_usages_2.yaml'), as_yaml(schema), filtr=yaml_filter)

    def test_multi_usages_3(self):
        """ Illegal alias usage """
        with self.assertRaises(ValueError) as e:
            schema = SchemaLoader(env.input_path('multi_usages_3.yaml')).resolve()
        self.assertIn('Class: "child_class1" - alias not permitted in slot_usage slot: foo', str(e.exception))


if __name__ == '__main__':
    unittest.main()
