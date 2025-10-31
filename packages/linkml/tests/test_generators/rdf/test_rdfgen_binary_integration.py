from pathlib import Path

import pytest

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


def test_binary_serializer_with_output_keeps_stdout_empty_and_writes_binary(tmp_path):
    """With binary serializer and -o: stdout is empty, file contains binary data."""
    pytest.importorskip("rdflib.plugins.serializers.jelly")

    schema_path = _write_min_schema(tmp_path / "schema.yaml")
    out_path = tmp_path / "out.jelly"

    gen = RDFGenerator(str(schema_path), mergeimports=False)
    gen.format = "jelly"

    ret = gen.serialize(output=str(out_path))

    assert ret.strip() == ""
    assert out_path.exists() and out_path.stat().st_size > 0

    with pytest.raises(UnicodeDecodeError):
        _ = out_path.read_text(encoding="utf-8")


def test_text_serializer_with_output_preserves_stdout_and_writes_text(tmp_path):
    """With text serializer and -o: stdout returns text; file contains the same text."""
    schema_path = _write_min_schema(tmp_path / "schema.yaml")
    out_path = tmp_path / "out.ttl"

    gen = RDFGenerator(str(schema_path), mergeimports=False)
    gen.format = "ttl"

    ret = gen.serialize(output=str(out_path))

    assert isinstance(ret, str) and len(ret.strip()) > 0
    txt = out_path.read_text(encoding="utf-8")
    assert txt.rstrip("\n") == ret.rstrip("\n") and len(txt) > 0
