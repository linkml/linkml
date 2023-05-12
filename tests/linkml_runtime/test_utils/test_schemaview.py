import os
import unittest
import logging
from copy import copy
from pathlib import Path
from typing import List
from unittest import TestCase

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition, SlotDefinitionName, SlotDefinition, \
    ClassDefinitionName
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schemaview import SchemaView, SchemaUsage, OrderedBy
from linkml_runtime.utils.schemaops import roll_up, roll_down
from tests.test_utils import INPUT_DIR

SCHEMA_NO_IMPORTS = Path(INPUT_DIR) / 'kitchen_sink_noimports.yaml'
SCHEMA_WITH_IMPORTS = Path(INPUT_DIR) / 'kitchen_sink.yaml'
SCHEMA_WITH_STRUCTURED_PATTERNS = Path(INPUT_DIR) / "pattern-example.yaml"

yaml_loader = YAMLLoader()
IS_CURRENT = 'is current'
EMPLOYED_AT = 'employed at'
COMPANY = 'Company'
AGENT = 'agent'
ACTIVITY = 'activity'
RELATED_TO = 'related to'
AGE_IN_YEARS = 'age in years'


class SchemaViewTestCase(unittest.TestCase):

    def test_children_method(self):
        view = SchemaView(SCHEMA_NO_IMPORTS)
        children = view.get_children("Person")
        self.assertEqual(children, ['Adult'])

    def test_all_aliases(self):
        view = SchemaView(SCHEMA_NO_IMPORTS)
        aliases = view.all_aliases()
        self.assertIn("identifier", aliases["id"])
        self.assertIn("A", aliases["subset A"])
        self.assertIn("B", aliases["subset B"])
        self.assertIn("dad", aliases["Adult"])
        self.assertNotIn("test", aliases["Adult"])

    def test_schemaview_enums(self):
        view = SchemaView(SCHEMA_NO_IMPORTS)
        for en, e in view.all_enums().items():
            if e.name == "Animals":
                for pv, v in e.permissible_values.items():
                    if pv == "CAT":
                        self.assertEqual(view.permissible_value_parent(pv, e.name), None)
                        self.assertEqual(view.permissible_value_ancestors(pv, e.name), ['CAT'])
                    if pv == "ANGRY_LION":
                        self.assertEqual(view.permissible_value_parent(pv, e.name), ['LION'])
                        self.assertEqual(view.permissible_value_ancestors(pv, e.name), ['ANGRY_LION', 'LION', 'CAT'])
        for cn, c in view.all_classes().items():
            if c.name == "Adult":
                self.assertEqual(view.class_ancestors(c.name), ['Adult', 'Person', 'HasAliases', 'Thing'])

    def test_schemaview(self):
        # no import schema
        view = SchemaView(SCHEMA_NO_IMPORTS)
        logging.debug(view.imports_closure())
        self.assertEqual(len(view.imports_closure()), 1)
        all_cls = view.all_classes()
        logging.debug(f'n_cls = {len(all_cls)}')

        self.assertEqual(list(view.annotation_dict(IS_CURRENT).values()), ['bar'])
        logging.debug(view.annotation_dict(EMPLOYED_AT))
        e = view.get_element(EMPLOYED_AT)
        logging.debug(e.annotations)
        e = view.get_element('has employment history')
        logging.debug(e.annotations)

        elements = view.get_elements_applicable_by_identifier("ORCID:1234")
        self.assertIn("Person", elements)
        elements = view.get_elements_applicable_by_identifier("PMID:1234")
        self.assertIn("Organization", elements)
        elements = view.get_elements_applicable_by_identifier("http://www.ncbi.nlm.nih.gov/pubmed/1234")
        self.assertIn("Organization", elements)
        elements = view.get_elements_applicable_by_identifier("TEST:1234")
        self.assertNotIn("anatomical entity", elements)
        self.assertEqual(list(view.annotation_dict(SlotDefinitionName(IS_CURRENT)).values()), ['bar'])
        logging.debug(view.annotation_dict(SlotDefinitionName(EMPLOYED_AT)))
        element = view.get_element(SlotDefinitionName(EMPLOYED_AT))
        logging.debug(element.annotations)
        element = view.get_element(SlotDefinitionName('has employment history'))
        logging.debug(element.annotations)

        self.assertTrue(view.is_mixin('WithLocation'))
        self.assertFalse(view.is_mixin('BirthEvent'))

        self.assertTrue(view.inverse('employment history of'), 'has employment history')
        self.assertTrue(view.inverse('has employment history'), 'employment history of')
        
        mapping = view.get_mapping_index()
        self.assertTrue(mapping is not None)

        category_mapping = view.get_element_by_mapping("GO:0005198")
        self.assertTrue(category_mapping, [ACTIVITY])

        self.assertTrue(view.is_multivalued('aliases'))
        self.assertFalse(view.is_multivalued('id'))
        self.assertTrue(view.is_multivalued('dog addresses'))

        self.assertTrue(view.slot_is_true_for_metadata_property('aliases', 'multivalued'))
        self.assertTrue(view.slot_is_true_for_metadata_property('id', 'identifier'))
        with self.assertRaises(ValueError):
            view.slot_is_true_for_metadata_property('aliases', 'aliases')

        for tn, t in view.all_types().items():
            logging.info(f'TN = {tn}')
            self.assertEqual('https://w3id.org/linkml/tests/kitchen_sink', t.from_schema)
        for sn, s in view.all_slots().items():
            logging.info(f'SN = {sn} RANGE={s.range}')
            self.assertEqual('https://w3id.org/linkml/tests/kitchen_sink', s.from_schema)
            # range should always be populated: See https://github.com/linkml/linkml/issues/733
            rng = view.induced_slot(sn).range
            self.assertIsNotNone(rng)
        # this section is mostly for debugging
        for cn in all_cls.keys():
            c = view.get_class(cn)
            self.assertEqual('https://w3id.org/linkml/tests/kitchen_sink', c.from_schema)
            logging.debug(f'{cn} PARENTS = {view.class_parents(cn)}')
            logging.debug(f'{cn} ANCS = {view.class_ancestors(cn)}')
            logging.debug(f'{cn} CHILDREN = {view.class_children(cn)}')
            logging.debug(f'{cn} DESCS = {view.class_descendants(cn)}')
            logging.debug(f'{cn} SCHEMA = {view.in_schema(cn)}')
            logging.debug(f'  SLOTS = {view.class_slots(cn)}')
            for sn in view.class_slots(cn):
                slot = view.get_slot(sn)
                self.assertEqual('https://w3id.org/linkml/tests/kitchen_sink', slot.from_schema)
                logging.debug(f'  SLOT {sn} R: {slot.range} U: {view.get_uri(sn)} ANCS: {view.slot_ancestors(sn)}')
                induced_slot = view.induced_slot(sn, cn)
                logging.debug(f'    INDUCED {sn}={induced_slot}')
                # range should always be populated: See https://github.com/linkml/linkml/issues/733
                self.assertIsNotNone(induced_slot.range)


        logging.debug(f'ALL = {view.all_elements().keys()}')

        # -- TEST ANCESTOR/DESCENDANTS FUNCTIONS --

        self.assertCountEqual(['Company', 'Organization', 'HasAliases', 'Thing'],
                              view.class_ancestors(COMPANY))
        self.assertCountEqual(['Organization', 'HasAliases', 'Thing'],
                              view.class_ancestors(COMPANY, reflexive=False))
        self.assertCountEqual(['Thing', 'Person', 'Organization', COMPANY, 'Adult'],
                              view.class_descendants('Thing'))

        # -- TEST CLASS SLOTS --

        self.assertCountEqual(['id', 'name',  ## From Thing
                               'has employment history', 'has familial relationships', 'has medical history',
                               AGE_IN_YEARS, 'addresses', 'has birth event', ## From Person
                               'aliases'  ## From HasAliases
                                ],
                              view.class_slots('Person'))
        self.assertCountEqual(view.class_slots('Person'), view.class_slots('Adult'))
        self.assertCountEqual(['id', 'name',  ## From Thing
                               'ceo', ## From COMPANY
                               'aliases'  ## From HasAliases
                               ],
                              view.class_slots(COMPANY))

        self.assertEqual(view.get_class(AGENT).class_uri, 'prov:Agent')
        self.assertEqual(view.get_uri(AGENT), 'prov:Agent')
        logging.debug(view.get_class(COMPANY).class_uri)

        self.assertEqual(view.get_uri(COMPANY), 'ks:Company')

        # test induced slots

        for c in [COMPANY, 'Person', 'Organization',]:
            islot = view.induced_slot('aliases', c)
            assert islot.multivalued is True
            self.assertEqual(islot.owner, c, 'owner does not match')
            self.assertEqual(view.get_uri(islot, expand=True), 'https://w3id.org/linkml/tests/kitchen_sink/aliases')

        self.assertEqual(view.get_identifier_slot('Company').name, 'id')
        self.assertEqual(view.get_identifier_slot('Thing').name, 'id')
        self.assertTrue(view.get_identifier_slot('FamilialRelationship') is None)
        for c in [COMPANY, 'Person', 'Organization', 'Thing']:
            self.assertTrue(view.induced_slot('id', c).identifier)
            self.assertFalse(view.induced_slot('name', c).identifier)
            self.assertFalse(view.induced_slot('name', c).required)
            self.assertEqual(view.induced_slot('name', c).range, 'string')
            self.assertEqual(view.induced_slot('id', c).owner, c, 'owner does not match')
            self.assertEqual(view.induced_slot('name', c).owner, c, 'owner does not match')
        for c in ['Event', 'EmploymentEvent', 'MedicalEvent']:
            s = view.induced_slot('started at time', c)
            logging.debug(f's={s.range} // c = {c}')
            self.assertEqual(s.range, 'date')
            self.assertEqual(s.slot_uri, 'prov:startedAtTime')
            self.assertEqual(s.owner, c, 'owner does not match')
            c_induced = view.induced_class(c)
            # an induced class should have no slots
            self.assertEqual(c_induced.slots, [])
            self.assertNotEqual(c_induced.attributes, [])
            s2 = c_induced.attributes['started at time']
            self.assertEqual(s2.range, 'date')
            self.assertEqual(s2.slot_uri, 'prov:startedAtTime')
        # test slot_usage
        self.assertEqual(view.induced_slot(AGE_IN_YEARS, 'Person').minimum_value, 0)
        self.assertEqual(view.induced_slot(AGE_IN_YEARS, 'Adult').minimum_value, 16)
        self.assertTrue(view.induced_slot('name', 'Person').pattern is not None)
        self.assertEqual(view.induced_slot('type', 'FamilialRelationship').range, 'FamilialRelationshipType')
        self.assertEqual(view.induced_slot(RELATED_TO, 'FamilialRelationship').range, 'Person')
        self.assertEqual(view.get_slot(RELATED_TO).range, 'Thing')
        self.assertEqual(view.induced_slot(RELATED_TO, 'Relationship').range, 'Thing')
        # https://github.com/linkml/linkml/issues/875
        self.assertCountEqual(['Thing', 'Place'], view.induced_slot('name').domain_of)

        a = view.get_class(ACTIVITY)
        self.assertCountEqual(a.exact_mappings, ['prov:Activity'])
        logging.debug(view.get_mappings(ACTIVITY, expand=True))
        self.assertCountEqual(view.get_mappings(ACTIVITY)['exact'], ['prov:Activity'])
        self.assertCountEqual(view.get_mappings(ACTIVITY, expand=True)['exact'], ['http://www.w3.org/ns/prov#Activity'])

        u = view.usage_index()
        for k, v in u.items():
            logging.debug(f' {k} = {v}')
        self.assertIn(SchemaUsage(used_by='FamilialRelationship', slot=RELATED_TO,
                           metaslot='range', used='Person', inferred=False), u['Person'])

        # test methods also work for attributes
        leaves = view.class_leaves()
        logging.debug(f'LEAVES={leaves}')
        self.assertIn('MedicalEvent', leaves)
        roots = view.class_roots()
        logging.debug(f'ROOTS={roots}')
        self.assertIn('Dataset', roots)
        ds_slots = view.class_slots('Dataset')
        logging.debug(ds_slots)
        self.assertEqual(len(ds_slots), 3)
        self.assertCountEqual(['persons', 'companies', 'activities'], ds_slots)
        for sn in ds_slots:
            s = view.induced_slot(sn, 'Dataset')
            logging.debug(s)

    def test_all_classes_ordered_lexical(self):
        view = SchemaView(SCHEMA_NO_IMPORTS)
        classes = view.all_classes(ordered_by=OrderedBy.LEXICAL)

        ordered_c = []
        for c in classes.values():
            ordered_c.append(c.name)
        self.assertEqual(ordered_c, sorted(ordered_c))

    def test_all_classes_ordered_rank(self):
        view = SchemaView(SCHEMA_NO_IMPORTS)
        classes = view.all_classes(ordered_by=OrderedBy.RANK)
        ordered_c = []
        for c in classes.values():
            ordered_c.append(c.name)
        first_in_line = []
        second_in_line = []
        for name, definition in classes.items():
            if definition.rank == 1:
                first_in_line.append(name)
            elif definition.rank == 2:
                second_in_line.append(name)
        self.assertIn(ordered_c[0], first_in_line)
        self.assertNotIn(ordered_c[10], second_in_line)

    def test_all_classes_ordered_no_ordered_by(self):
        view = SchemaView(SCHEMA_NO_IMPORTS)
        classes = view.all_classes()
        ordered_c = []
        for c in classes.values():
            ordered_c.append(c.name)
        self.assertEqual("HasAliases", ordered_c[0])
        self.assertEqual("EmptyClass", ordered_c[-1])
        self.assertEqual("agent", ordered_c[-2])

    def test_all_slots_ordered_lexical(self):
        view = SchemaView(SCHEMA_NO_IMPORTS)
        slots = view.all_slots(ordered_by=OrderedBy.LEXICAL)
        ordered_s = []
        for s in slots.values():
            ordered_s.append(s.name)
        self.assertEqual(ordered_s, sorted(ordered_s))

    def test_all_slots_ordered_rank(self):
        view = SchemaView(SCHEMA_NO_IMPORTS)
        slots = view.all_slots(ordered_by=OrderedBy.RANK)
        ordered_s = []
        for s in slots.values():
            ordered_s.append(s.name)
        first_in_line = []
        second_in_line = []
        for name, definition in slots.items():
            if definition.rank == 1:
                first_in_line.append(name)
            elif definition.rank == 2:
                second_in_line.append(name)
        self.assertIn(ordered_s[0], first_in_line)
        self.assertNotIn(ordered_s[10], second_in_line)

    def test_rollup_rolldown(self):
        # no import schema
        view = SchemaView(SCHEMA_NO_IMPORTS)
        element_name = 'Event'
        roll_up(view, element_name)
        for slot in view.class_induced_slots(element_name):
            logging.debug(slot)
        induced_slot_names = [s.name for s in view.class_induced_slots(element_name)]
        logging.debug(induced_slot_names)
        self.assertCountEqual(['started at time', 'ended at time', IS_CURRENT, 'in location', EMPLOYED_AT, 'married to'],
                              induced_slot_names)
        # check to make sure rolled-up classes are deleted
        self.assertEqual(view.class_descendants(element_name, reflexive=False), [])
        roll_down(view, view.class_leaves())

        for element_name in view.all_classes():
            c = view.get_class(element_name)
            logging.debug(f'{element_name}')
            logging.debug(f'  {element_name} SLOTS(i) = {view.class_slots(element_name)}')
            logging.debug(f'  {element_name} SLOTS(d) = {view.class_slots(element_name, direct=True)}')
            self.assertCountEqual(view.class_slots(element_name), view.class_slots(element_name, direct=True))
        self.assertNotIn('Thing', view.all_classes())
        self.assertNotIn('Person', view.all_classes())
        self.assertIn('Adult', view.all_classes())
        
    def test_caching(self):
        """
        Determine if cache is reset after modifications made to schema
        """
        schema = SchemaDefinition(id='test', name='test')
        view = SchemaView(schema)
        self.assertCountEqual([], view.all_classes())
        view.add_class(ClassDefinition('X'))
        self.assertCountEqual(['X'], view.all_classes())
        view.add_class(ClassDefinition('Y'))
        self.assertCountEqual(['X', 'Y'], view.all_classes())
        # bypass view method and add directly to schema;
        # in general this is not recommended as the cache will
        # not be updated
        view.schema.classes['Z'] = ClassDefinition('Z')
        # as expected, the view doesn't know about Z
        self.assertCountEqual(['X', 'Y'], view.all_classes())
        # inform the view modifications have been made
        view.set_modified()
        # should be in sync
        self.assertCountEqual(['X', 'Y', 'Z'], view.all_classes())
        # recommended way to make updates
        view.delete_class('X')
        # cache will be up to date
        self.assertCountEqual(['Y', 'Z'], view.all_classes())
        view.add_class(ClassDefinition('W'))
        self.assertCountEqual(['Y', 'Z', 'W'], view.all_classes())

    def test_imports(self):
        """
        view should by default dynamically include imports chain
        """
        view = SchemaView(SCHEMA_WITH_IMPORTS)
        self.assertIsNotNone(view.schema.source_file)
        logging.debug(view.imports_closure())
        self.assertCountEqual(['kitchen_sink', 'core', 'linkml:types'], view.imports_closure())
        for t in view.all_types().keys():
            logging.debug(f'T={t} in={view.in_schema(t)}')
        self.assertEqual(view.in_schema(ClassDefinitionName('Person')), 'kitchen_sink')
        self.assertEqual(view.in_schema(SlotDefinitionName('id')), 'core')
        self.assertEqual(view.in_schema(SlotDefinitionName('name')), 'core')
        self.assertEqual(view.in_schema(SlotDefinitionName(ACTIVITY)), 'core')
        self.assertEqual(view.in_schema(SlotDefinitionName('string')), 'types')
        self.assertIn(ACTIVITY, view.all_classes())
        self.assertNotIn(ACTIVITY, view.all_classes(imports=False))
        self.assertIn('string', view.all_types())
        self.assertNotIn('string', view.all_types(imports=False))
        self.assertCountEqual(['SymbolString', 'string'], view.type_ancestors('SymbolString'))

        for tn, t in view.all_types().items():
            self.assertEqual(tn, t.name)
            induced_t = view.induced_type(tn)
            self.assertIsNotNone(induced_t.uri)
            #self.assertIsNotNone(induced_t.repr)
            self.assertIsNotNone(induced_t.base)
            if t in view.all_types(imports=False).values():
                self.assertEqual('https://w3id.org/linkml/tests/kitchen_sink', t.from_schema)
            else:
                self.assertIn(t.from_schema, ['https://w3id.org/linkml/tests/core', 'https://w3id.org/linkml/types'])
        for en, e in view.all_enums().items():
            self.assertEqual(en, e.name)
            if e in view.all_enums(imports=False).values():
                self.assertEqual('https://w3id.org/linkml/tests/kitchen_sink', e.from_schema)
            else:
                self.assertEqual('https://w3id.org/linkml/tests/core', e.from_schema)
        for sn, s in view.all_slots().items():
            self.assertEqual(sn, s.name)
            s_induced = view.induced_slot(sn)
            self.assertIsNotNone(s_induced.range)
            if s in view.all_slots(imports=False).values():
                self.assertEqual('https://w3id.org/linkml/tests/kitchen_sink', s.from_schema)
            else:
                self.assertEqual('https://w3id.org/linkml/tests/core', s.from_schema)
        for cn, c in view.all_classes().items():
            self.assertEqual(cn, c.name)
            if c in view.all_classes(imports=False).values():
                self.assertEqual('https://w3id.org/linkml/tests/kitchen_sink', c.from_schema)
            else:
                self.assertEqual('https://w3id.org/linkml/tests/core', c.from_schema)
            for s in view.class_induced_slots(cn):
                if s in view.all_classes(imports=False).values():
                    self.assertIsNotNone(s.slot_uri)
                    self.assertEqual('https://w3id.org/linkml/tests/kitchen_sink', s.from_schema)

        for c in ['Company', 'Person', 'Organization', 'Thing']:
            self.assertTrue(view.induced_slot('id', c).identifier)
            self.assertFalse(view.induced_slot('name', c).identifier)
            self.assertFalse(view.induced_slot('name', c).required)
            self.assertEqual(view.induced_slot('name', c).range, 'string')
        for c in ['Event', 'EmploymentEvent', 'MedicalEvent']:
            s = view.induced_slot('started at time', c)
            self.assertEqual(s.range, 'date')
            self.assertEqual(s.slot_uri, 'prov:startedAtTime')
        self.assertEqual(view.induced_slot(AGE_IN_YEARS, 'Person').minimum_value, 0)
        self.assertEqual(view.induced_slot(AGE_IN_YEARS, 'Adult').minimum_value, 16)

        self.assertEqual(view.get_class('agent').class_uri, 'prov:Agent')
        self.assertEqual(view.get_uri(AGENT), 'prov:Agent')
        logging.debug(view.get_class('Company').class_uri)

        self.assertEqual(view.get_uri(COMPANY), 'ks:Company')
        self.assertEqual(view.get_uri(COMPANY, expand=True), 'https://w3id.org/linkml/tests/kitchen_sink/Company')
        logging.debug(view.get_uri('TestClass'))
        self.assertEqual(view.get_uri('TestClass'), 'core:TestClass')
        self.assertEqual(view.get_uri('TestClass', expand=True), 'https://w3id.org/linkml/tests/core/TestClass')

        self.assertEqual(view.get_uri('string'), 'xsd:string')

        # dynamic enums
        e = view.get_enum('HCAExample')
        self.assertCountEqual(['GO:0007049',
                               'GO:0022403'],
                              e.include[0].reachable_from.source_nodes)

        # units
        height = view.get_slot('height_in_m')
        self.assertEqual("m", height.unit.ucum_code)

    def test_imports_from_schemaview(self):
        """
        view should by default dynamically include imports chain
        """
        view = SchemaView(SCHEMA_WITH_IMPORTS)
        view2 = SchemaView(view.schema)
        self.assertCountEqual(view.all_classes(), view2.all_classes())
        self.assertCountEqual(view.all_classes(imports=False), view2.all_classes(imports=False))

    def test_direct_remote_imports(self):
        """
        Tests that building a SchemaView directly from a remote URL works.

        Note: this should be the only test in this suite that fails if there is
        no network connection.
        """
        view = SchemaView("https://w3id.org/linkml/meta.yaml")
        main_classes = ["class_definition", "prefix"]
        imported_classes = ["annotation"]
        for c in main_classes:
            self.assertIn(c, view.all_classes(imports=True))
            self.assertIn(c, view.all_classes(imports=False))
        for c in imported_classes:
            self.assertIn(c, view.all_classes(imports=True))
            self.assertNotIn(c, view.all_classes(imports=False))

    @unittest.skip("Skipped as fragile: will break if the remote schema changes")
    def test_direct_remote_imports_additional(self):
        """
        Alternative test to: https://github.com/linkml/linkml/pull/1379
        """
        url = "https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/model/schema/mixs.yaml"
        view = SchemaView(url)
        self.assertEqual(view.schema.name, "MIxS")
        class_count = len(view.all_classes())
        self.assertGreater(class_count, 0)


    def test_merge_imports(self):
        """
        ensure merging and merging imports closure works
        """
        view = SchemaView(SCHEMA_WITH_IMPORTS)
        all_c = copy(view.all_classes())
        all_c_noi = copy(view.all_classes(imports=False))
        self.assertLess(len(all_c_noi), len(all_c))
        view.merge_imports()
        all_c2 = copy(view.all_classes())
        self.assertCountEqual(all_c, all_c2)
        all_c2_noi = copy(view.all_classes(imports=False))
        self.assertEqual(len(all_c2_noi), len(all_c2))

    def test_metamodel_imports(self):
        """
        Tests imports of the metamodel.

        Note: this test and others should be able to run without network connectivity.
        SchemaView should make use of the version of the metamodel distributed with the package
        over the network available version.

        TODO: use mock testing framework to emulate no access to network.

        - `<https://github.com/linkml/linkml/issues/502>`_
        :return:
        """
        schema = SchemaDefinition(id='test', name='metamodel-imports-test',
                                  imports=["linkml:meta"])
        sv = SchemaView(schema)
        all_classes = sv.all_classes()
        self.assertGreater(len(all_classes), 20)
        schema_str = yaml_dumper.dumps(schema)
        sv = SchemaView(schema_str)
        self.assertGreater(len(sv.all_classes()), 20)
        self.assertCountEqual(all_classes, sv.all_classes())


    def test_traversal(self):
        schema = SchemaDefinition(id='test', name='traversal-test')
        view = SchemaView(schema)
        view.add_class(ClassDefinition('Root', mixins=['RootMixin']))
        view.add_class(ClassDefinition('A', is_a='Root', mixins=['Am1', 'Am2', 'AZ']))
        view.add_class(ClassDefinition('B', is_a='A', mixins=['Bm1', 'Bm2', 'BY']))
        view.add_class(ClassDefinition('C', is_a='B', mixins=['Cm1', 'Cm2', 'CX']))
        view.add_class(ClassDefinition('RootMixin', mixin=True))
        view.add_class(ClassDefinition('Am1', is_a='RootMixin', mixin=True))
        view.add_class(ClassDefinition('Am2', is_a='RootMixin', mixin=True))
        view.add_class(ClassDefinition('Bm1', is_a='Am1', mixin=True))
        view.add_class(ClassDefinition('Bm2', is_a='Am2', mixin=True))
        view.add_class(ClassDefinition('Cm1', is_a='Bm1', mixin=True))
        view.add_class(ClassDefinition('Cm2', is_a='Bm2', mixin=True))
        view.add_class(ClassDefinition('AZ', is_a='RootMixin', mixin=True))
        view.add_class(ClassDefinition('BY', is_a='RootMixin', mixin=True))
        view.add_class(ClassDefinition('CX', is_a='RootMixin', mixin=True))

        def check(ancs: List, expected: List):
            self.assertEqual(ancs, expected)
        check(view.class_ancestors('C', depth_first=True),
              ['C', 'Cm1', 'Cm2', 'CX', 'B', 'Bm1', 'Bm2', 'BY', 'A', 'Am1', 'Am2', 'AZ', 'Root', 'RootMixin'])
        check(view.class_ancestors('C', depth_first=False),
              ['C', 'Cm1', 'Cm2', 'CX', 'B', 'Bm1', 'Bm2', 'RootMixin', 'BY', 'A', 'Am1', 'Am2', 'AZ', 'Root'])
        check(view.class_ancestors('C', mixins=False),
              ['C', 'B', 'A', 'Root'])
        check(view.class_ancestors('C', is_a=False),
              ['C', 'Cm1', 'Cm2', 'CX'])

    def test_slot_inheritance(self):
        schema = SchemaDefinition(id='test', name='test')
        view = SchemaView(schema)
        view.add_class(ClassDefinition('C', slots=['s1', 's2']))
        view.add_class(ClassDefinition('D'))
        view.add_class(ClassDefinition('Z'))
        view.add_class(ClassDefinition('W'))
        #view.add_class(ClassDefinition('C2',
        #                               is_a='C')
        #                              # slot_usage=[SlotDefinition(s1, range='C2')])
        view.add_slot(SlotDefinition('s1', multivalued=True, range='D'))
        view.add_slot(SlotDefinition('s2', is_a='s1'))
        view.add_slot(SlotDefinition('s3', is_a='s2', mixins=['m1']))
        view.add_slot(SlotDefinition('s4', is_a='s2', mixins=['m1'], range='W'))
        view.add_slot(SlotDefinition('m1', mixin=True, multivalued=False, range='Z'))
        slot1 = view.induced_slot('s1', 'C')
        self.assertEqual(slot1.is_a, None)
        self.assertEqual('D', slot1.range)
        self.assertIsNotNone(slot1.multivalued)
        slot2 = view.induced_slot('s2', 'C')
        self.assertEqual(slot2.is_a, 's1')
        self.assertEqual('D', slot2.range)
        self.assertIsNotNone(slot2.multivalued)
        slot3 = view.induced_slot('s3', 'C')
        self.assertIsNotNone(slot3.multivalued)
        self.assertEqual('Z', slot3.range)
        slot4 = view.induced_slot('s4', 'C')
        self.assertIsNotNone(slot4.multivalued)
        self.assertEqual('W', slot4.range)
        # test dangling
        view.add_slot(SlotDefinition('s5', is_a='does-not-exist'))
        with self.assertRaises(ValueError):
            view.slot_ancestors('s5')

    def test_attribute_inheritance(self):
        """
        Tests attribute inheritance edge cases
        :return:
        """
        view = SchemaView(os.path.join(INPUT_DIR, 'attribute_edge_cases.yaml'))
        expected = [
            ('Root', 'a1', None, "a1"),
            ('Root', 'a2', None, "a2"),
            ('Root', 'a3', None, "a3"),
            ('C1', 'a1', True, "a1m1"),
            ('C1', 'a2', True, "a2c1"),
            ('C1', 'a3', None, "a3"),
            ('C1', 'a4', None, "a4"),
            ('C2', 'a1', False, "a1m2"),
            ('C2', 'a2', True, "a2c2"),
            ('C2', 'a3', None, "a3"),
            ('C2', 'a4', True, "a4m2"),
            ('C1x', 'a1', True, "a1m1"),
            ('C1x', 'a2', True, "a2c1x"),
            ('C1x', 'a3', None, "a3"),
            ('C1x', 'a4', None, "a4"),
        ]
        for cn, sn, req, desc in expected:
            slot = view.induced_slot(sn, cn)
            self.assertEqual(req, slot.required, f"in: {cn}.{sn}")
            self.assertEqual(desc, slot.description, f"in: {cn}.{sn}")
            self.assertEqual('string', slot.range, f"in: {cn}.{sn}")

    def test_ambiguous_attributes(self):
        """
        Tests behavior where multiple attributes share the same name
        """
        schema = SchemaDefinition(id='test', name='test')
        view = SchemaView(schema)
        a1 = SlotDefinition('a1', range='string')
        a2 = SlotDefinition('a2', range='FooEnum')
        a3 = SlotDefinition('a3', range='C3')
        view.add_class(ClassDefinition('C1', attributes={a1.name: a1, a2.name: a2, a3.name: a3}))
        a1x = SlotDefinition('a1', range='integer')
        a2x = SlotDefinition('a2', range='BarEnum')
        view.add_class(ClassDefinition('C2', attributes={a1x.name: a1x, a2x.name: a2x}))
        # a1 and a2 are ambiguous: only stub information available
        # without class context
        self.assertIsNone(view.get_slot(a1.name).range)
        self.assertIsNone(view.get_slot(a2.name).range)
        self.assertIsNotNone(view.get_slot(a3.name).range)
        self.assertEqual(3, len(view.all_slots(attributes=True)))
        self.assertEqual(0, len(view.all_slots(attributes=False)))
        # default is to include attributes
        self.assertEqual(3, len(view.all_slots()))
        self.assertEqual(a3.range, view.induced_slot(a3.name).range)
        self.assertEqual(a1.range, view.induced_slot(a1.name, 'C1').range)
        self.assertEqual(a2.range, view.induced_slot(a2.name, 'C1').range)
        self.assertEqual(a1x.range, view.induced_slot(a1x.name, 'C2').range)
        self.assertEqual(a2x.range, view.induced_slot(a2x.name, 'C2').range)

    def test_metamodel_in_schemaview(self):
        view = package_schemaview('linkml_runtime.linkml_model.meta')
        self.assertIn('meta', view.imports_closure())
        self.assertIn('linkml:types', view.imports_closure())
        self.assertIn('meta', view.imports_closure(imports=False))
        self.assertNotIn('linkml:types', view.imports_closure(imports=False))
        self.assertEqual(1, len(view.imports_closure(imports=False)))
        all_classes = list(view.all_classes().keys())
        all_classes_no_imports = list(view.all_classes(imports=False).keys())
        for cn in ['class_definition', 'type_definition', 'slot_definition']:
            self.assertIn(cn, all_classes)
            self.assertIn(cn, all_classes_no_imports)
            self.assertEqual(view.get_identifier_slot(cn).name, 'name')
        for cn in ['annotation', 'extension']:
            self.assertIn(cn, all_classes, "imports should be included by default")
            self.assertNotIn(cn, all_classes_no_imports, "imported class unexpectedly included")
        for sn in ['id', 'name', 'description']:
            self.assertIn(sn, view.all_slots())
        for tn in ['uriorcurie', 'string', 'float']:
            self.assertIn(tn, view.all_types())
        for tn in ['uriorcurie', 'string', 'float']:
            self.assertNotIn(tn, view.all_types(imports=False))
        for cn, c in view.all_classes().items():
            uri = view.get_uri(cn, expand=True)
            self.assertIsNotNone(uri)
            if cn != 'structured_alias' and cn != 'UnitOfMeasure' and cn != 'ValidationReport' and \
                cn != 'ValidationResult':
                self.assertIn('https://w3id.org/linkml/', uri)
            induced_slots = view.class_induced_slots(cn)
            for s in induced_slots:
                exp_slot_uri = view.get_uri(s, expand=True)
                self.assertIsNotNone(exp_slot_uri)

    def test_get_classes_by_slot(self):
        sv = SchemaView(SCHEMA_WITH_IMPORTS)

        slot = sv.get_slot(AGE_IN_YEARS)

        actual_result = sv.get_classes_by_slot(slot)
        expected_result = ["Person"]

        self.assertListEqual(expected_result, actual_result)

        actual_result = sv.get_classes_by_slot(slot, include_induced=True)
        expected_result = ["Person", "Adult"]

        self.assertListEqual(actual_result, expected_result)

    def test_materialize_patterns(self):
        sv = SchemaView(SCHEMA_WITH_STRUCTURED_PATTERNS)

        sv.materialize_patterns()

        height_slot = sv.get_slot("height")
        weight_slot = sv.get_slot("weight")

        self.assertEqual(height_slot.pattern, "\d+[\.\d+] (centimeter|meter|inch)")
        self.assertEqual(weight_slot.pattern, "\d+[\.\d+] (kg|g|lbs|stone)")

    def test_materialize_patterns_slot_usage(self):
        sv = SchemaView(SCHEMA_WITH_STRUCTURED_PATTERNS)

        sv.materialize_patterns()

        name_slot_usage = sv.get_class("FancyPersonInfo").slot_usage['name']

        self.assertEqual(name_slot_usage.pattern, "\\S+ \\S+-\\S+")

    def test_materialize_patterns_attribute(self):
        sv = SchemaView(SCHEMA_WITH_STRUCTURED_PATTERNS)

        sv.materialize_patterns()

        weight_attribute = sv.get_class('ClassWithAttributes').attributes['weight']

        self.assertEqual(weight_attribute.pattern, "\d+[\.\d+] (kg|g|lbs|stone)")

    def test_mergeimports(self):
        sv = SchemaView(SCHEMA_WITH_IMPORTS, merge_imports=False)
        # activity class is in core, but not in kitchen_sink
        classes_list = list(sv.schema.classes.keys())
        self.assertNotIn("activity", classes_list)

        # was generated by slot is in core, but not in kitchen_sink
        slots_list = list(sv.schema.slots.keys())
        self.assertNotIn("was generated by", slots_list)

        # list of prefixes only in kitchen_sink
        prefixes_list = list(sv.schema.prefixes.keys())
        self.assertListEqual(
                ["pav", "dce", "lego", "linkml", "biolink", "ks", "RO", "BFO", "tax"], 
                prefixes_list
        )

        # merge_imports=True, so activity class should be present
        sv = SchemaView(SCHEMA_WITH_IMPORTS, merge_imports=True)
        classes_list = list(sv.schema.classes.keys())
        self.assertIn("activity", classes_list)

        slots_list = list(sv.schema.slots.keys())
        self.assertIn("was generated by", slots_list)

        prefixes_list = list(sv.schema.prefixes.keys())
        if 'schema' not in prefixes_list:
            prefixes_list.append('schema')
        self.assertCountEqual(
                ["pav", 
                "dce", 
                "lego", 
                "linkml", 
                "biolink", 
                "ks", 
                "RO", 
                "BFO", 
                "tax", 
                "core", 
                "prov", 
                "xsd",
                "schema",
                "shex",
                ],
                prefixes_list
        )

    def test_is_inlined(self):
        schema_path = os.path.join(INPUT_DIR, "schemaview_is_inlined.yaml")
        sv = SchemaView(schema_path)
        cases = [
            # slot name, expected is_inline
            ("a_thing_with_id", False),
            ("inlined_thing_with_id", True),
            ("inlined_as_list_thing_with_id", True),
            ("a_thing_without_id", True),
            ("inlined_thing_without_id", True),
            ("inlined_as_list_thing_without_id", True),
            ("an_integer", False),
            ("inlined_integer", False),
            ("inlined_as_list_integer", False)
        ]
        for slot_name, expected_result in cases:
            with self.subTest(slot_name=slot_name):
                slot = sv.get_slot(slot_name)
                actual_result = sv.is_inlined(slot)
                self.assertEqual(actual_result, expected_result)


if __name__ == '__main__':
    unittest.main()
