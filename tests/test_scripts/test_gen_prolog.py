import unittest

from linkml.generators import lpgen
from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase

class GenPrologTestCase(ClickTestCase):
    testdir = "genprolog"
    click_ep = lpgen.cli
    prog_name = "gen-prolog"
    env = env

    def test_help(self):
        self.do_test("--help", 'help')

    def test_meta(self):
        self.do_test([], 'meta.lp')

if __name__ == '__main__':
    unittest.main()
