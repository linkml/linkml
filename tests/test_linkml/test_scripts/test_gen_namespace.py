import re

from click.testing import CliRunner

from linkml.generators.namespacegen import cli

from ..conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate a namespace manager for all of the prefixes represented in a LinkML model" in re.sub(
        r"\s+", " ", result.output
    )


def test_metamodel(snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, [KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == snapshot("gennamespace/meta_namespaces.py")
