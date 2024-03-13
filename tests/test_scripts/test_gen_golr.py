from click.testing import CliRunner

from linkml.generators import golrgen

from ..conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(golrgen.cli, ["--help"])
    assert "Generate GOLR representation of a LinkML model" in result.output


def test_metamodel_valid_call(tmp_path, snapshot):
    runner = CliRunner()
    result = runner.invoke(golrgen.cli, ["-d", tmp_path, KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert tmp_path == snapshot("gengolr/meta")


def test_metamodel_invalid_call(tmp_path):
    runner = CliRunner()
    result = runner.invoke(golrgen.cli, ["-f", "xsv", "-d", tmp_path, KITCHEN_SINK_PATH], standalone_mode=False)
    assert result.exit_code != 0
    assert "xsv" in str(result.exception)
