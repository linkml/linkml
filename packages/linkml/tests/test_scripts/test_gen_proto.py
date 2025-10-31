from click.testing import CliRunner

from linkml.generators.protogen import cli

from ..conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate proto representation of LinkML model" in result.output


def test_metamodel(snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, [KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == snapshot("genproto/meta.proto")
