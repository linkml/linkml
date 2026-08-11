import pytest
import yaml
from openapi_spec_validator import OpenAPIV30SpecValidator, OpenAPIV31SpecValidator, validate
from referencing.exceptions import PointerToNowhere

from linkml.generators.openapigen import OpenApiGenerator


def gen_openapi_spec(head_path, kitchen_sink_path):
    openapigen = OpenApiGenerator(kitchen_sink_path)
    return openapigen.serialize(head_path)


@pytest.fixture
def templating(request):
    """Templating (head path, validator) for openapi_spec.

    Defaults to OpenAPI 3.0.3 when a test does not parametrize it indirectly.
    """
    return getattr(request, "param", ("openapi/spec-head-v30.openapi.yaml", OpenAPIV30SpecValidator))


@pytest.fixture
def openapi_spec(input_path, templating, kitchen_sink_path):
    head_path = str(input_path(templating[0]))
    openapigen = OpenApiGenerator(kitchen_sink_path)
    return yaml.safe_load(openapigen.serialize(head_path))


@pytest.mark.parametrize(
    "templating",
    [
        ("openapi/spec-head-v30.openapi.yaml", OpenAPIV30SpecValidator),
        ("openapi/spec-head-v31.openapi.yaml", OpenAPIV31SpecValidator),
    ],
)
def test_openapi(input_path, templating, kitchen_sink_path):
    """Test if generation succeeds without failure and returns valid YAML."""
    head_path = str(input_path(templating[0]))
    openapi_spec = gen_openapi_spec(head_path, kitchen_sink_path)
    # ensure that valid YAML has been generated
    assert yaml.safe_load(openapi_spec)
    # ensure that valid OpenAPI spec has been generated
    assert validate(yaml.safe_load(openapi_spec), cls=templating[1]) is None


def test_openapi_missing_template(kitchen_sink_path):
    """Test that serialize raises ValueError when no template file is provided."""
    with pytest.raises(ValueError, match="An OpenAPI template file is required"):
        OpenApiGenerator(kitchen_sink_path).serialize()


def test_openapi_fixed_template(input_path, kitchen_sink_path):
    """Test that serialize raises ValueError when no template file is provided."""
    head_path = str(input_path("openapi/spec-fixed.openapi.yaml"))
    oa_spec = OpenApiGenerator(kitchen_sink_path).serialize(head_path)
    assert open(head_path).read() == oa_spec


def test_openapi_spec_no_defs_references(openapi_spec):
    """Test that all $defs references are converted to components/schemas."""
    for schema in openapi_spec["components"]["schemas"].values():
        assert "#/$defs/" not in str(schema)


@pytest.mark.parametrize(
    "templating",
    [("openapi/spec-head-v31.openapi.yaml", OpenAPIV31SpecValidator)],
    indirect=True,
)
def test_openapi_v31_no_linkml_meta(openapi_spec):
    for schema in openapi_spec["components"]["schemas"].values():
        assert "linkml_meta" not in str(schema)


def test_openapi_v30_const_to_enum_conversion(openapi_spec):
    """Test that const values are converted to single-item enum arrays (OpenAPI 3.0.3)."""
    person = openapi_spec["components"]["schemas"]["Person"]
    assert person["properties"]["species_name"]["enum"] == ["human"]
    assert person["properties"]["stomach_count"]["enum"] == [1]
    assert "const" not in person["properties"]["species_name"]
    assert "const" not in person["properties"]["stomach_count"]


@pytest.mark.parametrize(
    "templating",
    [("openapi/spec-head-v31.openapi.yaml", OpenAPIV31SpecValidator)],
    indirect=True,
)
def test_openapi_v31_const_preserved(openapi_spec):
    """Test that const values are preserved as-is (OpenAPI 3.1.0)."""
    person = openapi_spec["components"]["schemas"]["Person"]
    species_name = person["properties"]["species_name"]
    if "anyOf" in species_name:
        const_branches = [b for b in species_name["anyOf"] if "const" in b]
        assert len(const_branches) > 0, "const should be present in anyOf branches for v3.1.0"
    else:
        assert "const" in species_name, "const should be preserved in v3.1.0"


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
    that, so the generated OpenAPI schemas must stay open — at every nesting level,
    including inlined sub-schemas.
    """

    def _closed_paths(obj, path=""):
        if isinstance(obj, dict):
            if obj.get("additionalProperties") is False:
                yield path or "<root>"
            for key, value in obj.items():
                yield from _closed_paths(value, f"{path}/{key}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                yield from _closed_paths(item, f"{path}[{i}]")

    closed = list(_closed_paths(openapi_spec["components"]["schemas"]))
    assert not closed, f"closed schemas (additionalProperties: false) block API extension: {closed}"


@pytest.mark.parametrize(
    "templating",
    [("openapi/spec-head-v31.openapi.yaml", OpenAPIV31SpecValidator)],
    indirect=True,
)
def test_openapi_v31_schemas_are_extensible(openapi_spec):
    """Test that v3.1.0 (Pydantic path) also emits open schemas at every nesting level.

    The Pydantic generator must be driven with ``extra_fields="allow"`` so no
    ``additionalProperties: false`` leaks into the generated components.
    """

    def _closed_paths(obj, path=""):
        if isinstance(obj, dict):
            if obj.get("additionalProperties") is False:
                yield path or "<root>"
            for key, value in obj.items():
                yield from _closed_paths(value, f"{path}/{key}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                yield from _closed_paths(item, f"{path}[{i}]")

    closed = list(_closed_paths(openapi_spec["components"]["schemas"]))
    assert not closed, f"closed schemas (additionalProperties: false) block API extension: {closed}"


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
    assert parsed["openapi"] == "x.y.z"
    assert "paths" in parsed
    assert "schemas" in parsed["components"]
    # the schema id from kitchen_sink must appear in the template
    assert "https://w3id.org/linkml/tests/kitchen_sink" in output


@pytest.mark.parametrize(
    "template_path", ["openapi/spec-wrong-schema-id-v30.openapi.yaml", "openapi/spec-wrong-schema-id-v31.openapi.yaml"]
)
def test_schema_id_mismatch_raises(input_path, template_path, kitchen_sink_path):
    """Test that a mismatched x-linkml-schema raises ValueError with a descriptive message."""
    head_path = str(input_path(template_path))
    with pytest.raises(ValueError, match="x-linkml-schema"):
        OpenApiGenerator(kitchen_sink_path).serialize(head_path)


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
    schema_path = str(input_path("openapi/test_schema_type_constraints.yaml"))
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


def test_openapi_v31_type_constraints(input_path):
    """Test that a template schema backed by a LinkML type is generated on the v3.1.0 path.

    LinkML types are not emitted as Pydantic classes; their constraints are inlined
    into referencing slots. An endpoint that references a type directly (via
    ``x-linkml-source``) must therefore still produce a standalone component schema,
    otherwise the spec contains a dangling ``$ref``.
    """
    schema_path = str(input_path("openapi/test_schema_type_constraints.yaml"))
    head_path = str(input_path("openapi/spec-types-v31.openapi.yaml"))
    spec = yaml.safe_load(OpenApiGenerator(schema_path).serialize(head_path))
    schemas = spec["components"]["schemas"]
    # the type schema is exposed under the template's resource name, not dangling
    code_str = schemas["CodeStringRef"]
    assert code_str["type"] == "string"
    assert code_str["pattern"] == "^[A-Z]{2,10}$"
    assert code_str["description"] == "A 2-10 character uppercase code"
    # the produced spec is valid OpenAPI 3.1.0 (no dangling reference)
    assert validate(spec, cls=OpenAPIV31SpecValidator) is None
    for schema in schemas.values():
        assert "#/$defs/" not in str(schema)


@pytest.mark.parametrize(
    "template_path", ["openapi/spec-renaming-v30.openapi.yaml", "openapi/spec-renaming-v31.openapi.yaml"]
)
def test_renaming(input_path, template_path, kitchen_sink_path):
    """Test that resource names differing from LinkML class names are renamed throughout the spec."""
    head_path = str(input_path(template_path))
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path).serialize(head_path))
    schemas = spec["components"]["schemas"]
    # resource is exposed under the template name, not the LinkML class name
    assert "PersonResource" in schemas
    assert "Person" not in schemas
    # all $ref values in the spec must use the renamed
    assert "Person" not in str(spec).replace("PersonResource", "")


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
    template_text = open(head_path).read()
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
    # and is exposed under its OpenAPI resource name, not the LinkML class name
    assert "OpaqueEvent" in schemas
    assert "MarriageEvent" not in schemas


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
    head_path = str(input_path("openapi/spec-head-v30.openapi.yaml"))
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
