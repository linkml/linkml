import unittest

# This has to occur post ClickTestCase
import click

from linkml.generators import dotgen
from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase


class GraphvizTestCase(ClickTestCase):
    testdir = "gengraphviz"
    click_ep = dotgen.cli
    prog_name = "gen-graphviz"
    env = env

    def test_help(self):
        self.do_test("--help", 'help')

    @unittest.skipIf(False, 'Determine whether we need graphviz before moving further')
    def test_meta(self):

        # 'ALL' may be useful, but it is very time consuming
        self.do_test(f'-o all', 'meta', is_directory=True)
        self.do_test(f'-f svg -o all', 'meta1', is_directory=True)
        self.do_test(f'-f xyz -o all', 'nada', is_directory=True,
                     expected_error=click.exceptions.BadParameter)
        self.do_test(f'-c definition', 'meta2', is_directory=True)
        self.do_test(["-c", "class_definition", "-c", "element"], 'meta3', is_directory=True)
        self.do_test(["-c", "nada"], "nada", is_directory=True, expected_error=ValueError)


if __name__ == '__main__':
    unittest.main()
