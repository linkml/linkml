import pytest
from click.testing import CliRunner

from linkml.generators.openapigen import cli
from tests.conftest import KITCHEN_SINK_PATH

OPENAPI_TEMPLATE_PATH_PREFIX = str(__import__("pathlib").Path(__file__).parent.parent / "test_generators" / "input")


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate an OpenAPI spec" in result.output


@pytest.mark.parametrize(
    "template_path",
    ["openapi/spec-head-v30.openapi.yaml", "openapi/spec-head-v31.openapi.yaml"],
)
def test_valid_call(template_path):
    runner = CliRunner()
    result = runner.invoke(cli, [KITCHEN_SINK_PATH, "--template", f"{OPENAPI_TEMPLATE_PATH_PREFIX}/{template_path}"])
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
