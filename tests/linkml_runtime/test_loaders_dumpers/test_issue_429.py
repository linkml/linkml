import os
import unittest
from rdflib import Graph, Literal
from rdflib import Namespace
from rdflib.namespace import RDF
from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView
from tests.test_loaders_dumpers import INPUT_DIR, OUTPUT_DIR
from tests.test_loaders_dumpers.models.personinfo_test_issue_429 import Container

SCHEMA = os.path.join(INPUT_DIR, 'personinfo_test_issue_429.yaml')
DATA = os.path.join(INPUT_DIR, 'example_personinfo_test_issue_429_data.yaml')
OUT = os.path.join(OUTPUT_DIR, 'example_personinfo_test_issue_429_data.ttl')

ORCID = Namespace('https://orcid.org/')
personinfo = Namespace('https://w3id.org/linkml/examples/personinfo/')
SDO = Namespace('http://schema.org/')


class RdfLibDumperTestCase(unittest.TestCase):

    def test_rdflib_dumper(self):
        view = SchemaView(SCHEMA)
        container = yaml_loader.load(DATA, target_class=Container)
        rdflib_dumper.dump(container, schemaview=view, to_file=OUT)
        g = Graph()
        g.parse(OUT, format='ttl')
        self.assertIn((ORCID['1234'], RDF.type, SDO.Person), g)
        self.assertIn((ORCID['1234'], personinfo.full_name, Literal("Clark Kent")), g)
        self.assertIn((ORCID['1234'], personinfo.age, Literal("32")), g)
        self.assertIn((ORCID['1234'], personinfo.phone, Literal("555-555-5555")), g)
        self.assertIn((ORCID['4567'], RDF.type, SDO.Person), g)
        self.assertIn((ORCID['4567'], personinfo.full_name, Literal("Lois Lane")), g)
        self.assertIn((ORCID['4567'], personinfo.age, Literal("33")), g)
        self.assertIn((ORCID['4567'], personinfo.phone, Literal("555-555-5555")), g)

    def test_prefixes(self):
        with open(OUT, encoding='UTF-8') as file:
            for line in file:
                if 'prefix' in line:
                    print(line)


if __name__ == '__main__':
    unittest.main()

