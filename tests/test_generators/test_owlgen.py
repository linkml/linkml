import sys
import unittest
from rdflib import Graph

from linkml.generators.owlgen import OwlSchemaGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path('kitchen_sink.yaml')
DATA = env.input_path('kitchen_sink_inst_01.yaml')
SHEXLOG = env.expected_path('owl_log.txt')
OWL_OUTPUT = env.expected_path('kitchen_sink.owl.ttl')


class OwlGeneratorTestCase(unittest.TestCase):
    def test_owlgen(self):
        """ owl  """
        owl = OwlSchemaGenerator(SCHEMA, mergeimports=False, ontology_uri_suffix='.owl.ttl').serialize()
        with open(OWL_OUTPUT, 'w') as stream:
            stream.write(owl)
        g = Graph()
        g.parse(OWL_OUTPUT, format="turtle")





if __name__ == '__main__':
    unittest.main()
