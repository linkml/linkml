import unittest
import click

from linkml.generators import protogen
from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase


class GenProtoTestCase(ClickTestCase):
    testdir = "genproto"
    click_ep = protogen.cli
    prog_name = "gen-proto"
    env = env

    def test_help(self):
        self.do_test("--help", 'help')

    def test_meta(self):
        self.do_test([], 'meta.proto')
        self.do_test('-f proto', 'meta.proto')
        self.do_test('-f xsv', 'meta_error', expected_error=click.exceptions.BadParameter)


if __name__ == '__main__':
    unittest.main()
