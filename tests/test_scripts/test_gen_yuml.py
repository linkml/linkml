import unittest

import click

from linkml.generators import yumlgen
from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase


class GenYUMLTestCase(ClickTestCase):
    testdir = "genyuml"
    click_ep = yumlgen.cli
    prog_name = "gen-yuml"
    env = env

    def test_help(self):
        self.do_test("--help", 'help')

    def test_meta(self):
        self.temp_file_path('meta.yuml')
        self.do_test([], 'meta.yuml')
        self.do_test('-f yuml', 'meta.yuml')
        self.do_test('-f xsv', 'meta_error', expected_error=click.exceptions.BadParameter)
        self.do_test('-c definition', 'definition.yuml')
        self.do_test('-c definition -c element', 'definition_element.yuml')
        self.do_test('-c noclass', 'definition.yuml', expected_error=ValueError)

        self.do_test(['-c', 'schema_definition'], 'meta', is_directory=True)
        self.do_test(['-c', 'definition'], 'meta1', is_directory=True)
        self.do_test(['-c', 'element'], 'meta2', is_directory=True)

        # Directory tests
        for fmt in yumlgen.YumlGenerator.valid_formats:
            if fmt != 'yuml':
                self.do_test(['-f', fmt, '-c', 'schema_definition'],
                             'meta_' + fmt, is_directory=True)


if __name__ == '__main__':
    unittest.main()
