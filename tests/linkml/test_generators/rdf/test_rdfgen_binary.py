"""Tests for RDFGenerator.serialize() with and without output paths.

After the switch to canonicalize_rdf_graph (pyoxigraph RDFC-1.0),
the old binary fallback (UnicodeDecodeError → destination) no longer
exists.  These tests verify the current behaviour: serialize always
returns a str, and when an output path is given the same text is
written to the file.
"""

from pathlib import Path

from linkml.generators.rdfgen import RDFGenerator


def _write_min_schema(p: Path) -> Path:
    p.write_text(
        "id: http://example.org/min\n"
        "name: min\n"
        "prefixes:\n"
        "  ex: http://example.org/\n"
        "default_curi_maps:\n"
        "  - semweb_context\n"
        "classes:\n"
        "  A: {}\n",
        encoding="utf-8",
    )
    return p


def test_without_output_returns_text(tmp_path):
    """Without -o, serialize() returns a non-empty str."""
    schema_path = _write_min_schema(tmp_path / "s.yaml")
    gen = RDFGenerator(str(schema_path), mergeimports=False)
    gen.format = "turtle"

    ret = gen.serialize()
    assert isinstance(ret, str)
    assert len(ret.strip()) > 0


def test_with_output_writes_file_and_returns_text(tmp_path):
    """With -o, serialize() writes UTF-8 file and returns the same text."""
    schema_path = _write_min_schema(tmp_path / "schema.yaml")
    out_path = tmp_path / "out.ttl"

    gen = RDFGenerator(str(schema_path), mergeimports=False)
    gen.format = "ttl"

    ret = gen.serialize(output=str(out_path))

    assert isinstance(ret, str)
    assert len(ret.strip()) > 0
    assert out_path.exists()
    txt = out_path.read_text(encoding="utf-8")
    assert txt == ret
