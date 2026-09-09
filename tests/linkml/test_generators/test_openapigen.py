from pathlib import Path

import pytest
import yaml
from openapi_spec_validator import OpenAPIV30SpecValidator, validate
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError
from referencing.exceptions import PointerToNowhere

from linkml.generators.openapigen import OVERRIDABLE_SCHEMA_KEYS, OpenApiGenerator


def gen_openapi_spec(head_path, kitchen_sink_path):
    openapigen = OpenApiGenerator(kitchen_sink_path)
    return openapigen.serialize(head_path)


@pytest.fixture
def openapi_spec(input_path, kitchen_sink_path):
    head_path = str(input_path("openapi/spec-head.openapi.yaml"))
    openapigen = OpenApiGenerator(kitchen_sink_path)
    return yaml.safe_load(openapigen.serialize(head_path))


def test_openapi(input_path, kitchen_sink_path):
    """Test if generation succeeds without failure and returns valid YAML."""
    head_path = str(input_path("openapi/spec-head.openapi.yaml"))
    openapi_spec = gen_openapi_spec(head_path, kitchen_sink_path)
    # ensure that valid YAML has been generated
    assert yaml.safe_load(openapi_spec)
    # ensure that valid OpenAPI spec has been generated
    assert validate(yaml.safe_load(openapi_spec), cls=OpenAPIV30SpecValidator) is None


def test_openapi_missing_template(kitchen_sink_path):
    """Test that serialize raises ValueError when no template file is provided."""
    with pytest.raises(ValueError, match="An OpenAPI template file is required"):
        OpenApiGenerator(kitchen_sink_path).serialize()


def test_openapi_fixed_template(input_path, kitchen_sink_path):
    """Test that serialize raises ValueError when no template file is provided."""
    head_path = str(input_path("openapi/spec-fixed.openapi.yaml"))
    oa_spec = OpenApiGenerator(kitchen_sink_path).serialize(head_path)
    assert Path(head_path).read_text() == oa_spec


def test_openapi_spec_no_defs_references(openapi_spec):
    """Test that all $defs references are converted to components/schemas."""
    for schema in openapi_spec["components"]["schemas"].values():
        assert "#/$defs/" not in str(schema)


def test_openapi_spec_const_to_enum_conversion(openapi_spec):
    """Test that const values are converted to single-item enum arrays."""
    person = openapi_spec["components"]["schemas"]["Person"]
    assert person["properties"]["species_name"]["enum"] == ["human"]
    assert person["properties"]["stomach_count"]["enum"] == [1]
    assert "const" not in person["properties"]["species_name"]
    assert "const" not in person["properties"]["stomach_count"]


def test_openapi_spec_class_level_title_stripped(openapi_spec):
    """Test that class-level title (redundant with dict key) is removed but property-level description preserved."""
    person = openapi_spec["components"]["schemas"]["Person"]
    assert "title" not in person
    assert person["properties"]["age_in_years"]["description"] == "number of years since birth"


def test_openapi_spec_nullable_type_conversion(openapi_spec):
    """Test that nullable type arrays are converted to anyOf."""
    emp_event = openapi_spec["components"]["schemas"]["EmploymentEvent"]
    assert "anyOf" in emp_event["properties"]["type"]
    assert "type" not in emp_event["properties"]["type"] or not isinstance(
        emp_event["properties"]["type"]["type"], list
    )


def test_openapi_spec_schemas_are_extensible(openapi_spec):
    """Test that generated class schemas are extensible (additionalProperties not false).

    APIs are typically extended backwards-compatibly by adding new objects or new
    attributes to existing objects. Closed schemas (additionalProperties: false) block
    that, so the generated OpenAPI schemas must stay open.
    """
    for name, schema in openapi_spec["components"]["schemas"].items():
        assert schema.get("additionalProperties") is not False, (
            f"schema '{name}' is closed (additionalProperties: false), blocking API extension"
        )


def test_resources_presence_and_absence(openapi_spec):
    # ensure expected resource schemas are present
    assert "MarriageEvent" in openapi_spec["components"]["schemas"].keys()
    assert "MedicalEvent" in openapi_spec["components"]["schemas"].keys()
    assert "DiagnosisConcept" in openapi_spec["components"]["schemas"].keys()
    assert "Person" in openapi_spec["components"]["schemas"].keys()
    # ensure unneeded resource schemas are not present
    assert "AnyOfSimpleType" not in openapi_spec["components"]["schemas"].keys()


def test_printout_template(kitchen_sink_path):
    """Test that printout_template returns a valid YAML generic template."""
    output = OpenApiGenerator(kitchen_sink_path).printout_template()
    parsed = yaml.safe_load(output)
    assert parsed["openapi"] == "3.0.3"
    assert "paths" in parsed
    assert "schemas" in parsed["components"]
    # the schema id from kitchen_sink must appear in the template
    assert "https://w3id.org/linkml/tests/kitchen_sink" in output


def test_schema_id_mismatch_raises(input_path, kitchen_sink_path):
    """Test that a mismatched x-linkml-schema raises ValueError with a descriptive message."""
    head_path = str(input_path("openapi/spec-wrong-schema-id.openapi.yaml"))
    with pytest.raises(ValueError, match="x-linkml-schema"):
        OpenApiGenerator(kitchen_sink_path).serialize(head_path)


def test_missing_x_linkml_source_raises(input_path):
    """Test that a template schema missing x-linkml-source raises a descriptive KeyError.

    x-linkml-schema presence/value are validated nicely, but x-linkml-source was
    skipped, surfacing as a bare ``KeyError: 'x-linkml-source'`` during instantiation.
    """
    schema_path = str(input_path("openapi/schema_missing_xlinkml_source.yaml"))
    head_path = str(input_path("openapi/spec-missing-x-linkml-source.openapi.yaml"))
    with pytest.raises(KeyError, match="Bar.*missing required 'x-linkml-source'"):
        OpenApiGenerator(schema_path, keep_unreferenced=True).serialize(head_path)


def test_referenced_parameter_does_not_crash(input_path):
    """Test that a template parameter given as a $ref does not raise KeyError.

    A parameter entry of the form ``{$ref: '#/components/parameters/Limit'}`` has no
    ``schema`` key of its own (the schema lives inside ``components/parameters``), so
    reading ``param_spec["schema"]`` unconditionally crashed before generation.
    """
    schema_path = str(input_path("openapi/schema_referenced_parameter.yaml"))
    head_path = str(input_path("openapi/spec-referenced-parameter.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(schema_path).serialize(head_path))
    # the reusable parameter survives untouched
    assert spec["paths"]["/foo"]["get"]["parameters"] == [{"$ref": "#/components/parameters/Limit"}]
    # and the endpoint schema is generated as usual
    assert "Foo" in spec["components"]["schemas"]
    assert validate(spec, cls=OpenAPIV30SpecValidator) is None


def test_missing_schema_declaration_raises(tmp_path, kitchen_sink_path):
    """Test that referencing a non-existent schema in the template raises an error."""
    template = tmp_path / "bad.yaml"
    template.write_text(
        "openapi: 3.0.3\ninfo:\n  title: t\n  version: '1'\n"
        "paths:\n  /x:\n    get:\n"
        "      responses:\n"
        "        '200':\n"
        "          description: test\n"
        "          content:\n"
        "            application/json:\n"
        "              schema:\n"
        "                $ref: '#/components/schemas/NonExistent'\n"
        "components:\n"
        "  schemas: {}\n"
    )
    # The OpenAPI validator resolves $ref and catches a missing target
    with pytest.raises(PointerToNowhere):
        OpenApiGenerator(kitchen_sink_path).serialize(str(template))


def test_openapi_type_constraints(input_path):
    """Test that LinkML types with constraints (e.g., pattern) are properly generated in the spec."""
    schema_path = str(input_path("openapi/schema_type_constraints.yaml"))
    head_path = str(input_path("openapi/spec-types.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(schema_path).serialize(head_path))
    schemas = spec["components"]["schemas"]
    # the type schema is exposed under the template's resource name
    code_str = schemas["CodeStringRef"]
    assert code_str["type"] == "string"
    assert code_str["pattern"] == "^[A-Z]{2,10}$"
    assert code_str["description"] == "A 2-10 character uppercase code"
    assert validate(spec, cls=OpenAPIV30SpecValidator) is None
    for schema in schemas.values():
        assert "#/$defs/" not in str(schema)


def test_renaming(input_path, kitchen_sink_path):
    """Test that resource names differing from LinkML class names are renamed throughout the spec."""
    head_path = str(input_path("openapi/spec-renaming.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path).serialize(head_path))
    schemas = spec["components"]["schemas"]
    # resource is exposed under the template name, not the LinkML class name
    assert "PersonResource" in schemas
    assert "Person" not in schemas
    # all $ref values in the spec must use the renamed
    assert "Person" not in str(spec).replace("PersonResource", "")


def test_openapi_examples_converted_to_singular_example(input_path):
    """Test that a slot's ``examples`` list is converted to OpenAPI's singular ``example``.

    OpenAPI 3.0 has no plural ``examples`` keyword on the Schema Object, only ``example``.
    Without this conversion, generation fails validation entirely for any schema with a
    slot declaring ``examples`` -- this is a blocker, not a cosmetic gap.
    """
    schema_path = str(input_path("openapi/schema_examples.yaml"))
    head_path = str(input_path("openapi/spec-examples.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(schema_path).serialize(head_path))
    name_schema = spec["components"]["schemas"]["WithExamples"]["properties"]["name"]
    # first example is kept; the plural form is gone entirely
    assert name_schema["example"] == "sample"
    assert "examples" not in name_schema
    assert validate(spec, cls=OpenAPIV30SpecValidator) is None


def test_template_text_preserved(input_path, kitchen_sink_path):
    """Test that everything above ``components/schemas`` is emitted verbatim.

    The generator no longer YAML round-trips the whole template (which would drop
    comments and normalise quoting/styling). Only the ``components/schemas`` section
    is regenerated; the header, paths and any comments above it must survive intact.
    """
    head_path = str(input_path("openapi/spec-comments.openapi.yaml"))
    result = OpenApiGenerator(kitchen_sink_path).serialize(head_path)
    # comments are dropped by a YAML round-trip but preserved by text handling
    assert "# top-level comment must survive round-trip" in result
    assert "# this endpoint comment must survive" in result
    # original quoting style is preserved (round-trip would normalise this)
    assert "version: '1.0.0'" in result
    # the untouched template prefix is emitted byte-for-byte
    template_text = Path(head_path).read_text()
    schemas_marker = "\ncomponents:\n"
    prefix = template_text[: template_text.index(schemas_marker) + len(schemas_marker)]
    assert result.startswith(prefix)


def test_unreferenced_schema_removed_by_default(input_path, kitchen_sink_path):
    """Test that template schemas not referenced by any endpoint are removed by default."""
    head_path = str(input_path("openapi/spec-keep-unreferenced.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "Person" in schemas
    # OpaqueEvent(OpenAPI)/MarriageEvent(LinkML) is declared in the template but no endpoint references it
    assert "MarriageEvent" not in schemas


def test_keep_unreferenced_preserves_template_schema(input_path, kitchen_sink_path):
    """Test that keep_unreferenced retains template schemas not referenced by any endpoint.

    Unreferenced sub-schemas can convey objects that are opaque to the API but relevant
    to clients (e.g. present in provided artifacts). The keep_unreferenced flag makes
    their removal switchable.
    """
    head_path = str(input_path("openapi/spec-keep-unreferenced.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path, keep_unreferenced=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "Person" in schemas
    # OpaqueEvent(OpenAPI)/MarriageEvent(LinkML) is kept even though no endpoint references it,
    # and is published under the OpenAPI name the template gave it, not the LinkML one
    assert "OpaqueEvent" in schemas
    assert "MarriageEvent" not in schemas


def test_unreferenced_chain_pruned_by_default(input_path):
    """Test that a chain of mutually-referencing unreferenced schemas is pruned in one pass.

    ``Foo Bar`` (note the space in the name) references ``Baz Qux`` but neither is
    reachable from the endpoint-seeded ``Foo``. A naive single prune pass that only drops
    schemas *directly* citing an unreferenced name would keep ``Baz Qux`` (it is only
    referenced by ``Foo Bar``, and ``Foo Bar`` is dropped for not being referenced at all);
    the reference closure must remove the whole island. Space-named classes also exercise
    the YAML quoting of schema keys and ``$ref`` targets.
    """
    schema_path = str(input_path("openapi/schema_chain_unreferenced.yaml"))
    head_path = str(input_path("openapi/spec-chain-unreferenced.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(schema_path).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "Foo" in schemas
    assert "Foo Bar" not in schemas
    assert "Baz Qux" not in schemas


def test_keep_unreferenced_pulls_transitive_chain(input_path):
    """Test that keep_unreferenced retains a declared schema and its transitive dependencies.

    The template declares ``Foo Bar`` (with a space in its name, unreferenced by any
    endpoint) alongside ``Foo``. With ``keep_unreferenced`` the declared ``Foo Bar`` is
    kept, and its dependency ``Baz Qux`` — which is not itself declared in the template —
    must be kept too, because pruning out ``Baz Qux`` would leave the kept ``Foo Bar``
    with a dangling reference.
    """
    schema_path = str(input_path("openapi/schema_chain_unreferenced.yaml"))
    head_path = str(input_path("openapi/spec-chain-unreferenced.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(schema_path, keep_unreferenced=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "Foo" in schemas
    assert "Foo Bar" in schemas
    assert "Baz Qux" in schemas


def test_keep_unreferenced_does_not_add_unrelated_schemas(input_path):
    """Test that keep_unreferenced stays scoped to the template, not "dump everything".

    The chain schema also contains classes not reachable from ``Foo`` or the template
    declarations. ``keep_unreferenced`` only keeps the template-declared schemas and their
    transitive dependencies — it must not pull in the whole schema. Here the only other
    hidden class in the fixture is ``Baz Qux`` (already pulled by ``Foo Bar``), so a
    dedicated fixture with an unrelated class proves the flag does not regress to dumping
    every class.
    """
    schema_path = str(input_path("openapi/schema_unreferenced_with_unrelated.yaml"))
    head_path = str(input_path("openapi/spec-keep-scoped.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(schema_path, keep_unreferenced=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "Foo" in schemas
    output = "".join(str(spec))
    # the unrelated class is not pulled in
    assert "Unrelated" not in output


def test_enums_as_separate_schemas_by_default(openapi_spec):
    """Test that enums are emitted as separate sub-schemas referenced via $ref by default."""
    schemas = openapi_spec["components"]["schemas"]
    # the enum has its own schema entry
    assert "EmploymentEventType" in schemas
    assert schemas["EmploymentEventType"]["enum"] == ["HIRE", "FIRE", "PROMOTION", "TRANSFER"]
    # and is referenced, not inlined, by the owning class
    type_schema = schemas["EmploymentEvent"]["properties"]["type"]
    assert {"$ref": "#/components/schemas/EmploymentEventType"} in type_schema["anyOf"]


def test_inline_enums_inlines_enum_schemas(input_path, kitchen_sink_path):
    """Test that inline_enums inlines enum sub-schemas into their parents.

    With the flag set, an enum no longer gets its own ``components/schemas`` entry;
    instead its definition is inlined where it was referenced.
    """
    head_path = str(input_path("openapi/spec-head.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path, inline_enums=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    # the enum no longer has a standalone schema entry
    assert "EmploymentEventType" not in schemas
    # its values are inlined where it was referenced
    type_schema = schemas["EmploymentEvent"]["properties"]["type"]
    inlined = [member for member in type_schema["anyOf"] if member.get("enum")]
    assert any(member["enum"] == ["HIRE", "FIRE", "PROMOTION", "TRANSFER"] for member in inlined)
    # no dangling $ref to the removed enum schema remains
    assert "EmploymentEventType" not in str(spec)


def test_inline_enums_does_not_inline_types(input_path):
    """Test that inline_enums does not mistake fixed-value LinkML types for enums.

    A type with ``equals_string`` becomes a single-element ``enum`` after the
    ``const`` -> ``enum`` transform. A naive enum detection would then inline it away
    (``_inline_enum_schemas`` matches any schema with ``enum`` and no ``properties``);
    types must keep their named schema entry even when inlining is enabled.
    """
    schema_path = str(input_path("openapi/schema_types_and_enums.yaml"))
    head_path = str(input_path("openapi/spec-types-enums.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(schema_path, inline_enums=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    # the fixed-value type keeps its own named schema entry (not inlined)
    assert "FixedType" in schemas
    assert schemas["FixedType"]["enum"] == ["fixed-value"]
    assert schemas["FixedType"]["type"] == "string"


def test_inline_enums_disabled_keeps_types_and_enums_separate(input_path):
    """Test that with inline_enums disabled both types and enums keep separate schema entries."""
    schema_path = str(input_path("openapi/schema_types_and_enums.yaml"))
    head_path = str(input_path("openapi/spec-types-enums.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(schema_path, inline_enums=False).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "FixedType" in schemas
    assert schemas["FixedType"]["enum"] == ["fixed-value"]
    assert schemas["FixedType"]["type"] == "string"


def test_inline_enums_keeps_endpoint_referenced_enum(input_path):
    """Test that inline_enums does not inline an enum referenced directly by an endpoint.

    Inlining removes the enum's standalone ``components/schemas`` entry, which would
    leave the endpoint's ``$ref`` dangling. An enum that is itself the seeded schema of an
    endpoint must therefore keep its entry even when inlining is enabled.
    """
    schema_path = str(input_path("openapi/schema_endpoint_enum.yaml"))
    head_path = str(input_path("openapi/spec-endpoint-enum.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(schema_path, inline_enums=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "FixedEnum" in schemas
    assert schemas["FixedEnum"]["enum"] == ["FOO", "BAR"]
    assert spec["paths"]["/fixed-enum"]["get"]["responses"]["200"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/FixedEnum"
    }


def test_inline_enums_does_not_inline_renamed_enums(input_path):
    """Test that inlining a renamed enum does not bypass the type guard.

    When the endpoint refers to a LinkML ``enum`` under a different OpenAPI name, the
    rename must not hide the fact that the source element is an enum. Otherwise the schema
    would be inlined away, leaving the endpoint's ``$ref`` dangling.
    """
    schema_path = str(input_path("openapi/schema_types_and_enums.yaml"))
    head_path = str(input_path("openapi/spec-renamed-type.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(schema_path, inline_enums=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "Fixed" in schemas
    assert schemas["Fixed"]["enum"] == ["fixed-value"]
    assert spec["paths"]["/fixed"]["get"]["responses"]["200"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/Fixed"
    }


def test_inline_enums_shared_enum_no_yaml_anchors(input_path):
    """Test that inlining a shared enum does not emit YAML anchors.

    When the same enum is referenced from two classes, the inlined copy must not be the
    very same Python object: reusing the object makes ``yaml.dump`` emit an ``&idNNN``
    anchor with an ``*idNNN`` alias for the second reference. The generated YAML must
    contain no anchors or aliases.
    """
    schema_path = str(input_path("openapi/schema_shared_enum.yaml"))
    head_path = str(input_path("openapi/spec-shared-enum.openapi.yaml"))
    result = OpenApiGenerator(schema_path, inline_enums=True).serialize(head_path)
    spec = yaml.safe_load(result)
    color_foo = spec["components"]["schemas"]["Foo"]["properties"]["color"]
    color_bar = spec["components"]["schemas"]["Bar"]["properties"]["color"]
    # both classes carry the inlined enum definition
    assert color_foo["enum"] == ["FOO", "BAR"]
    assert color_bar["enum"] == ["FOO", "BAR"]
    # no YAML anchor/alias markers leak into the emitted document
    assert "&id" not in result
    assert "*id" not in result
    # the duplicated values must not alias the same object instance
    assert color_foo is not color_bar


def test_inline_enums_preserves_slot_description(input_path):
    """Test that inlining an enum keeps the slot-level description of the referencing property.

    A property that references an enum carries its own ``description`` next to the
    ``$ref``. Inlining must merge the enum definition into that property without
    discarding the slot-level ``description`` (the enum's own, here empty, description
    must not eclipse it).
    """
    schema_path = str(input_path("openapi/schema_enum_slot_description.yaml"))
    head_path = str(input_path("openapi/spec-enum-slot-description.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(schema_path, inline_enums=True).serialize(head_path))
    color = spec["components"]["schemas"]["Foo"]["properties"]["color"]
    assert color["enum"] == ["FOO", "BAR"]
    assert color["description"] == "the color of foo"


def test_no_dangling_references_for_valid_schema(openapi_spec):
    """Test that a valid schema produces a spec whose every $ref resolves."""
    schema_names = set(openapi_spec["components"]["schemas"].keys())

    def _refs(obj):
        if isinstance(obj, dict):
            if "$ref" in obj and isinstance(obj["$ref"], str):
                yield obj["$ref"]
            for value in obj.values():
                yield from _refs(value)
        elif isinstance(obj, list):
            for item in obj:
                yield from _refs(item)

    for ref in _refs(openapi_spec):
        assert ref.startswith("#/components/schemas/")
        assert ref.removeprefix("#/components/schemas/") in schema_names


def test_lowercase_class_name_preserved(input_path, kitchen_sink_path):
    """Test that a lowercase LinkML class name is preserved, not camelCased, in the spec.

    ``JsonSchemaGenerator`` camelCases ``$defs`` keys unless ``preserve_names=True``.
    In kitchen_sink the class ``activity`` (lowercase) is transitively reachable from
    ``Dataset`` via the ``activities`` slot. Without name preservation the emitted schema
    is keyed ``Activity`` while the ``$ref`` from ``Dataset`` points to ``activity``,
    yielding a missing schema and a dangling reference.
    """
    head_path = str(input_path("openapi/spec-lowercase-class.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path).serialize(head_path))
    schemas = spec["components"]["schemas"]
    # the LinkML name is preserved verbatim, not camelCased
    assert "activity" in schemas
    assert "Activity" not in schemas
    # Dataset references the activity schema under its original name
    assert schemas["Dataset"]["properties"]["activities"]["items"] == {"$ref": "#/components/schemas/activity"}
    # the produced spec is valid (no dangling reference)
    assert validate(spec, cls=OpenAPIV30SpecValidator) is None


def test_dangling_reference_raises(input_path, kitchen_sink_path):
    """Test that a generated spec containing an unresolvable $ref is rejected.

    The template declares a ``Foo`` schema sourced from a non-existent LinkML class,
    so no schema is generated for it while an endpoint still references it. The
    generator must detect the dangling ``$ref`` and fail loudly.
    """
    head_path = str(input_path("openapi/spec-dangling-ref.openapi.yaml"))
    with pytest.raises(ValueError, match="Dangling .ref"):
        OpenApiGenerator(kitchen_sink_path).serialize(head_path)


def test_dangling_reference_reports_all(input_path, kitchen_sink_path):
    """All dangling ``$ref`` targets must be gathered and reported together, not just the first one.

    The template declares two schemas (``Foo`` and ``Bar``) sourced from non-existent LinkML classes,
    each referenced by its own endpoint. The single raised error must mention both.
    """
    head_path = str(input_path("openapi/spec-dangling-refs-multiple.openapi.yaml"))
    with pytest.raises(ValueError, match="Dangling .ref") as exc_info:
        OpenApiGenerator(kitchen_sink_path).serialize(head_path)
    message = str(exc_info.value)
    assert "#/components/schemas/Foo" in message
    assert "#/components/schemas/Bar" in message


def test_refs_to_non_schema_components_allowed(input_path, kitchen_sink_path):
    """Test that $refs to reusable components other than schemas (e.g. responses) are allowed.

    The dangling-reference check must resolve every internal ``$ref`` against its own
    ``components`` section rather than assuming all targets live under ``schemas``.
    """
    head_path = str(input_path("openapi/spec-shared-responses.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path).serialize(head_path))
    # the reusable response survives and is still referenced by the endpoint
    assert "NotFound" in spec["components"]["responses"]
    assert spec["paths"]["/foo"]["get"]["responses"]["404"] == {"$ref": "#/components/responses/NotFound"}
    # the schema is generated as usual
    assert "Person" in spec["components"]["schemas"]
    assert validate(spec, cls=OpenAPIV30SpecValidator) is None


@pytest.fixture
def override_text(input_path):
    """Raw generated YAML for the template-annotation-override fixtures."""
    schema_path = str(input_path("openapi/schema_template_overrides.yaml"))
    head_path = str(input_path("openapi/spec-template-overrides.openapi.yaml"))
    return OpenApiGenerator(schema_path).serialize(head_path)


@pytest.fixture
def override_spec(override_text):
    """Parsed generated spec for the template-annotation-override fixtures."""
    return yaml.safe_load(override_text)


# The two tests below split `OVERRIDABLE_SCHEMA_KEYS` between them along different axes;
# `test_overridable_key_coverage_is_complete` asserts the split leaves no key untested.
DESCRIPTION_OVERRIDE_CASES = [
    ("Described", "class description from the template"),
    ("Colour", "enum description from the template"),
    ("FixedRef", "type description from the template"),
]
NON_DESCRIPTION_OVERRIDE_CASES = [
    ("title", "Described Title"),
    ("example", {"color": "RED"}),
    ("externalDocs", {"url": "https://example.org/docs", "description": "more"}),
    ("deprecated", True),
]


@pytest.mark.parametrize(("schema_name", "expected"), DESCRIPTION_OVERRIDE_CASES)
def test_template_description_overrides_linkml_description(override_spec, schema_name, expected):
    """Test that a description declared in the template wins over the LinkML-derived one.

    The LinkML value is the default; a template placeholder that explicitly declares an
    annotation signals deliberate intent for the published API and must take precedence.
    Covers classes, enums and types, which reach the output via different code paths.

    Keep apart from :func:`test_every_overridable_annotation_is_applied` because:

    * Property. That test asserts pass-through, this one precedence. Only ``description``
      can appear in both LinkML and override, so it alone can collide. The others are
      never generated, and ``title`` is stripped before overlay - reaching an empty slot.
    * Axis. That test varies key, schema fixed; this one varies schema kind, key fixed.
      Merging would need every key declared on every schema; the fixture does that for
      ``Described`` alone.
    """
    assert override_spec["components"]["schemas"][schema_name]["description"] == expected


@pytest.mark.parametrize(("key", "expected"), NON_DESCRIPTION_OVERRIDE_CASES)
def test_every_overridable_annotation_is_applied(override_spec, key, expected):
    """Test that each overridable key other than ``description`` is overlaid verbatim.

    ``description`` is covered by :func:`test_template_description_overrides_linkml_description`,
    which asserts the stronger precedence property that only that key needs; see its docstring
    for why the two are kept apart.

    ``title`` is notable: the generator strips the generated (name-duplicating) title, but
    a title the template declares explicitly is deliberate and must survive.

    The non-scalar cases matter too -- ``example`` and ``externalDocs`` are mappings, so this
    also pins that the overlay copies a value of any shape rather than only scalars.
    """
    assert override_spec["components"]["schemas"]["Described"][key] == expected


def test_overridable_key_coverage_is_complete():
    """Test that the two tests above between them cover every key in ``OVERRIDABLE_SCHEMA_KEYS``.

    Their parametrize lists are written by hand, so without this guard adding a key to
    ``OVERRIDABLE_SCHEMA_KEYS`` would ship with no test and nothing would fail. A failure here
    means: add the new key to ``NON_DESCRIPTION_OVERRIDE_CASES`` and declare it on the
    ``Described`` placeholder in spec-template-overrides.openapi.yaml.
    """
    covered = {key for key, _ in NON_DESCRIPTION_OVERRIDE_CASES} | {"description"}
    assert covered == OVERRIDABLE_SCHEMA_KEYS


def test_linkml_description_kept_when_template_declares_none(override_spec):
    """Test that a schema whose placeholder declares no description keeps the LinkML one."""
    schemas = override_spec["components"]["schemas"]
    assert schemas["Untouched"]["description"] == "class description from LinkML, untouched"
    assert schemas["Undescribed"]["description"] == ""


def test_template_override_does_not_clobber_generated_type(override_spec):
    """Test that a placeholder's ``type: object`` never overwrites the generated type.

    Placeholders conventionally carry ``type: object`` (the generic template emits it),
    but LinkML types and enums generate as ``type: string``. Overlaying structural keys
    would yield a schema rejecting every valid payload, so only annotations are merged.
    """
    schemas = override_spec["components"]["schemas"]
    assert schemas["FixedRef"]["type"] == "string"
    assert schemas["FixedRef"]["enum"] == ["fixed-value"]
    assert schemas["Colour"]["type"] == "string"
    assert schemas["Colour"]["enum"] == ["RED", "BLUE"]


def test_template_override_applies_to_renamed_schema(override_spec):
    """Test that overrides are keyed by OpenAPI name, so renamed resources receive them.

    ``FixedRef`` is the template's name for the LinkML type ``FixedType``; the override
    must be applied after renaming or it would silently miss every renamed resource.
    """
    schemas = override_spec["components"]["schemas"]
    assert "FixedRef" in schemas
    assert "FixedType" not in schemas
    assert schemas["FixedRef"]["description"] == "type description from the template"


def test_rename_applies_to_transitively_reached_schema(override_spec):
    """Test that a declared placeholder renames its schema even without an endpoint.

    ``Colour`` is declared for the LinkML enum ``ColorEnum`` but no endpoint references
    it; it is reached only through ``Described.color``. It must still be published under
    the declared name, with its ``$ref`` rewired and its override applied -- otherwise a
    renamed-but-unreferenced placeholder is silently ignored.
    """
    schemas = override_spec["components"]["schemas"]
    assert "Colour" in schemas
    assert "ColorEnum" not in schemas
    assert schemas["Described"]["properties"]["color"] == {"$ref": "#/components/schemas/Colour"}


def test_vendor_extensions_pass_through_but_bookkeeping_does_not(override_spec):
    """Test that ``x-`` extensions are published while LinkML bookkeeping keys are not.

    ``x-linkml-schema``/``x-linkml-source`` map the template to the LinkML schema and are
    meaningless to API consumers, so they must never reach the generated document.
    """
    described = override_spec["components"]["schemas"]["Described"]
    assert described["x-vendor-flag"] == "kept"
    assert "x-linkml-" not in str(override_spec)


def test_shared_template_anchor_is_not_emitted_as_yaml_alias(override_text, override_spec):
    """Test that a value shared between placeholders via a YAML anchor is emitted inline.

    ``yaml.safe_load`` resolves an anchor and its aliases to one Python object; inserting
    that object into several schemas would make ``yaml.dump`` re-emit it as ``&id001`` /
    ``*id001``, which is valid YAML but unidiomatic OpenAPI that anchor-unaware tooling
    rejects. Each schema must receive its own copy.
    """
    schemas = override_spec["components"]["schemas"]
    assert schemas["Described"]["externalDocs"] == schemas["Untouched"]["externalDocs"]
    # an alias would emit the URL once and `*id001` the second time
    assert override_text.count("url: https://example.org/docs") == 2
    assert "*id" not in override_text


def test_spec_with_template_overrides_is_valid(override_spec):
    """Test that applying overrides still yields a valid OpenAPI 3.0.3 document."""
    assert validate(override_spec, cls=OpenAPIV30SpecValidator) is None


def test_wrongly_typed_annotation_override_is_rejected(tmp_path, input_path):
    """Test that an annotation override of the wrong type fails template validation.

    OpenAPI requires ``deprecated`` to be a boolean. A LinkML-style string reason is
    rejected by the up-front template validation, before the override path runs, rather
    than being published into an invalid document.
    """
    schema_path = str(input_path("openapi/schema_template_overrides.yaml"))
    good = Path(str(input_path("openapi/spec-template-overrides.openapi.yaml"))).read_text()
    bad_path = tmp_path / "bad.openapi.yaml"
    bad_path.write_text(good.replace("deprecated: true", "deprecated: use something else"))
    with pytest.raises(OpenAPIValidationError):
        OpenApiGenerator(schema_path).serialize(str(bad_path))
