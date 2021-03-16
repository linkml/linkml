import unittest
import click

from linkml.generators import csvgen
from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase


class GenCSVTestCase(ClickTestCase):
    testdir = "gencsv"
    click_ep = csvgen.cli
    prog_name = "gen-csv"
    env = env

    def test_help(self):
        self.do_test("--help", 'help')

    def test_meta(self):
        self.do_test([], 'meta.csv')
        self.do_test('-f tsv', 'meta.tsv')
        self.do_test('-f xsv', 'meta_error', expected_error=click.exceptions.BadParameter)
        self.do_test(["-r", "schema_definition"], 'meta_sd')
        self.do_test(["-r", "schema_definition", "-r", "slot_definition"], 'meta_sd_sd')
        self.do_test(["-r", "nada"], 'meta_sd', expected_error=ValueError)


if __name__ == '__main__':
    unittest.main()
