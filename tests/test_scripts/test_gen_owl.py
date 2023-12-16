import os

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
    # Only do the snapshot comparison if we're not on Windows. rdflib has a bug when expanding
    # prefixes delimited by an underscore that appears to be platform-dependent.
    # See:
    #   https://github.com/RDFLib/rdflib/issues/2606
    #   https://github.com/linkml/linkml/issues/1650
    if os.name == "nt":
        return
    assert result.output == snapshot(f"genowl/{snapshot_file}", rdf_format=rdf_format)
