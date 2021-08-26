import os
import unittest

from rdflib import URIRef, Graph
from rdflib.namespace import OWL, RDFS, RDF

from linkml.generators.owlgen import OwlSchemaGenerator
from tests.utils.compare_rdf import compare_rdf
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env

# Tests: https://github.com/biolink/biolinkml/issues/163
class IssueOWLNamespaceTestCase(TestEnvironmentTestCase):
    env = env

    def _test_owl(self, name: str) -> Graph:
        self.env.generate_single_file(f'{name}.owl',
                                      lambda: OwlSchemaGenerator(env.input_path(f'{name}.yaml'),
                                                                 importmap=env.import_map).serialize(),
                                      value_is_returned=True, comparator=compare_rdf)
        g = Graph()
        g.parse(env.expected_path(f'{name}.owl'), format="turtle")
        return g

    def test_issue_owl_namespace(self):
        """ Make sure that types are generated as part of the output """
        g = self._test_owl('issue_163')
        A = URIRef('http://example.org/A')
        self.assertIn((A, RDF.type, OWL.Class), g)
        NAME = URIRef('http://example.org/name')
        self.assertIn((NAME, RDF.type, OWL.ObjectProperty), g)

    def test_issue_no_default(self):
        """ Make sure that types are generated as part of the output """
        g = self._test_owl('issue_163b')
        A = URIRef('http://example.org/sample/example1/A')
        self.assertIn((A, RDF.type, OWL.Class), g)
        NAME = URIRef('http://example.org/sample/example1/name')
        self.assertIn((NAME, RDF.type, OWL.ObjectProperty), g)

    def test_aliases(self):
        """ Make sure aliases work """
        g = self._test_owl('issue_163c')


if __name__ == '__main__':
    unittest.main()
