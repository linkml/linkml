import sys
import unittest
import logging
import json
from rdflib import Graph, URIRef

from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.prefixmapgen import PrefixGenerator
from tests.test_prefixes.environment import env

SCHEMA = env.input_path('prefixtest.yaml')
OWL_OUTPUT = env.expected_path('prefixtest.owl.ttl')
RDF_OUTPUT = env.expected_path('prefixtest.rdf.nt')
PM_OUTPUT = env.expected_path('prefixtest.prefixmap.json')


class PrefixTestCase(unittest.TestCase):
    def test_owlgen(self):
        """ owl  """
        owl = OwlSchemaGenerator(SCHEMA, mergeimports=False, ontology_uri_suffix='.owl.ttl').serialize()
        with open(OWL_OUTPUT, 'w') as stream:
            stream.write(owl)
        g = Graph()
        g.parse(OWL_OUTPUT, format="turtle")
        self._check_triples(g,exceptions=[
            'http://schema.org/additionalName',
            'http://purl.obolibrary.org/obo/BFO_0000050',
            'http://schema.org/isPartOf'
        ])

    def test_rdfgen(self):
        # TODO: ttl output fails - check why
        # TODO: imports do not seem to work
        rdf = RDFGenerator(SCHEMA, mergeimports=True, format='nt').serialize()
        with open(RDF_OUTPUT, 'w') as stream:
            stream.write(rdf)
        g = Graph()
        g.parse(RDF_OUTPUT, format="nt")
        self._check_triples(g)

    def test_prefixmapgen(self):
        out = PrefixGenerator(SCHEMA, mergeimports=True).serialize()
        with open(PM_OUTPUT, 'w') as stream:
            stream.write(out)
        expected = {
            # TODO: rdf, rdfs, BFO, ... should all be here
            "CL": "http://purl.obolibrary.org/obo/CL_",
            "GO": "http://purl.obolibrary.org/obo/GO_",
            "SIO": "http://semanticscience.org/resource/SIO_",
            "biolink": "https://w3id.org/biolink/",
            "dbont": "http://dbpedia.org/ontology/",
            "dce": "http://purl.org/dc/elements/1.1/",
            "lego": "http://geneontology.org/lego/",
            "linkml": "https://w3id.org/linkml/",
            "owl": "http://www.w3.org/2002/07/owl#",
            "pav": "http://purl.org/pav/",
            "prefixtest": "https://w3id.org/linkml/tests/prefixtest/",
            "sdo": "http://schema.org/",
            "wd": "https://www.wikidata.org/wiki/"
        }
        with open(PM_OUTPUT) as stream:
            obj = json.load(stream)
        fails = 0
        for k, v in expected.items():
            if k in obj:
                if v != expected[k]:
                    logging.error(f'{k} = {v} expected {expected[k]}')
                    fails += 1
            else:
                logging.error(f'Missing key: {k}')
                fails += 1
        assert fails == 0

    def _check_triples(self, g, exceptions=[]):
        """
        currently testing is fairly weak: simply checks if the expected expanded URIs are
        present as objects
        """

        expected = [
            'http://purl.obolibrary.org/obo/PR_000000001',
            'http://purl.obolibrary.org/obo/SO_0000704',
            'http://semanticscience.org/resource/SIO_010035',
            'http://schema.org/additionalName',
            'http://purl.obolibrary.org/obo/BFO_0000050'
        ]
        for triple in g.triples((None,None,None)):
            #print(f'T= {triple}')
            (_,_,o) = triple
            if isinstance(o, URIRef):
                v = str(o)
                if v in expected:
                    expected.remove(v)
        for v in exceptions:
            if v in expected:
                logging.warning(f'TODO: figure why {v} not present')
                expected.remove(v)
        if len(expected) > 0:
            for e in expected:
                logging.error(f'Did not find {e}')
            assert False
        else:
            assert True




if __name__ == '__main__':
    unittest.main()
