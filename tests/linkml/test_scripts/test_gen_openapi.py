from click.testing import CliRunner

from linkml.generators.openapigen import cli
from tests.conftest import KITCHEN_SINK_PATH

OPENAPI_TEMPLATE_PATH = str(
    __import__("pathlib").Path(__file__).parent.parent
    / "test_generators"
    / "input"
    / "openapi"
    / "spec-head.openapi.yaml"
)


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate an OpenAPI spec" in result.output


def test_valid_call():
    runner = CliRunner()
    result = runner.invoke(cli, [KITCHEN_SINK_PATH, "--template", OPENAPI_TEMPLATE_PATH])
    assert result.exit_code == 0
    assert "MarriageEvent" in result.output
    assert "MedicalEvent" in result.output


def test_missing_template():
    """Test that omitting --template prints a generic OpenAPI template."""
    runner = CliRunner()
    result = runner.invoke(cli, [KITCHEN_SINK_PATH], standalone_mode=False)
    assert result.exit_code == 0
    assert "openapi: x.y.z" in result.output
    assert "x-linkml-schema:" in result.output
