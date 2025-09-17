import json
import os

import pytest

from linkml.generators import ContextGenerator, JSONLDGenerator
from tests.utils.compare_jsonld_context import CompareJsonldContext
from tests.utils.validate_jsonld_context import RdfExpectations
from linkml.generators.jsonldcontextgen import ContextGenerator as FrameContextGenerator
from linkml.generators.jsonldcontextgen import cli as jsonld_context_cli
from click.testing import CliRunner


def test_jsonld_context_integration(kitchen_sink_path, snapshot_path):
    jsonld_context = ContextGenerator(kitchen_sink_path).serialize()
    CompareJsonldContext.compare_with_snapshot(jsonld_context, snapshot_path("kitchen_sink.jsonld"))


def test_no_default_namespace_prefix(input_path, snapshot_path):
    jsonld_context = ContextGenerator(str(input_path("jsonld_context_no_default_namespace_prefix.yaml"))).serialize()
    CompareJsonldContext.compare_with_snapshot(jsonld_context, snapshot_path("no_default_namespace_prefix.jsonld"))


def test_class_uri_prefix(input_path, snapshot_path):
    jsonld_context = ContextGenerator(str(input_path("jsonld_context_class_uri_prefix.yaml"))).serialize()
    CompareJsonldContext.compare_with_snapshot(jsonld_context, snapshot_path("class_uri_prefix.jsonld"))


def test_inlined_external_types(input_path, snapshot_path):
    jsonld_context = ContextGenerator(str(input_path("jsonld_context_inlined_external_types.yaml"))).serialize()
    CompareJsonldContext.compare_with_snapshot(jsonld_context, snapshot_path("context_inlined_external_types.jsonld"))


@pytest.mark.parametrize(
    "schema",
    [
        pytest.param(
            "jsonld_context_class_uri_prefix.yaml",
            marks=pytest.mark.xfail(reason="Bug linkml#2677: class_uri and slot_uri not used for element URIs"),
        ),
        pytest.param(
            "jsonld_context_inlined_external_types.yaml",
            marks=pytest.mark.xfail(reason="Bug linkml#2679: unexpected example.org URI"),
        ),
        pytest.param(
            "jsonld_context_no_default_namespace_prefix.yaml",
            marks=pytest.mark.xfail(reason="Bug linkml#2677: class_uri and slot_uri not used for element URIs"),
        ),
    ],
)
def test_expected_rdf(input_path, schema):
    schema_path = input_path(schema)
    output = JSONLDGenerator(schema_path).serialize()
    rdf_expects = RdfExpectations(schema_path, json.loads(output))
    rdf_expects.check_expectations()


def test_emit_frame_inline_rules(tmp_path):
    """When framing is on and schema uses inlined true/false, both files are written with proper @embed."""
    schema = tmp_path / "mini_inline.yaml"
    schema.write_text(
        """
id: ex
name: mini_inline
default_prefix: ex
imports:
  - linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  ex: http://example.org/
  xsd: http://www.w3.org/2001/XMLSchema#
classes:
  Person:
    attributes:
      id: {identifier: true, range: string}
      friend: {range: Person, inlined: true}
      neighbor: {range: Person, inlined: false}
""",
        encoding="utf-8",
    )

    gen = FrameContextGenerator(str(schema))
    gen.emit_frame = True
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        gen.serialize()
    finally:
        os.chdir(cwd)

    ctx = (tmp_path / "mini_inline.context.jsonld").read_text(encoding="utf-8")
    frm = (tmp_path / "mini_inline.frame.jsonld").read_text(encoding="utf-8")

    jctx = json.loads(ctx)
    assert "friend" in jctx["@context"]
    assert jctx["@context"]["neighbor"]["@type"] == "@id"

    jfrm = json.loads(frm)
    assert jfrm["friend"]["@embed"] == "@always"
    assert jfrm["neighbor"]["@embed"] == "@never"


def test_emit_frame_not_written_without_inlined(tmp_path):
    """No frame should be written when there are no inlined slots, even if framing is enabled."""
    schema = tmp_path / "mini_no_inline.yaml"
    schema.write_text(
        """
id: ex
name: mini_no_inline
default_prefix: ex
imports:
  - linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  ex: http://example.org/
  xsd: http://www.w3.org/2001/XMLSchema#
classes:
  Person:
    attributes:
      id: {identifier: true, range: string}
      friend: {range: Person}
      neighbor: {range: Person}
""",
        encoding="utf-8",
    )

    gen = FrameContextGenerator(str(schema))
    gen.emit_frame = True
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        gen.serialize()
    finally:
        os.chdir(cwd)

    frm_path = tmp_path / "mini_no_inline.frame.jsonld"
    assert not frm_path.exists(), "Frame must not be written when no inlined slots are present"


# -------------------- NEW TESTS --------------------


def test_emit_frame_tree_root_preferred(tmp_path):
    """Frame @type should prefer the class marked as tree_root, not an arbitrary first class."""
    schema = tmp_path / "mini_root.yaml"
    schema.write_text(
        """
id: ex
name: mini_root
default_prefix: ex
imports:
  - linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  ex: http://example.org/
  xsd: http://www.w3.org/2001/XMLSchema#
classes:
  A:
    attributes:
      id: {identifier: true, range: string}
  B:
    tree_root: true
    class_uri: ex:B
    attributes:
      id: {identifier: true, range: string}
      rel: {range: A, inlined: true}
""",
        encoding="utf-8",
    )

    gen = FrameContextGenerator(str(schema))
    gen.emit_frame = True
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        gen.serialize()
    finally:
        os.chdir(cwd)

    frm = json.loads((tmp_path / "mini_root.frame.jsonld").read_text(encoding="utf-8"))
    assert frm["@type"] == "ex:B"
    # Only 'rel' should be present with @embed rule
    assert frm["rel"]["@embed"] == "@always"


def test_emit_frame_only_for_class_ranges(tmp_path):
    """Only slots with range=class and explicit inlined should appear in frame; datatypes/enums/URIs must not."""
    schema = tmp_path / "mini_mixed.yaml"
    schema.write_text(
        """
id: ex
name: mini_mixed
default_prefix: ex
imports:
  - linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  ex: http://example.org/
  xsd: http://www.w3.org/2001/XMLSchema#
enums:
  Color:
    permissible_values:
      red: {}
      green: {}
classes:
  Person:
    attributes:
      id: {identifier: true, range: string}
      name: {range: string}
  Root:
    tree_root: true
    attributes:
      id: {identifier: true, range: string}
      title: {range: string}
      color: {range: Color}
      ref: {range: Person, inlined: true}
      link: {range: uri}
""",
        encoding="utf-8",
    )

    gen = FrameContextGenerator(str(schema))
    gen.emit_frame = True
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        gen.serialize()
    finally:
        os.chdir(cwd)

    frm_path = tmp_path / "mini_mixed.frame.jsonld"
    frm = json.loads(frm_path.read_text(encoding="utf-8"))
    # Only 'ref' should be framed; 'title'/'color'/'link' must not be present
    assert "ref" in frm and frm["ref"]["@embed"] == "@always"
    assert "title" not in frm
    assert "color" not in frm
    assert "link" not in frm


def test_cli_emit_frame_writes_files(tmp_path):
    """CLI: invoking --emit-frame writes both files next to the schema."""
    schema_name = "mini_cli.yaml"
    schema = tmp_path / schema_name
    schema.write_text(
        """
id: ex
name: mini_cli
default_prefix: ex
imports:
  - linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  ex: http://example.org/
  xsd: http://www.w3.org/2001/XMLSchema#
classes:
  Person:
    attributes:
      id: {identifier: true, range: string}
      friend: {range: Person, inlined: true}
""",
        encoding="utf-8",
    )

    runner = CliRunner()
    with runner.isolated_filesystem():
        # copy schema into isolated FS
        with open(schema_name, "w", encoding="utf-8") as f:
            f.write(schema.read_text(encoding="utf-8"))
        # run CLI
        result = runner.invoke(jsonld_context_cli, [schema_name, "--emit-frame"])
        assert result.exit_code == 0

        # files should exist
        assert os.path.exists("mini_cli.context.jsonld")
        assert os.path.exists("mini_cli.frame.jsonld")

        # sanity-check: frame has @embed
        jfrm = json.loads(open("mini_cli.frame.jsonld", "r", encoding="utf-8").read())
        assert jfrm["friend"]["@embed"] == "@always"
