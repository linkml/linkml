from pathlib import Path
from textwrap import dedent

import pytest
import yaml
from openapi_spec_validator import OpenAPIV30SpecValidator, validate
from referencing.exceptions import PointerToNowhere

from linkml.generators.openapigen import OpenApiGenerator
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import YAMLLoader

# ---------------------------------------------------------------------------
# Reusable YAML fragments
# ---------------------------------------------------------------------------

# OpenAPI versions the test-suite is driven with, mapped to the output format name
# accepted by OpenApiGenerator (see OpenApiGenerator.valid_formats/_openapi_versions).
# The two must stay in lockstep: extend this dict and the generator together when a
# new OpenAPI version becomes supported.
OAS_VERSIONS: dict[str, str] = {
    "3.0.3": "openapi303",
}

# Default OpenAPI version used by templates/tests that are not version-parametrized.
DEFAULT_OAS_VERSION = "3.0.3"

# LinkML schema document preamble shared by the inline enum/chain test schemas.
LINKML_HEADER = """\
id: https://w3id.org/linkml/tests/{name}
name: {name}
default_prefix: {name}
imports:
  - linkml:types
"""

# OpenAPI template header (title + quoted version) shared by most small templates.
OPENAPI_HEADER = """\
openapi: {oas_version}
info:
  title: {title}
  version: '1.0.0'
"""

# servers/security block shared by several templates.
TEMPLATE_SERVERS_SECURITY = """\
servers:
  - url: https://example.org/
security:
  - PayloadSignature: []
"""

# The kitchen_sink post endpoint on /api/endpoint1 used by TEMPLATE_HEAD.
POST_MEDICAL_EVENT = """\
  /api/endpoint1:
    post:
      security:
        - PayloadSignature: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MedicalEvent'
      responses:
        '200':
          description: Success
"""

# A post endpoint with no replaceable fields (TEMPLATE_FIXED byte-equality test).
POST_FIXED = """\
  /api/endpoint1:
    post:
      security:
        - PayloadSignature: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
      responses:
        "200":
          description: Success
"""

# x-linkml-schema ids stamped on template schema stubs; each must equal the
# id of the LinkML schema loaded for the corresponding test.
KITCHEN_SINK_ID = "https://w3id.org/linkml/tests/kitchen_sink"
TYPES_AND_ENUMS_ID = "https://w3id.org/linkml/tests/types_and_enums"
CHAIN_UNREFERENCED_ID = "https://w3id.org/linkml/tests/chain_unreferenced"
SHARED_ENUM_ID = "https://w3id.org/linkml/tests/shared_enum"
ENDPOINT_ENUM_ID = "https://w3id.org/linkml/tests/endpoint_enum"
ENUM_SLOT_DESCRIPTION_ID = "https://w3id.org/linkml/tests/enum_slot_description"
UNREFERENCED_WITH_UNRELATED_ID = "https://w3id.org/linkml/tests/unreferenced_with_unrelated"
WRONG_SCHEMA_ID = "https://w3id.org/linkml/tests/WRONG_SCHEMA_ID"
FOO_ID = "https://example.org/foo"

# FixedEnum with FOO/BAR, shared by the several enum-focused schemas.
ENUM_FOO_BAR = """\
      FixedEnum:
        permissible_values:
          FOO: {}
          BAR: {}
"""

# Foo/Foo Bar/Baz Qux class chain, shared by the chain-pruning schemas.
CHAIN_CLASSES = """\
classes:
  Foo:
    description: the only class reachable from the endpoint
    attributes:
      name:
        range: string

  Foo Bar:
    description: unrelated class with a space in its name, not reachable from Foo, but present in the schema
    attributes:
      bar_ref:
        range: Baz Qux

  Baz Qux:
    description: should be pruned - only referenced by the also-unreachable Foo Bar
    attributes:
      value:
        range: string
"""

# Extra class appended to CHAIN_CLASSES in the keep-unreferenced-scoped schema.
UNRELATED_CLASS = """\

  Unrelated:
    description: completely unrelated class, neither referenced by the endpoint nor by any template-declared class
    attributes:
      value:
        range: string
"""


# ---------------------------------------------------------------------------
# Composition helpers
# ---------------------------------------------------------------------------


def linkml_schema(name: str, body: str) -> str:
    """Compose a minimal LinkML schema from the shared header and a ``body`` section.

    :param name: schema name (also its default_prefix and id suffix)
    :param body: the classes/enums/types section
    """
    return dedent(LINKML_HEADER).format(name=name) + dedent(body)


def schema_stub(name: str, schema_id: str, source: str) -> str:
    """Compose one ``components/schemas`` entry declaring an OpenAPI resource.

    :param name: OpenAPI resource name
    :param schema_id: ``x-linkml-schema`` id the resource is sourced from
    :param source: ``x-linkml-source`` element (class/type/enum) it maps to
    """
    return f"    {name}:\n      type: object\n      x-linkml-schema: {schema_id}\n      x-linkml-source: {source}\n"


def schema_stubs(stubs: list[tuple[str, str, str]]) -> str:
    """Compose several ``components/schemas`` entries.

    :param stubs: ``(name, schema_id, source)`` triples, one per entry
    """
    return "".join(schema_stub(name, schema_id, source) for name, schema_id, source in stubs)


def get_endpoint(
    path: str,
    schema: str,
    *,
    description: str = "Success",
    secure: bool = False,
    comment: str = "",
    extra: str = "",
    responses: str = "",
) -> str:
    """Compose a GET endpoint returning a resource via ``$ref``.

    :param path: URL path
    :param schema: OpenAPI resource name referenced by the endpoint
    :param description: response description for the ``200`` response
    :param secure: add per-endpoint ``security`` when True
    :param comment: optional comment line(s) above the path
    :param extra: extra keys under ``get:`` (e.g. parameters), indented
    :param responses: extra response entries under ``responses:``, indented
    """
    security = "      security:\n        - PayloadSignature: []\n" if secure else ""
    doc = "  " + dedent(comment).replace("\n", "\n  ") + "\n" if comment else ""
    doc += f"""\
  {path}:
    get:
{security}{extra}      responses:
        '200':
          description: {description}
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/{schema}'
{responses}"""
    return doc


def openapi_template(
    title: str,
    endpoints: str,
    schemas: str,
    *,
    header: str = "",
    comment: str = "",
    components: str = "",
    oas_version: str = DEFAULT_OAS_VERSION,
) -> str:
    """Compose an OpenAPI template from the shared header, endpoints and schemas.

    :param title: API title
    :param endpoints: the indented ``paths:`` block
    :param schemas: the indented ``components/schemas`` entries (may be empty)
    :param header: optional extra header block (e.g. servers/security)
    :param comment: optional leading comment line(s)
    :param components: extra ``components`` sections before ``schemas`` (e.g. responses)
    :param oas_version: the OpenAPI version the template advertises
    """
    doc = dedent(OPENAPI_HEADER).format(title=title, oas_version=oas_version)
    if header:
        doc += dedent(header) + "\n"
    doc += "paths:\n"
    doc += endpoints
    if schemas or components:
        doc += "components:\n"
        doc += components
        if schemas:
            doc += "  schemas:\n" + schemas
    if comment:
        doc = dedent(comment) + "\n" + doc
    return doc


def single_endpoint_template(
    title: str,
    path_name: str,
    schema_name: str,
    *,
    schema_id: str,
    source: str,
    description: str = "Success",
    header: str = "",
    comment: str = "",
    secure: bool = False,
    oas_version: str = DEFAULT_OAS_VERSION,
) -> str:
    """Compose a template with one GET endpoint referencing one generated schema.

    :param title: API title
    :param path_name: URL path of the single GET endpoint
    :param schema_name: OpenAPI resource name referenced by the endpoint
    :param schema_id: ``x-linkml-schema`` id stamped on the schema stub
    :param source: ``x-linkml-source`` element name stamped on the schema stub
    :param description: response description for the GET endpoint
    :param header: optional extra header block (e.g. servers/security)
    :param comment: optional leading comment line(s)
    :param secure: add per-endpoint ``security``
    :param oas_version: the OpenAPI version the template advertises
    """
    endpoint = get_endpoint(path_name, schema_name, description=description, secure=secure)
    schemas = schema_stub(schema_name, schema_id, source)
    return openapi_template(
        title, endpoints=endpoint, schemas=schemas, header=header, comment=comment, oas_version=oas_version
    )


# ---------------------------------------------------------------------------
# Inline LinkML schemas (kept inline only when composed from shared fragments)
# ---------------------------------------------------------------------------

SCHEMA_ENDPOINT_ENUM = linkml_schema(
    "endpoint_enum",
    """
    enums:
"""
    + ENUM_FOO_BAR
    + """\
    classes:
      Foo:
        attributes:
          color:
            range: FixedEnum
    """,
)

SCHEMA_ENUM_SLOT_DESCRIPTION = linkml_schema(
    "enum_slot_description",
    """
    enums:
"""
    + ENUM_FOO_BAR
    + """\
    classes:
      Foo:
        description: Foo class, I am
        attributes:
          color:
            description: the color of foo
            range: FixedEnum
    """,
)

SCHEMA_SHARED_ENUM = linkml_schema(
    "shared_enum",
    """
    enums:
"""
    + ENUM_FOO_BAR
    + """\
    classes:
      Foo:
        attributes:
          color:
            range: FixedEnum
      Bar:
        attributes:
          color:
            range: FixedEnum
    """,
)

SCHEMA_CHAIN_UNREFERENCED = linkml_schema("chain_unreferenced", CHAIN_CLASSES)

SCHEMA_UNREFERENCED_WITH_UNRELATED = linkml_schema("unreferenced_with_unrelated", CHAIN_CLASSES + UNRELATED_CLASS)


# ---------------------------------------------------------------------------
# Inline OpenAPI templates
# ---------------------------------------------------------------------------

TEMPLATE_ENDPOINT_ENUM = single_endpoint_template(
    "Endpoint Enum Test",
    "/fixed-enum",
    "FixedEnum",
    schema_id=ENDPOINT_ENUM_ID,
    source="FixedEnum",
    description="ok",
)

TEMPLATE_ENUM_SLOT_DESCRIPTION = single_endpoint_template(
    "Enum Slot Description Test",
    "/foo",
    "Foo",
    schema_id=ENUM_SLOT_DESCRIPTION_ID,
    source="Foo",
    description="ok",
)

TEMPLATE_EXAMPLES = single_endpoint_template(
    "LinkML examples test",
    "/api/with-examples",
    "WithExamples",
    schema_id=TYPES_AND_ENUMS_ID,
    source="WithExamples",
    header=TEMPLATE_SERVERS_SECURITY,
    comment="# OpenAPI template referring a class whose slot declares multiple examples",
)

TEMPLATE_FIXED = openapi_template(
    "LinkML tests",
    endpoints=POST_FIXED,
    schemas="",
    header=TEMPLATE_SERVERS_SECURITY,
    comment="# OpenAPI template provided as template that is fully fixed\n# because there are no fields to be replaced",
)

TEMPLATE_KEEP_SCOPED = single_endpoint_template(
    "Keep Unreferenced Scoped Test",
    "/api/foo",
    "Foo",
    schema_id=UNREFERENCED_WITH_UNRELATED_ID,
    source="Foo",
)

TEMPLATE_LOWERCASE_CLASS = single_endpoint_template(
    "LinkML tests",
    "/api/dataset",
    "Dataset",
    schema_id=KITCHEN_SINK_ID,
    source="Dataset",
)

TEMPLATE_MISSING_XLINKML_SOURCE = """\
openapi: 3.0.3
info: {title: Foo API, version: "1.0"}
paths:
  /foo:
    get:
      responses:
        '200':
          description: ok
          content:
            application/json:
              schema: {$ref: '#/components/schemas/Foo'}
components:
  schemas:
""" + "".join(
    [
        schema_stub("Foo", FOO_ID, "Foo"),
        """\
    Bar:
      type: object
      x-linkml-schema: https://example.org/foo
""",
    ]
)

TEMPLATE_RENAMED_TYPE = single_endpoint_template(
    "Renamed Type Test",
    "/fixed",
    "Fixed",
    schema_id=TYPES_AND_ENUMS_ID,
    source="FixedType",
    description="ok",
)

TEMPLATE_RENAMING = single_endpoint_template(
    "LinkML tests - renaming",
    "/api/persons",
    "PersonResource",
    schema_id=KITCHEN_SINK_ID,
    source="Person",
    header=TEMPLATE_SERVERS_SECURITY,
)

TEMPLATE_SHARED_RESPONSES = openapi_template(
    "Shared Responses Test",
    endpoints=get_endpoint(
        "/foo",
        "Person",
        description="ok",
        responses="""        '404':
          $ref: '#/components/responses/NotFound'
""",
    ),
    schemas=schema_stub("Person", KITCHEN_SINK_ID, "Person"),
    components="""  responses:
    NotFound:
      description: not found
""",
)

TEMPLATE_REFERENCED_PARAMETER = openapi_template(
    "t",
    endpoints=get_endpoint(
        "/foo",
        "Foo",
        description="ok",
        extra="""      parameters:
        - $ref: '#/components/parameters/Limit'
""",
    ),
    schemas=schema_stub("Foo", FOO_ID, "Foo"),
    components="""  parameters:
    Limit:
      name: limit
      in: query
      schema:
        type: integer
""",
)

TEMPLATE_TYPES = single_endpoint_template(
    "LinkML type constraints test",
    "/api/code",
    "CodeStringRef",
    schema_id=TYPES_AND_ENUMS_ID,
    source="CodeString",
    comment="# OpenAPI template referring a Type defined in the LinkML schema",
)

TEMPLATE_TYPES_ENUMS = single_endpoint_template(
    "Types and Enums Test",
    "/api/fixed",
    "FixedType",
    schema_id=TYPES_AND_ENUMS_ID,
    source="FixedType",
    header=TEMPLATE_SERVERS_SECURITY,
)

TEMPLATE_WRONG_SCHEMA_ID = single_endpoint_template(
    "LinkML tests - wrong schema id",
    "/api/endpoint1",
    "Person",
    schema_id=WRONG_SCHEMA_ID,
    source="Person",
    header=TEMPLATE_SERVERS_SECURITY,
)

TEMPLATE_COMMENTS = openapi_template(
    "Comment Preservation Test",
    endpoints=get_endpoint(
        "/api/person",
        "Person",
        secure=True,
        comment="# this endpoint comment must survive",
    ),
    schemas=schema_stub("Person", KITCHEN_SINK_ID, "Person"),
    header=TEMPLATE_SERVERS_SECURITY,
    comment="# top-level comment must survive round-trip",
)


# ---------------------------------------------------------------------------
# OpenAPI templates requiring two or more stubs/endpoints
# ---------------------------------------------------------------------------


TEMPLATE_CHAIN_UNREFERENCED = openapi_template(
    "Chain Pruning Test",
    endpoints=get_endpoint("/api/foo", "Foo", secure=True),
    schemas=schema_stubs(
        [
            ("Foo", CHAIN_UNREFERENCED_ID, "Foo"),
            ("Foo Bar", CHAIN_UNREFERENCED_ID, "Foo Bar"),
        ]
    ),
    header=TEMPLATE_SERVERS_SECURITY,
)

TEMPLATE_KEEP_UNREFERENCED = openapi_template(
    "Keep Unreferenced Test",
    endpoints=get_endpoint("/api/person", "Person", secure=True),
    schemas=schema_stubs(
        [
            ("Person", KITCHEN_SINK_ID, "Person"),
            ("OpaqueEvent", KITCHEN_SINK_ID, "MarriageEvent"),
        ]
    ),
    header=TEMPLATE_SERVERS_SECURITY,
)

TEMPLATE_SHARED_ENUM = openapi_template(
    "Shared Enum Test",
    endpoints=get_endpoint("/foo", "Foo", description="ok") + get_endpoint("/bar", "Bar", description="ok"),
    schemas=schema_stubs(
        [
            ("Foo", SHARED_ENUM_ID, "Foo"),
            ("Bar", SHARED_ENUM_ID, "Bar"),
        ]
    ),
)

TEMPLATE_DANGLING_REF = openapi_template(
    "Dangling Reference Test",
    endpoints=get_endpoint("/api/person", "Person", secure=True) + get_endpoint("/api/foo", "Foo", secure=True),
    schemas=schema_stubs(
        [
            ("Person", KITCHEN_SINK_ID, "Person"),
            ("Foo", KITCHEN_SINK_ID, "NonExistentClass"),
        ]
    ),
    header=TEMPLATE_SERVERS_SECURITY,
)

TEMPLATE_DANGLING_REFS_MULTIPLE = openapi_template(
    "Multiple Dangling References Test",
    endpoints=(
        get_endpoint("/api/person", "Person", secure=True)
        + get_endpoint("/api/foo", "Foo", secure=True)
        + get_endpoint("/api/bar", "Bar", secure=True)
    ),
    schemas=schema_stubs(
        [
            ("Person", KITCHEN_SINK_ID, "Person"),
            ("Foo", KITCHEN_SINK_ID, "NonExistentClassFoo"),
            ("Bar", KITCHEN_SINK_ID, "NonExistentClassBar"),
        ]
    ),
    header=TEMPLATE_SERVERS_SECURITY,
)


def template_head(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose the kitchen_sink template with one post and two get endpoints.

    :param oas_version: the OpenAPI version the template advertises
    """
    return openapi_template(
        "LinkML tests",
        endpoints=POST_MEDICAL_EVENT
        + get_endpoint("/api/person", "Person", secure=True)
        + get_endpoint("/api/endpoint2", "MarriageEvent", secure=True),
        schemas=schema_stubs(
            [
                ("MedicalEvent", KITCHEN_SINK_ID, "MedicalEvent"),
                ("Person", KITCHEN_SINK_ID, "Person"),
                ("MarriageEvent", KITCHEN_SINK_ID, "MarriageEvent"),
            ]
        ),
        header=TEMPLATE_SERVERS_SECURITY,
        oas_version=oas_version,
    )


TEMPLATE_HEAD = template_head()


# ---------------------------------------------------------------------------
# Helpers to feed LinkML schemas / OpenAPI templates to the generator
# ---------------------------------------------------------------------------


def load_schema(text: str) -> SchemaDefinition:
    """Parse inline LinkML schema text into a ``SchemaDefinition``."""
    return YAMLLoader().loads(dedent(text), target_class=SchemaDefinition)


def write_template(tmp_path: Path, text: str) -> str:
    """Write inline OpenAPI template text to a temp file and return its path."""
    path = tmp_path / "template.yaml"
    path.write_text(dedent(text))
    return str(path)


def gen_openapi_spec(head_path, kitchen_sink_path, format_name=None):
    openapigen = OpenApiGenerator(kitchen_sink_path, format=format_name)
    return openapigen.serialize(head_path)


@pytest.fixture(params=list(OAS_VERSIONS))
def openapi_spec(request, tmp_path, kitchen_sink_path):
    oas_version, format_name = request.param, OAS_VERSIONS[request.param]
    head_path = write_template(tmp_path, template_head(oas_version=oas_version))
    spec = yaml.safe_load(gen_openapi_spec(head_path, kitchen_sink_path, format_name))
    return spec


def test_openapi(tmp_path, kitchen_sink_path):
    """Test if generation succeeds without failure and returns valid YAML."""
    head_path = write_template(tmp_path, TEMPLATE_HEAD)
    openapi_spec = gen_openapi_spec(head_path, kitchen_sink_path)
    # ensure that valid YAML has been generated
    assert yaml.safe_load(openapi_spec)
    # ensure that valid OpenAPI spec has been generated
    assert validate(yaml.safe_load(openapi_spec), cls=OpenAPIV30SpecValidator) is None


def test_openapi_missing_template(kitchen_sink_path):
    """Test that serialize raises ValueError when no template file is provided."""
    with pytest.raises(ValueError, match="An OpenAPI template file is required"):
        OpenApiGenerator(kitchen_sink_path).serialize()


def test_openapi_fixed_template(tmp_path, kitchen_sink_path):
    """Test that a template with no replaceable fields is emitted byte-for-byte."""
    head_path = write_template(tmp_path, TEMPLATE_FIXED)
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


def test_schema_id_mismatch_raises(tmp_path, kitchen_sink_path):
    """Test that a mismatched x-linkml-schema raises ValueError with a descriptive message."""
    head_path = write_template(tmp_path, TEMPLATE_WRONG_SCHEMA_ID)
    with pytest.raises(ValueError, match="x-linkml-schema"):
        OpenApiGenerator(kitchen_sink_path).serialize(head_path)


def test_missing_x_linkml_source_raises(input_path, tmp_path):
    """Test that a template schema missing x-linkml-source raises a descriptive KeyError.

    x-linkml-schema presence/value are validated nicely, but x-linkml-source was
    skipped, surfacing as a bare ``KeyError: 'x-linkml-source'`` during instantiation.
    """
    schema_path = input_path("openapi/schema_foo.yaml")
    head_path = write_template(tmp_path, TEMPLATE_MISSING_XLINKML_SOURCE)
    with pytest.raises(KeyError, match="Bar.*missing required 'x-linkml-source'"):
        OpenApiGenerator(schema_path, keep_unreferenced=True).serialize(head_path)


def test_referenced_parameter_does_not_crash(input_path, tmp_path):
    """Test that a template parameter given as a $ref does not raise KeyError.

    A parameter entry of the form ``{$ref: '#/components/parameters/Limit'}`` has no
    ``schema`` key of its own (the schema lives inside ``components/parameters``), so
    reading ``param_spec["schema"]`` unconditionally crashed before generation.
    """
    schema_path = input_path("openapi/schema_foo.yaml")
    head_path = write_template(tmp_path, TEMPLATE_REFERENCED_PARAMETER)
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


def test_openapi_type_constraints(input_path, tmp_path):
    """Test that LinkML types with constraints (e.g., pattern) are properly generated in the spec."""
    schema_path = input_path("openapi/schema_types_and_enums.yaml")
    head_path = write_template(tmp_path, TEMPLATE_TYPES)
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


def test_renaming(tmp_path, kitchen_sink_path):
    """Test that resource names differing from LinkML class names are renamed throughout the spec."""
    head_path = write_template(tmp_path, TEMPLATE_RENAMING)
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path).serialize(head_path))
    schemas = spec["components"]["schemas"]
    # resource is exposed under the template name, not the LinkML class name
    assert "PersonResource" in schemas
    assert "Person" not in schemas
    # all $ref values in the spec must use the renamed
    assert "Person" not in str(spec).replace("PersonResource", "")


def test_openapi_examples_converted_to_singular_example(input_path, tmp_path):
    """Test that a slot's ``examples`` list is converted to OpenAPI's singular ``example``.

    OpenAPI 3.0 has no plural ``examples`` keyword on the Schema Object, only ``example``.
    Without this conversion, generation fails validation entirely for any schema with a
    slot declaring ``examples`` -- this is a blocker, not a cosmetic gap.
    """
    schema_path = input_path("openapi/schema_types_and_enums.yaml")
    head_path = write_template(tmp_path, TEMPLATE_EXAMPLES)
    spec = yaml.safe_load(OpenApiGenerator(schema_path).serialize(head_path))
    name_schema = spec["components"]["schemas"]["WithExamples"]["properties"]["name"]
    # first example is kept; the plural form is gone entirely
    assert name_schema["example"] == "sample"
    assert "examples" not in name_schema
    assert validate(spec, cls=OpenAPIV30SpecValidator) is None


def test_template_text_preserved(tmp_path, kitchen_sink_path):
    """Test that everything above ``components/schemas`` is emitted verbatim.

    The generator no longer YAML round-trips the whole template (which would drop
    comments and normalise quoting/styling). Only the ``components/schemas`` section
    is regenerated; the header, paths and any comments above it must survive intact.
    """
    head_path = write_template(tmp_path, TEMPLATE_COMMENTS)
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


def test_unreferenced_schema_removed_by_default(tmp_path, kitchen_sink_path):
    """Test that template schemas not referenced by any endpoint are removed by default."""
    head_path = write_template(tmp_path, TEMPLATE_KEEP_UNREFERENCED)
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "Person" in schemas
    # OpaqueEvent(OpenAPI)/MarriageEvent(LinkML) is declared in the template but no endpoint references it
    assert "MarriageEvent" not in schemas


def test_keep_unreferenced_preserves_template_schema(tmp_path, kitchen_sink_path):
    """Test that keep_unreferenced retains template schemas not referenced by any endpoint.

    Unreferenced sub-schemas can convey objects that are opaque to the API but relevant
    to clients (e.g. present in provided artifacts). The keep_unreferenced flag makes
    their removal switchable.
    """
    head_path = write_template(tmp_path, TEMPLATE_KEEP_UNREFERENCED)
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path, keep_unreferenced=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "Person" in schemas
    # OpaqueEvent(OpenAPI)/MarriageEvent(LinkML) is kept even though no endpoint references it
    assert "MarriageEvent" in schemas


def test_unreferenced_chain_pruned_by_default(tmp_path):
    """Test that a chain of mutually-referencing unreferenced schemas is pruned in one pass.

    ``Foo Bar`` (note the space in the name) references ``Baz Qux`` but neither is
    reachable from the endpoint-seeded ``Foo``. A naive single prune pass that only drops
    schemas *directly* citing an unreferenced name would keep ``Baz Qux`` (it is only
    referenced by ``Foo Bar``, and ``Foo Bar`` is dropped for not being referenced at all);
    the reference closure must remove the whole island. Space-named classes also exercise
    the YAML quoting of schema keys and ``$ref`` targets.
    """
    schema_path = load_schema(SCHEMA_CHAIN_UNREFERENCED)
    head_path = write_template(tmp_path, TEMPLATE_CHAIN_UNREFERENCED)
    spec = yaml.safe_load(OpenApiGenerator(schema_path).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "Foo" in schemas
    assert "Foo Bar" not in schemas
    assert "Baz Qux" not in schemas


def test_keep_unreferenced_pulls_transitive_chain(tmp_path):
    """Test that keep_unreferenced retains a declared schema and its transitive dependencies.

    The template declares ``Foo Bar`` (with a space in its name, unreferenced by any
    endpoint) alongside ``Foo``. With ``keep_unreferenced`` the declared ``Foo Bar`` is
    kept, and its dependency ``Baz Qux`` - which is not itself declared in the template -
    must be kept too, because pruning out ``Baz Qux`` would leave the kept ``Foo Bar``
    with a dangling reference.
    """
    schema_path = load_schema(SCHEMA_CHAIN_UNREFERENCED)
    head_path = write_template(tmp_path, TEMPLATE_CHAIN_UNREFERENCED)
    spec = yaml.safe_load(OpenApiGenerator(schema_path, keep_unreferenced=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "Foo" in schemas
    assert "Foo Bar" in schemas
    assert "Baz Qux" in schemas


def test_keep_unreferenced_does_not_add_unrelated_schemas(tmp_path):
    """Test that keep_unreferenced stays scoped to the template, not "dump everything".

    The chain schema also contains classes not reachable from ``Foo`` or the template
    declarations. ``keep_unreferenced`` only keeps the template-declared schemas and their
    transitive dependencies - it must not pull in the whole schema. Here the only other
    hidden class in the fixture is ``Baz Qux`` (already pulled by ``Foo Bar``), so a
    dedicated fixture with an unrelated class proves the flag does not regress to dumping
    every class.
    """
    schema_path = load_schema(SCHEMA_UNREFERENCED_WITH_UNRELATED)
    head_path = write_template(tmp_path, TEMPLATE_KEEP_SCOPED)
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


def test_inline_enums_inlines_enum_schemas(tmp_path, kitchen_sink_path):
    """Test that inline_enums inlines enum sub-schemas into their parents.

    With the flag set, an enum no longer gets its own ``components/schemas`` entry;
    instead its definition is inlined where it was referenced.
    """
    head_path = write_template(tmp_path, TEMPLATE_HEAD)
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


def test_inline_enums_does_not_inline_types(input_path, tmp_path):
    """Test that inline_enums does not mistake fixed-value LinkML types for enums.

    A type with ``equals_string`` becomes a single-element ``enum`` after the
    ``const`` -> ``enum`` transform. A naive enum detection would then inline it away
    (``_inline_enum_schemas`` matches any schema with ``enum`` and no ``properties``);
    types must keep their named schema entry even when inlining is enabled.
    """
    schema_path = input_path("openapi/schema_types_and_enums.yaml")
    head_path = write_template(tmp_path, TEMPLATE_TYPES_ENUMS)
    spec = yaml.safe_load(OpenApiGenerator(schema_path, inline_enums=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    # the fixed-value type keeps its own named schema entry (not inlined)
    assert "FixedType" in schemas
    assert schemas["FixedType"]["enum"] == ["fixed-value"]
    assert schemas["FixedType"]["type"] == "string"


def test_inline_enums_disabled_keeps_types_and_enums_separate(input_path, tmp_path):
    """Test that with inline_enums disabled both types and enums keep separate schema entries."""
    schema_path = input_path("openapi/schema_types_and_enums.yaml")
    head_path = write_template(tmp_path, TEMPLATE_TYPES_ENUMS)
    spec = yaml.safe_load(OpenApiGenerator(schema_path, inline_enums=False).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "FixedType" in schemas
    assert schemas["FixedType"]["enum"] == ["fixed-value"]
    assert schemas["FixedType"]["type"] == "string"


def test_inline_enums_keeps_endpoint_referenced_enum(tmp_path):
    """Test that inline_enums does not inline an enum referenced directly by an endpoint.

    Inlining removes the enum's standalone ``components/schemas`` entry, which would
    leave the endpoint's ``$ref`` dangling. An enum that is itself the seeded schema of an
    endpoint must therefore keep its entry even when inlining is enabled.
    """
    schema_path = load_schema(SCHEMA_ENDPOINT_ENUM)
    head_path = write_template(tmp_path, TEMPLATE_ENDPOINT_ENUM)
    spec = yaml.safe_load(OpenApiGenerator(schema_path, inline_enums=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "FixedEnum" in schemas
    assert schemas["FixedEnum"]["enum"] == ["FOO", "BAR"]
    assert spec["paths"]["/fixed-enum"]["get"]["responses"]["200"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/FixedEnum"
    }


def test_inline_enums_does_not_inline_renamed_enums(input_path, tmp_path):
    """Test that inlining a renamed enum does not bypass the type guard.

    When the endpoint refers to a LinkML ``enum`` under a different OpenAPI name, the
    rename must not hide the fact that the source element is an enum. Otherwise the schema
    would be inlined away, leaving the endpoint's ``$ref`` dangling.
    """
    schema_path = input_path("openapi/schema_types_and_enums.yaml")
    head_path = write_template(tmp_path, TEMPLATE_RENAMED_TYPE)
    spec = yaml.safe_load(OpenApiGenerator(schema_path, inline_enums=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "Fixed" in schemas
    assert schemas["Fixed"]["enum"] == ["fixed-value"]
    assert spec["paths"]["/fixed"]["get"]["responses"]["200"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/Fixed"
    }


def test_inline_enums_shared_enum_no_yaml_anchors(tmp_path):
    """Test that inlining a shared enum does not emit YAML anchors.

    When the same enum is referenced from two classes, the inlined copy must not be the
    very same Python object: reusing the object makes ``yaml.dump`` emit an ``&idNNN``
    anchor with an ``*idNNN`` alias for the second reference. The generated YAML must
    contain no anchors or aliases.
    """
    schema_path = load_schema(SCHEMA_SHARED_ENUM)
    head_path = write_template(tmp_path, TEMPLATE_SHARED_ENUM)
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


def test_inline_enums_preserves_slot_description(tmp_path):
    """Test that inlining an enum keeps the slot-level description of the referencing property.

    A property that references an enum carries its own ``description`` next to the
    ``$ref``. Inlining must merge the enum definition into that property without
    discarding the slot-level ``description`` (the enum's own, here empty, description
    must not eclipse it).
    """
    schema_path = load_schema(SCHEMA_ENUM_SLOT_DESCRIPTION)
    head_path = write_template(tmp_path, TEMPLATE_ENUM_SLOT_DESCRIPTION)
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


def test_lowercase_class_name_preserved(tmp_path, kitchen_sink_path):
    """Test that a lowercase LinkML class name is preserved, not camelCased, in the spec.

    ``JsonSchemaGenerator`` camelCases ``$defs`` keys unless ``preserve_names=True``.
    In kitchen_sink the class ``activity`` (lowercase) is transitively reachable from
    ``Dataset`` via the ``activities`` slot. Without name preservation the emitted schema
    is keyed ``Activity`` while the ``$ref`` from ``Dataset`` points to ``activity``,
    yielding a missing schema and a dangling reference.
    """
    head_path = write_template(tmp_path, TEMPLATE_LOWERCASE_CLASS)
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path).serialize(head_path))
    schemas = spec["components"]["schemas"]
    # the LinkML name is preserved verbatim, not camelCased
    assert "activity" in schemas
    assert "Activity" not in schemas
    # Dataset references the activity schema under its original name
    assert schemas["Dataset"]["properties"]["activities"]["items"] == {"$ref": "#/components/schemas/activity"}
    # the produced spec is valid (no dangling reference)
    assert validate(spec, cls=OpenAPIV30SpecValidator) is None


def test_dangling_reference_raises(tmp_path, kitchen_sink_path):
    """Test that a generated spec containing an unresolvable $ref is rejected.

    The template declares a ``Foo`` schema sourced from a non-existent LinkML class,
    so no schema is generated for it while an endpoint still references it. The
    generator must detect the dangling ``$ref`` and fail loudly.
    """
    head_path = write_template(tmp_path, TEMPLATE_DANGLING_REF)
    with pytest.raises(ValueError, match="Dangling .ref"):
        OpenApiGenerator(kitchen_sink_path).serialize(head_path)


def test_dangling_reference_reports_all(tmp_path, kitchen_sink_path):
    """All dangling ``$ref`` targets must be gathered and reported together, not just the first one.

    The template declares two schemas (``Foo`` and ``Bar``) sourced from non-existent LinkML classes,
    each referenced by its own endpoint. The single raised error must mention both.
    """
    head_path = write_template(tmp_path, TEMPLATE_DANGLING_REFS_MULTIPLE)
    with pytest.raises(ValueError, match="Dangling .ref") as exc_info:
        OpenApiGenerator(kitchen_sink_path).serialize(head_path)
    message = str(exc_info.value)
    assert "#/components/schemas/Foo" in message
    assert "#/components/schemas/Bar" in message


def test_refs_to_non_schema_components_allowed(tmp_path, kitchen_sink_path):
    """Test that $refs to reusable components other than schemas (e.g. responses) are allowed.

    The dangling-reference check must resolve every internal ``$ref`` against its own
    ``components`` section rather than assuming all targets live under ``schemas``.
    """
    head_path = write_template(tmp_path, TEMPLATE_SHARED_RESPONSES)
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path).serialize(head_path))
    # the reusable response survives and is still referenced by the endpoint
    assert "NotFound" in spec["components"]["responses"]
    assert spec["paths"]["/foo"]["get"]["responses"]["404"] == {"$ref": "#/components/responses/NotFound"}
    # the schema is generated as usual
    assert "Person" in spec["components"]["schemas"]
    assert validate(spec, cls=OpenAPIV30SpecValidator) is None
