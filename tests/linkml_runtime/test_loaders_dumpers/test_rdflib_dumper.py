import json
import os
import unittest
import logging

from rdflib import Graph, Literal
from rdflib.namespace import RDF
from rdflib import Namespace

from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition, SlotDefinitionName
from linkml_runtime.loaders import json_loader
from linkml_runtime.dumpers.rdflib_dumper import RDFLibDumper
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.schemaops import roll_up, roll_down
from tests.test_loaders_dumpers import INPUT_DIR, OUTPUT_DIR
from tests.test_loaders_dumpers.models.personinfo import Container

SCHEMA = os.path.join(INPUT_DIR, 'personinfo.yaml')
DATA = os.path.join(INPUT_DIR, 'example_personinfo_data.yaml')
OUT = os.path.join(OUTPUT_DIR, 'example_personinfo_data.ttl')

yaml_loader = YAMLLoader()


class RdfLibDumperTestCase(unittest.TestCase):

    def test_rdflib_dumper(self):
        view = SchemaView(SCHEMA)
        dataset = yaml_loader.load(DATA, target_class=Container)
        pm = {
            'CODE': 'http://example.org/code/',
            'ROR': 'http://example.org/ror/',
            'P': 'http://example.org/P/',
            'GEO': 'http://example.org/GEO/',
        }
        rdflib_dumper = RDFLibDumper()
        rdflib_dumper.dump(dataset, schemaview=view, to_file=OUT, prefix_map=pm)
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


if __name__ == '__main__':
    unittest.main()
