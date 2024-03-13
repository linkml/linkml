from click.testing import CliRunner

from linkml.generators.yamlgen import cli

from ..conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, "--help")
    assert "Validate input and produce fully resolved yaml equivalent" in result.output


def test_metamodel(snapshot):
    """Test emitting a YAML file"""
    runner = CliRunner()
    result = runner.invoke(cli, [KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == snapshot("genyaml/meta.yaml")


def test_validate_yaml(input_path, snapshot):
    """Test YAML file validation"""
    runner = CliRunner()
    result = runner.invoke(cli, [input_path("yaml_validate_clean.yaml"), "-v"])
    assert result.exit_code == 0
    assert result.output == snapshot("genyaml/clean.yaml")

    result = runner.invoke(cli, [input_path("yaml_validate_invalid.yaml"), "-v"], standalone_mode=False)
    assert result.exit_code != 0
    assert "slot: k - unrecognized range (none)" in str(result.exception)
