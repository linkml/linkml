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

class IssueInheritMetaslotsTestCase(TestEnvironmentTestCase):
    """
    Tests: https://github.com/linkml/linkml/issues/270

    """
    env = env

    def test_metaslot_inheritance(self):
        name = 'linkml_issue_270'
        infile = env.input_path(f'{name}.yaml')
        gen = YAMLGenerator(infile)
        schema = gen.schema
        for sn, s in schema.slots.items():
            print(f'{sn} name={s.name} alias={s.alias} {s}')
        s = schema.slots['s1']
        c2_s1 = schema.slots['C2_s1']
        self.assertEqual(c2_s1.alias, s.name)
        self.assertEqual(c2_s1.owner, 'C2')

        for k in ['description', 'comments', 'todos', 'pattern', 'recommended', 'slot_uri']:
            self.assertEqual(getattr(s, k), getattr(c2_s1, k))
        print(gen.serialize())




if __name__ == '__main__':
    unittest.main()
