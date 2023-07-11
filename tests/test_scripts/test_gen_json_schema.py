import unittest

import click
from click.testing import CliRunner

from linkml.generators import jsonschemagen
from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase


class GenJSONSchemaTestCase(ClickTestCase):
    testdir = "genjsonschema"
    click_ep = jsonschemagen.cli
    prog_name = "gen-json-schema"
    env = env

    def test_help(self):
        self.do_test("--help", "help")

    def test_meta(self):
        self.do_test([], "meta.json")
        self.do_test("-f json", "meta.json")
        self.do_test("-f xsv", "meta_error", expected_error=click.exceptions.BadParameter)
        self.do_test("-i", "meta_inline.json")

    def test_tree_root(self):
        self.do_test([env.input_path("roottest.yaml")], "rootttest.jsonld", add_yaml=False)

    def test_tree_root_args(self):
        self.do_test(
            [env.input_path("roottest.yaml"), "-t", "c2"],
            "rootttest2.jsonld",
            add_yaml=False,
        )

    def test_tree_root_closed(self):
        self.do_test(
            [env.input_path("roottest.yaml"), "--closed"],
            "rootttest3.jsonld",
            add_yaml=False,
        )

    def test_tree_root_not_closed(self):
        self.do_test(
            [env.input_path("roottest.yaml"), "--not-closed"],
            "rootttest4.jsonld",
            add_yaml=False,
        )

    def test_indent_option(self):
        runner = CliRunner()

        # the default is to pretty-print with new lines + 4 spaces
        result = runner.invoke(self.click_ep, [env.input_path("roottest.yaml")])
        self.assertRegex(result.output, r'^{\n    "\$defs"')

        # test custom indent level with 2 spaces
        result = runner.invoke(self.click_ep, ["--indent", 2, env.input_path("roottest.yaml")])
        self.assertRegex(result.output, r'^{\n  "\$defs"')

        # test no newlines or spaces when indent = 0
        result = runner.invoke(self.click_ep, ["--indent", 0, env.input_path("roottest.yaml")])
        self.assertRegex(result.output, r'^{"\$defs"')


if __name__ == "__main__":
    unittest.main()
