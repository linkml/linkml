"""
tests generation of CSV summaries
"""

import pytest
from click.testing import CliRunner

from linkml.generators import csvgen

from ..conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(csvgen.cli, ["--help"])
    assert "Generate CSV/TSV file from LinkML model" in result.output


@pytest.mark.parametrize(
    "arguments,snapshot_name",
    [
        ([], "meta.csv"),
        (["-f", "tsv"], "meta.tsv"),
        (["-r", "Person"], "meta_schema_def.csv"),
        (["-r", "Person", "-r", "Event"], "meta_schema_def_slot_def.csv"),
    ],
)
def test_metamodel_valid_calls(arguments, snapshot_name, snapshot):
    runner = CliRunner()
    result = runner.invoke(csvgen.cli, arguments + [KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == snapshot(f"gencsv/{snapshot_name}")


@pytest.mark.parametrize("arguments,message", [(["-f", "xsv"], "xsv"), (["-r", "nada"], "Unrecognized class: nada")])
def test_metamodel_invalid_calls(arguments, message):
    runner = CliRunner()
    result = runner.invoke(csvgen.cli, arguments + [KITCHEN_SINK_PATH], standalone_mode=False)
    assert result.exit_code != 0
    assert message in str(result.exception)
