import pytest
from click.testing import CliRunner

from linkml import LOCAL_METAMODEL_YAML_FILE
from linkml.generators.owlgen import cli


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate an OWL representation of a LinkML model" in result.output


@pytest.mark.parametrize(
    "arguments,snapshot_file,rdf_format",
    [
        ([], "meta_owl.ttl", "turtle"),
        (["-f", "json-ld"], "meta_owl.jsonld", "json-ld"),
        (["-f", "n3"], "meta_owl.n3", "n3"),
    ],
)
def test_metamodel(arguments, snapshot_file, rdf_format, snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, arguments + [LOCAL_METAMODEL_YAML_FILE])
    assert result.exit_code == 0
    assert result.output == snapshot(f"genowl/{snapshot_file}", rdf_format=rdf_format)
