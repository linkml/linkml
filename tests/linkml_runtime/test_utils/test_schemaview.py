import os
import json
import unittest
import logging
from typing import List, Tuple, Any

from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.schemaops import roll_up, roll_down

from tests.test_utils import INPUT_DIR

SCHEMA_NO_IMPORTS = os.path.join(INPUT_DIR, 'kitchen_sink_noimports.yaml')
SCHEMA_WITH_IMPORTS = os.path.join(INPUT_DIR, 'kitchen_sink.yaml')

yaml_loader = YAMLLoader()

class SchemaViewTestCase(unittest.TestCase):

    def test_schemaview(self):
        # no import schema
        view = SchemaView(SCHEMA_NO_IMPORTS)
        logging.debug(view.imports_closure())
        assert len(view.imports_closure()) == 1
        all_cls = view.all_class()
        logging.debug(f'n_cls = {len(all_cls)}')

        e = view.get_element('is current')
        assert list(view.annotation_dict('is current').values()) == ['bar']
        logging.debug(view.annotation_dict('employed at'))
        e = view.get_element('employed at')
        logging.debug(e.annotations)
        e = view.get_element('has employment history')
        logging.debug(e.annotations)
        #assert list(view.annotation_dict('employed at')[]

        if True:
            for sn, s in view.all_slot().items():
                logging.info(f'SN = {sn} RANGE={s.range}')
            # this section is mostly for debugging
            for cn in all_cls.keys():
                logging.debug(f'{cn} PARENTS = {view.class_parents(cn)}')
                logging.debug(f'{cn} ANCS = {view.class_ancestors(cn)}')
                logging.debug(f'{cn} CHILDREN = {view.class_children(cn)}')
                logging.debug(f'{cn} DESCS = {view.class_descendants(cn)}')
                logging.debug(f'{cn} SCHEMA = {view.in_schema(cn)}')
                logging.debug(f'  SLOTS = {view.class_slots(cn)}')
                for sn in view.class_slots(cn):
                    slot = view.get_slot(sn)
                    if slot is None:
                        logging.debug(f'NO SLOT: {sn}')
                    else:
                        logging.debug(f'  SLOT {sn} R: {slot.range} U: {view.get_uri(sn)} ANCS: {view.slot_ancestors(sn)}')
                    induced_slot = view.induced_slot(sn, cn)
                    logging.debug(f'    INDUCED {sn}={induced_slot}')

        logging.debug(f'ALL = {view.all_element().keys()}')

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
        logging.debug(view.get_class('Company').class_uri)
        #assert view.get_class('Company').class_uri == 'prov:Agent'
        assert view.get_uri('Company') == 'ks:Company'

        # test induced slots

        for c in ['Company', 'Person', 'Organization',]:
            assert view.induced_slot('aliases', c).multivalued is True

        assert view.get_identifier_slot('Company').name == 'id'
        assert view.get_identifier_slot('Thing').name == 'id'
        assert view.get_identifier_slot('FamilialRelationship') is None
        for c in ['Company', 'Person', 'Organization', 'Thing']:
            assert view.induced_slot('id', c).identifier is True
            assert view.induced_slot('name', c).identifier is not True
            assert view.induced_slot('name', c).required is False
            assert view.induced_slot('name', c).range == 'string'
        for c in ['Event', 'EmploymentEvent', 'MedicalEvent']:
            s = view.induced_slot('started at time', c)
            logging.debug(f's={s.range} // c = {c}')
            assert s.range == 'date'
            assert s.slot_uri == 'prov:startedAtTime'
        # test slot_usage
        assert view.induced_slot('age in years', 'Person').minimum_value == 0
        assert view.induced_slot('age in years', 'Adult').minimum_value == 16
        assert view.induced_slot('name', 'Person').pattern is not None
        assert view.induced_slot('type', 'FamilialRelationship').range == 'FamilialRelationshipType'
        assert view.induced_slot('related to', 'FamilialRelationship').range == 'Person'
        assert view.get_slot('related to').range == 'Thing'
        assert view.induced_slot('related to', 'Relationship').range == 'Thing'

        a = view.get_class('activity')
        self.assertCountEqual(a.exact_mappings, ['prov:Activity'])
        logging.debug(view.get_mappings('activity',expand=True))
        self.assertCountEqual(view.get_mappings('activity')['exact'], ['prov:Activity'])
        self.assertCountEqual(view.get_mappings('activity', expand=True)['exact'], ['http://www.w3.org/ns/prov#Activity'])

        u = view.usage_index()
        for k, v in u.items():
            logging.debug(f' {k} = {v}')


        # test methods also work for attributes
        leaves = view.class_leaves()
        logging.debug(f'LEAVES={leaves}')
        assert 'MedicalEvent' in leaves
        roots = view.class_roots()
        logging.debug(f'ROOTS={roots}')
        assert 'Dataset' in roots
        ds_slots = view.class_slots('Dataset')
        logging.debug(ds_slots)
        assert len(ds_slots) == 3
        self.assertCountEqual(['persons', 'companies', 'activities'], ds_slots)
        for sn in ds_slots:
            s = view.induced_slot(sn, 'Dataset')
            logging.debug(s)

        #for e in view.all_element(imports=True):
        #    logging.debug(view.annotation_dict(e))
        #logging.debug(u)

    def test_rollup_rolldown(self):
        # no import schema
        view = SchemaView(SCHEMA_NO_IMPORTS)
        original_schema = view.copy_schema()
        cn = 'Event'
        roll_up(view, cn)
        for s in view.class_induced_slots(cn):
            logging.debug(s)
        induced_slot_names = [s.name for s in view.class_induced_slots(cn)]
        logging.debug(induced_slot_names)
        self.assertCountEqual(['started at time', 'ended at time', 'is current', 'in location', 'employed at', 'married to'],
                              induced_slot_names)
        # check to make sure rolled-up classes are deleted
        assert view.class_descendants(cn, reflexive=False) == []
        roll_down(view, view.class_leaves())
        for cn in view.all_class():
            c = view.get_class(cn)
            logging.debug(f'{cn}')
            logging.debug(f'  {cn} SLOTS(i) = {view.class_slots(cn)}')
            logging.debug(f'  {cn} SLOTS(d) = {view.class_slots(cn, direct=True)}')
            self.assertCountEqual(view.class_slots(cn), view.class_slots(cn, direct=True))
        assert 'Thing' not in view.all_class()
        assert 'Person' not in view.all_class()
        assert 'Adult' in view.all_class()



    def test_caching(self):
        """
        Determine if cache is reset after modifications made to schema
        """
        s = SchemaDefinition(id='test', name='test')
        view = SchemaView(s)
        self.assertCountEqual([], view.all_class())
        view.add_class(ClassDefinition('X'))
        self.assertCountEqual(['X'], view.all_class())
        view.add_class(ClassDefinition('Y'))
        self.assertCountEqual(['X', 'Y'], view.all_class())
        # bypass view method and add directly to schema;
        # in general this is not recommended as the cache will
        # not be updated
        view.schema.classes['Z'] = ClassDefinition('Z')
        # as expected, the view doesn't know about Z
        self.assertCountEqual(['X', 'Y'], view.all_class())
        # inform the view modifications have been made
        view.set_modified()
        # should be in sync
        self.assertCountEqual(['X', 'Y', 'Z'], view.all_class())
        # recommended way to make updates
        view.delete_class('X')
        # cache will be up to date
        self.assertCountEqual(['Y', 'Z'], view.all_class())
        view.add_class(ClassDefinition('W'))
        self.assertCountEqual(['Y', 'Z', 'W'], view.all_class())

    def test_imports(self):
        """
        view should by default dynamically include imports chain
        """
        view = SchemaView(SCHEMA_WITH_IMPORTS)
        logging.debug(view.imports_closure())
        self.assertCountEqual(['kitchen_sink', 'core', 'linkml:types'], view.imports_closure())
        for t in view.all_type().keys():
            logging.debug(f'T={t} in={view.in_schema(t)}')
        assert view.in_schema('Person') == 'kitchen_sink'
        assert view.in_schema('id') == 'core'
        assert view.in_schema('name') == 'core'
        assert view.in_schema('activity') == 'core'
        assert view.in_schema('string') == 'types'
        assert 'activity' in view.all_class()
        assert 'activity' not in view.all_class(imports=False)

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
        logging.debug(view.get_class('Company').class_uri)
        #assert view.get_class('Company').class_uri == 'prov:Agent'
        assert view.get_uri('Company') == 'ks:Company'
        assert view.get_uri('Company', expand=True) == 'https://w3id.org/linkml/tests/kitchen_sink/Company'
        logging.debug(view.get_uri("TestClass"))
        assert view.get_uri('TestClass') == 'core:TestClass'
        assert view.get_uri('TestClass', expand=True) == 'https://w3id.org/linkml/tests/core/TestClass'

        assert view.get_uri('string') == 'xsd:string'


if __name__ == '__main__':
    unittest.main()
