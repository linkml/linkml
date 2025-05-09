import pytest
from click.testing import CliRunner

from linkml.generators.markdowngen import cli

from ..conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate markdown documentation of a LinkML model" in result.output


def test_metamodel(tmp_path):
    runner = CliRunner()
    result = runner.invoke(cli, ["-d", tmp_path, KITCHEN_SINK_PATH])
    assert result.exit_code == 0


@pytest.mark.network
def test_issue_2(tmp_path):
    runner = CliRunner()
    result = runner.invoke(cli, ["-d", tmp_path, "-c", "Person", "-i", KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert (tmp_path / "images/Person.svg").exists()


def test_no_types(tmp_path):
    """Test the no types directory setting"""
    runner = CliRunner()
    result = runner.invoke(
        cli, ["-d", tmp_path, "--notypesdir", "--warnonexist", "--log_level", "WARNING", KITCHEN_SINK_PATH]
    )
    assert result.exit_code == 0
