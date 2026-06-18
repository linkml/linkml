from click.testing import CliRunner

from linkml.generators.openapigen import cli
from tests.conftest import KITCHEN_SINK_PATH

OPENAPI_TEMPLATE_PATH_V303 = str(
    __import__("pathlib").Path(__file__).parent.parent
    / "test_generators"
    / "input"
    / "openapi"
    / "spec-head.openapi.yaml"
)

OPENAPI_TEMPLATE_PATH_V310 = str(
    __import__("pathlib").Path(__file__).parent.parent
    / "test_generators"
    / "input"
    / "openapi"
    / "spec-head-v31.openapi.yaml"
)


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate an OpenAPI spec" in result.output


def test_valid_call_v303():
    runner = CliRunner()
    result = runner.invoke(cli, [KITCHEN_SINK_PATH, "--template", OPENAPI_TEMPLATE_PATH_V303])
    assert result.exit_code == 0
    assert "MarriageEvent" in result.output
    assert "MedicalEvent" in result.output


def test_valid_call_v310():
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            KITCHEN_SINK_PATH,
            "--template",
            OPENAPI_TEMPLATE_PATH_V310,
            "--openapi-version",
            "3.1.0",
        ],
    )
    assert result.exit_code == 0
    assert "MarriageEvent" in result.output
    assert "MedicalEvent" in result.output


def test_missing_template():
    runner = CliRunner()
    result = runner.invoke(cli, [KITCHEN_SINK_PATH], standalone_mode=False)
    assert result.exit_code != 0
