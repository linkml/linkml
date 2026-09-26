"""CLI integration checks for optional diff-stable RDF labels."""

import re
from pathlib import Path

import click
import pyoxigraph as ox
import pytest
from click.testing import CliRunner
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import OWL, RDF, SH

from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.owlgen import cli as owl_cli
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.rdfgen import cli as rdf_cli
from linkml.generators.shaclgen import ShaclGenerator
from linkml.generators.shaclgen import cli as shacl_cli
from linkml.generators.shexgen import ShExGenerator
from linkml.generators.shexgen import cli as shex_cli
from linkml.utils.generator import Generator


@pytest.mark.parametrize(
    ("command", "args", "rdf_type"),
    [
        pytest.param(owl_cli, [], OWL.Class, id="owlgen"),
        pytest.param(
            rdf_cli, [], URIRef("https://w3id.org/linkml/ClassDefinition"), id="rdfgen", marks=pytest.mark.network
        ),
        pytest.param(shacl_cli, [], SH.NodeShape, id="shaclgen"),
        pytest.param(
            shex_cli,
            ["--format", "rdf"],
            URIRef("http://www.w3.org/ns/shex#Shape"),
            id="shexgen",
            marks=pytest.mark.network,
        ),
    ],
)
@pytest.mark.parametrize(
    ("flag", "label_pattern"),
    [
        pytest.param("--no-diff-stable", r"c14n[0-9]+", id="disabled"),
        pytest.param("--diff-stable", r"b[0-9a-f]{12}(?:_[1-9][0-9]*)?", id="enabled"),
    ],
)
def test_diff_stable_cli(
    tmp_path: Path, command: click.Command, args: list[str], rdf_type: URIRef, flag: str, label_pattern: str
) -> None:
    """Every RDF CLI produces the requested labels and the expected class."""
    schema = tmp_path / "schema.yaml"
    schema.write_text(
        """id: https://example.org/cli
name: cli
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/cli/
default_prefix: ex
imports: [linkml:types]
classes:
  Thing:
    attributes:
      label:
        range: string
""",
        encoding="utf-8",
    )
    result = CliRunner().invoke(command, [str(schema), flag, *args])
    assert result.exit_code == 0, result.output
    quads = list(ox.parse(result.stdout, format=ox.RdfFormat.TURTLE))
    blank_nodes = {term for q in quads for term in (q.subject, q.object) if isinstance(term, ox.BlankNode)}
    assert blank_nodes
    assert all(re.fullmatch(label_pattern, node.value) for node in blank_nodes)
    graph = Graph().parse(data=result.stdout, format="turtle")
    assert (Namespace("https://example.org/cli/").Thing, RDF.type, rdf_type) in graph


@pytest.mark.parametrize(
    ("generator", "command"),
    [
        pytest.param(OwlSchemaGenerator, owl_cli, id="owlgen"),
        pytest.param(RDFGenerator, rdf_cli, id="rdfgen"),
        pytest.param(ShaclGenerator, shacl_cli, id="shaclgen"),
        pytest.param(ShExGenerator, shex_cli, id="shexgen"),
    ],
)
def test_diff_stable_defaults_and_help(generator: type[Generator], command: click.Command) -> None:
    """Defaults are off and terminal help points to the shared guide."""
    assert generator.diff_stable is False
    (option,) = [param for param in command.params if param.name == "diff_stable"]
    assert option.default is False
    result = CliRunner().invoke(command, ["--help"])
    assert result.exit_code == 0
    assert "--diff-stable / --no-diff-stable" in result.output
    assert "[default: no-diff-stable]" in result.output
    assert "https://linkml.io/linkml/howtos/collaborative-development.html#rdf-in-version-control" in "".join(
        result.output.split()
    )
