import os
import unittest
import logging

from rdflib import URIRef, Graph
from rdflib.namespace import OWL, RDFS, RDF, SKOS
from rdflib import Namespace

from linkml.generators.yamlgen import YAMLGenerator
from tests.utils.compare_rdf import compare_rdf
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env

# Tests: https://github.com/linkml/linkml/issues/313
class Issue313TestCase(TestEnvironmentTestCase):
    env = env

    def test_roundtrip(self):
        name = 'linkml_issue_313'
        inpath = env.input_path(f'{name}.yaml')
        outpath = env.expected_path(f'{name}-roundtrip.yaml')
        gen = YAMLGenerator(inpath)
        gen.serialize(output=outpath)
        schema = gen.schema
        assert 'c1' in schema.classes
        c1 = schema.classes['c1']
        if c1.id_prefixes != ['c1val']:
            logging.error(f'Unexpected change in class {c1}.\n See  https://github.com/linkml/linkml/issues/313')
        e1 = schema.enums['e1']
        pv = list(e1.permissible_values.values())[0]
        assert pv.text == 'v1'
        assert pv.description == 'v1val'





if __name__ == '__main__':
    unittest.main()
