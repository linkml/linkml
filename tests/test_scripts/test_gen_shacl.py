import unittest

from linkml.generators import shaclgen
from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase


class GenShaclTestCase(ClickTestCase):
    testdir = "genshacl"
    click_ep = shaclgen.cli
    prog_name = "gen-shacl"
    env = env

    def test_help(self):
        self.do_test("--help", "help")


if __name__ == "__main__":
    unittest.main()
