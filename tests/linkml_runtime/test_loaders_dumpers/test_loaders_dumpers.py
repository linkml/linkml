import json
import os
import unittest
import logging
from decimal import Decimal

import yaml
from rdflib import Graph
from rdflib import Namespace

from linkml_runtime.loaders import json_loader
from linkml_runtime.dumpers import rdflib_dumper, yaml_dumper, json_dumper
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.loaders import rdflib_loader
from linkml_runtime.utils.schemaview import SchemaView
from tests.test_loaders_dumpers import INPUT_DIR, OUTPUT_DIR
from tests.test_loaders_dumpers.models.personinfo import Container, Person
from tests.test_loaders_dumpers.models.node_object import NodeObject, Triple

logger = logging.getLogger(__name__)


SCHEMA = os.path.join(INPUT_DIR, 'personinfo.yaml')
DATA = os.path.join(INPUT_DIR, 'example_personinfo_data.yaml')
OUT_TTL = os.path.join(OUTPUT_DIR, 'example_out.ttl')
OUT_JSON = os.path.join(OUTPUT_DIR, 'example_out.json')
OUT_YAML = os.path.join(OUTPUT_DIR, 'example_out.yaml')

prefix_map = {
    'CODE': 'http://example.org/code/',
    'ROR': 'http://example.org/ror/',
    'P': 'http://example.org/P/',
    'GEO': 'http://example.org/GEO/',
}

P = Namespace('http://example.org/P/')
ROR = Namespace('http://example.org/ror/')
CODE = Namespace('http://example.org/code/')
INFO = Namespace('https://w3id.org/linkml/examples/personinfo/')
SDO = Namespace('http://schema.org/')
GSSO = Namespace('http://purl.obolibrary.org/obo/GSSO_')
HP = Namespace('http://purl.obolibrary.org/obo/HP_')
SYMP = Namespace('http://purl.obolibrary.org/obo/SYMP_')
WD = Namespace('http://www.wikidata.org/entity/')

class LoadersDumpersTestCase(unittest.TestCase):

    def setUp(self):
        view = SchemaView(SCHEMA)
        container: Container
        container = yaml_loader.load(DATA, target_class=Container)
        self._check_objs(view, container)
        test_fn = OUT_TTL
        rdflib_dumper.dump(container, schemaview=view, to_file=test_fn, prefix_map=prefix_map)
        container = rdflib_loader.load(test_fn, target_class=Container, schemaview=view, prefix_map=prefix_map)
        self._check_objs(view, container)
        test_fn = OUT_JSON
        json_dumper.dump(container, to_file=test_fn)
        container = json_loader.load(test_fn, target_class=Container)
        self._check_objs(view, container)
        test_fn = OUT_YAML
        yaml_dumper.dump(container, to_file=test_fn)
        container = yaml_loader.load(test_fn, target_class=Container)
        self._check_objs(view, container)
        # TODO: use jsonpatch to compare files

    def test_load_from_list(self):
        """
        Tests the load_any loader method, which can be used to load directly to a list
        """
        view = SchemaView(SCHEMA)
        with open(DATA, encoding='UTF-8') as stream:
            data = yaml.safe_load(stream)
        #persons = yaml_loader.load_source(data, target_class=Person)
        #container = Container(persons=persons)
        person_dicts = data['persons']
        tuples = [(yaml_loader, yaml.dump(person_dicts)), (json_loader, json.dumps(person_dicts, default=str))]
        for loader, person_list_str in tuples:
            persons = loader.loads_any(person_list_str, target_class=Person)
            assert isinstance(persons, list)
            assert isinstance(persons[0], Person)
            [p1] = [p for p in persons if p.id == 'P:001']
            [p2] = [p for p in persons if p.id == 'P:002']
            self.assertEqual(p1.name, 'fred bloggs')
            self.assertEqual(p2.name, 'joe schmö')
            self.assertEqual(p1.age_in_years, 33)
            self.assertEqual(p1.gender.code.text, 'cisgender man')
            self.assertEqual(p2.gender.code.text, 'transgender man')

    def test_encoding(self):
        """
        This will reveal if generated yaml or json files are utf-8 encoded
        """
        # pyyaml or json read non-ascii strings just fine no matter if the
        # file is ascii or utf-8 encoded. So we use Python's open function
        # to detect undesired ascii encoding. (linkml issue #634)
        with open(OUT_YAML, encoding='UTF-8') as f:
            [p2_name_line] = [l for l in f.readlines() if 'joe schm' in l]
        self.assertIn('joe schmö', p2_name_line)

        with open(OUT_JSON, encoding='UTF-8') as f:
            [p2_name_line] = [l for l in f.readlines() if 'joe schm' in l]
        self.assertIn('joe schmö', p2_name_line)


    def _check_objs(self, view: SchemaView, container: Container):
        persons = container.persons
        orgs = container.organizations.values()
        [p1] = [p for p in persons if p.id == 'P:001']
        [p2] = [p for p in persons if p.id == 'P:002']
        [o1] = [o for o in orgs if o.id == 'ROR:1']
        [o2] = [o for o in orgs if o.id == 'ROR:2']
        [o3] = [o for o in orgs if o.id == 'ROR:3']
        [o4] = [o for o in orgs if o.id == 'ROR:4']
        o1cats = [c.code.text for c in o1.categories]
        o2cats = [c.code.text for c in o2.categories]
        self.assertEqual(p1.name, 'fred bloggs')
        self.assertEqual(p2.name, 'joe schmö')
        self.assertEqual(p1.age_in_years, 33)
        self.assertEqual(p1.gender.code.text, 'cisgender man')
        self.assertEqual(p2.gender.code.text, 'transgender man')
        self.assertCountEqual(o1cats, ['non profit', 'charity'])
        self.assertCountEqual(o2cats, ['shell company'])
        p2: Person
        emp = p2.has_employment_history[0]
        self.assertEqual(emp.started_at_time, '2019-01-01')
        self.assertEqual(emp.is_current, True)
        self.assertEqual(emp.employed_at, o1.id)
        frel = p2.has_familial_relationships[0]
        self.assertEqual(frel.related_to, p1.id)
        # TODO: check PV vs PVText
        self.assertEqual(str(frel.type), 'SIBLING_OF')
        med = p2.has_medical_history[0]
        self.assertEqual(med.in_location, 'GEO:1234')
        self.assertEqual(med.diagnosis.id, 'CODE:D0001')
        self.assertEqual(med.diagnosis.name, 'headache')
        self.assertEqual(med.diagnosis.code_system, 'CODE:D')
        # Check decimal representation
        self.assertEqual(o1.score, Decimal(1))
        self.assertEqual(o2.score, Decimal("1.5"))
        self.assertEqual(o3.score, Decimal(1))
        self.assertEqual(o4.score, Decimal(1))
        self.assertEqual(o1.min_salary, Decimal("99999.00"))


    def test_edge_cases(self):
        """
        Tests various edge cases:

         - unprocessed triples (triples that cannot be reached via root objects)
         - mismatch between expected range categories (Type vs Class) and value (Literal vs Node)
         - complex range expressions (e.g. modeling a range as being EITHER string OR object
        """
        # schema with following characterics:
        #  - reified triples
        #  - object has a complex union range (experimental new feature)
        view = SchemaView(os.path.join(INPUT_DIR, 'complex_range_example.yaml'))
        graph = Graph()
        taxon_prefix_map = {
            'NCBITaxon': 'http://purl.obolibrary.org/obo/NCBITaxon_',
            'RO': 'http://purl.obolibrary.org/obo/RO_',
        }
        # this graph has the following characteristics
        #  - blank nodes to represent statements
        #  - some triples not reachable from roots
        #  - implicit schema with complex ranges (rdf:object has range of either node or literal)
        graph.parse(os.path.join(INPUT_DIR, 'bacteria-taxon-class.ttl'), format='ttl')
        objs = rdflib_loader.from_rdf_graph(graph, target_class=NodeObject,
                                            schemaview=view,
                                            cast_literals=False,    ## strict
                                            allow_unprocessed_triples=True,  ## known issue
                                            prefix_map=taxon_prefix_map)
        [obj] = objs
        for x in obj.statements:
            assert x.subject is None
            assert x.predicate is not None
            assert x.object is not None
            logger.info(f'  x={x}')
        # ranges that are objects are contracted
        assert Triple(subject=None, predicate='rdfs:subClassOf', object='owl:Thing') in obj.statements
        assert Triple(subject=None, predicate='rdfs:subClassOf', object='NCBITaxon:1') in obj.statements
        # string ranges
        assert Triple(subject=None, predicate='rdfs:label', object='Bacteria') in obj.statements
        with self.assertRaises(ValueError) as context:
            rdflib_loader.from_rdf_graph(graph, target_class=NodeObject,
                                         schemaview=view,
                                         cast_literals=False,
                                         allow_unprocessed_triples=False,
                                         prefix_map=taxon_prefix_map)
            logger.error(f'Passed unexpectedly: there are known to be unreachable triples')
        # removing complex range, object has a range of string
        view.schema.slots['object'].exactly_one_of = []
        view.set_modified()
        rdflib_loader.from_rdf_graph(graph, target_class=NodeObject,
                                     schemaview=view,
                                     cast_literals=True,   ## required to pass
                                     allow_unprocessed_triples=True,
                                     prefix_map=taxon_prefix_map)
        with self.assertRaises(ValueError) as context:
            rdflib_loader.from_rdf_graph(graph, target_class=NodeObject,
                                         schemaview=view,
                                         cast_literals=False,
                                         allow_unprocessed_triples=True,
                                         prefix_map=taxon_prefix_map)
            logger.error(f'Passed unexpectedly: rdf:object is known to have a mix of literals and nodes')


if __name__ == '__main__':
    unittest.main()
