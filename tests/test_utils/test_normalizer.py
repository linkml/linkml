import unittest
from typing import Dict

import yaml
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition, ClassDefinition, EnumDefinition
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schemaview import SchemaView

from linkml.transformers.relmodel_transformer import RelationalModelTransformer, TransformationResult, \
    get_primary_key_attributes, get_foreign_key_map, ForeignKeyPolicy
from linkml.transformers.schema_renamer import SchemaRenamer
from linkml.utils.normalizer import DataNormalizer
from linkml.utils.schema_builder import SchemaBuilder
from tests.test_generators.environment import env

SCHEMA = env.input_path('personinfo.yaml')
OUT_PATH = env.expected_path('personinfo.normalized.yaml')

MAP = {
    ClassDefinition: lambda s: s.upper(),
    SlotDefinition: lambda s: f'{s.lower()}_slot',
    EnumDefinition: lambda s: f'{s.lower()}_ENUM',
}

class NormalizerTestCase(unittest.TestCase):
    """
    Tests data normalizer
    """

    def test_normalizer(self):
        metamodel = package_schemaview('linkml_runtime.linkml_model.meta')
        normalizer = DataNormalizer(schemaview=metamodel)
        data = SchemaView(SCHEMA).schema
        data2 = normalizer.as_normalized_dict(data)
        print(yaml.safe_dump(data2, sort_keys=False))
        address = data2['classes']['Address']
        elt_keys = address.keys()
        def before(d: Dict, k1, k2):
            l = list(d)
            print(f'CHECK: {k1} < {k2} {l.index(k1)} < {l.index(k2)}')
            assert l.index(k1) < l.index(k2)
        before(elt_keys, 'attributes', 'all_of')
        #before(elt_keys, 'name', 'slots')
        before(elt_keys, 'name', 'id_prefixes')
        before(elt_keys, 'slots', 'slot_usage')
        data2_obj = normalizer.as_normalized_obj(data)
        with open(OUT_PATH, 'w') as stream:
            stream.write(yaml_dumper.dumps(data2_obj))









if __name__ == '__main__':
    unittest.main()
