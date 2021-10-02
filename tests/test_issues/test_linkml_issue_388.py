import os
import unittest

from rdflib import URIRef, Graph
from rdflib.namespace import OWL, RDFS, RDF

from linkml import METAMODEL_CONTEXT_URI
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.yamlgen import YAMLGenerator
from tests.utils.compare_rdf import compare_rdf
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env

class IssueOWLNamespaceTestCase(TestEnvironmentTestCase):
    """
    Tests: https://github.com/linkml/linkml/issues/388

    Note: this test is currently for exploration, it does not yet do tests beyond ensuring conversion
    generates no errors
    """
    env = env


    def test_attribute_behavior(self):
        name = 'linkml_issue_388'
        infile = env.input_path(f'{name}.yaml')
        self.env.generate_single_file(f'{name}.yaml',
                                      lambda: YAMLGenerator(env.input_path(f'{name}.yaml'),
                                                            importmap=env.import_map).serialize(),
                                      value_is_returned=True)
        self.env.generate_single_file(f'{name}.schema.json',
                                      lambda: JsonSchemaGenerator(env.input_path(f'{name}.yaml'),
                                                            importmap=env.import_map).serialize(),
                                      value_is_returned=True)

        self.env.generate_single_file(f'{name}.ttl',
                                      lambda: RDFGenerator(env.input_path(f'{name}.yaml'),

                                                               importmap=env.import_map).serialize(context=[METAMODEL_CONTEXT_URI],),
                                      value_is_returned=True)
        self.env.generate_single_file(f'{name}.owl',
                                      lambda: OwlSchemaGenerator(env.input_path(f'{name}.yaml'),
                                                                 metaclasses=False,
                                                                 ).serialize(context=[METAMODEL_CONTEXT_URI]),
                                      value_is_returned=True)
        g = Graph()
        g.parse(env.expected_path(f'{name}.owl'), format='turtle')
        C1 = URIRef('https://example.org/this/C1')
        this_a = URIRef('https://example.org/this/a')
        other_a = URIRef('https://example.org/other/a')
        # slot_uri refers to two attributes, ambiguous, so minimal metadata;
        assert len(list(g.triples((this_a, None, None)))) == 1
        self.assertIn((other_a, RDFS.range, C1), g)



if __name__ == '__main__':
    unittest.main()
