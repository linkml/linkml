"""Regression tests for ``--importmap`` propagation in generators.

Several generators construct a secondary ``SchemaView`` from
``self.schema`` without forwarding ``importmap`` (and ``base_dir``).
When the source schema imports a sibling module via a URI-style
prefix (e.g. ``ex:schema/core``) the resulting view falls back to a
network fetch and fails with ``HTTPError: HTTP Error 403`` (or
similar). This test exercises each affected generator end-to-end
with a fixture schema whose imports can only be resolved through
``importmap``, asserting that generation succeeds and the imported
class flows through.

See also: docgen.py / pythongen.py / excelgen.py / linkmlgen.py /
sqltablegen.py / jsonldgen.py.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from linkml.generators.docgen import DocGenerator
from linkml.generators.excelgen import ExcelGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.linkmlgen import LinkmlGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.sqltablegen import SQLTableGenerator

# Class names baked into the fixture below. Tests assert that the
# imported class (``Thing``) survives the full generation pipeline.
IMPORTED_CLASS = "Thing"
LOCAL_CLASS = "Widget"


@pytest.fixture
def importmap_schema(tmp_path: Path) -> tuple[Path, Path]:
    """Materialise a two-file schema reachable only via importmap.

    Returns ``(main_yaml, importmap_json)``. The imported module is
    referenced as ``ex:schema/core`` in ``main.yaml``; without the
    importmap the loader would try to fetch ``https://example.org/...``
    and fail.
    """
    root = tmp_path
    schema_dir = root / "src" / "ex" / "schema"
    schema_dir.mkdir(parents=True)

    (schema_dir / "core.yaml").write_text(
        "id: https://example.org/ex/schema/core\n"
        "name: core\n"
        "prefixes:\n"
        "  linkml: https://w3id.org/linkml/\n"
        "  ex: https://example.org/ex/\n"
        "default_prefix: ex\n"
        "default_range: string\n"
        "imports:\n"
        "  - linkml:types\n"
        "classes:\n"
        "  Thing:\n"
        "    attributes:\n"
        "      id:\n"
        "        identifier: true\n"
        "        range: string\n"
    )

    main_yaml = schema_dir / "main.yaml"
    main_yaml.write_text(
        "id: https://example.org/ex/schema/main\n"
        "name: main\n"
        "prefixes:\n"
        "  linkml: https://w3id.org/linkml/\n"
        "  ex: https://example.org/ex/\n"
        "default_prefix: ex\n"
        "default_range: string\n"
        "imports:\n"
        "  - linkml:types\n"
        "  - ex:schema/core\n"
        "classes:\n"
        "  Widget:\n"
        "    is_a: Thing\n"
    )

    importmap_json = root / "importmap.json"
    src_ex = str(root / "src" / "ex") + "/"
    importmap_json.write_text(json.dumps({"ex": src_ex, "ex:": src_ex}))

    return main_yaml, importmap_json


def test_pythongen_forwards_importmap(importmap_schema, tmp_path):
    """gen-python must honour ``importmap`` (uses_schemaloader=True path)."""
    main_yaml, importmap_json = importmap_schema
    gen = PythonGenerator(str(main_yaml), importmap=str(importmap_json))
    out = gen.serialize()
    assert isinstance(out, str) and out
    assert f"class {LOCAL_CLASS}" in out
    assert f"class {IMPORTED_CLASS}" in out


def test_linkmlgen_forwards_importmap(importmap_schema, tmp_path):
    """gen-linkml overwrites self.schemaview post-super; importmap must survive."""
    main_yaml, importmap_json = importmap_schema
    gen = LinkmlGenerator(str(main_yaml), importmap=str(importmap_json), mergeimports=True)
    out = gen.serialize()
    assert isinstance(out, str) and out
    assert LOCAL_CLASS in out
    assert IMPORTED_CLASS in out


def test_docgen_forwards_importmap(importmap_schema, tmp_path):
    """gen-doc overwrites self.schemaview after super(); see report §9."""
    main_yaml, importmap_json = importmap_schema
    out_dir = tmp_path / "docs"
    gen = DocGenerator(str(main_yaml), importmap=str(importmap_json), mergeimports=True)
    gen.serialize(directory=str(out_dir))
    written = {p.name for p in out_dir.glob("*.md")}
    assert f"{LOCAL_CLASS}.md" in written
    assert f"{IMPORTED_CLASS}.md" in written


def test_excelgen_forwards_importmap(importmap_schema, tmp_path):
    """gen-excel constructs a secondary SchemaView after super()."""
    main_yaml, importmap_json = importmap_schema
    out_path = tmp_path / "schema.xlsx"
    gen = ExcelGenerator(
        str(main_yaml),
        importmap=str(importmap_json),
        mergeimports=True,
        output=str(out_path),
    )
    gen.serialize()
    assert out_path.exists() and out_path.stat().st_size > 0


def test_sqltablegen_forwards_importmap(importmap_schema, tmp_path):
    """gen-sqltables builds two SchemaViews internally; both must honour importmap."""
    main_yaml, importmap_json = importmap_schema
    gen = SQLTableGenerator(str(main_yaml), importmap=str(importmap_json), mergeimports=True)
    ddl = gen.serialize()
    assert isinstance(ddl, str) and ddl
    # SQLTableGenerator emits one CREATE TABLE per non-abstract class
    assert "CREATE TABLE" in ddl
    assert LOCAL_CLASS.lower() in ddl.lower()


def test_jsonldgen_forwards_importmap(importmap_schema, tmp_path):
    """gen-jsonld delegates context generation; importmap must reach ContextGenerator."""
    main_yaml, importmap_json = importmap_schema
    gen = JSONLDGenerator(str(main_yaml), importmap=str(importmap_json), mergeimports=True)
    out = gen.serialize()
    assert isinstance(out, str) and out
    # Parses as JSON and includes our local class
    payload = json.loads(out)
    assert isinstance(payload, dict)
    assert LOCAL_CLASS in out
