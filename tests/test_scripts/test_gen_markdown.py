from click.testing import CliRunner

from linkml import LOCAL_METAMODEL_YAML_FILE
from linkml.generators.markdowngen import cli


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate markdown documentation of a LinkML model" in result.output


def test_metamodel(tmp_path):
    runner = CliRunner()
    result = runner.invoke(cli, ["-d", tmp_path, LOCAL_METAMODEL_YAML_FILE])
    assert result.exit_code == 0


def test_issue_2(tmp_path):
    runner = CliRunner()
    result = runner.invoke(cli, ["-d", tmp_path, "-c", "example", "-i", LOCAL_METAMODEL_YAML_FILE])
    assert result.exit_code == 0
    assert (tmp_path / "images/Example.svg").exists()


def test_no_types(tmp_path):
    """Test the no types directory setting"""
    runner = CliRunner()
    result = runner.invoke(
        cli, ["-d", tmp_path, "--notypesdir", "--warnonexist", "--log_level", "WARNING", LOCAL_METAMODEL_YAML_FILE]
    )
    assert result.exit_code == 0
