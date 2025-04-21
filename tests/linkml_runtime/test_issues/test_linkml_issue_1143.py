import unittest
from copy import deepcopy
from unittest import TestCase

from linkml_runtime.linkml_model import SchemaDefinition, ClassDefinition, SlotDefinition, EnumDefinition, TypeDefinition, Prefix, \
    SubsetDefinition
from linkml_runtime.utils.schemaview import SchemaView

from tests.test_issues.environment import env

ELEMENTS = ['prefixes', 'classes', 'slots', 'enums', 'types', 'subsets']
EXPECTED = {
            'prefixes': ['sc1p1', 'sc2p1'],
            'classes': ['sc1c1', 'sc1c2', 'sc2c1', 'sc2c2'],
            'slots': ['sc1s1', 'sc1s2', 'sc2s1', 'sc2s2'],
            'enums': ['sc1e1', 'sc2e1'],
            'types': ['sc1t1', 'sc2t1'],
            'subsets': ['sc1ss1', 'sc2ss1'],
        }


def make_schema(name: str,
                prefixes: list[Prefix] = None,
                classes: list[ClassDefinition] = None,
                slots: list[SlotDefinition] = None,
                enums: list[EnumDefinition] = None,
                types: list[TypeDefinition] = None,
                subsets: list[SubsetDefinition] = None,
                ) -> SchemaDefinition:
    """
    Make a schema with the given elements

    :param name:
    :param prefixes:
    :param classes:
    :param slots:
    :param enums:
    :param types:
    :param subsets:
    :return:
    """
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
        """
        Makes 3 schema view objects for testing

        sv1 and sv2 have disjoint elements
        sv3 is empty

        :return:
        """
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
        """
        Compares two schemas for strict identity

        :param sv1:
        :param sv2:
        :return:
        """
        s1 = sv1.schema
        s2 = sv2.schema
        for k in ELEMENTS:
            self.assertCountEqual(getattr(s1, k).keys(), getattr(s2, k).keys(), f'{k} keys not equal')
            self.assertCountEqual(getattr(s1, k).values(), getattr(s2, k).values(), f'{k} vals not equal')

    def test_merge_empty(self):
        """
        Trivial case: merge a schema into an empty schema
        """
        self.make_schemas()
        self.sv3.merge_schema(self.sv1.schema)
        self.is_identical(self.sv3, self.sv1)

    def test_merge_empty_rev(self):
        """
        Trivial case: merge an empty schema into a non-empty schema
        """
        self.make_schemas()
        sv1_orig = deepcopy(self.sv1)
        self.sv1.merge_schema(self.sv3.schema)
        self.is_identical(sv1_orig, self.sv1)

    def test_merge_schema(self):
        """
        Merge two schemas with disjoint elements
        """
        self.make_schemas()
        self.sv2.merge_schema(self.sv1.schema)

        for k, vs in EXPECTED.items():
            self.assertCountEqual(getattr(self.sv2.schema, k).keys(), vs, f'{k} keys not equal')
    def _get_clobbered_field_val(self, element: str) -> tuple[str, str]:
        if element == 'prefixes':
            return 'prefix_reference', 'http://example.org/clobbered'
        else:
            return 'description', 'clobbered'

    def test_no_clobber(self):
        """
        Merge non-disjoint schemas, ensuring that elements in
        the source schema are not clobbered
        """
        self.make_schemas()
        self.sv2.merge_schema(self.sv1.schema)
        for element in ELEMENTS:
            (field, val) = self._get_clobbered_field_val(element)
            for k, v in getattr(self.sv1.schema, element).items():
                setattr(v, field, val)
        self.sv2.merge_schema(self.sv1.schema, clobber=False)
        for element in ELEMENTS:
            (field, val) = self._get_clobbered_field_val(element)
            for k, v in getattr(self.sv2.schema, element).items():
                if k in getattr(self.sv1.schema, element):
                    self.assertNotEqual(getattr(v, field), val, f'{element} {k} clobbered')

    def test_clobber(self):
        """
        Merge non-disjoint schemas, ensuring that elements in source schema
        are clobbered by elements in the other schema
        """
        self.make_schemas()
        self.sv2.merge_schema(self.sv1.schema)
        for element in ELEMENTS:
            (field, val) = self._get_clobbered_field_val(element)
            for k, v in getattr(self.sv1.schema, element).items():
                setattr(v, field, val)
        self.sv2.merge_schema(self.sv1.schema, clobber=True)
        for element in ELEMENTS:
            (field, val) = self._get_clobbered_field_val(element)
            for k, v in getattr(self.sv2.schema, element).items():
                if k in getattr(self.sv1.schema, element):
                    self.assertEqual(getattr(v, field), val, f'{element} {k} not clobbered')


if __name__ == "__main__":
    unittest.main()
