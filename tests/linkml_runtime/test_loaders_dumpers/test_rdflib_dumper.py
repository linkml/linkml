import json
import os
import unittest
import logging

from rdflib import Graph, Literal
from rdflib.namespace import RDF
from rdflib import Namespace

from linkml_runtime.loaders import json_loader
from linkml_runtime.dumpers import rdflib_dumper, yaml_dumper
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.loaders import rdflib_loader
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.schemaops import roll_up, roll_down
from tests.test_loaders_dumpers import INPUT_DIR, OUTPUT_DIR
from tests.test_loaders_dumpers.models.personinfo import Container, Person

SCHEMA = os.path.join(INPUT_DIR, 'personinfo.yaml')
DATA = os.path.join(INPUT_DIR, 'example_personinfo_data.yaml')
DATA_TTL = os.path.join(INPUT_DIR, 'example_personinfo_data.ttl')
OUT = os.path.join(OUTPUT_DIR, 'example_personinfo_data.ttl')
DATA_ROUNDTRIP = os.path.join(OUTPUT_DIR, 'example_personinfo_data.roundtrip-rdf.yaml')

prefix_map = {
    'CODE': 'http://example.org/code/',
    'ROR': 'http://example.org/ror/',
    'P': 'http://example.org/P/',
    'GEO': 'http://example.org/GEO/',
}

class RdfLibDumperTestCase(unittest.TestCase):

    def test_rdflib_dumper(self):
        view = SchemaView(SCHEMA)
        container = yaml_loader.load(DATA, target_class=Container)
        self._check_objs(view, container)
        rdflib_dumper.dump(container, schemaview=view, to_file=OUT, prefix_map=prefix_map)
        g = Graph()
        g.parse(OUT, format='ttl')
        P = Namespace('http://example.org/P/')
        ROR = Namespace('http://example.org/ror/')
        CODE = Namespace('http://example.org/code/')
        INFO = Namespace('https://w3id.org/linkml/examples/personinfo/')
        SDO = Namespace('http://schema.org/')
        GSSO = Namespace('http://purl.obolibrary.org/obo/GSSO_')
        self.assertIn((P['001'], RDF.type, SDO.Person), g)
        self.assertIn((P['001'], SDO.name, Literal("fred bloggs")), g)
        self.assertIn((P['001'], SDO.email, Literal("fred.bloggs@example.com")), g)
        self.assertIn((P['001'], INFO.age_in_years, Literal(33)), g)
        self.assertIn((P['001'], SDO.gender, GSSO['000371']), g)
        #for (s,p,o) in g.triples((None, None, None)):
        #    print(f'{s} {p} {o}')
        self.assertIn((CODE['D0001'], RDF.type, INFO.DiagnosisConcept), g)
        [container] = g.subjects(RDF.type, INFO.Container)
        self.assertIn((container, INFO.organizations, ROR['1']), g)
        self.assertIn((container, INFO.organizations, ROR['2']), g)
        self.assertIn((container, INFO.persons, P['001']), g)
        self.assertIn((container, INFO.persons, P['002']), g)
        container: Container = rdflib_loader.load(OUT, target_class=Container, schemaview=view, prefix_map=prefix_map)
        self._check_objs(view, container)


    def test_rdflib_loader(self):
        view = SchemaView(SCHEMA)
        container: Container = rdflib_loader.load(DATA_TTL, target_class=Container, schemaview=view, prefix_map=prefix_map)
        self._check_objs(view, container)
        yaml_dumper.dump(container, to_file=DATA_ROUNDTRIP)


    def _check_objs(self, view: SchemaView, container: Container):
        persons = container.persons
        orgs = container.organizations.values()
        [p1] = [p for p in persons if p.id == 'P:001']
        [p2] = [p for p in persons if p.id == 'P:002']
        [o1] = [o for o in orgs if o.id == 'ROR:1']
        [o2] = [o for o in orgs if o.id == 'ROR:2']
        o1cats = [c.code.text for c in o1.categories]
        o2cats = [c.code.text for c in o2.categories]
        self.assertEqual(p1.name, 'fred bloggs')
        self.assertEqual(p2.name, 'joe schmoe')
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



if __name__ == '__main__':
    unittest.main()
