"""
tests generation of CSV summaries
"""

import pytest
from click.testing import CliRunner

from linkml import LOCAL_METAMODEL_YAML_FILE
from linkml.generators import csvgen


def test_help():
    runner = CliRunner()
    result = runner.invoke(csvgen.cli, ["--help"])
    assert "Generate CSV/TSV file from LinkML model" in result.output


@pytest.mark.parametrize(
    "arguments,snapshot_name",
    [
        ("", "meta.csv"),
        ("-f tsv", "meta.tsv"),
        ("-r schema_definition", "meta_schema_def.csv"),
        ("-r schema_definition -r slot_definition", "meta_schema_def_slot_def.csv"),
    ],
)
def test_metamodel_valid_calls(arguments, snapshot_name, snapshot):
    runner = CliRunner()
    result = runner.invoke(csvgen.cli, f"{arguments} {LOCAL_METAMODEL_YAML_FILE}")
    assert result.exit_code == 0
    assert result.output == snapshot(f"gencsv/{snapshot_name}")


@pytest.mark.parametrize("arguments,message", [("-f xsv", "xsv"), ("-r nada", "Unrecognized class: nada")])
def test_metamodel_invalid_calls(arguments, message):
    runner = CliRunner()
    result = runner.invoke(csvgen.cli, f"{arguments} {LOCAL_METAMODEL_YAML_FILE}", standalone_mode=False)
    assert result.exit_code != 0
    assert message in str(result.exception)
