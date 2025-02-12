import pytest
from click.testing import CliRunner

from linkml.validator.cli import cli


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.mark.parametrize(
    "data_file,valid",
    [
        ("data_valid.tsv", True),
        ("data_invalid.tsv", False),
    ],
)
def test_tsv_mixed_ints_strings(cli_runner, input_path, data_file, valid):
    """
    Tests that validator uses schema to coerce ints and strings in TSV data.

    See https://github.com/linkml/linkml/issues/2124
    """
    schema_path = input_path("issue_2124/schema.yaml")
    data_path = input_path(f"issue_2124/{data_file}.tsv")
    result = cli_runner.invoke(cli, ["-s", schema_path, data_path])
    if valid:
        assert result.exit_code == 0, "Expected to validate successfully"
    else:
        assert result.exit_code != 0, "Expected validation to fail"
