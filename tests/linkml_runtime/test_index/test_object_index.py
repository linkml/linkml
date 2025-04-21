import os
import unittest

from linkml_runtime import SchemaView
from linkml_runtime.loaders import yaml_loader
import tests.test_index.model.container_test as src_dm
from linkml_runtime.index.object_index import ObjectIndex, ProxyObject
from linkml_runtime.utils.inference_utils import infer_slot_value, Config
from tests.test_index import INPUT_DIR

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
        # domain object
        container = self.container
        frt = container.persons[0].has_familial_relationships[0].type
        self.assertIsInstance(frt, src_dm.FamilialRelationshipType)
        # create an index
        oix = ObjectIndex(container, schemaview=self.schemaview)
        self.assertEqual(0, oix.proxy_object_cache_size)
        self.assertGreater(oix.source_object_cache_size, 4)
        # test basic lookups
        proxy_obj = oix.bless(container)
        # proxy objects mock the domain object class, plus
        # they also instantiate ProxyObject
        self.assertIsInstance(proxy_obj, ProxyObject)
        self.assertIsInstance(proxy_obj, src_dm.Container)
        proxy_obj = oix.bless(container.persons[0])
        self.assertIsInstance(proxy_obj, ProxyObject)
        self.assertIsInstance(proxy_obj, src_dm.Person)
        v = proxy_obj.name
        self.assertEqual("fred bloggs", v)
        self.assertEqual(33, proxy_obj.age_in_years)
        self.assertCountEqual(["a", "b"], proxy_obj.aliases)
        addr = proxy_obj.current_address
        self.assertIsInstance(addr, ProxyObject)
        self.assertIsInstance(addr, src_dm.Address)
        self.assertEqual("1 oak street", addr.street)
        self.assertIsInstance(proxy_obj.has_familial_relationships, list)
        fr = proxy_obj.has_familial_relationships[0]
        self.assertIsInstance(fr, ProxyObject)
        # test automatic dereferencing;
        # related_to is *not* inlined in the schema
        self.assertEqual("Alison Wu", fr.related_to.name)
        self.assertIsInstance(fr.type, src_dm.FamilialRelationshipType)
        self.assertIsNone(fr.related_to.age_in_years)
        self.assertIsInstance(fr.related_to, ProxyObject)
        self.assertEqual(2, len(proxy_obj.has_medical_history))
        fr2 = fr.related_to.has_familial_relationships[0]
        self.assertEqual("fred bloggs", fr2.related_to.name)
        self.assertEqual(33, fr2.related_to.age_in_years)
        self.assertIsInstance(fr2.related_to, ProxyObject)
        fr3 = fr2.related_to.has_familial_relationships[0]
        self.assertIsInstance(fr3.related_to, ProxyObject)
        self.assertEqual("Alison Wu", fr3.related_to.name)
        self.assertGreater(oix.proxy_object_cache_size, 1)
        self.assertLess(oix.proxy_object_cache_size, 9)
        oix.clear_proxy_object_cache()
        self.assertEqual(0, oix.proxy_object_cache_size)
        fr = proxy_obj.has_familial_relationships[0].related_to
        # test that attributes are closed
        with self.assertRaises(ValueError):
            v = proxy_obj.fake_attribute
        # test setting attributes, and that this affects shadowed object
        proxy_obj.age_in_years = 44
        self.assertEqual(44, proxy_obj.age_in_years)
        self.assertEqual(44, self.container.persons[0].age_in_years)
        # test evaluation of expressions
        self.assertEqual(5, oix.eval_expr("5"))
        self.assertEqual(5, oix.eval_expr("2*2+1"))
        self.assertEqual("P:001", oix.eval_expr("persons", container)[0].id)
        self.assertEqual("P:001", oix.eval_expr("persons[0].id", container))
        self.assertEqual(oix.eval_expr("persons", container), oix.eval_expr("persons"))
        person = oix.eval_expr("persons")[0]
        self.assertIsInstance(oix.bless(container).persons[0], ProxyObject)
        self.assertIsInstance(person, ProxyObject)
        self.assertEqual("1 oak street", oix.eval_expr("current_address.street", person))
        self.assertEqual("Alison Wu", oix.eval_expr("has_familial_relationships[0].related_to.name", person))
        # experimental: reverse direction
        self.assertEqual("P:001", oix.eval_expr("persons[0]._parents[0][1].persons[0].id"))
        self.assertEqual("P:001", oix.eval_expr("persons[0].persons__inverse[0].persons[0].id"))
        # test inference
        #infer_all_slot_values(person, self.schemaview, class_name="Person")
        config = Config(use_expressions=True)
        infer_slot_value(person, "description", schemaview=self.schemaview, class_name="Person", config=config)
        self.assertEqual("name: fred bloggs address: 1 oak street", person.description)


if __name__ == '__main__':
    unittest.main()
