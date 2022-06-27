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


class RdfLibPrefixTestCase(unittest.TestCase):
    SCHEMA = os.path.join(INPUT_DIR, 'personinfo_test_issue_429.yaml')
    DATA = os.path.join(INPUT_DIR, 'example_personinfo_test_issue_429_data.yaml')
    OUT = os.path.join(OUTPUT_DIR, 'example_personinfo_test_issue_429_data.ttl')

    ORCID = Namespace('https://orcid.org/')
    personinfo = Namespace('https://w3id.org/linkml/examples/personinfo/')
    SDO = Namespace('http://schema.org/')

    def setUp(self):
        self.g = self.create_rdf_output()

    def create_rdf_output(self):
        view = SchemaView(self.SCHEMA)
        container = yaml_loader.load(self.DATA, target_class=Container)
        rdflib_dumper.dump(container, schemaview=view, to_file=self.OUT)
        g = Graph()
        g.parse(self.OUT, format='ttl')
        return g

    def test_rdf_output(self):
        self.assertIn((self.ORCID['1234'], RDF.type, self.SDO.Person), self.g)
        self.assertIn((self.ORCID['1234'], self.personinfo.full_name, Literal("Clark Kent")), self.g)
        self.assertIn((self.ORCID['1234'], self.personinfo.age, Literal("32")), self.g)
        self.assertIn((self.ORCID['1234'], self.personinfo.phone, Literal("555-555-5555")), self.g)
        self.assertIn((self.ORCID['4567'], RDF.type, self.SDO.Person), self.g)
        self.assertIn((self.ORCID['4567'], self.personinfo.full_name, Literal("Lois Lane")), self.g)
        self.assertIn((self.ORCID['4567'], self.personinfo.age, Literal("33")), self.g)
        self.assertIn((self.ORCID['4567'], self.personinfo.phone, Literal("555-555-5555")), self.g)

    def test_output_prefixes(self):
        with open(self.OUT, encoding='UTF-8') as file:
            file_string = file.read()
        prefixes = ['prefix ORCID:', 'prefix personinfo:', 'prefix sdo:', 'sdo:Person', 'personinfo:age', 'ORCID:1234']
        for prefix in prefixes:
            assert(prefix in file_string)


if __name__ == '__main__':
    unittest.main()
