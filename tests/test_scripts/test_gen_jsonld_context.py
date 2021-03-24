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

    def test_slot_class_uri(self):
        self.do_test(env.input_path('uri_tests.yaml'), 'uri_tests.jsonld', filtr=ldcontext_metadata_filter,
                     add_yaml=False)


if __name__ == '__main__':
    unittest.main()
