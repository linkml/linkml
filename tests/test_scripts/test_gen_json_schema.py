import unittest

import click
from linkml.generators import jsonschemagen

from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase


class GenJSONSchemaTestCase(ClickTestCase):
    testdir = "genjsonschema"
    click_ep = jsonschemagen.cli
    prog_name = "gen-json-schema"
    env = env

    def test_help(self):
        self.do_test("--help", 'help')

    def test_meta(self):
        self.do_test([], 'meta.json')
        self.do_test('-f json', 'meta.json')
        self.do_test('-f xsv', 'meta_error', expected_error=click.exceptions.BadParameter)
        self.do_test('-i', 'meta_inline.json')

    def test_tree_root(self):
        self.do_test([env.input_path('roottest.yaml')], 'rootttest.jsonld', add_yaml=False)

    def test_tree_root_args(self):
        self.do_test([env.input_path('roottest.yaml'), '-t', 'c2'], 'rootttest2.jsonld', add_yaml=False)

    def test_tree_root_closed(self):
        self.do_test([env.input_path('roottest.yaml'), '--closed'], 'rootttest3.jsonld', add_yaml=False)
    
    def test_tree_root_closed(self):
        self.do_test([env.input_path('roottest.yaml'), '--not-closed'], 'rootttest4.jsonld', add_yaml=False)
        
if __name__ == '__main__':
    unittest.main()
