import os
import unittest

from linkml_runtime import SchemaView
from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF, RDFS

from linkml import METAMODEL_CONTEXT_URI
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.yamlgen import YAMLGenerator
from tests.test_issues.environment import env
from tests.utils.compare_rdf import compare_rdf
from tests.utils.test_environment import TestEnvironmentTestCase


class IssueSlotInheritanceTestCase(TestEnvironmentTestCase):
    """
    Tests: https://github.com/linkml/linkml/issues/774

    Ensures that mappings and
    """

    env = env

    def test_slot_inheritance(self):
        name = "linkml_issue_774"
        infile = env.input_path(f"{name}.yaml")
        sv = SchemaView(infile)
        slot = sv.induced_slot("s", "C")
        self.assertEqual(["ex:1"], slot.exact_mappings)
        any_of_ranges = [x.range for x in slot.any_of]
        self.assertCountEqual(["D", "E"], any_of_ranges)
        induced_c = sv.induced_class("C")
        # slots converted to attributes for derived view:
        # this allows local properties to be inlined
        self.assertEqual([], induced_c.slots)
        self.assertEqual(["s"], list(induced_c.attributes.keys()))
        slot = induced_c.attributes["s"]
        self.assertEqual(["ex:1"], slot.exact_mappings)
        any_of_ranges = [x.range for x in slot.any_of]
        self.assertCountEqual(["D", "E"], any_of_ranges)


if __name__ == "__main__":
    unittest.main()
