from pathlib import Path

import pytest
from click.testing import CliRunner

from linkml.validator.cli import cli

TEST_INPUTS_DIR = Path(__file__).parent / "input" / "issue_1446"


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.mark.parametrize(
    "target_class,schema,data,valid",
    [
        ("DummyHuman", "dummy", "person", True),
        ("DummyHuman", "dummy", "person2", True),
        ("Human", "dummy", "person", False),
    ],
)
def test_valid_yaml(cli_runner, target_class, schema, data, valid):
    """Tests https://github.com/linkml/linkml/issues/1446"""

    schema_path = str(TEST_INPUTS_DIR / f"{schema}.yaml")
    data_path = str(TEST_INPUTS_DIR / f"{data}.yaml")
    result = cli_runner.invoke(cli, ["-s", schema_path, "-C", target_class, data_path])
    if valid:
        assert result.exception is None
        assert result.output.startswith("No issues found")
        assert result.exit_code == 0
    else:
        assert result.exit_code != 0
