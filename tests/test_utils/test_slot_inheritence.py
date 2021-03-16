import unittest

from linkml.utils.schemaloader import SchemaLoader
from tests.test_utils.environment import env


class InheritedSlotTestCase(unittest.TestCase):

    def test_inherited_slot(self):
        """ Validate default slot range settings """
        schema = SchemaLoader(env.input_path('inherited_slots.yaml')).resolve()
        self.assertTrue('same as' in schema.classes['named thing'].slots)


if __name__ == '__main__':
    unittest.main()
