import os
import unittest

from rdflib import URIRef, Graph
from rdflib.namespace import OWL, RDFS, RDF

from linkml.generators.owlgen import OwlSchemaGenerator
from tests.utils.compare_rdf import compare_rdf
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env


class IssueSymmetryInverseOWLTestCase(TestEnvironmentTestCase):
    env = env

    def _test_owl(self, name: str) -> Graph:
        self.env.generate_single_file(f'{name}.owl',
                                      lambda: OwlSchemaGenerator(env.input_path(f'{name}.yaml'),
                                                                 importmap=env.import_map).serialize(),
                                      value_is_returned=True, comparator=compare_rdf)
        g = Graph()
        g.parse(env.expected_path(f'{name}.owl'), format="turtle")
        return g

    def test_issue_owl(self):
        """ Make sure property characteristics are included """
        g = self._test_owl('issue_290')
        s = URIRef('http://example.org/s')
        t = URIRef('http://example.org/t')
        self.assertIn((s, RDF.type, OWL.SymmetricProperty), g)
        self.assertIn((s, OWL.inverseOf, t), g)




if __name__ == '__main__':
    unittest.main()
