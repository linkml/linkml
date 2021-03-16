import os
import unittest

import click
from linkml import METAMODEL_NAMESPACE
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators import shexgen
from pyshex import ShExEvaluator
from rdflib import Graph
from tests import SKIP_SHEX_VALIDATION, SKIP_SHEX_VALIDATION_REASON
from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase
from tests.utils.dirutils import make_and_clear_directory


class GenShExTestCase(ClickTestCase):
    testdir = "genshex"
    click_ep = shexgen.cli
    prog_name = "gen-shex"
    env = env

    def test_help(self):
        self.do_test("--help", 'help')

    def test_meta(self):
        """ Generate various forms of the metamodel in ShEx """
        self.maxDiff = None
        self.do_test([], 'metashex.shex')
        self.do_test('-f json', 'metashex.json')
        self.do_test('-f rdf', 'metashex.ttl')
        self.do_test('-f shex', 'metashex.shex')
        self.do_test('--metauris', 'metashexn.shex')
        self.do_test('-f json', 'metashex.json')
        self.do_test('-f rdf', 'metashex.ttl')
        self.do_test('-f shex', 'metashex.shex')
        self.do_test(env.meta_yaml + f' -f xsv', 'meta_error', expected_error=click.exceptions.BadParameter)

    def test_rdf_shex(self):
        """ Generate ShEx and RDF for the model and verify that the RDF represents a valid instance """
        test_dir = self.temp_file_path('meta_conformance_test', is_dir=True)

        json_file = os.path.join(test_dir, 'meta.jsonld')
        json_str = JSONLDGenerator(env.meta_yaml, importmap=env.import_map).serialize()
        with open(json_file, 'w') as f:
            f.write(json_str)

        context_file = os.path.join(test_dir, 'metacontext.jsonld')
        ContextGenerator(env.meta_yaml, importmap=env.import_map).serialize(output=context_file)
        self.assertTrue(os.path.exists(context_file))

        rdf_file = os.path.join(test_dir, 'meta.ttl')
        RDFGenerator(env.meta_yaml, importmap=env.import_map).serialize(output=rdf_file, context=context_file)
        self.assertTrue(os.path.exists(rdf_file))

        shex_file = os.path.join(test_dir, 'meta.shex')
        shexgen.ShExGenerator(env.meta_yaml, importmap=env.import_map).serialize(output=shex_file, collections=False)
        self.assertTrue(os.path.exists(shex_file))

        if SKIP_SHEX_VALIDATION:
            print(f"tests/test_scripts/test_gen_shex.py: {SKIP_SHEX_VALIDATION_REASON}")
        else:
            g = Graph()
            g.load(rdf_file, format='ttl')
            focus = METAMODEL_NAMESPACE.metamodel
            start = METAMODEL_NAMESPACE.SchemaDefinition
            results = ShExEvaluator(g, shex_file, focus, start).evaluate(debug=False)
            success = all(r.result for r in results)
            if not success:
                for r in results:
                    if not r.result:
                        print(r.reason)
            else:
                make_and_clear_directory(test_dir)
            self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()
