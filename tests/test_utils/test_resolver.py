import os
import unittest

from linkml.utils.schemaloader import SchemaLoader
from jsonasobj2 import as_dict, as_json, JsonObj, load

from tests.test_utils.environment import env


class ResolverTestCase(unittest.TestCase):

    def test_default_range(self):
        """ Validate default slot range settings """
        schema = SchemaLoader(env.input_path('resolver1.yaml')).resolve()
        self.assertEqual({'s1':'t1', 's2':'t2'}, {slot.name: slot.range for slot in schema.slots.values()})
        schema = SchemaLoader(env.input_path('resolver2.yaml')).resolve()
        self.assertEqual({'s1': 'string', 's2': 't2'}, {slot.name: slot.range for slot in schema.slots.values()})

    def test_type_uri(self):
        """ Validate type URI's and the fact that they aren't inherited """
        schema = SchemaLoader(env.input_path('resolver2.yaml')).resolve()
        self.assertEqual({'string': 'xsd:string', 't1': 'xsd:string', 't2': 'xsd:int', 't3': 'xsd:string'},
                         {t.name: t.uri for t in schema.types.values()})

    def test_element_slots(self):
        """ Test all element slots and their inheritence """
        schema = SchemaLoader(env.input_path('resolver3.yaml')).resolve()
        x = {k: v for k, v in as_dict(schema.slots['s1']).items() if v is not None and v != []}
        outfile = env.expected_path('resolver3.json')
        if not os.path.exists(outfile):
            with open(outfile, 'w') as f:
                f.write(as_json(x))
        with open(outfile) as f:
            expected = as_dict(load(f))

        self.assertEqual(expected, x)


if __name__ == '__main__':
    unittest.main()
