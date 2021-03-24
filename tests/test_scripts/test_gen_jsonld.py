import os
import re
import unittest
# This has to occur post ClickTestCase
from functools import reduce
from typing import List, Tuple

import click
from rdflib import Graph, URIRef

from linkml import METAMODEL_NAMESPACE
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators import jsonldgen

from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase

cwd = os.path.dirname(__file__)
meta_context = 'file:./output/gencontext/meta.jsonld'

repl: List[Tuple[str, str]] = [
    (r'"source_file_size": [0-9]+', ''),
    (r'"source_file_date": "[^"]+"', ''),
    (r'"generation_date": "[^"]+"', ''),
    (r'"source_file": "[^"]+"', '')
]


def filtr(txt: str) -> str:
    return reduce(lambda s, expr: re.sub(expr[0], expr[1], s), repl, txt)


class GenJSONLDTestCase(ClickTestCase):
    testdir = "genjsonld"
    click_ep = jsonldgen.cli
    prog_name = "gen-jsonld"
    env = env

    def test_help(self):
        self.do_test("--help", 'help')

    def test_meta(self):
        self.temp_file_path('meta.jsonld')
        self.do_test(f"--context {meta_context}", 'meta.jsonld', filtr=filtr)
        self.do_test(f'-f jsonld --context {meta_context}', 'meta.jsonld', filtr=filtr)
        self.do_test(f'-f xsv --context {meta_context}', 'meta_error',
                     expected_error=click.exceptions.BadParameter)

    def check_size(self, g: Graph, g2: Graph, root: URIRef, expected_classes: int, expected_slots: int,
                   expected_types: int, expected_subsets: int, expected_enums: int, model: str) -> None:
        """
        Check
        :param g:
        :param g2:
        :param root:
        :param expected_classes:
        :param expected_slots:
        :param expected_types:
        :param expected_subsets:
        :param expected_enums:
        :param model:
        :return:
        """
        for graph in [g, g2]:
            n_classes = len(list(graph.objects(root, METAMODEL_NAMESPACE.classes)))
            n_slots = len(list(graph.objects(root, METAMODEL_NAMESPACE.slots)))
            n_types = len(list(graph.objects(root, METAMODEL_NAMESPACE.types)))
            n_subsets = len(list(graph.objects(root, METAMODEL_NAMESPACE.subsets)))
            n_enums = len(list(graph.objects(root, METAMODEL_NAMESPACE.enums)))
            self.assertEqual(expected_classes, n_classes, f"Expected {expected_classes} classes in {model}")
            self.assertEqual(expected_slots, n_slots, f"Expected {expected_slots} slots in {model}")
            self.assertEqual(expected_types, n_types, f"Expected {expected_types} types in {model}")
            self.assertEqual(expected_subsets, n_subsets, f"Expected {expected_subsets} subsets in {model}")
            self.assertEqual(expected_enums, n_enums, f"Expected {expected_enums} enums in {model}")

    def test_meta_output(self):
        """ Generate a context AND a jsonld for the metamodel and make sure it parses as RDF """
        tmp_jsonld_path = self.temp_file_path('metajson.jsonld')
        tmp_rdf_path = self.temp_file_path('metardf.ttl')
        tmp_meta_context_path = self.temp_file_path('metacontext.jsonld')

        # Generate an image of the metamodel
        gen = ContextGenerator(env.meta_yaml, importmap=env.import_map)
        base = gen.namespaces[gen.schema.default_prefix]
        if str(base)[-1] not in '/#':
            base += '/'
        schema = base + "meta"

        # Generate context
        with open(tmp_meta_context_path, 'w') as tfile:
            tfile.write(gen.serialize())

        # Generate JSON
        with open(tmp_jsonld_path, 'w') as tfile:
            tfile.write(jsonldgen.JSONLDGenerator(env.meta_yaml, fmt=jsonldgen.JSONLDGenerator.valid_formats[0],
                                                  importmap=env.import_map).serialize(context=tmp_meta_context_path))

        # Convert JSON to TTL
        g = Graph()
        g.load(tmp_jsonld_path, format="json-ld")
        g.serialize(tmp_rdf_path, format="ttl")
        g.bind('meta', METAMODEL_NAMESPACE)
        new_ttl = g.serialize(format="turtle").decode()

        # Make sure that the generated TTL matches the JSON-LD (probably not really needed, as this is more of a test
        # of rdflib than our tooling but it doesn't hurt
        new_g = Graph()
        new_g.parse(data=new_ttl, format="turtle")

        # Make sure that both match the expected size (classes, slots, types, and model name for error reporting)
        self.check_size(g, new_g, URIRef(schema), 17, 122, 14, 1, 1, "meta")


if __name__ == '__main__':
    unittest.main()
