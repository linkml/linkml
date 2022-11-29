import logging
import unittest
from copy import deepcopy
from typing import List
from unittest import TestCase

from examples import SchemaDefinition, ClassDefinition, SlotDefinition, EnumDefinition, TypeDefinition, Prefix, \
    SubsetDefinition
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.schemaview import SchemaView

from tests.test_issues.environment import env

def make_schema(name: str,
                prefixes: List[Prefix] = None,
                classes: List[ClassDefinition] = None,
                slots: List[SlotDefinition] = None,
                enums: List[EnumDefinition] = None,
                types: List[TypeDefinition] = None,
                subsets: List[SubsetDefinition] = None,
                ) -> SchemaDefinition:
    schema = SchemaDefinition(id=name, name=name)
    if prefixes:
        for p in prefixes:
            schema.prefixes[p.prefix_prefix] = p
    if classes:
        for c in classes:
            schema.classes[c.name] = c
    if slots:
        for s in slots:
            schema.slots[s.name] = s
    if enums:
        for e in enums:
            schema.enums[e.name] = e
    if types:
        for t in types:
            schema.types[t.name] = t
    if subsets:
        for s in subsets:
            schema.subsets[s.name] = s
    return schema

class Issue1143TestCase(TestCase):
    """
    https://github.com/linkml/linkml/issues/1143
    """
    env = env

    def make_schemas(self) -> None:
        s1 = make_schema(
            's1',
             prefixes=[Prefix(prefix_prefix='sc1p1', prefix_reference='http://example.org/sc1url1')],
             classes=[ClassDefinition(name='sc1c1', slots=['sc1s1']),
                      ClassDefinition(name='sc1c2', slots=['sc1s2'])],
             slots=[SlotDefinition(name='sc1s1', range='string'),
                    SlotDefinition(name='sc1s2', range='float')],
             enums=[EnumDefinition(name='sc1e1',
                                   permissible_values={'sc1e1v1': 'sc1e1v1',}
                                      )],
            types=[TypeDefinition(name='sc1t1', base='string')],
            subsets=[SubsetDefinition(name='sc1ss1', description='sc1ss1')],
        )
        s2 = make_schema(
            's2',
             prefixes=[Prefix(prefix_prefix='sc2p1', prefix_reference='http://example.org/sc2url1')],
             classes=[ClassDefinition(name='sc2c1', slots=['sc2s1']),
                        ClassDefinition(name='sc2c2', slots=['sc2s2'])],
             slots=[SlotDefinition(name='sc2s1', range='string'),
                     SlotDefinition(name='sc2s2', range='float')],
             enums=[EnumDefinition(name='sc2e1',
                                   permissible_values={'sc2e1v1': 'sc2e1v1',}
                                      )],
            types=[TypeDefinition(name='sc2t1', base='string')],
            subsets=[SubsetDefinition(name='sc2ss1', description='sc2ss1')],
        )
        s3 = make_schema('s3')
        self.sv1 = SchemaView(s1)
        self.sv2 = SchemaView(s2)
        self.sv3 = SchemaView(s3)

    def is_identical(self, sv1: SchemaView, sv2: SchemaView) -> None:
        s1 = sv1.schema
        s2 = sv2.schema
        for k in ['prefixes', 'classes', 'slots', 'enums', 'types', 'subsets']:
            self.assertCountEqual(getattr(s1, k).keys(), getattr(s2, k).keys(), f'{k} keys not equal')
            self.assertCountEqual(getattr(s1, k).values(), getattr(s2, k).values(), f'{k} vals not equal')

    def test_merge_empty(self):
        self.make_schemas()
        self.sv3.merge_schema(self.sv1.schema)
        self.is_identical(self.sv3, self.sv1)

    def test_merge_empty_rev(self):
        self.make_schemas()
        sv1_orig = deepcopy(self.sv1)
        self.sv1.merge_schema(self.sv3.schema)
        self.is_identical(sv1_orig, self.sv1)

    def test_merge_schema(self):
        self.make_schemas()
        self.sv2.merge_schema(self.sv1.schema)
        expected = {
            'prefixes': ['sc1p1', 'sc2p1'],
            'classes': ['sc1c1', 'sc1c2', 'sc2c1', 'sc2c2'],
            'slots': ['sc1s1', 'sc1s2', 'sc2s1', 'sc2s2'],
            'enums': ['sc1e1', 'sc2e1'],
            'types': ['sc1t1', 'sc2t1'],
            'subsets': ['sc1ss1', 'sc2ss1'],
        }
        for k, vs in expected.items():
            self.assertCountEqual(getattr(self.sv2.schema, k).keys(), vs, f'{k} keys not equal')


if __name__ == "__main__":
    unittest.main()
