import unittest

import rdflib

from linkml.generators.shaclgen import ShaclGenerator
from tests.test_generators.environment import env


SCHEMA = env.input_path("kitchen_sink.yaml")
DATA = env.input_path("kitchen_sink_inst_01.yaml")
LOG = env.expected_path("ShaclGen_log.txt")
OUT = env.expected_path("kitchen_sink.shacl.ttl")


EXPECTED = [
    (rdflib.term.URIRef('https://w3id.org/linkml/tests/kitchen_sink/Person'),
     rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
     rdflib.term.URIRef('http://www.w3.org/ns/shacl#NodeShape')),
    (rdflib.term.URIRef('https://w3id.org/linkml/tests/kitchen_sink/Person'),
     rdflib.term.URIRef('http://www.w3.org/ns/shacl#closed'),
     rdflib.term.Literal('false', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#boolean')))
]

class ShaclTestCase(unittest.TestCase):
    def test_shacl(self):
        """tests shacl generation"""
        shaclstr = ShaclGenerator(SCHEMA, mergeimports=True).serialize()
        with open(OUT, "w") as stream:
            stream.write(shaclstr)
        g = rdflib.Graph()
        g.parse(OUT)
        triples = list(g.triples((None, None, None)))
        for et in EXPECTED:
            self.assertIn(et, triples)
        # TODO: test shacl validation; pyshacl requires rdflib6


if __name__ == "__main__":
    unittest.main()
