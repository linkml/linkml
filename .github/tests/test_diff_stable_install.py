"""Run each selection in a fresh environment containing the built wheels."""

import importlib
import re
import sys
import sysconfig
from importlib.metadata import metadata, version
from importlib.util import find_spec
from pathlib import Path

import pytest
from packaging.requirements import Requirement

_SCHEMA = """id: https://example.org/install
name: install
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/install/
default_prefix: ex
imports: [linkml:types]
classes:
  Thing:
    attributes:
      label:
        range: string
"""


def _assert_installed(package: str) -> None:
    """Require imports from this environment's installed package directory."""
    module = importlib.import_module(package)
    assert Path(module.__file__).resolve().is_relative_to(Path(sysconfig.get_path("purelib")).resolve())


def _assert_runtime_requirements() -> None:
    """Check ordinary compatibility and the extra's forwarding in wheel metadata."""
    requirements = [Requirement(value) for value in metadata("linkml").get_all("Requires-Dist")]
    (ordinary,) = [r for r in requirements if r.name == "linkml-runtime" and r.marker is None]
    (forwarded,) = [r for r in requirements if r.name == "linkml-runtime" and r.marker is not None]
    assert ordinary.extras == set()
    assert forwarded.extras == {"diff-stable"}
    assert forwarded.marker.evaluate({"extra": "diff-stable"})
    assert not forwarded.marker.evaluate({"extra": ""})
    assert ordinary.specifier == forwarded.specifier
    assert ordinary.specifier.contains(version("linkml-runtime"), prereleases=True)


def _assert_diff_stable_labels(output: str) -> None:
    """Require actual blank-node terms with the enabled label syntax."""
    import pyoxigraph as ox

    quads = ox.parse(output, format=ox.RdfFormat.TURTLE)
    nodes = {term for q in quads for term in (q.subject, q.object) if isinstance(term, ox.BlankNode)}
    assert nodes
    assert all(re.fullmatch(r"b[0-9a-f]{12}(?:_[1-9][0-9]*)?", node.value) for node in nodes)


def test_runtime_without_extra() -> None:
    """Ordinary runtime installs work and explain how to enable the option."""
    assert find_spec("diffable_rdf") is None
    _assert_installed("linkml_runtime")
    from rdflib import Graph
    from rdflib.compare import isomorphic

    from linkml_runtime.utils.rdf_canonicalize import canonicalize_rdf_graph

    graph = Graph().parse(data='<https://example.org/s> <https://example.org/p> [ <https://example.org/q> "v" ] .')
    for kwargs in ({}, {"diff_stable": False}):
        output = canonicalize_rdf_graph(graph, **kwargs)
        assert isomorphic(graph, Graph().parse(data=output, format="turtle"))
    assert "diffable_rdf" not in sys.modules
    with pytest.raises(ImportError, match=r"linkml-runtime\[diff-stable\]"):
        canonicalize_rdf_graph(graph, diff_stable=True)


def test_linkml_without_extra(tmp_path: Path) -> None:
    """Generator imports, help and default output do not require the extra."""
    assert find_spec("diffable_rdf") is None
    _assert_installed("linkml_runtime")
    _assert_installed("linkml")
    _assert_runtime_requirements()
    from click.testing import CliRunner
    from rdflib import Graph
    from rdflib.namespace import RDF, SH

    from linkml.generators.shaclgen import cli

    for name in ("owlgen", "rdfgen", "shaclgen", "shexgen"):
        command = importlib.import_module(f"linkml.generators.{name}").cli
        result = CliRunner().invoke(command, ["--help"])
        assert result.exit_code == 0, result.output
    schema = tmp_path / "schema.yaml"
    schema.write_text(_SCHEMA, encoding="utf-8")
    result = CliRunner().invoke(cli, [str(schema)])
    assert result.exit_code == 0, result.output
    graph = Graph().parse(data=result.stdout, format="turtle")
    assert list(graph.subjects(RDF.type, SH.NodeShape))
    assert "diffable_rdf" not in sys.modules
    result = CliRunner().invoke(cli, [str(schema), "--diff-stable"])
    assert result.exit_code != 0
    assert isinstance(result.exception, ImportError)
    assert "linkml[diff-stable]" in str(result.exception)


def test_runtime_with_extra() -> None:
    """The runtime extra supplies the relabeler and preserves the source graph."""
    assert find_spec("diffable_rdf") is not None
    _assert_installed("linkml_runtime")
    from rdflib import Graph
    from rdflib.compare import isomorphic

    from linkml_runtime.utils.rdf_canonicalize import canonicalize_rdf_graph

    graph = Graph().parse(data='<https://example.org/s> <https://example.org/p> [ <https://example.org/q> "v" ] .')
    canonicalize_rdf_graph(graph)
    assert "diffable_rdf" not in sys.modules
    output = canonicalize_rdf_graph(graph, output_format="nt", diff_stable=True)
    parsed = Graph().parse(data=output, format="nt")
    assert len(parsed) == len(graph)
    assert isomorphic(graph, parsed)
    _assert_diff_stable_labels(output)
    _assert_installed("diffable_rdf")


def test_linkml_with_extra(tmp_path: Path) -> None:
    """The LinkML extra installs the relabeler through the runtime extra."""
    assert find_spec("diffable_rdf") is not None
    _assert_installed("linkml_runtime")
    _assert_installed("linkml")
    _assert_runtime_requirements()
    from click.testing import CliRunner
    from rdflib import Graph, Namespace
    from rdflib.namespace import RDF, SH

    from linkml.generators.shaclgen import cli

    schema = tmp_path / "schema.yaml"
    schema.write_text(_SCHEMA, encoding="utf-8")
    result = CliRunner().invoke(cli, [str(schema), "--diff-stable"])
    assert result.exit_code == 0, result.output
    graph = Graph().parse(data=result.stdout, format="turtle")
    ex = Namespace("https://example.org/install/")
    assert (ex.Thing, RDF.type, SH.NodeShape) in graph
    assert (ex.Thing, SH.targetClass, ex.Thing) in graph
    assert {graph.value(node, SH.path) for node in graph.objects(ex.Thing, SH.property)} == {ex.label}
    _assert_diff_stable_labels(result.stdout)
    _assert_installed("diffable_rdf")
