import os
import json
import unittest
from typing import List, Tuple, Any

from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.utils.schemaview import SchemaView

from tests.test_utils import INPUT_DIR

SCHEMA_NO_IMPORTS = os.path.join(INPUT_DIR, 'kitchen_sink_noimports.yaml')
SCHEMA_WITH_IMPORTS = os.path.join(INPUT_DIR, 'kitchen_sink.yaml')

yaml_loader = YAMLLoader()

class SchemaViewTestCase(unittest.TestCase):

    def test_schemaview(self):
        # no import schema
        view = SchemaView(SCHEMA_NO_IMPORTS)
        print(view.imports_closure())
        assert len(view.imports_closure()) == 1
        all_cls = view.all_class()
        print(f'n_cls = {len(all_cls)}')

        e = view.get_element('is current')
        assert list(view.annotation_dict('is current').values()) == ['bar']
        print(view.annotation_dict('employed at'))
        e = view.get_element('employed at')
        print(e.annotations)
        e = view.get_element('has employment history')
        print(e.annotations)
        #assert list(view.annotation_dict('employed at')[]

        if True:
            # this section is mostly for debugging
            for cn in all_cls.keys():
                print(f'{cn} PARENTS = {view.class_parents(cn)}')
                print(f'{cn} ANCS = {view.class_ancestors(cn)}')
                print(f'{cn} CHILDREN = {view.class_children(cn)}')
                print(f'{cn} DESCS = {view.class_descendants(cn)}')
                print(f'{cn} SCHEMA = {view.in_schema(cn)}')
                print(f'  SLOTS = {view.class_slots(cn)}')
                for sn in view.class_slots(cn):
                    slot = view.get_slot(sn)
                    if slot is None:
                        print(f'NO SLOT: {sn}')
                    else:
                        print(f'  SLOT {sn} R: {slot.range} U: {view.get_uri(sn)} ANCS: {view.slot_ancestors(sn)}')
                    induced_slot = view.induced_slot(sn, cn)
                    print(f'    INDUCED {sn}={induced_slot}')

        print(f'ALL = {view.all_element().keys()}')

        # -- TEST ANCESTOR/DESCENDANTS FUNCTIONS --

        self.assertCountEqual(['Company', 'Organization', 'HasAliases', 'Thing'],
                              view.class_ancestors('Company'))
        self.assertCountEqual(['Organization', 'HasAliases', 'Thing'],
                              view.class_ancestors('Company', reflexive=False))
        self.assertCountEqual(['Thing', 'Person', 'Organization', 'Company', 'Adult'],
                              view.class_descendants('Thing'))

        # -- TEST CLASS SLOTS --


        self.assertCountEqual(['id', 'name',  ## From Thing
                               'has employment history', 'has familial relationships', 'has medical history',
                               'age in years', 'addresses', 'has birth event', ## From Person
                               'aliases'  ## From HasAliases
                                ],
                              view.class_slots('Person'))
        self.assertCountEqual(view.class_slots('Person'), view.class_slots('Adult'))
        self.assertCountEqual(['id', 'name',  ## From Thing
                               'ceo', ## From Company
                               'aliases'  ## From HasAliases
                               ],
                              view.class_slots('Company'))

        assert view.get_class('agent').class_uri == 'prov:Agent'
        assert view.get_uri('agent') == 'prov:Agent'
        print(view.get_class('Company').class_uri)
        #assert view.get_class('Company').class_uri == 'prov:Agent'
        assert view.get_uri('Company') == 'ks:Company'

        for c in ['Company', 'Person', 'Organization',]:
            assert view.induced_slot('aliases', c).multivalued is True

        for c in ['Company', 'Person', 'Organization', 'Thing']:
            assert view.induced_slot('id', c).identifier is True
            assert view.induced_slot('name', c).identifier is not True
            assert view.induced_slot('name', c).required is False
            assert view.induced_slot('name', c).range == 'string'
        for c in ['Event', 'EmploymentEvent', 'MedicalEvent']:
            s = view.induced_slot('started at time', c)
            print(f's={s.range} // c = {c}')
            assert s.range == 'date'
            assert s.slot_uri == 'prov:startedAtTime'
        assert view.induced_slot('age in years', 'Person').minimum_value == 0
        assert view.induced_slot('age in years', 'Adult').minimum_value == 16
        assert view.induced_slot('type', 'FamilialRelationship').range == 'FamilialRelationshipType'
        assert view.induced_slot('related to', 'FamilialRelationship').range == 'Person'

        u = view.usage_index()
        for k, v in u.items():
            print(f' {k} = {v}')

        #for e in view.all_element(imports=True):
        #    print(view.annotation_dict(e))
        #print(u)


    def test_caching(self):
        s = SchemaDefinition(id='test', name='test')
        view = SchemaView(s)
        self.assertCountEqual([], view.all_class())
        view.add_class(ClassDefinition('X'))
        self.assertCountEqual(['X'], view.all_class())
        view.add_class(ClassDefinition('Y'))
        self.assertCountEqual(['X', 'Y'], view.all_class())
        # bypass view method
        view.schema.classes['Z'] = ClassDefinition('Z')
        self.assertCountEqual(['X', 'Y'], view.all_class())
        view.set_modified()
        self.assertCountEqual(['X', 'Y', 'Z'], view.all_class())
        view.delete_class('X')
        self.assertCountEqual(['Y', 'Z'], view.all_class())

    def test_imports(self):
        view = SchemaView(SCHEMA_WITH_IMPORTS)
        print(view.imports_closure())
        self.assertCountEqual(['kitchen_sink', 'core', 'linkml:types'], view.imports_closure())
        for t in view.all_type().keys():
            print(f'T={t} in={view.in_schema(t)}')
        assert view.in_schema('Person') == 'kitchen_sink'
        assert view.in_schema('id') == 'core'
        assert view.in_schema('name') == 'core'
        assert view.in_schema('activity') == 'core'
        assert view.in_schema('string') == 'types'

        for c in ['Company', 'Person', 'Organization', 'Thing']:
            assert view.induced_slot('id', c).identifier is True
            assert view.induced_slot('name', c).identifier is not True
            assert view.induced_slot('name', c).required is False
            assert view.induced_slot('name', c).range == 'string'
        for c in ['Event', 'EmploymentEvent', 'MedicalEvent']:
            s = view.induced_slot('started at time', c)
            print(f's={s.range} // c = {c}')
            assert s.range == 'date'
            assert s.slot_uri == 'prov:startedAtTime'
        assert view.induced_slot('age in years', 'Person').minimum_value == 0
        assert view.induced_slot('age in years', 'Adult').minimum_value == 16


        assert view.get_class('agent').class_uri == 'prov:Agent'
        assert view.get_uri('agent') == 'prov:Agent'
        print(view.get_class('Company').class_uri)
        #assert view.get_class('Company').class_uri == 'prov:Agent'
        assert view.get_uri('Company') == 'ks:Company'
        assert view.get_uri('Company', expand=True) == 'https://w3id.org/linkml/tests/kitchen_sink/Company'
        print(view.get_uri("TestClass"))
        assert view.get_uri('TestClass') == 'core:TestClass'
        assert view.get_uri('TestClass', expand=True) == 'https://w3id.org/linkml/tests/core/TestClass'

        assert view.get_uri('string') == 'xsd:string'


if __name__ == '__main__':
    unittest.main()
