"""Minimal tests for the RDFS generator.

The generator code is in LinkML-Scala, so the tests here check mostly that all the
options work correctly.
"""

from pathlib import Path

import pytest
from click.testing import CliRunner
from rdflib import RDF, RDFS, Graph, URIRef
from rdflib.compare import isomorphic

from linkml.generators.common.scala import build_info
from linkml.generators.rdfsgen import RdfsGenerator, cli

linkml_scala = pytest.importorskip("linkml_scala", reason="LinkML-Scala has no build for this platform")

pytestmark = pytest.mark.rdfsgen

SCHEMA = Path(__file__).parent / "input" / "rdfs_vocabulary.yaml"

RV = "https://example.org/rdfsvocab/"
SCHEMA_ORG = "http://schema.org/"
IMPORTED_CLASS = URIRef("https://w3id.org/linkml/tests/core/Activity")
"""A class from core.yaml, which :data:`SCHEMA` imports."""


@pytest.fixture(scope="module")
def graph() -> Graph:
    """The generated vocabulary for :data:`SCHEMA`, parsed."""
    return RdfsGenerator(str(SCHEMA)).as_graph()


@pytest.mark.parametrize("fmt", RdfsGenerator.valid_formats)
def test_format_selection(fmt):
    """Turtle and N-Triples must be passed through directly."""
    generator = RdfsGenerator(str(SCHEMA), format=fmt)
    upstream = {"ttl": generator.as_turtle, "nt": generator.as_ntriples}[fmt]
    assert generator.serialize() == upstream()


def test_as_graph_keeps_upstream_prefixes(graph):
    """``schema:`` must expand to what the schema declared, not rdflib's https spelling.

    rdflib pre-binds ``schema:`` to ``https://schema.org/`` and will not rebind it, so the graph
    is built with ``bind_namespaces="none"``.
    """
    assert str(dict(graph.namespaces())["schema"]) == SCHEMA_ORG


@pytest.mark.parametrize(
    "uri",
    [
        f"{RV}HasAliases",
        f"{RV}Person",
        f"{SCHEMA_ORG}Organization",
        f"{RV}VitalStatus",
    ],
)
def test_classes_and_enums_become_rdfs_class(graph, uri):
    """Basic test: check if the generator emits something."""
    assert (URIRef(uri), RDF.type, RDFS.Class) in graph


@pytest.mark.parametrize("fmt", RdfsGenerator.valid_formats)
def test_every_format_contains_the_same_triples(graph, fmt):
    """Serializing to each supported format and reading it back gives the same graph.

    Driven off ``valid_formats`` so that adding a format cannot skip this check.
    """
    parsed = Graph().parse(data=RdfsGenerator(str(SCHEMA), format=fmt).serialize(), format=fmt)
    assert isomorphic(parsed, graph)


def test_unknown_format_is_rejected():
    """The base generator validates ``--format`` against ``valid_formats``."""
    with pytest.raises(ValueError, match="Unrecognized format"):
        RdfsGenerator(str(SCHEMA), format="yaml")


def test_exclude_imports_drops_imported_classes(graph):
    """``--exclude-imports`` becomes LinkML-Scala's ``only_classes_from_root_schema``."""
    excluded = RdfsGenerator(str(SCHEMA), exclude_imports=True).as_graph()
    assert (IMPORTED_CLASS, RDF.type, RDFS.Class) in graph
    assert (IMPORTED_CLASS, RDF.type, RDFS.Class) not in excluded


def test_cli_exclude_imports():
    """``--exclude-imports`` reaches the generator."""
    result = CliRunner().invoke(cli, [str(SCHEMA), "--format", "nt", "--exclude-imports"])
    assert result.exit_code == 0
    assert f"<{IMPORTED_CLASS}> <{RDF.type}> <{RDFS.Class}>" not in result.output


def test_cli_output_writes_a_file(tmp_path):
    """``-o`` writes the vocabulary to a file instead of stdout."""
    destination = tmp_path / "vocab.ttl"
    result = CliRunner().invoke(cli, [str(SCHEMA), "-o", str(destination)])
    assert result.exit_code == 0
    assert result.output == ""
    assert Graph().parse(data=destination.read_text(), format="turtle")


def test_cli():
    """``gen-rdfs schema.yaml`` prints Turtle."""
    result = CliRunner().invoke(cli, [str(SCHEMA)])
    assert result.exit_code == 0
    assert Graph().parse(data=result.output, format="turtle")


def test_cli_version_reports_both_versions():
    """A bug report needs the linkml version and the LinkML-Scala version, so ``-V`` shows both."""
    result = CliRunner().invoke(cli, ["-V"])
    assert result.exit_code == 0
    assert "linkml " in result.output
    assert f"LinkML-Scala {build_info()['linkml_scala_version']}" in result.output
