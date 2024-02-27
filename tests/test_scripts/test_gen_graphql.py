from click.testing import CliRunner

from linkml import LOCAL_METAMODEL_YAML_FILE
from linkml.generators import graphqlgen


def test_help():
    runner = CliRunner()
    result = runner.invoke(graphqlgen.cli, ["--help"])
    assert "Generate graphql representation of a LinkML model" in result.output


def test_metamodel_valid_call(snapshot):
    runner = CliRunner()
    result = runner.invoke(graphqlgen.cli, [LOCAL_METAMODEL_YAML_FILE])
    assert result.exit_code == 0
    assert result.output == snapshot("gengraphql/meta.graphql")


def test_metamodel_invalid_call():
    runner = CliRunner()
    result = runner.invoke(graphqlgen.cli, ["-f", "xsv", LOCAL_METAMODEL_YAML_FILE], standalone_mode=False)
    assert result.exit_code != 0
    assert "xsv" in str(result.exception)
