from pathlib import Path
from typing import Any

from rdflib import Graph

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


def test_with_output_binary_path_on_decode_error(monkeypatch, tmp_path):
    """On UnicodeDecodeError: write via destination, keep stdout empty."""
    calls: dict[str, Any] = {"destination_called": False, "format": None}

    def fake_serialize(self, *args, **kwargs):
        if "destination" not in kwargs:
            raise UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid start byte")
        calls["destination_called"] = True
        calls["format"] = kwargs.get("format")
        dest = kwargs["destination"]
        Path(dest).write_bytes(b"\x00\x01\x02BINARY-DATA")
        return None

    monkeypatch.setattr(Graph, "serialize", fake_serialize, raising=True)

    schema_path = _write_min_schema(tmp_path / "schema.yaml")
    out_path = tmp_path / "out.bin"

    gen = RDFGenerator(str(schema_path), mergeimports=False)
    gen.format = "ttl"  # maps to 'turtle'

    ret = gen.serialize(output=str(out_path))

    assert ret.strip() == ""
    assert calls["destination_called"] is True
    assert calls["format"] == "turtle"
    assert out_path.exists() and out_path.stat().st_size > 0

    data = out_path.read_bytes()
    assert data.startswith(b"\x00\x01\x02BINARY-DATA")


def test_with_output_text_path_returns_text_and_writes_file(monkeypatch, tmp_path):
    """If serialization returns text, write UTF-8 file and return the same text."""
    calls: dict[str, Any] = {"destination_called": False, "format": None}

    def fake_serialize(self, *args, **kwargs):
        if "destination" in kwargs:
            calls["destination_called"] = True
            calls["format"] = kwargs.get("format")
            return None
        fmt = kwargs.get("format")
        return f"# fake {fmt} content"

    monkeypatch.setattr(Graph, "serialize", fake_serialize, raising=True)

    schema_path = _write_min_schema(tmp_path / "schema.yaml")
    out_path = tmp_path / "out.ttl"

    gen = RDFGenerator(str(schema_path), mergeimports=False)
    gen.format = "ttl"  # => 'turtle'

    ret = gen.serialize(output=str(out_path))

    assert isinstance(ret, str) and ret.startswith("# fake turtle")
    assert calls["destination_called"] is False
    txt = out_path.read_text(encoding="utf-8")
    assert txt.rstrip("\n") == ret.rstrip("\n")


def test_without_output_returns_text(monkeypatch, tmp_path):
    """Without -o, return text."""

    def fake_serialize(self, *args, **kwargs):
        assert "destination" not in kwargs
        return "# fake turtle content"

    monkeypatch.setattr(Graph, "serialize", fake_serialize, raising=True)

    schema_path = _write_min_schema(tmp_path / "s.yaml")
    gen = RDFGenerator(str(schema_path), mergeimports=False)
    gen.format = "turtle"

    ret = gen.serialize()
    assert isinstance(ret, str) and ret.startswith("# fake turtle")
