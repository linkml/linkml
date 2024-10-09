import unittest
from unittest import TestCase

import rdflib

from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.loaders import yaml_loader, rdflib_loader
from linkml_runtime.utils.schemaview import SchemaView

from tests.test_issues.environment import env
from tests.test_issues.models.linkml_issue_576 import Dataset

class Issue576TestCase(TestCase):
    """
    https://github.com/linkml/linkml/issues/576
    """
    env = env

    def test_issue_no_namespace(self):
        view = SchemaView(env.input_path('linkml_issue_576.yaml'))
        inst = yaml_loader.load(env.input_path('linkml_issue_576_data.yaml'), target_class=Dataset)
        s = rdflib_dumper.dumps(inst, view, 'turtle', prefix_map={"@base": "http://example.org/default/"})
        self.assertIn("@base <http://example.org/default/> .", s)
        g = rdflib.Graph().parse(data=s, format='turtle')
        for t in g.triples((None, None, None)):
            print(t)
        cases = [
            (None,
             rdflib.term.URIRef('https://w3id.org/linkml/personinfo/source'),
             rdflib.term.Literal('ex:source',
                                 datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#anyURI'))),
            (None,
             rdflib.term.URIRef('https://w3id.org/linkml/personinfo/pets'),
             rdflib.term.URIRef('https://example.org/PetA')),
            (rdflib.term.URIRef('http://example.org/default/org%201'),
             rdflib.term.URIRef('http://schema.org/name'),
             rdflib.term.Literal('Acme Inc. (US)')),
            (rdflib.term.URIRef('https://example.org/P1'),
             rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
             rdflib.term.URIRef('http://schema.org/Person')),
            (rdflib.term.URIRef('https://example.org/P1'),
             rdflib.term.URIRef('http://schema.org/name'),
            rdflib.term.Literal('John Doe')),
        ]
        for case in cases:
            s, p, o = case
            if s is None:
                self.assertIn(o, g.objects(s, p))
            else:
                self.assertIn(case, g)
        inst2 = rdflib_loader.load(g, target_class=Dataset, schemaview=view)
        #print(yaml_dumper.dumps(inst2))
        self.assertCountEqual(inst.persons, inst2.persons)
        self.assertCountEqual(inst.organizations, inst2.organizations)
        self.assertCountEqual(inst.pets, inst2.pets)


if __name__ == "__main__":
    unittest.main()
