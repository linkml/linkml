from click.testing import CliRunner

from linkml.generators.shaclgen import cli
from ..conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate SHACL turtle from a LinkML model" in result.output
