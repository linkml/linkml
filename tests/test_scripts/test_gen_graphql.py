import unittest

import click

from linkml.generators import graphqlgen

from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase


class GenGraphqlTestCase(ClickTestCase):
    testdir = "gengraphql"
    click_ep = graphqlgen.cli
    prog_name = "gen-graphql"
    env = env

    def test_help(self):
        self.do_test("--help", 'help')

    def test_meta(self):
        self.do_test([], 'meta.graphql')
        self.do_test('-f xsv', 'meta_error', expected_error=click.exceptions.BadParameter)


if __name__ == '__main__':
    unittest.main()
