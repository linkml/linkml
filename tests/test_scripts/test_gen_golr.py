import unittest

import click

from linkml.generators import golrgen
from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase


class GolrViewTestCase(ClickTestCase):
    testdir = "gengolr"
    click_ep = golrgen.cli
    prog_name = "gen-golr-views"
    env = env

    def test_help(self):
        self.do_test("--help", 'help')

    def test_meta(self):
        self.do_test([], 'meta', is_directory=True)
        self.do_test(f'-f xsv', 'error', is_directory=True, expected_error=click.exceptions.BadParameter)


if __name__ == '__main__':
    unittest.main()
