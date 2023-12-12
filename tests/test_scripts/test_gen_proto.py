from click.testing import CliRunner

from linkml import LOCAL_METAMODEL_YAML_FILE
from linkml.generators.protogen import cli


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, "--help")
    assert "Generate proto representation of LinkML model" in result.output


def test_metamodel(snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, LOCAL_METAMODEL_YAML_FILE)
    assert result.exit_code == 0
    assert result.output == snapshot("genproto/meta.proto")
