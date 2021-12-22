import os
import unittest

from linkml_runtime.loaders import rdflib_loader
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import URIRef, Graph, Literal
from rdflib.namespace import OWL, RDFS, RDF, XSD

from linkml import METAMODEL_CONTEXT_URI
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.yamlgen import YAMLGenerator
from linkml.validators import JsonSchemaDataValidator
from tests.utils.compare_rdf import compare_rdf
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env

class Issue532TestCase(TestEnvironmentTestCase):
    """
    Tests: https://github.com/linkml/linkml/issues/532

    """
    env = env


    def test_issue_532(self):

        schemafile = env.input_path('linkml_issue_532.yaml')
        sv = SchemaView(schemafile)
        datafile = env.input_path('linkml_issue_532_data.jsonld')
        python_module = PythonGenerator(schemafile).compile_module()
        target_class = python_module.__dict__['PhysicalSampleRecord']
        obj = rdflib_loader.load(datafile,
                                 fmt='json-ld',
                                 target_class=target_class,
                                 schemaview=sv)
        validator = JsonSchemaDataValidator(sv.schema)
        # throws an error if invalid
        validator.validate_object(obj)

        # test deliberately invalid data
        with self.assertRaises(Exception):
            bad_obj = rdflib_loader.load(env.input_path('linkml_issue_532_data_fail.jsonld'),
                                         fmt='json-ld',
                                         target_class=target_class,
                                         schemaview=sv)
            results = validator.validate_object(bad_obj)


if __name__ == '__main__':
    unittest.main()
