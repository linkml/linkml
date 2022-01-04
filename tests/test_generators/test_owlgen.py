import sys
import unittest
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, OWL

from linkml.generators.owlgen import OwlSchemaGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path('kitchen_sink.yaml')
DATA = env.input_path('kitchen_sink_inst_01.yaml')
SHEXLOG = env.expected_path('owl_log.txt')
OWL_OUTPUT = env.expected_path('kitchen_sink.owl.ttl')

SYMP = Namespace('http://purl.obolibrary.org/obo/SYMP_')
KS = Namespace('https://w3id.org/linkml/tests/kitchen_sink/')
LINKML = Namespace('https://w3id.org/linkml/')
BIZ = Namespace('https://example.org/bizcodes/')

class OwlGeneratorTestCase(unittest.TestCase):
    def test_owlgen(self):
        """ owl  """
        owl = OwlSchemaGenerator(SCHEMA,
                                 mergeimports=False,
                                 metaclasses=False,
                                 type_objects=False,
                                 ontology_uri_suffix='.owl.ttl').serialize(mergeimports=False)
        with open(OWL_OUTPUT, 'w') as stream:
            stream.write(owl)
        g = Graph()
        g.parse(OWL_OUTPUT, format="turtle")
        owl_classes = list(g.subjects(RDF.type, OWL.Class))
        for c in owl_classes:
            print(f'Class={c}')
        assert KS.MedicalEvent in owl_classes
        # test that enums are treated as classes
        assert KS.EmploymentEventType in owl_classes
        assert BIZ['001'] in owl_classes





if __name__ == '__main__':
    unittest.main()
