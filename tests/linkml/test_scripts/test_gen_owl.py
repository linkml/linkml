import os

import pytest
from click.testing import CliRunner

from linkml.generators.owlgen import cli
from tests.conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate an OWL representation of a LinkML model" in result.output


def test_output_option_writes_file(tmp_path):
    """--output writes the OWL to the file instead of stdout (#2752)."""
    output = tmp_path / "out.owl.ttl"
    runner = CliRunner()
    result = runner.invoke(cli, ["--output", str(output), KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == ""
    assert output.exists()
    assert "owl:Ontology" in output.read_text(encoding="UTF-8")


@pytest.mark.slow
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
    result = runner.invoke(cli, arguments + [KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    # Only do the snapshot comparison if we're not on Windows. rdflib has a bug when expanding
    # prefixes delimited by an underscore that appears to be platform-dependent.
    # See:
    #   https://github.com/RDFLib/rdflib/issues/2606
    #   https://github.com/linkml/linkml/issues/1650
    if os.name == "nt":
        return
    assert result.output == snapshot(f"genowl/{snapshot_file}", rdf_format=rdf_format)


@pytest.mark.slow
@pytest.mark.parametrize(
    "arguments,snapshot_file,rdf_format",
    [
        ([], "meta_owl_custom_enum_separator.ttl", "turtle"),
        (["-f", "json-ld"], "meta_owl_custom_enum_separator.jsonld", "json-ld"),
        (["-f", "n3"], "meta_owl_custom_enum_separator.n3", "n3"),
    ],
)
def test_metamodel_with_enum_iri_separator(arguments, snapshot_file, rdf_format, snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, arguments + [KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    # Only do the snapshot comparison if we're not on Windows. rdflib has a bug when expanding
    # prefixes delimited by an underscore that appears to be platform-dependent.
    # See:
    #   https://github.com/RDFLib/rdflib/issues/2606
    #   https://github.com/linkml/linkml/issues/1650
    if os.name == "nt":
        return
    assert result.output == snapshot(f"genowl/{snapshot_file}", rdf_format=rdf_format)
