import json
import textwrap

import pytest
from click.testing import CliRunner

from linkml.generators import ContextGenerator, JSONLDGenerator
from linkml.generators.jsonldcontextgen import ContextGenerator as FrameContextGenerator
from linkml.generators.jsonldcontextgen import cli as jsonld_context_cli
from tests.linkml.utils.compare_jsonld_context import CompareJsonldContext
from tests.linkml.utils.validate_jsonld_context import RdfExpectations


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
    out_path = tmp_path / "mini_inline.context.jsonld"
    gen.serialize(output=str(out_path))

    ctx = out_path.read_text(encoding="utf-8")
    frm = out_path.with_suffix(".frame.jsonld").read_text(encoding="utf-8")

    jctx = json.loads(ctx)
    assert "friend" in jctx["@context"]
    assert jctx["@context"]["neighbor"]["@type"] == "@id"

    jfrm = json.loads(frm)
    assert jfrm["friend"]["@embed"] == "@always"
    assert jfrm["neighbor"]["@embed"] == "@never"


def test_emit_frame_not_written_without_inlined(tmp_path):
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
    out_path = tmp_path / "mini_no_inline.context.jsonld"
    gen.serialize(output=str(out_path))

    frm_path = out_path.with_suffix(".frame.jsonld")
    assert not frm_path.exists(), "Frame must not be written when no inlined slots are present"


def test_emit_frame_tree_root_preferred(tmp_path):
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
    out_path = tmp_path / "mini_root.context.jsonld"
    gen.serialize(output=str(out_path))

    frm = json.loads(out_path.with_suffix(".frame.jsonld").read_text(encoding="utf-8"))
    assert frm["@type"] == "ex:B"
    assert frm["rel"]["@embed"] == "@always"


def test_emit_frame_only_for_class_ranges(tmp_path):
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
    out_path = tmp_path / "mini_mixed.context.jsonld"
    gen.serialize(output=str(out_path))

    frm_path = out_path.with_suffix(".frame.jsonld")
    frm = json.loads(frm_path.read_text(encoding="utf-8"))
    assert "ref" in frm and frm["ref"]["@embed"] == "@always"
    assert "title" not in frm
    assert "color" not in frm
    assert "link" not in frm


def test_cli_emit_frame_writes_files(tmp_path):
    schema = tmp_path / "mini_cli.yaml"
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
    out_path = tmp_path / "mini_cli.context.jsonld"
    result = runner.invoke(
        jsonld_context_cli,
        [str(schema), "--emit-frame", "--output", str(out_path)],
    )
    assert result.exit_code == 0
    assert out_path.exists()
    assert out_path.with_suffix(".frame.jsonld").exists()

    jfrm = json.loads(out_path.with_suffix(".frame.jsonld").read_text(encoding="utf-8"))
    assert jfrm["friend"]["@embed"] == "@always"


def test_cli_emit_frame_requires_output(tmp_path):
    schema = tmp_path / "mini_cli2.yaml"
    schema.write_text(
        """
id: ex
name: mini_cli2
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
    result = runner.invoke(jsonld_context_cli, [str(schema), "--emit-frame"])
    assert result.exit_code != 0
    assert "requires --output" in result.output
    assert "--emit-frame" in result.output


def test_cli_embed_context_in_frame_writes_single_file(tmp_path):
    schema = tmp_path / "mini_cli_embed.yaml"
    schema.write_text(
        """
id: ex
name: mini_cli_embed
default_prefix: ex
imports:
  - linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  ex: http://example.org/
  xsd: http://www.w3.org/2001/XMLSchema#
classes:
  Person:
    tree_root: true
    attributes:
      id: {identifier: true, range: string}
      friend: {range: Person, inlined: true}
""",
        encoding="utf-8",
    )

    runner = CliRunner()
    out_base = tmp_path / "mini_cli_embed.jsonld"
    result = runner.invoke(
        jsonld_context_cli,
        [str(schema), "--embed-context-in-frame", "--output", str(out_base)],
    )
    assert result.exit_code == 0

    frame_path = out_base.with_suffix(".frame.jsonld")
    assert frame_path.exists()
    assert not out_base.exists()

    jfrm = json.loads(frame_path.read_text(encoding="utf-8"))
    assert "@context" in jfrm
    assert jfrm["friend"]["@embed"] == "@always"


def test_cli_embed_context_in_frame_requires_output(tmp_path):
    schema = tmp_path / "mini_cli_embed2.yaml"
    schema.write_text(
        """
id: ex
name: mini_cli_embed2
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
""",
        encoding="utf-8",
    )

    runner = CliRunner()
    result = runner.invoke(jsonld_context_cli, [str(schema), "--embed-context-in-frame"])
    assert result.exit_code != 0
    assert "requires --output" in result.output


@pytest.mark.parametrize(
    "fix_container,attribute,container_type",
    [
        [False, "int_list", ""],
        [False, "int_inlined_list", ""],
        [False, "int_dict", ""],
        [True, "int_list", "@set"],
        [True, "int_inlined_list", "@set"],
        [True, "int_dict", "@index"],
    ],
)
def test_container_list(input_path, fix_container, attribute, container_type):
    schema_path = input_path("jsonld_context_multivalued_slot_cardinality.yaml")
    context = json.loads(ContextGenerator(schema_path, fix_multivalue_containers=fix_container).serialize())
    assert ("@container" in context["@context"][attribute].keys()) == fix_container
    if fix_container:
        assert context["@context"][attribute]["@container"] == container_type


def test_any_of_mixed_literal_and_class_prefers_literal(tmp_path):
    """When any_of mixes a literal type and a class, prefer the literal for coercion.

    Regression test for the bug where ``any_of: [{range: decimal}, {range: SomeClass}]``
    incorrectly collapsed to ``@type: "@id"`` instead of using the literal type.

    See:
    - https://github.com/linkml/linkml/issues/1483
    - https://github.com/linkml/linkml/issues/2970
    """
    schema = tmp_path / "mixed_any_of.yaml"
    schema.write_text(
        """
id: https://example.org/mixed
name: mixed_any_of
default_prefix: ex
imports:
  - linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/mixed/
  schema: http://schema.org/
  xsd: http://www.w3.org/2001/XMLSchema#
classes:
  QuantitativeValue:
    class_uri: schema:QuantitativeValue
    attributes:
      min_value:
        range: decimal
        slot_uri: schema:minValue
      max_value:
        range: decimal
        slot_uri: schema:maxValue
  Measurement:
    attributes:
      id: {identifier: true, range: string}
      acceleration_value:
        slot_uri: ex:accelerationValue
        any_of:
          - range: decimal
          - range: QuantitativeValue
      lane_count_value:
        slot_uri: ex:laneCountValue
        any_of:
          - range: integer
          - range: QuantitativeValue
      pure_object_ref:
        range: QuantitativeValue
        slot_uri: ex:pureObjectRef
      pure_literal:
        range: float
        slot_uri: ex:pureLiteral
""",
        encoding="utf-8",
    )

    context = json.loads(ContextGenerator(str(schema)).serialize())
    ctx = context["@context"]

    # Mixed any_of: literal type should win over @id
    assert ctx["acceleration_value"]["@type"] == "xsd:decimal", (
        "any_of with decimal + class should coerce to xsd:decimal, not @id"
    )
    assert ctx["lane_count_value"]["@type"] == "xsd:integer", (
        "any_of with integer + class should coerce to xsd:integer, not @id"
    )

    # Pure class range should still get @id
    assert ctx["pure_object_ref"]["@type"] == "@id"

    # Pure literal range should get its type
    assert ctx["pure_literal"]["@type"] == "xsd:float"


def test_any_of_all_classes_still_uses_id(tmp_path):
    """When all any_of branches are classes, @type should remain @id."""
    schema = tmp_path / "all_classes_any_of.yaml"
    schema.write_text(
        """
id: https://example.org/allcls
name: all_classes_any_of
default_prefix: ex
imports:
  - linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/allcls/
classes:
  A:
    attributes:
      id: {identifier: true, range: string}
  B:
    attributes:
      id: {identifier: true, range: string}
  Container:
    attributes:
      id: {identifier: true, range: string}
      ref:
        slot_uri: ex:ref
        any_of:
          - range: A
          - range: B
""",
        encoding="utf-8",
    )

    context = json.loads(ContextGenerator(str(schema)).serialize())
    assert context["@context"]["ref"]["@type"] == "@id"


def test_any_of_string_and_class_drops_coercion(tmp_path):
    """When any_of mixes string and class, no @type coercion should be emitted.

    xsd:string maps to no coercion in JSON-LD, so the literal branch
    effectively requests "no @type".
    """
    schema = tmp_path / "string_class_any_of.yaml"
    schema.write_text(
        """
id: https://example.org/strcls
name: string_class_any_of
default_prefix: ex
imports:
  - linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/strcls/
classes:
  Description:
    attributes:
      id: {identifier: true, range: string}
  Container:
    attributes:
      id: {identifier: true, range: string}
      desc:
        slot_uri: ex:desc
        any_of:
          - range: string
          - range: Description
""",
        encoding="utf-8",
    )

    context = json.loads(ContextGenerator(str(schema)).serialize())
    # String type maps to no coercion — @type should NOT be @id
    assert "@type" not in context["@context"]["desc"], (
        "any_of with string + class should not emit @type (string = no coercion)"
    )


def test_any_of_multiple_literal_types_and_class_drops_coercion(tmp_path):
    """Mixed any_of with conflicting literal types must avoid order dependence."""
    schema = tmp_path / "multiple_literal_class_any_of.yaml"
    schema.write_text(
        """
id: https://example.org/multi
name: multiple_literal_class_any_of
default_prefix: ex
imports:
  - linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/multi/
classes:
  QuantitativeValue:
    attributes:
      id: {identifier: true, range: string}
  Container:
    attributes:
      id: {identifier: true, range: string}
      polymorphic:
        slot_uri: ex:polymorphic
        any_of:
          - range: integer
          - range: string
          - range: QuantitativeValue
""",
        encoding="utf-8",
    )

    context = json.loads(ContextGenerator(str(schema)).serialize())
    assert "@type" not in context["@context"]["polymorphic"], (
        "any_of with conflicting literal types and a class should omit coercion"
    )


def test_exclude_imports(input_path):
    """With --exclude-imports, slots and classes from imported schemas
    must not appear in the generated JSON-LD context, while inherited
    slots on local classes are still included.

    Reuses the ShaclGenerator's exclude_imports test fixtures which define
    a BaseClass (with baseProperty) in an imported schema and an
    ExtendedClass (with extendedProperty, is_a: BaseClass) in the main schema.
    """
    context_text = ContextGenerator(
        input_path("shaclgen/exclude_imports.yaml"),
        mergeimports=True,
        exclude_imports=True,
    ).serialize()
    context = json.loads(context_text)
    ctx = context["@context"]

    # Local class and slot must be present
    assert "ExtendedClass" in ctx, f"Local class 'ExtendedClass' must appear in context, got: {list(ctx.keys())}"
    assert "extendedProperty" in ctx, f"Local slot 'extendedProperty' must appear in context, got: {list(ctx.keys())}"

    # Imported class and slot must NOT be present
    assert "BaseClass" not in ctx, "Imported class 'BaseClass' must not appear in exclude-imports context"
    assert "baseProperty" not in ctx, "Imported slot 'baseProperty' must not appear in exclude-imports context"


@pytest.mark.parametrize("mergeimports", [True, False], ids=["merge", "no-merge"])
def test_exclude_external_imports(tmp_path, mergeimports):
    """With --exclude-external-imports, elements from URL-based external
    vocabulary imports must not appear in the generated JSON-LD context,
    while local file imports and linkml standard imports are kept.

    When a schema imports terms from an external vocabulary (e.g. W3C VC
    v2), those terms already have context definitions in their own JSON-LD
    context file.  Re-defining them in the local context can conflict with
    @protected term definitions from the external context (JSON-LD 1.1
    section 4.1.11).
    """
    ext_dir = tmp_path / "ext"
    ext_dir.mkdir()
    (ext_dir / "external_vocab.yaml").write_text(
        textwrap.dedent("""\
            id: https://example.org/external-vocab
            name: external_vocab
            default_prefix: ext
            prefixes:
              linkml: https://w3id.org/linkml/
              ext: https://example.org/external-vocab/
            imports:
              - linkml:types
            slots:
              issuer:
                slot_uri: ext:issuer
                range: string
              validFrom:
                slot_uri: ext:validFrom
                range: date
            classes:
              ExternalCredential:
                class_uri: ext:ExternalCredential
                slots:
                  - issuer
                  - validFrom
        """),
        encoding="utf-8",
    )

    (tmp_path / "main.yaml").write_text(
        textwrap.dedent("""\
            id: https://example.org/main
            name: main
            default_prefix: main
            prefixes:
              linkml: https://w3id.org/linkml/
              main: https://example.org/main/
              ext: https://example.org/external-vocab/
            imports:
              - linkml:types
              - https://example.org/external-vocab
            slots:
              localName:
                slot_uri: main:localName
                range: string
            classes:
              LocalThing:
                class_uri: main:LocalThing
                slots:
                  - localName
        """),
        encoding="utf-8",
    )

    importmap = {"https://example.org/external-vocab": str(ext_dir / "external_vocab")}

    context_text = ContextGenerator(
        str(tmp_path / "main.yaml"),
        exclude_external_imports=True,
        mergeimports=mergeimports,
        importmap=importmap,
        base_dir=str(tmp_path),
    ).serialize()
    context = json.loads(context_text)
    ctx = context["@context"]

    # Local terms must be present
    assert "localName" in ctx or "local_name" in ctx, (
        f"Local slot missing with mergeimports={mergeimports}, got: {list(ctx.keys())}"
    )
    assert "LocalThing" in ctx, f"Local class missing with mergeimports={mergeimports}, got: {list(ctx.keys())}"

    # External vocabulary terms must NOT be present
    assert "issuer" not in ctx, f"External slot 'issuer' present with mergeimports={mergeimports}"
    assert "validFrom" not in ctx and "valid_from" not in ctx, (
        f"External slot 'validFrom' present with mergeimports={mergeimports}"
    )
    assert "ExternalCredential" not in ctx, (
        f"External class 'ExternalCredential' present with mergeimports={mergeimports}"
    )


def test_exclude_external_imports_preserves_linkml_types(tmp_path):
    """linkml:types (standard library import) must NOT be treated as external.

    The ``linkml:types`` import resolves to a URL internally
    (``https://w3id.org/linkml/types``), but it is a standard LinkML import,
    not a user-declared external vocabulary.  The ``_collect_external_elements``
    method filters by ``schema_key.startswith("http")`` — this test verifies
    that linkml built-in types (string, integer, date, etc.) survive the filter.
    """
    (tmp_path / "schema.yaml").write_text(
        textwrap.dedent("""\
            id: https://example.org/test
            name: test_linkml_types
            default_prefix: ex
            prefixes:
              linkml: https://w3id.org/linkml/
              ex: https://example.org/
            imports:
              - linkml:types
            slots:
              name:
                slot_uri: ex:name
                range: string
              age:
                slot_uri: ex:age
                range: integer
            classes:
              Person:
                class_uri: ex:Person
                slots:
                  - name
                  - age
        """),
        encoding="utf-8",
    )

    context_text = ContextGenerator(
        str(tmp_path / "schema.yaml"),
        exclude_external_imports=True,
    ).serialize()
    ctx = json.loads(context_text)["@context"]

    # Local classes and slots must be present
    assert "Person" in ctx, f"Local class 'Person' missing, got: {list(ctx.keys())}"
    assert "name" in ctx, f"Local slot 'name' missing, got: {list(ctx.keys())}"
    assert "age" in ctx, f"Local slot 'age' missing, got: {list(ctx.keys())}"


def test_exclude_external_imports_preserves_local_file_imports(tmp_path):
    """Local file imports (non-URL) must be preserved when exclude_external_imports is set.

    Only URL-based imports (http:// or https://) are considered external.
    File-path imports between local schemas must remain in the context.
    """
    local_dir = tmp_path / "local"
    local_dir.mkdir()
    (local_dir / "base.yaml").write_text(
        textwrap.dedent("""\
            id: https://example.org/base
            name: base
            default_prefix: base
            prefixes:
              linkml: https://w3id.org/linkml/
              base: https://example.org/base/
            imports:
              - linkml:types
            slots:
              baseField:
                slot_uri: base:baseField
                range: string
            classes:
              BaseRecord:
                class_uri: base:BaseRecord
                slots:
                  - baseField
        """),
        encoding="utf-8",
    )

    (tmp_path / "main.yaml").write_text(
        textwrap.dedent("""\
            id: https://example.org/main
            name: main
            default_prefix: main
            prefixes:
              linkml: https://w3id.org/linkml/
              main: https://example.org/main/
              base: https://example.org/base/
            imports:
              - linkml:types
              - local/base
            slots:
              localField:
                slot_uri: main:localField
                range: string
            classes:
              MainRecord:
                class_uri: main:MainRecord
                slots:
                  - localField
        """),
        encoding="utf-8",
    )

    context_text = ContextGenerator(
        str(tmp_path / "main.yaml"),
        exclude_external_imports=True,
        mergeimports=True,
        base_dir=str(tmp_path),
    ).serialize()
    ctx = json.loads(context_text)["@context"]

    # Local file import terms must be present
    assert "MainRecord" in ctx, f"Local class 'MainRecord' missing, got: {list(ctx.keys())}"
    assert "BaseRecord" in ctx, f"Local-file-imported class 'BaseRecord' missing, got: {list(ctx.keys())}"
    assert "baseField" in ctx or "base_field" in ctx, (
        f"Local-file-imported slot 'baseField' missing, got: {list(ctx.keys())}"
    )


def test_exclude_external_imports_works_with_mergeimports_false(tmp_path):
    """exclude_external_imports is effective even when mergeimports=False.

    Although mergeimports=False prevents most imported elements from appearing,
    external vocabulary elements can still leak into the context via the
    schema_map.  The exclude_external_imports flag catches these.
    """
    ext_dir = tmp_path / "ext"
    ext_dir.mkdir()
    (ext_dir / "external_vocab.yaml").write_text(
        textwrap.dedent("""\
            id: https://example.org/external-vocab
            name: external_vocab
            default_prefix: ext
            prefixes:
              linkml: https://w3id.org/linkml/
              ext: https://example.org/external-vocab/
            imports:
              - linkml:types
            slots:
              issuer:
                slot_uri: ext:issuer
                range: string
            classes:
              ExternalCredential:
                class_uri: ext:ExternalCredential
                slots:
                  - issuer
        """),
        encoding="utf-8",
    )

    (tmp_path / "main.yaml").write_text(
        textwrap.dedent("""\
            id: https://example.org/main
            name: main
            default_prefix: main
            prefixes:
              linkml: https://w3id.org/linkml/
              main: https://example.org/main/
              ext: https://example.org/external-vocab/
            imports:
              - linkml:types
              - https://example.org/external-vocab
            slots:
              localName:
                slot_uri: main:localName
                range: string
            classes:
              LocalThing:
                class_uri: main:LocalThing
                slots:
                  - localName
        """),
        encoding="utf-8",
    )

    importmap = {"https://example.org/external-vocab": str(ext_dir / "external_vocab")}

    ctx_text = ContextGenerator(
        str(tmp_path / "main.yaml"),
        exclude_external_imports=True,
        mergeimports=False,
        importmap=importmap,
        base_dir=str(tmp_path),
    ).serialize()
    ctx = json.loads(ctx_text)["@context"]

    # Local terms must still be present
    assert "LocalThing" in ctx, f"Local class missing, got: {list(ctx.keys())}"

    # External vocabulary terms must be excluded
    assert "issuer" not in ctx, "External slot 'issuer' should be excluded with mergeimports=False"
    assert "ExternalCredential" not in ctx, "External class should be excluded with mergeimports=False"


# ---------------------------------------------------------------------------
# Enum @type: @vocab context generation (JSON-LD 1.1 §4.2.3 + §4.1.8)
# ---------------------------------------------------------------------------


def _ctx_for_yaml(yaml_text: str, tmp_path, **kwargs) -> dict:
    """Generate a context from inline YAML and return the @context dict."""
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(textwrap.dedent(yaml_text), encoding="utf-8")
    ctx_text = ContextGenerator(str(schema_path), **kwargs).serialize()
    return json.loads(ctx_text)["@context"]


ELIGIBLE_ENUM_SCHEMA = """\
    id: https://example.org/test
    name: test
    default_prefix: test
    prefixes:
      linkml: https://w3id.org/linkml/
      test: https://example.org/test/
      myns: https://example.org/myns/
    imports:
      - linkml:types
    enums:
      ColorEnum:
        enum_uri: myns:Color
        permissible_values:
          Red:
            meaning: myns:Red
          Green:
            meaning: myns:Green
          Blue:
            meaning: myns:Blue
    slots:
      favorite_color:
        slot_uri: test:favoriteColor
        range: ColorEnum
    classes:
      Thing:
        class_uri: test:Thing
        slots:
          - favorite_color
"""


def test_eligible_enum_gets_vocab_coercion(tmp_path):
    """Enum where all values have meanings with matching text gets @type: @vocab."""
    ctx = _ctx_for_yaml(ELIGIBLE_ENUM_SCHEMA, tmp_path)

    slot_ctx = ctx["favorite_color"]
    assert slot_ctx["@type"] == "@vocab", "Eligible enum slot should have @type: @vocab"
    assert "@context" in slot_ctx
    scoped = slot_ctx["@context"]
    assert scoped["@vocab"] == "https://example.org/myns/"
    # SKOS mappings preserved for backward compat with structured values
    assert scoped["meaning"] == "@id"
    assert scoped["text"] == "skos:notation"
    assert scoped["description"] == "skos:prefLabel"


INELIGIBLE_TEXT_MISMATCH_SCHEMA = """\
    id: https://example.org/test
    name: test
    default_prefix: test
    prefixes:
      linkml: https://w3id.org/linkml/
      test: https://example.org/test/
      codes: https://example.org/codes/
    imports:
      - linkml:types
    enums:
      EventType:
        permissible_values:
          HIRE:
            meaning: codes:001
          FIRE:
            meaning: codes:002
    slots:
      event_type:
        slot_uri: test:eventType
        range: EventType
    classes:
      Event:
        class_uri: test:Event
        slots:
          - event_type
"""


def test_text_mismatch_falls_back_to_enum_context(tmp_path):
    """Enum where text != meaning local name falls back to ENUM_CONTEXT only."""
    ctx = _ctx_for_yaml(INELIGIBLE_TEXT_MISMATCH_SCHEMA, tmp_path)

    slot_ctx = ctx["event_type"]
    assert "@type" not in slot_ctx, "Ineligible enum should not get @type"
    scoped = slot_ctx["@context"]
    assert "@vocab" not in scoped, "Ineligible enum should not get scoped @vocab"
    assert scoped["meaning"] == "@id"


INELIGIBLE_NO_MEANING_SCHEMA = """\
    id: https://example.org/test
    name: test
    default_prefix: test
    prefixes:
      linkml: https://w3id.org/linkml/
      test: https://example.org/test/
    imports:
      - linkml:types
    enums:
      MoodEnum:
        permissible_values:
          happy:
            description: feeling happy
          sad:
            description: feeling sad
    slots:
      mood:
        slot_uri: test:mood
        range: MoodEnum
    classes:
      Person:
        class_uri: test:Person
        slots:
          - mood
"""


def test_no_meaning_falls_back_to_enum_context(tmp_path):
    """Enum where some values lack meaning falls back to ENUM_CONTEXT."""
    ctx = _ctx_for_yaml(INELIGIBLE_NO_MEANING_SCHEMA, tmp_path)

    slot_ctx = ctx["mood"]
    assert "@type" not in slot_ctx
    scoped = slot_ctx["@context"]
    assert "@vocab" not in scoped


INELIGIBLE_MIXED_NS_SCHEMA = """\
    id: https://example.org/test
    name: test
    default_prefix: test
    prefixes:
      linkml: https://w3id.org/linkml/
      test: https://example.org/test/
      ns1: https://example.org/ns1/
      ns2: https://example.org/ns2/
    imports:
      - linkml:types
    enums:
      MixedEnum:
        permissible_values:
          Foo:
            meaning: ns1:Foo
          Bar:
            meaning: ns2:Bar
    slots:
      mixed:
        slot_uri: test:mixed
        range: MixedEnum
    classes:
      Container:
        class_uri: test:Container
        slots:
          - mixed
"""


def test_mixed_namespaces_falls_back_to_enum_context(tmp_path):
    """Enum with values from different namespaces falls back to ENUM_CONTEXT."""
    ctx = _ctx_for_yaml(INELIGIBLE_MIXED_NS_SCHEMA, tmp_path)

    slot_ctx = ctx["mixed"]
    assert "@type" not in slot_ctx
    scoped = slot_ctx["@context"]
    assert "@vocab" not in scoped


def test_eligible_enum_bare_string_expands_to_iri(tmp_path):
    """End-to-end: bare string enum value expands to the correct IRI.

    Verifies the generated context enables the JSON-LD 1.1 expansion
    described in §4.2.3 (type coercion via @vocab).

    Uses rdflib's JSON-LD parser for expansion verification.
    """
    from rdflib import Graph, URIRef

    ctx = _ctx_for_yaml(ELIGIBLE_ENUM_SCHEMA, tmp_path)

    doc = {
        "@context": ctx,
        "@id": "urn:test:instance",
        "favorite_color": "Red",
    }

    g = Graph()
    g.parse(data=json.dumps(doc), format="json-ld")

    pred = URIRef("https://example.org/test/favoriteColor")
    objects = list(g.objects(URIRef("urn:test:instance"), pred))
    assert len(objects) == 1
    assert isinstance(objects[0], URIRef), f"Expected URIRef, got {type(objects[0]).__name__}: {objects[0]}"
    assert str(objects[0]) == "https://example.org/myns/Red"


def test_eligible_enum_structured_value_still_works(tmp_path):
    """Structured enum value {text, meaning} still expands correctly.

    The combined context (@type: @vocab + SKOS mappings) supports both
    bare strings and structured objects simultaneously.

    Uses rdflib's JSON-LD parser for expansion verification.
    """
    from rdflib import Graph, URIRef

    ctx = _ctx_for_yaml(ELIGIBLE_ENUM_SCHEMA, tmp_path)

    doc = {
        "@context": ctx,
        "@id": "urn:test:instance",
        "favorite_color": {
            "text": "Red",
            "meaning": "https://example.org/myns/Red",
        },
    }

    g = Graph()
    g.parse(data=json.dumps(doc), format="json-ld")

    pred = URIRef("https://example.org/test/favoriteColor")
    subjects = list(g.objects(URIRef("urn:test:instance"), pred))
    assert len(subjects) == 1
    # The meaning → @id mapping makes the structured value a node with @id
    assert isinstance(subjects[0], URIRef), f"Expected URIRef, got {type(subjects[0]).__name__}: {subjects[0]}"
    assert str(subjects[0]) == "https://example.org/myns/Red"


def test_kitchen_sink_employment_event_type_falls_back(kitchen_sink_path):
    """Kitchen sink EmploymentEventType (HIRE→bizcodes:001) must fall back."""
    ctx_text = ContextGenerator(kitchen_sink_path).serialize()
    ctx = json.loads(ctx_text)["@context"]

    # EmploymentEventType has text!=local (HIRE vs 001)
    # Slots using this enum should not get @type: @vocab
    if "employed_at" in ctx:
        slot_def = ctx["employed_at"]
        if isinstance(slot_def, dict) and "@context" in slot_def:
            assert "@vocab" not in slot_def.get("@context", {})
