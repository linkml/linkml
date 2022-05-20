import os
import unittest

from rdflib import URIRef, Graph, Literal
from rdflib.namespace import OWL, RDFS, RDF, XSD

from linkml import METAMODEL_CONTEXT_URI
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.yamlgen import YAMLGenerator
from tests.utils.compare_rdf import compare_rdf
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env

class IssueOWLNamespaceTestCase(TestEnvironmentTestCase):
    """
    Tests: https://github.com/linkml/linkml/issues/387

    Ensure attributes have correct names in OWL
    """
    env = env


    def test_name_mangling(self):
        infile = env.input_path('linkml_issue_387.yaml')
        outpath = env.expected_path('linkml_issue_387.owl')
        gen = OwlSchemaGenerator(infile,
                                 mergeimports=False,
                                 metaclasses=False,
                                 type_objects=False,
                                 importmap=env.import_map)
        self.env.generate_single_file(outpath,
                                      lambda: gen.serialize(mergeimports=False),
                                      value_is_returned=True,
                                      comparator=compare_rdf)
        g = Graph()
        g.parse(env.expected_path(outpath), format="turtle")
        def uri(s) -> URIRef:
            return URIRef(f'https://w3id.org/linkml/examples/test/{s}')
        C1 = uri('C1')
        a = uri('a')
        self.assertIn((C1, RDFS.label, Literal("C1")), g)
        self.assertIn((C1, RDF.type, OWL.Class), g)
        self.assertIn((a, RDFS.label, Literal("a")), g)
        self.assertIn((a, RDFS.range, XSD.string), g)
        self.assertIn((a, RDF.type, OWL.DatatypeProperty), g)
        assert len(list(g.objects(a, RDF.type))) == 1
        assert len(list(g.objects(C1, RDF.type))) == 1
        schema = gen.schema
        my_str = schema.types['my_str']
        self.assertEqual(my_str.uri, 'xsd:string')
        self.assertEqual(my_str.definition_uri, 'https://w3id.org/linkml/examples/test/MyStr')



if __name__ == '__main__':
    unittest.main()
