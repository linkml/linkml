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


def test_xsd_anyuri_as_iri_flag():
    """Test that --xsd-anyuri-as-iri maps uri ranges to @type: @id.

    By default, ``range: uri`` (type_uri ``xsd:anyURI``) produces
    ``@type: xsd:anyURI`` (typed literal). With ``xsd_anyuri_as_iri=True``,
    it produces ``@type: @id`` (IRI node reference), aligning the JSON-LD
    context with the SHACL generator which already emits ``sh:nodeKind sh:IRI``
    for the same type.

    See:
      - W3C SHACL §4.8.1 sh:nodeKind (https://www.w3.org/TR/shacl/#NodeKindConstraintComponent)
      - JSON-LD 1.1 §4.2.2 Type Coercion (https://www.w3.org/TR/json-ld11/#type-coercion)
      - RDF 1.1 §3.3 Literals vs §3.2 IRIs (https://www.w3.org/TR/rdf11-concepts/)
    """
    schema_yaml = """
id: https://example.org/test-uri-context
name: test_uri_context

prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

default_prefix: ex
default_range: string

slots:
  homepage:
    range: uri
    slot_uri: ex:homepage
  node_ref:
    range: nodeidentifier
    slot_uri: ex:nodeRef
  name:
    range: string
    slot_uri: ex:name

classes:
  Thing:
    slots:
      - homepage
      - node_ref
      - name
"""
    # Default behaviour: uri → xsd:anyURI (backward compatible)
    ctx_default = json.loads(ContextGenerator(schema_yaml).serialize())["@context"]
    assert ctx_default["homepage"]["@type"] == "xsd:anyURI"

    # Opt-in: uri → @id (aligned with SHACL sh:nodeKind sh:IRI)
    ctx_iri = json.loads(ContextGenerator(schema_yaml, xsd_anyuri_as_iri=True).serialize())["@context"]
    assert ctx_iri["homepage"]["@type"] == "@id", (
        f"Expected @type: @id for uri range with xsd_anyuri_as_iri=True, got {ctx_iri['homepage'].get('@type')}"
    )

    # nodeidentifier is unaffected by the flag (not xsd:anyURI-typed)
    # Its default @type depends on URI_RANGES matching shex:nonLiteral;
    # we only verify the flag doesn't change its behaviour.
    assert ctx_default["node_ref"]["@type"] == ctx_iri["node_ref"]["@type"]

    # string → no @type regardless of flag
    assert "@type" not in ctx_default.get("name", {})
    assert "@type" not in ctx_iri.get("name", {})


def test_xsd_anyuri_as_iri_with_any_of():
    """The --xsd-anyuri-as-iri flag must also apply to ``any_of`` slots
    whose type branches include ``uri`` mixed with class ranges.

    ``_literal_coercion_for_ranges`` resolves mixed any_of type branches
    and must use the extended URI_RANGES when the flag is active.
    """
    schema_yaml = """
id: https://example.org/test-anyof-uri
name: test_anyof_uri

prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

default_prefix: ex
default_range: string

classes:
  Container:
    slots:
      - mixed_slot
  Target:
    class_uri: ex:Target

slots:
  mixed_slot:
    slot_uri: ex:mixed
    any_of:
      - range: Target
      - range: uri
"""
    # Default: mixed class+uri any_of — uri resolves to xsd:anyURI literal,
    # which disagrees with @id from the class branch → no coercion emitted
    ctx_default = json.loads(ContextGenerator(schema_yaml).serialize())["@context"]
    default_type = ctx_default.get("mixed_slot", {}).get("@type")
    assert default_type != "@id", f"Without flag, mixed any_of should not resolve to @id, got {default_type}"

    # With flag: uri branch now also resolves to @id, matching the class branch
    # → all branches agree → @id is emitted
    ctx_iri = json.loads(ContextGenerator(schema_yaml, xsd_anyuri_as_iri=True).serialize())["@context"]
    assert ctx_iri["mixed_slot"]["@type"] == "@id", (
        f"Expected @id for mixed any_of with flag, got {ctx_iri.get('mixed_slot', {}).get('@type')}"
    )


def test_xsd_anyuri_as_iri_owl():
    """OWL generator must produce owl:ObjectProperty for uri ranges when flag is set.

    Without the flag, ``range: uri`` produces ``owl:DatatypeProperty`` with
    ``rdfs:range xsd:anyURI``. With ``xsd_anyuri_as_iri=True``, it should
    produce ``owl:ObjectProperty`` (no rdfs:range restriction), aligning
    with the SHACL generator's ``sh:nodeKind sh:IRI``.
    """
    from rdflib import OWL, RDF, URIRef

    from linkml.generators.owlgen import OwlSchemaGenerator

    schema_yaml = """
id: https://example.org/test-owl-uri
name: test_owl_uri
prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  homepage:
    range: uri
    slot_uri: ex:homepage
  name:
    range: string
    slot_uri: ex:name
classes:
  Thing:
    slots:
      - homepage
      - name
"""
    # Default: uri → DatatypeProperty (must disable type_objects which
    # unconditionally returns ObjectProperty for all type-ranged slots)
    gen_default = OwlSchemaGenerator(schema_yaml, type_objects=False)
    g_default = gen_default.as_graph()
    homepage_uri = URIRef("https://example.org/homepage")
    default_rdf_type = set(g_default.objects(homepage_uri, RDF.type))
    assert OWL.DatatypeProperty in default_rdf_type, (
        f"Without flag, homepage should be DatatypeProperty, got {default_rdf_type}"
    )

    # With flag: uri → ObjectProperty
    gen_iri = OwlSchemaGenerator(schema_yaml, xsd_anyuri_as_iri=True, type_objects=False)
    g_iri = gen_iri.as_graph()
    iri_rdf_type = set(g_iri.objects(homepage_uri, RDF.type))
    assert OWL.ObjectProperty in iri_rdf_type, f"With flag, homepage should be ObjectProperty, got {iri_rdf_type}"
    assert OWL.DatatypeProperty not in iri_rdf_type, (
        f"With flag, homepage should NOT be DatatypeProperty, got {iri_rdf_type}"
    )

    # String slot must remain DatatypeProperty regardless of flag
    name_uri = URIRef("https://example.org/name")
    name_rdf_type = set(g_iri.objects(name_uri, RDF.type))
    assert OWL.DatatypeProperty in name_rdf_type, f"String slot should remain DatatypeProperty, got {name_rdf_type}"


def test_xsd_anyuri_as_iri_uriorcurie_range():
    """``uriorcurie`` also maps to ``xsd:anyURI`` and must behave identically
    to ``uri`` when the ``--xsd-anyuri-as-iri`` flag is active.

    This is a high-priority coverage gap: ``uriorcurie`` is distinct from
    ``uri`` at the LinkML level but shares the same XSD type.
    """
    schema_yaml = """
id: https://example.org/test-uriorcurie
name: test_uriorcurie

prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

default_prefix: ex
default_range: string

slots:
  reference:
    range: uriorcurie
    slot_uri: ex:reference
  homepage:
    range: uri
    slot_uri: ex:homepage

classes:
  Thing:
    slots:
      - reference
      - homepage
"""
    ctx_default = json.loads(ContextGenerator(schema_yaml).serialize())["@context"]
    assert ctx_default["reference"]["@type"] == "xsd:anyURI"
    assert ctx_default["homepage"]["@type"] == "xsd:anyURI"

    ctx_iri = json.loads(ContextGenerator(schema_yaml, xsd_anyuri_as_iri=True).serialize())["@context"]
    assert ctx_iri["reference"]["@type"] == "@id", "uriorcurie should map to @id with xsd_anyuri_as_iri=True"
    assert ctx_iri["homepage"]["@type"] == "@id", "uri should map to @id with xsd_anyuri_as_iri=True"


def test_xsd_anyuri_as_iri_curie_range_unchanged():
    """``curie`` maps to ``xsd:string`` (not ``xsd:anyURI``), so the flag
    must NOT affect its coercion.

    This documents the cross-type boundary: ``uri`` and ``uriorcurie``
    share ``xsd:anyURI``, but ``curie`` uses ``xsd:string``.
    """
    schema_yaml = """
id: https://example.org/test-curie
name: test_curie

prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

default_prefix: ex
default_range: string

slots:
  curie_slot:
    range: curie
    slot_uri: ex:curieSlot
  uri_slot:
    range: uri
    slot_uri: ex:uriSlot

classes:
  Thing:
    slots:
      - curie_slot
      - uri_slot
"""
    ctx_default = json.loads(ContextGenerator(schema_yaml).serialize())["@context"]
    ctx_iri = json.loads(ContextGenerator(schema_yaml, xsd_anyuri_as_iri=True).serialize())["@context"]

    # curie (xsd:string) must be unaffected by the flag
    curie_default = ctx_default.get("curie_slot", {}).get("@type")
    curie_iri = ctx_iri.get("curie_slot", {}).get("@type")
    assert curie_default == curie_iri, f"curie coercion should not change with flag: {curie_default} vs {curie_iri}"

    # uri (xsd:anyURI) must change — sanity check
    assert ctx_iri["uri_slot"]["@type"] == "@id"


def test_xsd_anyuri_as_iri_owl_curie_unchanged():
    """OWL generator must keep ``range: curie`` as DatatypeProperty even with flag.

    ``curie`` maps to ``xsd:string`` (not ``xsd:anyURI``), so the
    ``--xsd-anyuri-as-iri`` flag must not promote it to ObjectProperty.
    This verifies cross-generator consistency: the JSON-LD context generator
    already correctly excludes ``curie`` via ``URI_RANGES_WITH_XSD``; the
    OWL generator must match via ``is_xsd_anyuri_range()``.
    """
    from rdflib import OWL, RDF, URIRef

    from linkml.generators.owlgen import OwlSchemaGenerator

    schema_yaml = """
id: https://example.org/test-owl-curie
name: test_owl_curie
prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  compact_id:
    range: curie
    slot_uri: ex:compactId
  homepage:
    range: uri
    slot_uri: ex:homepage
classes:
  Thing:
    slots:
      - compact_id
      - homepage
"""
    compact_id_uri = URIRef("https://example.org/compact_id")
    homepage_uri = URIRef("https://example.org/homepage")

    # With flag: curie must stay DatatypeProperty, uri must become ObjectProperty
    gen = OwlSchemaGenerator(schema_yaml, xsd_anyuri_as_iri=True, type_objects=False)
    g = gen.as_graph()

    curie_types = set(g.objects(compact_id_uri, RDF.type))
    assert OWL.DatatypeProperty in curie_types, f"curie slot must remain DatatypeProperty with flag, got {curie_types}"
    assert OWL.ObjectProperty not in curie_types, (
        f"curie slot must NOT become ObjectProperty with flag, got {curie_types}"
    )

    # Sanity: uri must become ObjectProperty
    uri_types = set(g.objects(homepage_uri, RDF.type))
    assert OWL.ObjectProperty in uri_types, f"uri slot should be ObjectProperty with flag, got {uri_types}"


def test_xsd_anyuri_as_iri_cli_flag():
    """Verify the ``--xsd-anyuri-as-iri`` flag is wired through Click."""
    import tempfile
    from pathlib import Path

    from click.testing import CliRunner

    from linkml.generators.jsonldcontextgen import cli

    schema_yaml = """
id: https://example.org/test-cli
name: test_cli

prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

default_prefix: ex
default_range: string

slots:
  homepage:
    range: uri
    slot_uri: ex:homepage

classes:
  Thing:
    slots:
      - homepage
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        schema_path = Path(tmpdir) / "test.yaml"
        schema_path.write_text(schema_yaml)

        runner = CliRunner()

        # Without flag
        result_default = runner.invoke(cli, [str(schema_path)])
        assert result_default.exit_code == 0, result_default.output
        ctx_default = json.loads(result_default.output)["@context"]
        assert ctx_default["homepage"]["@type"] == "xsd:anyURI"

        # With flag
        result_iri = runner.invoke(cli, [str(schema_path), "--xsd-anyuri-as-iri"])
        assert result_iri.exit_code == 0, result_iri.output
        ctx_iri = json.loads(result_iri.output)["@context"]
        assert ctx_iri["homepage"]["@type"] == "@id"
