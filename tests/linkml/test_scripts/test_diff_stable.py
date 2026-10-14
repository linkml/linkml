"""CLI checks for the optional diff-stable RDF labels."""

import re
from pathlib import Path

import pyoxigraph as ox
import pytest
from click.testing import CliRunner

from linkml.generators.shaclgen import cli as shacl_cli

_SCHEMA = """id: https://example.org/cli
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
"""


@pytest.mark.parametrize(
    ("flag", "label_pattern"),
    [
        pytest.param("--no-diff-stable", r"c14n[0-9]+", id="disabled"),
        pytest.param("--diff-stable", r"b[0-9a-f]{12}(?:_[1-9][0-9]*)?", id="enabled", marks=pytest.mark.diffable_rdf),
    ],
)
def test_the_flag_reaches_the_serializer(tmp_path: Path, flag: str, label_pattern: str) -> None:
    """The CLI flag selects the blank-node labelling it names."""
    schema = tmp_path / "schema.yaml"
    schema.write_text(_SCHEMA, encoding="utf-8")

    result = CliRunner().invoke(shacl_cli, [str(schema), flag])

    assert result.exit_code == 0, result.output
    quads = list(ox.parse(result.stdout, format=ox.RdfFormat.TURTLE))
    blank_nodes = {term for q in quads for term in (q.subject, q.object) if isinstance(term, ox.BlankNode)}
    assert blank_nodes
    assert all(re.fullmatch(label_pattern, node.value) for node in blank_nodes)
