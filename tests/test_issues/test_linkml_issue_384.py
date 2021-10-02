import os
import unittest

from linkml_runtime.linkml_model import String
from rdflib import URIRef, Graph
from rdflib.namespace import OWL, RDFS, RDF, XSD

from linkml import METAMODEL_CONTEXT_URI
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.yamlgen import YAMLGenerator
from tests.utils.compare_rdf import compare_rdf
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env

TESTFILE = 'linkml_issue_384'

class IssueOWLNamespaceTestCase(TestEnvironmentTestCase):
    """
    Tests: https://github.com/linkml/linkml/issues/384
    """
    env = env



    def _test_other(self, name: str) -> None:
        infile = env.input_path(f'{name}.yaml')
        self.env.generate_single_file(f'{name}.yaml',
                                      lambda: YAMLGenerator(env.input_path(f'{name}.yaml'),
                                                            importmap=env.import_map).serialize(),
                                      value_is_returned=True)
        self.env.generate_single_file(f'{name}.context.jsonld',
                                      lambda: ContextGenerator(env.input_path(f'{name}.yaml'),
                                                               importmap=env.import_map).serialize(),
                                      value_is_returned=True)
        #print(f'Loading: {infile}')
        #rdfstr = RDFGenerator(infile, context=[METAMODEL_CONTEXT_URI]).serialize(context=[METAMODEL_CONTEXT_URI])
        #print(rdfstr)
        self.env.generate_single_file(f'{name}.ttl',
                                      lambda: RDFGenerator(infile,
                                                           importmap=env.import_map,
                                                           ).serialize(context=[METAMODEL_CONTEXT_URI]),
                                      value_is_returned=True, comparator=compare_rdf)
        self.env.generate_single_file(f'{name}.py',
                                      lambda: PythonGenerator(infile,
                                                              importmap=env.import_map,
                                                              ).serialize(),
                                      value_is_returned=True)

    def _test_owl(self, name: str, metaclasses=False, type_objects=False) -> Graph:
        infile = env.input_path(f'{name}.yaml')
        outpath = f'{name}-{metaclasses}-{type_objects}.owl'
        self.env.generate_single_file(outpath,
                                      lambda: OwlSchemaGenerator(infile,
                                                                 mergeimports=False,
                                                                 add_ols_annotations=True,
                                                                 metaclasses=metaclasses,
                                                                 type_objects=type_objects,
                                                                 importmap=env.import_map).serialize(mergeimports=False),
                                      value_is_returned=True,
                                      comparator=compare_rdf)
        g = Graph()
        g.parse(env.expected_path(outpath), format="turtle")
        return g

    def _contains_restriction(self, g: Graph, c: URIRef, prop: URIRef, pred: URIRef, filler: URIRef) -> bool:
        for r in g.objects(c, RDFS.subClassOf):
            if prop in g.objects(r, OWL.onProperty):
                if filler in g.objects(r, pred):
                    return True
        return False

    def test_issue_owl_properties(self):
        def uri(s) -> URIRef:
            return URIRef(f'https://w3id.org/linkml/examples/personinfo/{s}')
        for conf in [dict(metaclasses=False, type_objects=False),
                     dict(metaclasses=True, type_objects=True),
                     ]:
            g = self._test_owl(TESTFILE, **conf)
            Thing = uri('Thing')
            Person = uri('Person')
            Organization = uri('Organization')
            parent = uri('parent')
            age = uri('age')
            aliases = uri('aliases')
            full_name = uri('full_name')
            classes = [Thing, Person, Organization]
            props = [parent, age]
            # if type_objects=True then the range of slots that are types will be mapped to Object
            # representations of literals
            if conf['type_objects']:
                string_rep = URIRef(String.type_model_uri)
            else:
                string_rep = XSD.string
            for c in classes:
                self.assertIn((c, RDF.type, OWL.Class), g)
            for p in props:
                self.assertIn((p, RDF.type, OWL.ObjectProperty), g)
            assert self._contains_restriction(g, Person, parent, OWL.allValuesFrom, Person)
            assert self._contains_restriction(g, Organization, parent, OWL.allValuesFrom, Organization)
            assert self._contains_restriction(g, Person, aliases, OWL.allValuesFrom, string_rep)
            # TODO: also validate cardinality restrictions
            #assert self._contains_restriction(g, Thing, full_name, OWL.allValuesFrom, string_rep)

        #self.assertIn((A, RDF.type, OWL.Class), g)
        #NAME = URIRef('http://example.org/name')
        #self.assertIn((NAME, RDF.type, OWL.ObjectProperty), g)

    def test_other_formats(self):
        self._test_other(TESTFILE)

if __name__ == '__main__':
    unittest.main()
