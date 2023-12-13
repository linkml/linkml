from click.testing import CliRunner

from linkml import LOCAL_METAMODEL_YAML_FILE
from linkml.generators import golrgen


def test_help():
    runner = CliRunner()
    result = runner.invoke(golrgen.cli, ["--help"])
    assert "Generate GOLR representation of a LinkML model" in result.output


def test_metamodel_valid_call(tmp_path, snapshot):
    runner = CliRunner()
    result = runner.invoke(golrgen.cli, ["-d", tmp_path, LOCAL_METAMODEL_YAML_FILE])
    assert result.exit_code == 0
    assert tmp_path == snapshot("gengolr/meta")


def test_metamodel_invalid_call(tmp_path):
    runner = CliRunner()
    result = runner.invoke(golrgen.cli, ["-f", "xsv", "-d", tmp_path, LOCAL_METAMODEL_YAML_FILE], standalone_mode=False)
    assert result.exit_code != 0
    assert "xsv" in str(result.exception)
