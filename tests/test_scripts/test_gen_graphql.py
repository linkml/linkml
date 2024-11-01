from click.testing import CliRunner

from linkml.generators import graphqlgen

from ..conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(graphqlgen.cli, ["--help"])
    assert "Generate graphql representation of a LinkML model" in result.output


def test_metamodel_valid_call_1(snapshot):
    runner = CliRunner()
    result = runner.invoke(graphqlgen.cli, [KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == snapshot("gengraphql/meta.graphql")


def test_metamodel_valid_call_2():
    runner = CliRunner()
    result = runner.invoke(graphqlgen.cli, ["--strict-naming", KITCHEN_SINK_PATH], catch_exceptions=True)
    assert result.exit_code != 0
    assert result.output == ""
    assert isinstance(result.exception, ValueError)


def test_metamodel_invalid_call():
    runner = CliRunner()
    result = runner.invoke(graphqlgen.cli, ["-f", "xsv", KITCHEN_SINK_PATH], standalone_mode=False)
    assert result.exit_code != 0
    assert "xsv" in str(result.exception)
