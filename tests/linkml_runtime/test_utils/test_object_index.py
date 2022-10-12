import os
import unittest

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader
import tests.test_utils.model.container_test as src_dm
from linkml_runtime.utils.object_index import ObjectIndex, ProxyObject
from tests.test_utils import INPUT_DIR

SCHEMA = os.path.join(INPUT_DIR, 'container_test.yaml')
DATA = os.path.join(INPUT_DIR, 'object-indexer-data.yaml')


class ObjectIndexerTestCase(unittest.TestCase):
    """
    tests the data model
    """

    def setUp(self) -> None:
        self.schemaview = SchemaView(SCHEMA)
        obj: src_dm.Container
        self.container = yaml_loader.load(DATA, target_class=src_dm.Container)

    def test_object_index(self):
        """ checks indexing objects """
        c = self.container
        frt = c.persons[0].has_familial_relationships[0].type
        self.assertIsInstance(frt, src_dm.FamilialRelationshipType)
        fac = ObjectIndex(c, schemaview=self.schemaview)
        self.assertEqual(0, fac.proxy_object_cache_size)
        self.assertGreater(fac.source_object_cache_size, 4)
        obj = fac.bless(c)
        self.assertIsInstance(obj, ProxyObject)
        obj = fac.bless(c.persons[0])
        self.assertIsInstance(obj, ProxyObject)
        v = obj.name
        self.assertEqual("fred bloggs", v)
        self.assertEqual(33, obj.age_in_years)
        self.assertCountEqual(["a", "b"], obj.aliases)
        addr = obj.current_address
        self.assertIsInstance(addr, ProxyObject)
        self.assertEqual("1 oak street", addr.street)
        self.assertIsInstance(obj.has_familial_relationships, list)
        fr = obj.has_familial_relationships[0]
        self.assertIsInstance(fr, ProxyObject)
        self.assertEqual("Alison Wu", fr.related_to.name)
        self.assertIsInstance(fr.type, src_dm.FamilialRelationshipType)
        self.assertIsNone(fr.related_to.age_in_years)
        self.assertIsInstance(fr.related_to, ProxyObject)
        self.assertEqual(2, len(obj.has_medical_history))
        fr2 = fr.related_to.has_familial_relationships[0]
        self.assertEqual("fred bloggs", fr2.related_to.name)
        self.assertEqual(33, fr2.related_to.age_in_years)
        self.assertIsInstance(fr2.related_to, ProxyObject)
        fr3 = fr2.related_to.has_familial_relationships[0]
        self.assertIsInstance(fr3.related_to, ProxyObject)
        self.assertEqual("Alison Wu", fr3.related_to.name)
        self.assertGreater(fac.proxy_object_cache_size, 1)
        self.assertLess(fac.proxy_object_cache_size, 4)
        fac.clear_proxy_object_cache()
        self.assertEqual(0, fac.proxy_object_cache_size)
        fr = obj.has_familial_relationships[0].related_to
        with self.assertRaises(ValueError):
            v = obj.fake_attribute
        obj.age_in_years = 44
        self.assertEqual(44, obj.age_in_years)
        self.assertEqual(44, self.container.persons[0].age_in_years)


if __name__ == '__main__':
    unittest.main()
