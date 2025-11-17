import re

import pytest
from click.testing import CliRunner

from linkml.generators.jsonschemagen import cli

from ..conftest import KITCHEN_SINK_PATH

pytestmark = pytest.mark.jsonschemagen


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate JSON Schema representation of a LinkML model" in result.output


@pytest.mark.parametrize(
    "arguments,snapshot_file",
    [
        ([], "meta.json"),
        (["-f", "json"], "meta.json"),
        (["-i"], "meta_inline.json"),
    ],
)
def test_metamodel_valid_calls(arguments, snapshot_file, snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, arguments + [KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == snapshot(f"genjsonschema/{snapshot_file}")


@pytest.mark.parametrize(
    "arguments,snapshot_file",
    [
        ([], "roottest.json"),
        (["-t", "c2"], "roottest2.json"),
        (["--closed"], "roottest3.json"),
        (["--not-closed"], "roottest4.json"),
    ],
)
def test_tree_root(arguments, snapshot_file, input_path, snapshot):
    schema = input_path("roottest.yaml")
    runner = CliRunner()
    result = runner.invoke(cli, arguments + [str(schema)])
    assert result.exit_code == 0
    assert result.output == snapshot(f"genjsonschema/{snapshot_file}")


def test_indent_option(input_path):
    schema = str(input_path("roottest.yaml"))
    runner = CliRunner()

    # the default is to pretty-print with new lines + 4 spaces
    result = runner.invoke(cli, [schema])
    assert re.search(r'^{\n {4}"\$defs"', result.output)

    # test custom indent level with 2 spaces
    result = runner.invoke(cli, ["--indent", 2, schema])
    assert re.search(r'^{\n {2}"\$defs"', result.output)

    # test no newlines or spaces when indent = 0
    result = runner.invoke(cli, ["--indent", 0, schema])
    assert re.search(r'^{"\$defs"', result.output)


def test_include_option(input_path):
    schema = str(input_path("roottest.yaml"))
    runner = CliRunner()
    extra_import_path = str(input_path("deprecation.yaml"))
    result = runner.invoke(cli, ["--include", extra_import_path, schema])
    assert "C4" in result.output
