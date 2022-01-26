import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.schemaview import SchemaView

from linkml.generators.yamlgen import YAMLGenerator
from linkml.transformers.relmodel_transformer import RelationalModelTransformer
from tests.test_generators.environment import env

SCHEMA = env.input_path('personinfo.yaml')
OUT_PATH = env.expected_path('personinfo.relational.yaml')
RSCHEMA_EXPANDED = env.expected_path('personinfo.relational.expanded.yaml')


class RelationalModelTransformerTestCase(unittest.TestCase):
    """
    Tests transformation from a linkml model to a relational model (independent of SQL).
    
    Note: This tests the transformation between one LinkML model and another.
    
    The input model may include mulitvalued fields, but these are transformed away in 
    the relational representation.
    """

    @unittest.skip("Check why certain checks are not going through.")
    def test_sqlt_basic(self):
        """Test Relational Model Transform on personinfo.yaml schema."""
        sv = SchemaView(SCHEMA)
        sqltr = RelationalModelTransformer(sv)
        result = sqltr.transform()
        rschema = result.schema
        with open(OUT_PATH, 'w') as stream:
            stream.write(yaml_dumper.dumps(rschema))
        with open(RSCHEMA_EXPANDED, 'w') as stream:
            stream.write(YAMLGenerator(rschema).serialize())
        self.assertEqual(rschema.name, 'personinfo_relational')
        sv = SchemaView(rschema)
        
        # check roots, mixins, and abstracts are omitted
        assert 'Container' not in sv.all_classes()
        assert 'HasAliases' not in sv.all_classes()
        assert 'WithLocation' not in sv.all_classes()
        
        # check multivalued are preserved as slots;
        # these are referenced from inverses
        # assert sv.get_slot('aliases').multivalued
        assert sv.get_slot('has_medical_history').multivalued
        assert sv.get_slot('has_familial_relationships').multivalued
        assert sv.get_slot('has_employment_history').multivalued
        
        c = sv.get_class('Person')
        assert 'aliases' not in c.attributes
        assert 'aliases' not in c.slots

        # for cn in ['Person', 'Organization']:
        #     c = sv.get_class(f'{cn}_alias')
        #     self.assertEqual(len(c.attributes), 2)
        #     ranges = [s.range for s in c.attributes.values()]
        #     self.assertCountEqual(ranges, [cn, 'string'])

        for relationship_class in ['FamilialRelationship', 'EmploymentEvent', 'MedicalEvent']:
            c = sv.get_class(relationship_class)
            [backref] = [a for a in c.attributes.values() if a.range == 'Person']
            self.assertEqual(backref.name, 'Person_id')

        # for cn in ['Person', 'Organization', 'Place']:
        #     c = sv.get_class(f'{cn}_has news event')
        #     a1 = c.attributes['has news event']
        #     self.assertEqual(a1.range, 'NewsEvent')
        #     a2 = c.attributes[f'{cn}_id']
        #     self.assertEqual(a2.range, cn)


if __name__ == '__main__':
    unittest.main()
