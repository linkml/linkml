import unittest
import click

from linkml.generators import jsonldcontextgen
from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase
from tests.utils.filters import ldcontext_metadata_filter


class GenContextTestCase(ClickTestCase):
    testdir = "gencontext"
    click_ep = jsonldcontextgen.cli
    prog_name = "gen-jsonld-context"
    env = env

    def test_help(self):
        self.do_test("--help", 'help')

    def test_meta(self):
        self.maxDiff = None
        self.do_test([], 'meta.context.jsonld', filtr=ldcontext_metadata_filter)
        self.do_test('--metauris', 'meta_contextn.jsonld', filtr=ldcontext_metadata_filter)
        self.do_test('-f xsv', 'meta_error', expected_error=click.exceptions.BadParameter)
        self.do_test('--niggles', 'meta2_error', expected_error=click.exceptions.NoSuchOption)

    def test_prefix_options(self):
        """ Test various prefix emission options"""
        # prefixes only, no-merge
        self.do_test([self.env.input_path('simple_uri_test.yaml'), '--no-metadata', '--no-mergeimports', '--no-model'],
                     'simple_uri_test.no_merge.prefixes_only.context.jsonld', add_yaml=False)
        # flat prefixes only, no-merge
        self.do_test([self.env.input_path('simple_uri_test.yaml'), '--no-metadata', '--no-mergeimports', '--no-model', '--flatprefixes'],
                     'simple_uri_test.no_merge.flatprefixes_only.context.jsonld', add_yaml=False)
        # model only, no-merge
        self.do_test([self.env.input_path('simple_uri_test.yaml'), '--no-metadata', '--no-mergeimports', '--no-prefixes'],
                     'simple_uri_test.no_merge.model_only.context.jsonld', add_yaml=False)
        # both, no-merge
        self.do_test([self.env.input_path('simple_uri_test.yaml'), '--no-metadata', '--no-mergeimports', '--model', '--prefixes'],
                     'simple_uri_test.no_merge.context.jsonld', add_yaml=False)
        # prefixes only, merge
        self.do_test([self.env.input_path('simple_uri_test.yaml'), '--no-metadata', '--mergeimports', '--no-model'],
                     'simple_uri_test.merge.prefixes_only.context.jsonld', add_yaml=False)
        # flat prefixes only, merge
        self.do_test([self.env.input_path('simple_uri_test.yaml'), '--no-metadata', '--mergeimports', '--no-model', '--flatprefixes'],
                     'simple_uri_test.merge.flatprefixes_only.context.jsonld', add_yaml=False)
        # model only, merge
        self.do_test([self.env.input_path('simple_uri_test.yaml'), '--no-metadata', '--mergeimports', '--no-prefixes'],
                     'simple_uri_test.merge.model_only.context.jsonld', add_yaml=False)
        # both, merge
        self.do_test([self.env.input_path('simple_uri_test.yaml'), '--no-metadata', '--mergeimports', '--model', '--prefixes'],
                     'simple_uri_test.merge.context.jsonld', add_yaml=False)


    def test_slot_class_uri(self):
        # Note: two warnings are expected below:
        #   WARNING:ContextGenerator:No namespace defined for URI: http://example.org/slot/su
        #   WARNING:ContextGenerator:No namespace defined for URI: http://example.org/class/cu
        self.do_test(env.input_path('uri_tests.yaml'), 'uri_tests.jsonld', filtr=ldcontext_metadata_filter,
                     add_yaml=False)


if __name__ == '__main__':
    unittest.main()
