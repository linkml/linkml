import pytest
from click.testing import CliRunner

from linkml import LOCAL_METAMODEL_YAML_FILE
from linkml.generators.yumlgen import YumlGenerator, cli


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, "--help")
    assert "Generate a UML representation of a LinkML model" in result.output


@pytest.mark.parametrize(
    "arguments,snapshot_file",
    [
        ("", "meta.yuml"),
        ("-c definition", "definition.yuml"),
        ("-c definition -c element", "definition_element.yuml"),
    ],
)
def test_metamodel(arguments, snapshot_file, snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, f"{arguments} {LOCAL_METAMODEL_YAML_FILE}")
    assert result.exit_code == 0
    assert result.output == snapshot(f"genyuml/{snapshot_file}")


@pytest.mark.network
@pytest.mark.parametrize(
    "arguments,snapshot_dir",
    [
        ("-c schema_definition", "meta"),
        ("-c definition", "meta1"),
        ("-c element", "meta2"),
    ],
)
def test_metamodel_output_directory(arguments, snapshot_dir, snapshot, tmp_path):
    runner = CliRunner()
    result = runner.invoke(cli, f"{arguments} -d {tmp_path} {LOCAL_METAMODEL_YAML_FILE}")
    assert result.exit_code == 0
    assert tmp_path == snapshot(f"genyuml/{snapshot_dir}")


def test_invalid_classname():
    runner = CliRunner()
    result = runner.invoke(cli, f"-c noclass {LOCAL_METAMODEL_YAML_FILE}", standalone_mode=False)
    assert result.exit_code != 0
    assert "noclass" in str(result.exception)


@pytest.mark.parametrize("format", YumlGenerator.valid_formats)
def test_formats(format, tmp_path, snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, f"-f {format} -c schema_definition -d {tmp_path} {LOCAL_METAMODEL_YAML_FILE}")
    assert result.exit_code == 0
    assert tmp_path == snapshot(f"genyuml/meta_{format}")


def test_specified_diagram_name(tmp_path, snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, f"--diagram-name specified_name -d {tmp_path} {LOCAL_METAMODEL_YAML_FILE}")
    assert result.exit_code == 0
    assert tmp_path == snapshot("genyuml/specified_name_dir")
