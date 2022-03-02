import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schemaview import SchemaView

from linkml.transformers.relmodel_transformer import RelationalModelTransformer, TransformationResult, \
    get_primary_key_attributes, get_foreign_key_map
from linkml.utils.schema_builder import SchemaBuilder
from tests.test_generators.environment import env

SCHEMA = env.input_path('personinfo.yaml')
OUT_PATH = env.expected_path('personinfo.relational.yaml')
META_OUT_PATH = env.expected_path('meta.relational.yaml')
RSCHEMA_EXPANDED = env.expected_path('personinfo.relational.expanded.yaml')

DUMMY_CLASS = "c"


class RelationalModelTransformerTestCase(unittest.TestCase):
    """
    Tests transformation from a linkml model to a relational model (independent of SQL).
    
    Note: This tests the transformation between one LinkML model and another.
    
    The input model may include mulitvalued fields, but these are transformed away in 
    the relational representation.
    """

    def _translate(self, builder: SchemaBuilder) -> TransformationResult:
        sv = SchemaView(builder.schema)
        sqltr = RelationalModelTransformer(sv)
        return sqltr.transform()

    def test_inject_primary_key(self):
        """
        test a minimal schema with no primary names declared
        """
        b = SchemaBuilder()
        slots = ["name", "description"]
        b.add_class(DUMMY_CLASS, slots)
        results = self._translate(b)
        rel_schema = self._translate(b).schema
        #print(yaml_dumper.dumps(rel_schema))
        self.assertCountEqual(slots + ["id"], list(rel_schema.classes[DUMMY_CLASS].attributes.keys()))
        self.assertEqual([], rel_schema.mappings)
        rsv = SchemaView(rel_schema)
        self.assertEqual("id", rsv.get_identifier_slot(DUMMY_CLASS).name)
        self.assertCountEqual(["id"], get_primary_key_attributes(rel_schema.classes[DUMMY_CLASS]))
        self.assertDictEqual({}, get_foreign_key_map(rel_schema.classes[DUMMY_CLASS]))


    def test_injection_clash(self):
        """
        test conflict with injected primary key
        """
        b = SchemaBuilder()
        slots = ["id", "description"]
        b.add_class(DUMMY_CLASS, slots)
        with self.assertRaises(ValueError):
            results = self._translate(b)



    def test_no_inject_primary_key(self):
        """
        PKs should not be injected if identifier is declared
        """
        b = SchemaBuilder()
        slots = ["name", "description"]
        b.add_class(DUMMY_CLASS, slots).set_slot("name", identifier=True)
        results = self._translate(b)
        rel_schema = self._translate(b).schema
        #print(yaml_dumper.dumps(rel_schema))
        self.assertCountEqual(slots, list(rel_schema.classes[DUMMY_CLASS].attributes.keys()))
        self.assertEqual([], rel_schema.mappings)
        rsv = SchemaView(rel_schema)
        self.assertEqual("name", rsv.get_identifier_slot(DUMMY_CLASS).name)
        self.assertCountEqual(["name"], get_primary_key_attributes(rel_schema.classes[DUMMY_CLASS]))


    def test_multivalued_literal(self):
        """
        Test translation of lists of strings
        """
        b = SchemaBuilder()
        b.add_class("c", ["name", "description", "aliases"]).set_slot("aliases", multivalued=True, singular_name="alias")
        results = self._translate(b)
        rel_schema = self._translate(b).schema
        #print(yaml_dumper.dumps(rel_schema))
        rsv = SchemaView(rel_schema)
        c = rsv.get_class("c")
        assert c
        self.assertCountEqual(["id", "name", "description"], list(c.attributes.keys()))
        c_alias = rsv.get_class("c_alias")
        assert c_alias
        c_alias_c_id = rsv.induced_slot("c_id", c_alias.name)
        assert c_alias_c_id.range == "c"
        self.assertCountEqual(["c_id", "alias"], list(c_alias.attributes.keys()))
        self.assertEqual([], rel_schema.mappings)
        self.assertCountEqual(["id"], get_primary_key_attributes(c))
        self.assertDictEqual({}, get_foreign_key_map(c))
        self.assertDictEqual({"c_id": "c.id"}, get_foreign_key_map(c_alias))


    def test_inject_foreign_key(self):
        """
        test translation of a single-valuaed object reference to a foreign key
        """
        b = SchemaBuilder()
        slots = ["name", "description", "has_d"]
        b.add_class("c", slots).add_class("d", ["name"]).set_slot("has_d", range="d")
        results = self._translate(b)
        rel_schema = self._translate(b).schema
        rsv = SchemaView(rel_schema)
        #print(yaml_dumper.dumps(rel_schema))
        c = rsv.get_class("c")
        d = rsv.get_class("d")
        self.assertCountEqual(["id", "name", "description", "has_d_id"], list(c.attributes.keys()))
        self.assertCountEqual(["id", "name"], list(d.attributes.keys()))
        self.assertCountEqual(["id"], get_primary_key_attributes(c))
        self.assertCountEqual(["id"], get_primary_key_attributes(d))
        self.assertDictEqual({"has_d_id": "d.id"}, get_foreign_key_map(c))
        self.assertDictEqual({}, get_foreign_key_map(d))


    def test_inject_backref_foreign_key(self):
        """
        test translation of a multi-valued object reference to a foreign key from the referenced class
        """
        b = SchemaBuilder()
        slots = ["name", "description", "has_ds"]
        b.add_class("c", slots).add_class("d", ["name"]).set_slot("has_ds",
                                                                  singular_name="has_d",
                                                                  alias="d",
                                                                  range="d", multivalued=True, inlined=True)
        results = self._translate(b)
        rel_schema = self._translate(b).schema
        rsv = SchemaView(rel_schema)
        #print(yaml_dumper.dumps(rel_schema))
        c = rsv.get_class("c")
        d = rsv.get_class("d")
        self.assertCountEqual(["id", "name", "description",], list(c.attributes.keys()))
        self.assertCountEqual(["id", "name", "c_id"], list(d.attributes.keys()))
        self.assertCountEqual(["id"], get_primary_key_attributes(c))
        self.assertCountEqual(["id"], get_primary_key_attributes(d))
        self.assertDictEqual({}, get_foreign_key_map(c))
        self.assertDictEqual({"c_id": "c.id"}, get_foreign_key_map(d))

    def test_inject_many_to_many(self):
        """
        test translation of a non-inlined multivalued reference to a class into
        a linking table
        """
        b = SchemaBuilder()
        slots = ["name", "description", "has_ds"]
        b.add_class("c", slots).add_class("d", ["name"]).set_slot("has_ds", singular_name="has_d",
                                                                  range="d", multivalued=True, inlined=False)
        results = self._translate(b)
        rel_schema = self._translate(b).schema
        rsv = SchemaView(rel_schema)
        #print(yaml_dumper.dumps(rel_schema))
        c = rsv.get_class("c")
        d = rsv.get_class("d")
        c_has_d = rsv.get_class("c_has_d")
        self.assertCountEqual(["id", "name", "description"], list(c.attributes.keys()))
        self.assertCountEqual(["id", "name"], list(d.attributes.keys()))
        self.assertCountEqual(["c_id", "has_d_id"], list(c_has_d.attributes.keys()))
        self.assertCountEqual(["id"], get_primary_key_attributes(c))
        self.assertCountEqual(["id"], get_primary_key_attributes(d))
        self.assertCountEqual(["c_id", "has_d_id"], get_primary_key_attributes(c_has_d))
        self.assertDictEqual({}, get_foreign_key_map(c))
        self.assertDictEqual({}, get_foreign_key_map(d))
        self.assertDictEqual({"c_id": "c.id", "has_d_id": "d.id"}, get_foreign_key_map(c_has_d))


    def test_inject_many_to_many_with_inheritance(self):
        """
        as above, but with inheritance
        """
        b = SchemaBuilder()
        slots = ["name", "description", "has_ds"]
        b.add_class("c", slots).add_class("d", ["name"]).set_slot("has_ds", singular_name="has_d",
                                                                  range="d", multivalued=True, inlined=False)
        b.add_class("c1", is_a="c", slot_usage={"has_ds": SlotDefinition("has_ds", range="d1")})
        b.add_class("d1", is_a="d")
        #print(yaml_dumper.dumps(b.schema))
        results = self._translate(b)
        rel_schema = self._translate(b).schema
        rsv = SchemaView(rel_schema)
        print(yaml_dumper.dumps(rel_schema))
        c = rsv.get_class("c")
        d = rsv.get_class("d")
        c1 = rsv.get_class("c1")
        d1 = rsv.get_class("d1")
        c_has_d = rsv.get_class("c_has_d")
        c1_has_d = rsv.get_class("c1_has_d")
        self.assertCountEqual(["id"], get_primary_key_attributes(d1))
        self.assertCountEqual(["id", "name", "description"], list(c.attributes.keys()))
        self.assertCountEqual(["id", "name"], list(d.attributes.keys()))
        self.assertCountEqual(["c_id", "has_d_id"], list(c_has_d.attributes.keys()))
        self.assertCountEqual(["id"], get_primary_key_attributes(c))
        self.assertCountEqual(["id"], get_primary_key_attributes(d))
        self.assertCountEqual(["c_id", "has_d_id"], get_primary_key_attributes(c_has_d))
        self.assertDictEqual({}, get_foreign_key_map(c))
        self.assertDictEqual({}, get_foreign_key_map(d))
        self.assertDictEqual({"c_id": "c.id", "has_d_id": "d.id"}, get_foreign_key_map(c_has_d))


    def test_aliases(self):
        """
        tests using alias to override name
        """
        b = SchemaBuilder()
        slots = ["foo_name", "foo_description", "foo_has_d", "foo_aliases"]
        b.add_class("c", [SlotDefinition("foo_name", alias="name"),
                          SlotDefinition("foo_description", alias="description"),
                          SlotDefinition("foo_aliases", alias="aliases", multivalued=True),
                          SlotDefinition("foo_has_d", alias="has_d", multivalued=True, range="d")])
        b.add_class("d", [SlotDefinition("name")])
        results = self._translate(b)
        rel_schema = self._translate(b).schema
        rsv = SchemaView(rel_schema)
        #print(yaml_dumper.dumps(rel_schema))
        c = rsv.get_class("c")
        d = rsv.get_class("d")
        c_has_d = rsv.get_class("c_has_d")
        self.assertCountEqual(["id", "name", "description"], list(c.attributes.keys()))
        self.assertCountEqual(["id", "name"], list(d.attributes.keys()))
        self.assertCountEqual(["c_id", "has_d_id"], list(c_has_d.attributes.keys()))
        self.assertCountEqual(["id"], get_primary_key_attributes(c))
        self.assertCountEqual(["id"], get_primary_key_attributes(d))
        self.assertCountEqual(["c_id", "has_d_id"], get_primary_key_attributes(c_has_d))
        self.assertDictEqual({}, get_foreign_key_map(c))
        self.assertDictEqual({}, get_foreign_key_map(d))
        self.assertDictEqual({"c_id": "c.id", "has_d_id": "d.id"}, get_foreign_key_map(c_has_d))

    def test_sqlt_on_metamodel(self):
        sv = package_schemaview("linkml_runtime.linkml_model.meta")
        sqltr = RelationalModelTransformer(sv)
        result = sqltr.transform()
        rschema = result.schema
        #print(rschema.imports)
        with open(META_OUT_PATH, "w") as stream:
            stream.write(yaml_dumper.dumps(rschema))
        # test Annotation is handled correctly. This has a key annotation_tag with alias 'tag'
        self.assertNotIn("id", rschema.classes["annotation"].attributes.keys())
        self.assertIn("tag", rschema.classes["annotation"].attributes.keys())
        self.assertIn("value", rschema.classes["annotation"].attributes.keys())
        cd = rschema.classes["class_definition"]
        self.assertEqual("class_definition", cd.name)
        self.assertIn("name", cd.attributes.keys())
        self.assertIn("primary_key", cd.attributes["name"].annotations)

    def test_sqlt_complete_example(self):
        """Test Relational Model Transform on personinfo.yaml schema."""
        sv = SchemaView(SCHEMA)
        sqltr = RelationalModelTransformer(sv)
        result = sqltr.transform()
        rschema = result.schema
        with open(OUT_PATH, 'w') as stream:
            stream.write(yaml_dumper.dumps(rschema))
        #with open(RSCHEMA_EXPANDED, 'w') as stream:
        #    stream.write(YAMLGenerator(rschema).serialize())
        self.assertEqual(rschema.name, 'personinfo_relational')
        sv = SchemaView(rschema)

        # check roots, mixins, and abstracts are omitted
        # NOTE: for now we keep all classes in
        #assert 'Container' not in sv.all_classes()
        #assert 'HasAliases' not in sv.all_classes()
        #assert 'WithLocation' not in sv.all_classes()

        # check multivalued are preserved as slots;
        # these are referenced from inverses
        # assert sv.get_slot('aliases').multivalued
        assert sv.get_slot('has_medical_history').multivalued
        assert sv.get_slot('has_familial_relationships').multivalued
        assert sv.get_slot('has_employment_history').multivalued

        c = sv.get_class('Person')
        assert 'aliases' not in c.attributes
        assert 'aliases' not in c.slots

        for cn in ['Person', 'Organization']:
            c = sv.get_class(f'{cn}_alias')
            self.assertEqual(len(c.attributes), 2)
            ranges = [s.range for s in c.attributes.values()]
            self.assertCountEqual(ranges, [cn, 'string'])

        for relationship_class in ['FamilialRelationship', 'EmploymentEvent', 'MedicalEvent']:
            c = sv.get_class(relationship_class)
            #print(f'RC: {relationship_class} // {c}')
            assert any(a for a in c.attributes.values() if a.range == 'Person' and a.name == 'Person_id')
            pk = sv.get_identifier_slot(cn)
            self.assertIsNotNone(pk)
            assert pk.name == 'id'

        news_event_pk = sv.get_identifier_slot('NewsEvent')
        self.assertIsNotNone(news_event_pk)
        self.assertEqual(news_event_pk.name, "id")

        for cn in ['Person', 'Organization']:
            c = sv.get_class(f'{cn}_has_news_event')
            #print(list(c.attributes.keys()))
            #print(list(c.attributes.values()))
            a1 = c.attributes['has_news_event_id']
            self.assertEqual(a1.range, 'NewsEvent')
            a2 = c.attributes[f'{cn}_id']
            self.assertEqual(a2.range, cn)


if __name__ == '__main__':
    unittest.main()
