import os
import unittest

from rdflib import URIRef, Graph
from rdflib.namespace import OWL, RDFS, RDF, SKOS
from rdflib import Namespace

from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.rdfgen import JSONLDGenerator
from tests.utils.compare_rdf import compare_rdf
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env

BIOLINK = Namespace('https://w3id.org/biolink/vocab/')

# as reported in https://github.com/linkml/linkml/issues/163,
# rdfgenerator can create unparseable files if ttl is used.
# TODO: make this test work when format = 'ttl'
RDF_FORMAT = 'ttl'

# Tests: https://github.com/linkml/linkml/issues/163
class IssueRDFNamespaceTestCase(TestEnvironmentTestCase):
    env = env

    def _test_rdf(self, name: str) -> Graph:
        path = f'{name}.{RDF_FORMAT}'
        self.env.generate_single_file(path,
                                      lambda: RDFGenerator(env.input_path(f'{name}.yaml'), format=RDF_FORMAT).serialize(),
                                      value_is_returned=True, comparator=compare_rdf)
        g = Graph()
        g.parse(env.expected_path(path), format=RDF_FORMAT)
        return g

    def test_roundtrip(self):
        name = 'linkml_issue_163'
        inpath = env.input_path(f'{name}.yaml')
        outpath = env.expected_path(f'{name}-gen.{RDF_FORMAT}')
        gen = RDFGenerator(inpath, format=RDF_FORMAT)
        gen.serialize(output=outpath)
        g = Graph()
        g.parse(outpath, format=RDF_FORMAT)

    def test_namespace(self):
        name = 'linkml_issue_163'
        inpath = env.input_path(f'{name}.yaml')
        outpath = env.expected_path(f'{name}-gen.jsonld')
        gen = JSONLDGenerator(inpath, metadata=True, importmap={})
        jsonld_str = gen.serialize()
        with open(outpath, 'w') as stream:
            stream.write(jsonld_str)
        nsl = gen.namespaces
        for k, v in nsl.items():
            print(f'{k}: "{v}"')
        # namespaces directly declared
        assert nsl['RO'] == "http://purl.obolibrary.org/obo/RO_"
        assert nsl['biolink'] == "https://w3id.org/biolink/vocab/"
        assert nsl['linkml'] == "https://w3id.org/linkml/"
        assert nsl['SIO'] == "http://semanticscience.org/resource/SIO_"
        assert nsl['prov'] == "http://www.w3.org/ns/prov#"

        # from OBO context
        assert nsl['SO'] == "http://purl.obolibrary.org/obo/SO_"

        # from semweb
        assert nsl['rdf'] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        assert nsl['owl'] == "http://www.w3.org/2002/07/owl#"

        im = gen.importmap
        print(im)

        em = gen.emit_metadata
        print(em)

        graph = Graph()
        graph.parse(data=jsonld_str, format="json-ld", base=str(gen.namespaces._base), prefix=True)

        with open(env.expected_path(f'{name}-via-jsonld.ttl'), 'w') as outf:
            outf.write(graph.serialize(format='turtle').decode())


    def test_issue_mappings_namespace(self):
        """ Make sure that types are generated as part of the output """
        g = self._test_rdf('linkml_issue_163')
        HAS_EVIDENCE = BIOLINK.has_evidence
        SNV = BIOLINK.Snv
        NAME = BIOLINK.name
        self.assertIn((HAS_EVIDENCE, SKOS.exactMatch, URIRef('http://purl.obolibrary.org/obo/RO_0002558')), g)
        self.assertIn((SNV, SKOS.exactMatch, URIRef('http://example.org/UNKNOWN/UNKNOWN_PREFIX/1234567')), g)
        #for s,p,o in g.triples((None,None,None)):
        #    print(f'{s} {p} {o}')
        self.assertIn((SNV, SKOS.exactMatch, URIRef('http://purl.obolibrary.org/obo/SO_0001483')), g)
        self.assertIn((NAME, SKOS.narrowMatch, URIRef('http://purl.org/dc/terms/title')), g)




if __name__ == '__main__':
    unittest.main()
