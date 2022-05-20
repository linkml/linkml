import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition, ClassDefinition, EnumDefinition
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schemaview import SchemaView

from linkml.transformers.relmodel_transformer import RelationalModelTransformer, TransformationResult, \
    get_primary_key_attributes, get_foreign_key_map, ForeignKeyPolicy
from linkml.transformers.schema_renamer import SchemaRenamer
from linkml.utils.schema_builder import SchemaBuilder
from tests.test_generators.environment import env

SCHEMA = env.input_path('personinfo.yaml')
OUT_PATH = env.expected_path('personinfo.renamed.yaml')

MAP = {
    ClassDefinition: lambda s: s.upper(),
    SlotDefinition: lambda s: f'{s.lower()}_slot',
    EnumDefinition: lambda s: f'{s.lower()}_ENUM',
}

class SchemaRenamerTestCase(unittest.TestCase):
    """
    Tests schema renamer
    """

    def test_renamer(self):
        """Test Relational Model Transform on personinfo.yaml schema."""
        sv = SchemaView(SCHEMA)
        renamer = SchemaRenamer(rename_function_map=MAP)
        rschema = renamer.rename_elements(sv.schema)
        with open(OUT_PATH, 'w') as stream:
            stream.write(yaml_dumper.dumps(rschema))
        sv2 = SchemaView(OUT_PATH)
        p = sv2.get_class('PERSON')
        assert 'primary_email_slot' in p.slots
        diagnosis_slot = sv2.induced_slot('diagnosis_slot', 'MEDICALEVENT')
        assert diagnosis_slot.range == 'DIAGNOSISCONCEPT'






if __name__ == '__main__':
    unittest.main()
