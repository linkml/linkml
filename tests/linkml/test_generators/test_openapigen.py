import re
from pathlib import Path
from textwrap import dedent

import pytest
import yaml
from click.testing import CliRunner
from openapi_spec_validator import OpenAPIV30SpecValidator, OpenAPIV31SpecValidator, validate
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError
from referencing.exceptions import PointerToNowhere

from linkml.generators.openapigen import OVERRIDABLE_SCHEMA_KEYS, OpenApiGenerator, cli
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import YAMLLoader

# ---------------------------------------------------------------------------
# Reusable YAML fragments
# ---------------------------------------------------------------------------

# OpenAPI versions the test-suite is driven with, mapped to the validator class from
# openapi-spec-validator used to check the generated specs. The generator selects the
# generation path from the template's top-level ``openapi`` attribute, so a version is
# exercised simply by advertising it in the template. Extend this dict together with
# the generator when a new OpenAPI version becomes supported.
OAS_VALIDATORS: dict[str, type] = {
    "3.0.3": OpenAPIV30SpecValidator,
    "3.1.0": OpenAPIV31SpecValidator,
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
TEMPLATE_OVERRIDES_ID = "https://w3id.org/linkml/tests/template_overrides"

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


def template_endpoint_enum(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template whose endpoint references an enum defined in the LinkML schema.

    :param oas_version: the OpenAPI version the template advertises
    """
    return single_endpoint_template(
        "Endpoint Enum Test",
        "/fixed-enum",
        "FixedEnum",
        schema_id=ENDPOINT_ENUM_ID,
        source="FixedEnum",
        description="ok",
        oas_version=oas_version,
    )


def template_enum_slot_description(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template whose referenced class has a slot-level enum description.

    :param oas_version: the OpenAPI version the template advertises
    """
    return single_endpoint_template(
        "Enum Slot Description Test",
        "/foo",
        "Foo",
        schema_id=ENUM_SLOT_DESCRIPTION_ID,
        source="Foo",
        description="ok",
        oas_version=oas_version,
    )


def template_examples(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template whose referenced class declares multiple slot examples.

    :param oas_version: the OpenAPI version the template advertises
    """
    return single_endpoint_template(
        "LinkML examples test",
        "/api/with-examples",
        "WithExamples",
        schema_id=TYPES_AND_ENUMS_ID,
        source="WithExamples",
        header=TEMPLATE_SERVERS_SECURITY,
        comment="# OpenAPI template referring a class whose slot declares multiple examples",
        oas_version=oas_version,
    )


def template_fixed(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a fully fixed template with no replaceable fields.

    :param oas_version: the OpenAPI version the template advertises
    """
    return openapi_template(
        "LinkML tests",
        endpoints=POST_FIXED,
        schemas="",
        header=TEMPLATE_SERVERS_SECURITY,
        comment="# OpenAPI template provided as template that is fully fixed\n"
        + "# because there are no fields to be replaced",
        oas_version=oas_version,
    )


def template_keep_scoped(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template whose single schema keeps ``keep_unreferenced`` scoped.

    :param oas_version: the OpenAPI version the template advertises
    """
    return single_endpoint_template(
        "Keep Unreferenced Scoped Test",
        "/api/foo",
        "Foo",
        schema_id=UNREFERENCED_WITH_UNRELATED_ID,
        source="Foo",
        oas_version=oas_version,
    )


def template_lowercase_class(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template whose endpoint references a lowercase-named LinkML class.

    :param oas_version: the OpenAPI version the template advertises
    """
    return single_endpoint_template(
        "LinkML tests",
        "/api/dataset",
        "Dataset",
        schema_id=KITCHEN_SINK_ID,
        source="Dataset",
        oas_version=oas_version,
    )


def template_renamed_type(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template exposing a LinkML type under a different OpenAPI resource name.

    :param oas_version: the OpenAPI version the template advertises
    """
    return single_endpoint_template(
        "Renamed Type Test",
        "/fixed",
        "Fixed",
        schema_id=TYPES_AND_ENUMS_ID,
        source="FixedType",
        description="ok",
        oas_version=oas_version,
    )


def template_renaming(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template exposing a LinkML class under a different OpenAPI resource name."""
    return single_endpoint_template(
        "LinkML tests - renaming",
        "/api/persons",
        "PersonResource",
        schema_id=KITCHEN_SINK_ID,
        source="Person",
        header=TEMPLATE_SERVERS_SECURITY,
        oas_version=oas_version,
    )


def template_missing_xlinkml_source(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template whose second schema stub omits the ``x-linkml-source`` key.

    :param oas_version: the OpenAPI version the template advertises
    """
    return openapi_template(
        "Foo API",
        endpoints=get_endpoint("/foo", "Foo", description="ok"),
        schemas=""
        + "".join(
            [
                schema_stub("Foo", FOO_ID, "Foo"),
                """\
    Bar:
      type: object
      x-linkml-schema: https://example.org/foo
""",
            ]
        ),
        oas_version=oas_version,
    )


def template_shared_responses(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template referencing a reusable ``components/responses`` entry.

    :param oas_version: the OpenAPI version the template advertises
    """
    return openapi_template(
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
        oas_version=oas_version,
    )


def template_referenced_parameter(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template whose endpoint parameter is given as a ``$ref``.

    :param oas_version: the OpenAPI version the template advertises
    """
    return openapi_template(
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
        oas_version=oas_version,
    )


def template_types(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template whose endpoint references a LinkML Type (constraints inlined)."""
    return single_endpoint_template(
        "LinkML type constraints test",
        "/api/code",
        "CodeStringRef",
        schema_id=TYPES_AND_ENUMS_ID,
        source="CodeString",
        comment="# OpenAPI template referring a Type defined in the LinkML schema",
        oas_version=oas_version,
    )


def template_types_enums(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template whose endpoint references a LinkML type.

    :param oas_version: the OpenAPI version the template advertises
    """
    return single_endpoint_template(
        "Types and Enums Test",
        "/api/fixed",
        "FixedType",
        schema_id=TYPES_AND_ENUMS_ID,
        source="FixedType",
        header=TEMPLATE_SERVERS_SECURITY,
        oas_version=oas_version,
    )


def template_wrong_schema_id(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template whose schema declares a mismatched ``x-linkml-schema`` id."""
    return single_endpoint_template(
        "LinkML tests - wrong schema id",
        "/api/endpoint1",
        "Person",
        schema_id=WRONG_SCHEMA_ID,
        source="Person",
        header=TEMPLATE_SERVERS_SECURITY,
        oas_version=oas_version,
    )


def template_comments(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template carrying comments on the header and an endpoint.

    :param oas_version: the OpenAPI version the template advertises
    """
    return openapi_template(
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
        oas_version=oas_version,
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


def template_keep_unreferenced(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template whose second schema is not referenced by any endpoint.

    :param oas_version: the OpenAPI version the template advertises
    """
    return openapi_template(
        "Keep Unreferenced Test",
        endpoints=get_endpoint("/api/person", "Person", secure=True),
        schemas=schema_stubs(
            [
                ("Person", KITCHEN_SINK_ID, "Person"),
                ("OpaqueEvent", KITCHEN_SINK_ID, "MarriageEvent"),
            ]
        ),
        header=TEMPLATE_SERVERS_SECURITY,
        oas_version=oas_version,
    )


def template_shared_enum(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template whose two endpoints reference classes sharing an enum.

    :param oas_version: the OpenAPI version the template advertises
    """
    return openapi_template(
        "Shared Enum Test",
        endpoints=get_endpoint("/foo", "Foo", description="ok") + get_endpoint("/bar", "Bar", description="ok"),
        schemas=schema_stubs(
            [
                ("Foo", SHARED_ENUM_ID, "Foo"),
                ("Bar", SHARED_ENUM_ID, "Bar"),
            ]
        ),
        oas_version=oas_version,
    )


def template_dangling_ref(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template with one schema sourced from a non-existent LinkML class.

    :param oas_version: the OpenAPI version the template advertises
    """
    return openapi_template(
        "Dangling Reference Test",
        endpoints=get_endpoint("/api/person", "Person", secure=True) + get_endpoint("/api/foo", "Foo", secure=True),
        schemas=schema_stubs(
            [
                ("Person", KITCHEN_SINK_ID, "Person"),
                ("Foo", KITCHEN_SINK_ID, "NonExistentClass"),
            ]
        ),
        header=TEMPLATE_SERVERS_SECURITY,
        oas_version=oas_version,
    )


def template_dangling_refs_multiple(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template with several schemas sourced from non-existent LinkML classes.

    :param oas_version: the OpenAPI version the template advertises
    """
    return openapi_template(
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
        oas_version=oas_version,
    )


def template_overrides(oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a template whose placeholders declare annotations overriding the LinkML ones.

    :param oas_version: the OpenAPI version the template advertises
    """
    ids = f"      x-linkml-schema: {TEMPLATE_OVERRIDES_ID}\n"
    schemas = f"""\
    # every overridable annotation on a class that already has a LinkML description;
    # externalDocs is a YAML anchor shared with Untouched below
    Described:
      type: object
      title: Described Title
      description: class description from the template
      example: {{color: RED}}
      externalDocs: &shared_docs {{url: https://example.org/docs, description: more}}
      deprecated: true
      x-vendor-flag: kept
{ids}      x-linkml-source: Described
    # no override declared, no LinkML description either
    Undescribed:
      type: object
{ids}      x-linkml-source: Undescribed
    # no description override, so the LinkML description must survive; reuses the anchor
    Untouched:
      type: object
      externalDocs: *shared_docs
{ids}      x-linkml-source: Untouched
    # override on a renamed enum that no endpoint references: it is reached only
    # through Described.color and must still be published as Colour
    Colour:
      type: object
      description: enum description from the template
{ids}      x-linkml-source: ColorEnum
    # override on a renamed type; `type: object` here must not clobber the generated type
    FixedRef:
      type: object
      description: type description from the template
{ids}      x-linkml-source: FixedType
"""
    return openapi_template(
        "Template Annotation Override Test",
        endpoints=get_endpoint("/api/described", "Described")
        + get_endpoint("/api/undescribed", "Undescribed")
        + get_endpoint("/api/untouched", "Untouched")
        + get_endpoint("/api/fixed", "FixedRef"),
        schemas=schemas,
        oas_version=oas_version,
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


# Each nested-reference shape gets its own single-endpoint template, so no shape can
# pass because another endpoint already referenced its resources.
NESTED_REF_SHAPES = {
    # A list endpoint: the resource sits under ``items`` of an array response.
    "items": (
        """\
    get:
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Person'
""",
        ["Person"],
    ),
    # A polymorphic response: the resources are members of ``oneOf``.
    "oneOf": (
        """\
    get:
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                oneOf:
                  - $ref: '#/components/schemas/MarriageEvent'
                  - $ref: '#/components/schemas/MedicalEvent'
""",
        ["MarriageEvent", "MedicalEvent"],
    ),
    # A request body that wraps its resource in ``allOf``.
    "allOf": (
        """\
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/Company'
      responses:
        '201':
          description: Created
""",
        ["Company"],
    ),
}


def template_nested_ref(shape: str, oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Compose a one-endpoint template that references its resources only under ``shape``.

    :param shape: a key of ``NESTED_REF_SHAPES``
    :param oas_version: the OpenAPI version the template advertises
    """
    operation, classes = NESTED_REF_SHAPES[shape]
    return openapi_template(
        "LinkML tests",
        endpoints="  /api/things:\n" + operation,
        schemas=schema_stubs([(name, KITCHEN_SINK_ID, name) for name in classes]),
        oas_version=oas_version,
    )


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


def gen_openapi_spec(head_path, kitchen_sink_path):
    openapigen = OpenApiGenerator(kitchen_sink_path)
    return openapigen.serialize(head_path)


def assert_fixed_value(schema: dict, expected, oas_version: str) -> None:
    """Assert a fixed-value schema exposes ``expected`` via the const/enum keyword of its version.

    The v3.0.3 JsonSchema path emits a fixed LinkML type as a single-item ``enum`` while
    the v3.1.0 Pydantic path keeps JSON Schema's native ``const``.
    """
    if oas_version == "3.0.3":
        assert schema["enum"] == [expected]
        assert "const" not in schema
    else:
        assert schema["const"] == expected
        assert "enum" not in schema


@pytest.fixture(params=list(OAS_VALIDATORS))
def oas_version(request):
    """The OpenAPI version under test; drives the version-parametrized fixtures/tests."""
    return request.param


@pytest.fixture
def openapi_spec(tmp_path, kitchen_sink_path, oas_version):
    head_path = write_template(tmp_path, template_head(oas_version=oas_version))
    return yaml.safe_load(gen_openapi_spec(head_path, kitchen_sink_path))


def test_openapi(tmp_path, kitchen_sink_path, oas_version):
    """Test if generation succeeds without failure and returns valid YAML."""
    head_path = write_template(tmp_path, template_head(oas_version=oas_version))
    openapi_spec = gen_openapi_spec(head_path, kitchen_sink_path)
    # ensure that valid YAML has been generated
    assert yaml.safe_load(openapi_spec)
    # ensure that valid OpenAPI spec has been generated
    assert validate(yaml.safe_load(openapi_spec), cls=OAS_VALIDATORS[oas_version]) is None


def test_openapi_missing_template(kitchen_sink_path):
    """Test that serialize raises ValueError when no template file is provided."""
    with pytest.raises(ValueError, match="An OpenAPI template file is required"):
        OpenApiGenerator(kitchen_sink_path).serialize()


def test_openapi_fixed_template(tmp_path, kitchen_sink_path, oas_version):
    """Test that a template with no replaceable fields is emitted byte-for-byte."""
    head_path = write_template(tmp_path, template_fixed(oas_version=oas_version))
    oa_spec = OpenApiGenerator(kitchen_sink_path).serialize(head_path)
    assert Path(head_path).read_text() == oa_spec


def test_openapi_spec_no_defs_references(openapi_spec):
    """Test that all $defs references are converted to components/schemas."""
    for schema in openapi_spec["components"]["schemas"].values():
        assert "#/$defs/" not in str(schema)


def test_openapi_spec_const_conversion(openapi_spec, oas_version):
    """Test const handling per version: enum arrays on 3.0.3, preserved const on 3.1.0."""
    person = openapi_spec["components"]["schemas"]["Person"]
    species_name = person["properties"]["species_name"]
    stomach_count = person["properties"]["stomach_count"]
    if oas_version == "3.0.3":
        # OpenAPI 3.0 has no ``const``; the generator rewrites it to a single-item ``enum``
        assert species_name["enum"] == ["human"]
        assert stomach_count["enum"] == [1]
        assert "const" not in species_name
        assert "const" not in stomach_count
    else:
        # OpenAPI 3.1 is aligned with JSON Schema 2020-12, so ``const`` is kept as-is
        assert "const" in str(species_name)
        assert "const" in str(stomach_count)


def test_openapi_v31_no_linkml_meta(tmp_path, kitchen_sink_path):
    """Test that the v3.1.0 Pydantic path strips ``linkml_meta`` annotations from schemas."""
    head_path = write_template(tmp_path, template_head(oas_version="3.1.0"))
    spec = yaml.safe_load(gen_openapi_spec(head_path, kitchen_sink_path))
    for schema in spec["components"]["schemas"].values():
        assert "linkml_meta" not in str(schema)


def test_openapi_spec_class_level_title_stripped(openapi_spec):
    """Test that class-level title (redundant with dict key) is removed but property-level description preserved."""
    person = openapi_spec["components"]["schemas"]["Person"]
    assert "title" not in person
    assert person["properties"]["age_in_years"]["description"] == "number of years since birth"


def test_openapi_spec_nullable_type_conversion(openapi_spec, oas_version):
    """Test nullable handling per version: anyOf on 3.0.3, native type arrays on 3.1.0."""
    emp_event = openapi_spec["components"]["schemas"]["EmploymentEvent"]
    type_prop = emp_event["properties"]["type"]
    if oas_version == "3.0.3":
        # OpenAPI 3.0 forbids type arrays; nullable ``["x", "null"]`` becomes ``anyOf``
        assert "anyOf" in type_prop
        assert "type" not in type_prop or not isinstance(type_prop["type"], list)
    else:
        # OpenAPI 3.1 permits nullable type arrays and ``anyOf`` alike; either is valid
        assert "anyOf" in type_prop or isinstance(type_prop.get("type"), list)


def test_openapi_spec_schemas_are_extensible(openapi_spec):
    """Test that generated class schemas are extensible (additionalProperties not false).

    APIs are typically extended backwards-compatibly by adding new objects or new
    attributes to existing objects. Closed schemas (additionalProperties: false) block
    that, so the generated OpenAPI schemas must stay open -- at every nesting level,
    including inlined sub-schemas (relevant for the v3.1.0 Pydantic path, which must be
    driven with ``extra_fields="allow"``).
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


def test_schema_id_mismatch_raises(tmp_path, kitchen_sink_path, oas_version):
    """Test that a mismatched x-linkml-schema raises ValueError with a descriptive message."""
    head_path = write_template(tmp_path, template_wrong_schema_id(oas_version=oas_version))
    with pytest.raises(ValueError, match="x-linkml-schema"):
        OpenApiGenerator(kitchen_sink_path).serialize(head_path)


def test_missing_x_linkml_source_raises(input_path, tmp_path, oas_version):
    """Test that a template schema missing x-linkml-source raises a descriptive KeyError.

    x-linkml-schema presence/value are validated nicely, but x-linkml-source was
    skipped, surfacing as a bare ``KeyError: 'x-linkml-source'`` during instantiation.
    """
    schema_path = input_path("openapi/schema_foo.yaml")
    head_path = write_template(tmp_path, template_missing_xlinkml_source(oas_version=oas_version))
    with pytest.raises(KeyError, match="Bar.*missing required 'x-linkml-source'"):
        OpenApiGenerator(schema_path, keep_unreferenced=True).serialize(head_path)


def test_referenced_parameter_does_not_crash(input_path, tmp_path, oas_version):
    """Test that a template parameter given as a $ref does not raise KeyError.

    A parameter entry of the form ``{$ref: '#/components/parameters/Limit'}`` has no
    ``schema`` key of its own (the schema lives inside ``components/parameters``), so
    reading ``param_spec["schema"]`` unconditionally crashed before generation.
    """
    schema_path = input_path("openapi/schema_foo.yaml")
    head_path = write_template(tmp_path, template_referenced_parameter(oas_version=oas_version))
    spec = yaml.safe_load(OpenApiGenerator(schema_path).serialize(head_path))
    # the reusable parameter survives untouched
    assert spec["paths"]["/foo"]["get"]["parameters"] == [{"$ref": "#/components/parameters/Limit"}]
    # and the endpoint schema is generated as usual
    assert "Foo" in spec["components"]["schemas"]
    assert validate(spec, cls=OAS_VALIDATORS[oas_version]) is None


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


def test_openapi_type_constraints(input_path, tmp_path, oas_version):
    """Test that a LinkML type (constraints inlined) still yields a standalone component schema.

    On both the v3.0.3 (JsonSchema) and v3.1.0 (Pydantic) paths, LinkML types are not
    emitted as classes; an endpoint referencing a type directly (via x-linkml-source)
    must still produce a component schema, otherwise the spec has a dangling ``$ref``.
    """
    schema_path = input_path("openapi/schema_types_and_enums.yaml")
    head_path = write_template(tmp_path, template_types(oas_version=oas_version))
    spec = yaml.safe_load(OpenApiGenerator(schema_path).serialize(head_path))
    schemas = spec["components"]["schemas"]
    # the type schema is exposed under the template's resource name, not dangling
    code_str = schemas["CodeStringRef"]
    assert code_str["type"] == "string"
    assert code_str["pattern"] == "^[A-Z]{2,10}$"
    assert code_str["description"] == "A 2-10 character uppercase code"
    assert validate(spec, cls=OAS_VALIDATORS[oas_version]) is None
    for schema in schemas.values():
        assert "#/$defs/" not in str(schema)


def test_renaming(tmp_path, kitchen_sink_path, oas_version):
    """Test that resource names differing from LinkML class names are renamed throughout the spec."""
    head_path = write_template(tmp_path, template_renaming(oas_version=oas_version))
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
    head_path = write_template(tmp_path, template_examples())
    spec = yaml.safe_load(OpenApiGenerator(schema_path).serialize(head_path))
    name_schema = spec["components"]["schemas"]["WithExamples"]["properties"]["name"]
    # first example is kept; the plural form is gone entirely
    assert name_schema["example"] == "sample"
    assert "examples" not in name_schema
    assert validate(spec, cls=OpenAPIV30SpecValidator) is None


def test_template_text_preserved(tmp_path, kitchen_sink_path, oas_version):
    """Test that everything above ``components/schemas`` is emitted verbatim.

    The generator no longer YAML round-trips the whole template (which would drop
    comments and normalise quoting/styling). Only the ``components/schemas`` section
    is regenerated; the header, paths and any comments above it must survive intact.
    """
    head_path = write_template(tmp_path, template_comments(oas_version=oas_version))
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


def test_unreferenced_schema_removed_by_default(tmp_path, kitchen_sink_path, oas_version):
    """Test that template schemas not referenced by any endpoint are removed by default."""
    head_path = write_template(tmp_path, template_keep_unreferenced(oas_version=oas_version))
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "Person" in schemas
    # OpaqueEvent(OpenAPI)/MarriageEvent(LinkML) is declared in the template but no endpoint references it
    assert "MarriageEvent" not in schemas


def test_keep_unreferenced_preserves_template_schema(tmp_path, kitchen_sink_path, oas_version):
    """Test that keep_unreferenced retains template schemas not referenced by any endpoint.

    Unreferenced sub-schemas can convey objects that are opaque to the API but relevant
    to clients (e.g. present in provided artifacts). The keep_unreferenced flag makes
    their removal switchable.
    """
    head_path = write_template(tmp_path, template_keep_unreferenced(oas_version=oas_version))
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path, keep_unreferenced=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "Person" in schemas
    # OpaqueEvent(OpenAPI)/MarriageEvent(LinkML) is kept even though no endpoint references it,
    # and is exposed under its OpenAPI resource name, not the LinkML class name
    assert "OpaqueEvent" in schemas
    assert "MarriageEvent" not in schemas


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


def test_keep_unreferenced_does_not_add_unrelated_schemas(tmp_path, oas_version):
    """Test that keep_unreferenced stays scoped to the template, not "dump everything".

    The chain schema also contains classes not reachable from ``Foo`` or the template
    declarations. ``keep_unreferenced`` only keeps the template-declared schemas and their
    transitive dependencies - it must not pull in the whole schema. Here the only other
    hidden class in the fixture is ``Baz Qux`` (already pulled by ``Foo Bar``), so a
    dedicated fixture with an unrelated class proves the flag does not regress to dumping
    every class.
    """
    schema_path = load_schema(SCHEMA_UNREFERENCED_WITH_UNRELATED)
    head_path = write_template(tmp_path, template_keep_scoped(oas_version=oas_version))
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


def test_inline_enums_inlines_enum_schemas(tmp_path, kitchen_sink_path, oas_version):
    """Test that inline_enums inlines enum sub-schemas into their parents.

    With the flag set, an enum no longer gets its own ``components/schemas`` entry;
    instead its definition is inlined where it was referenced.
    """
    head_path = write_template(tmp_path, template_head(oas_version=oas_version))
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


def test_inline_enums_does_not_inline_types(input_path, tmp_path, oas_version):
    """Test that inline_enums does not mistake fixed-value LinkML types for enums.

    A type with ``equals_string`` becomes a single-element ``enum`` after the
    ``const`` -> ``enum`` transform. A naive enum detection would then inline it away
    (``_inline_enum_schemas`` matches any schema with ``enum`` and no ``properties``);
    types must keep their named schema entry even when inlining is enabled.
    """
    schema_path = input_path("openapi/schema_types_and_enums.yaml")
    head_path = write_template(tmp_path, template_types_enums(oas_version=oas_version))
    spec = yaml.safe_load(OpenApiGenerator(schema_path, inline_enums=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    # the fixed-value type keeps its own named schema entry (not inlined)
    assert "FixedType" in schemas
    assert_fixed_value(schemas["FixedType"], "fixed-value", oas_version)
    assert schemas["FixedType"]["type"] == "string"


def test_inline_enums_disabled_keeps_types_and_enums_separate(input_path, tmp_path, oas_version):
    """Test that with inline_enums disabled both types and enums keep separate schema entries."""
    schema_path = input_path("openapi/schema_types_and_enums.yaml")
    head_path = write_template(tmp_path, template_types_enums(oas_version=oas_version))
    spec = yaml.safe_load(OpenApiGenerator(schema_path, inline_enums=False).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "FixedType" in schemas
    assert_fixed_value(schemas["FixedType"], "fixed-value", oas_version)
    assert schemas["FixedType"]["type"] == "string"


def test_inline_enums_keeps_endpoint_referenced_enum(tmp_path, oas_version):
    """Test that inline_enums does not inline an enum referenced directly by an endpoint.

    Inlining removes the enum's standalone ``components/schemas`` entry, which would
    leave the endpoint's ``$ref`` dangling. An enum that is itself the seeded schema of an
    endpoint must therefore keep its entry even when inlining is enabled.
    """
    schema_path = load_schema(SCHEMA_ENDPOINT_ENUM)
    head_path = write_template(tmp_path, template_endpoint_enum(oas_version=oas_version))
    spec = yaml.safe_load(OpenApiGenerator(schema_path, inline_enums=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "FixedEnum" in schemas
    assert schemas["FixedEnum"]["enum"] == ["FOO", "BAR"]
    assert spec["paths"]["/fixed-enum"]["get"]["responses"]["200"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/FixedEnum"
    }


def test_inline_enums_does_not_inline_renamed_enums(input_path, tmp_path, oas_version):
    """Test that inlining a renamed enum does not bypass the type guard.

    When the endpoint refers to a LinkML ``enum`` under a different OpenAPI name, the
    rename must not hide the fact that the source element is an enum. Otherwise the schema
    would be inlined away, leaving the endpoint's ``$ref`` dangling.
    """
    schema_path = input_path("openapi/schema_types_and_enums.yaml")
    head_path = write_template(tmp_path, template_renamed_type(oas_version=oas_version))
    spec = yaml.safe_load(OpenApiGenerator(schema_path, inline_enums=True).serialize(head_path))
    schemas = spec["components"]["schemas"]
    assert "Fixed" in schemas
    assert_fixed_value(schemas["Fixed"], "fixed-value", oas_version)
    assert spec["paths"]["/fixed"]["get"]["responses"]["200"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/Fixed"
    }


def test_inline_enums_shared_enum_no_yaml_anchors(tmp_path, oas_version):
    """Test that inlining a shared enum does not emit YAML anchors.

    When the same enum is referenced from two classes, the inlined copy must not be the
    very same Python object: reusing the object makes ``yaml.dump`` emit an ``&idNNN``
    anchor with an ``*idNNN`` alias for the second reference. The generated YAML must
    contain no anchors or aliases.
    """
    schema_path = load_schema(SCHEMA_SHARED_ENUM)
    head_path = write_template(tmp_path, template_shared_enum(oas_version=oas_version))
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


def test_inline_enums_preserves_slot_description(tmp_path, oas_version):
    """Test that inlining an enum keeps the slot-level description of the referencing property.

    A property that references an enum carries its own ``description`` next to the
    ``$ref``. Inlining must merge the enum definition into that property without
    discarding the slot-level ``description`` (the enum's own, here empty, description
    must not eclipse it).
    """
    schema_path = load_schema(SCHEMA_ENUM_SLOT_DESCRIPTION)
    head_path = write_template(tmp_path, template_enum_slot_description(oas_version=oas_version))
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


def test_lowercase_class_name_preserved(tmp_path, kitchen_sink_path, oas_version):
    """Test that a lowercase LinkML class name is preserved, not camelCased, in the spec.

    ``JsonSchemaGenerator`` camelCases ``$defs`` keys unless ``preserve_names=True``.
    In kitchen_sink the class ``activity`` (lowercase) is transitively reachable from
    ``Dataset`` via the ``activities`` slot. Without name preservation the emitted schema
    is keyed ``Activity`` while the ``$ref`` from ``Dataset`` points to ``activity``,
    yielding a missing schema and a dangling reference.
    """
    head_path = write_template(tmp_path, template_lowercase_class(oas_version=oas_version))
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path).serialize(head_path))
    schemas = spec["components"]["schemas"]
    # the LinkML name is preserved verbatim, not camelCased
    assert "activity" in schemas
    assert "Activity" not in schemas
    # Dataset references the activity schema under its original name
    assert schemas["Dataset"]["properties"]["activities"]["items"] == {"$ref": "#/components/schemas/activity"}
    # the produced spec is valid (no dangling reference)
    assert validate(spec, cls=OAS_VALIDATORS[oas_version]) is None


def test_dangling_reference_raises(tmp_path, kitchen_sink_path, oas_version):
    """Test that a generated spec containing an unresolvable $ref is rejected.

    The template declares a ``Foo`` schema sourced from a non-existent LinkML class,
    so no schema is generated for it while an endpoint still references it. The
    generator must detect the dangling ``$ref`` and fail loudly.
    """
    head_path = write_template(tmp_path, template_dangling_ref(oas_version=oas_version))
    with pytest.raises(ValueError, match="Dangling .ref"):
        OpenApiGenerator(kitchen_sink_path).serialize(head_path)


def test_dangling_reference_reports_all(tmp_path, kitchen_sink_path, oas_version):
    """All dangling ``$ref`` targets must be gathered and reported together, not just the first one.

    The template declares two schemas (``Foo`` and ``Bar``) sourced from non-existent LinkML classes,
    each referenced by its own endpoint. The single raised error must mention both.
    """
    head_path = write_template(tmp_path, template_dangling_refs_multiple(oas_version=oas_version))
    with pytest.raises(ValueError, match="Dangling .ref") as exc_info:
        OpenApiGenerator(kitchen_sink_path).serialize(head_path)
    message = str(exc_info.value)
    assert "#/components/schemas/Foo" in message
    assert "#/components/schemas/Bar" in message


@pytest.mark.parametrize("shape", list(NESTED_REF_SHAPES))
def test_nested_references_seed_generation(tmp_path, kitchen_sink_path, oas_version, shape):
    """Test that a ``$ref`` below the top level of an endpoint schema seeds generation.

    The template's only endpoint refers to its resources under ``items``, ``oneOf``
    or ``allOf``, never with a top-level ``$ref``. Each resource must be generated
    from the LinkML class rather than pruned as unreferenced, which would leave a
    dangling ``$ref``, and the endpoint schema must be kept as written.
    """
    template = template_nested_ref(shape, oas_version=oas_version)
    head_path = write_template(tmp_path, template)
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path).serialize(head_path))
    schemas = spec["components"]["schemas"]
    for name in NESTED_REF_SHAPES[shape][1]:
        assert "properties" in schemas[name], f"{name} was not generated"
    expected_paths = yaml.safe_load(template)["paths"]
    assert spec["paths"]["/api/things"] == expected_paths["/api/things"]


def test_refs_to_non_schema_components_allowed(tmp_path, kitchen_sink_path, oas_version):
    """Test that $refs to reusable components other than schemas (e.g. responses) are allowed.

    The dangling-reference check must resolve every internal ``$ref`` against its own
    ``components`` section rather than assuming all targets live under ``schemas``.
    """
    head_path = write_template(tmp_path, template_shared_responses(oas_version=oas_version))
    spec = yaml.safe_load(OpenApiGenerator(kitchen_sink_path).serialize(head_path))
    # the reusable response survives and is still referenced by the endpoint
    assert "NotFound" in spec["components"]["responses"]
    assert spec["paths"]["/foo"]["get"]["responses"]["404"] == {"$ref": "#/components/responses/NotFound"}
    # the schema is generated as usual
    assert "Person" in spec["components"]["schemas"]
    assert validate(spec, cls=OAS_VALIDATORS[oas_version]) is None


@pytest.fixture
def override_text(input_path, tmp_path, oas_version):
    """Raw generated YAML for the template-annotation-override fixtures."""
    schema_path = input_path("openapi/schema_template_overrides.yaml")
    head_path = write_template(tmp_path, template_overrides(oas_version=oas_version))
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
    ``Described`` placeholder in :func:`template_overrides`.
    """
    covered = {key for key, _ in NON_DESCRIPTION_OVERRIDE_CASES} | {"description"}
    assert covered == OVERRIDABLE_SCHEMA_KEYS


def test_linkml_description_kept_when_template_declares_none(override_spec):
    """Test that a schema whose placeholder declares no description keeps the LinkML one."""
    schemas = override_spec["components"]["schemas"]
    assert schemas["Untouched"]["description"] == "class description from LinkML, untouched"
    assert schemas["Undescribed"]["description"] == ""


def test_template_override_does_not_clobber_generated_type(override_spec, oas_version):
    """Test that a placeholder's ``type: object`` never overwrites the generated type.

    Placeholders conventionally carry ``type: object`` (the generic template emits it),
    but LinkML types and enums generate as ``type: string``. Overlaying structural keys
    would yield a schema rejecting every valid payload, so only annotations are merged.
    """
    schemas = override_spec["components"]["schemas"]
    assert schemas["FixedRef"]["type"] == "string"
    assert_fixed_value(schemas["FixedRef"], "fixed-value", oas_version)
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


def test_spec_with_template_overrides_is_valid(override_spec, oas_version):
    """Test that applying overrides still yields a valid OpenAPI document."""
    assert validate(override_spec, cls=OAS_VALIDATORS[oas_version]) is None


def test_wrongly_typed_annotation_override_is_rejected(input_path, tmp_path, oas_version):
    """Test that an annotation override of the wrong type fails template validation.

    OpenAPI requires ``deprecated`` to be a boolean. A LinkML-style string reason is
    rejected by the up-front template validation, before the override path runs, rather
    than being published into an invalid document.
    """
    schema_path = input_path("openapi/schema_template_overrides.yaml")
    template = template_overrides(oas_version=oas_version).replace("deprecated: true", "deprecated: use something else")
    head_path = write_template(tmp_path, template)
    with pytest.raises(OpenAPIValidationError):
        OpenApiGenerator(schema_path).serialize(head_path)


# The tests below pass gen-openapi its settings in a config file, with -C.


def openapi_config_yaml(**settings) -> str:
    """Return a config file in gen-project's format that holds ``settings`` under ``generator_args.openapi``.

    :param settings: option names, with dashes as underscores, and their values
    """
    return yaml.safe_dump({"generator_args": {"openapi": settings}}, sort_keys=False)


def template_described(title: str, oas_version: str = DEFAULT_OAS_VERSION) -> str:
    """Return a template with a path for ``Described`` and a placeholder for ``Untouched``, which no path references.

    :param title: the API title, which tells a test which of two templates was instantiated
    :param oas_version: the OpenAPI version the template declares
    """
    return openapi_template(
        title,
        endpoints=get_endpoint("/api/described", "Described"),
        schemas=schema_stubs(
            [("Described", TEMPLATE_OVERRIDES_ID, "Described"), ("Untouched", TEMPLATE_OVERRIDES_ID, "Untouched")]
        ),
        oas_version=oas_version,
    )


def test_cli_config_file_supplies_template_and_flags(input_path, tmp_path, oas_version):
    """Test that ``-C`` sets ``template``, ``keep_unreferenced`` and ``inline_enums`` together.

    The config file takes the place of ``-t``, ``-k`` and ``-e``. The generator instantiates
    the template the file names, keeps the placeholder ``Untouched`` that no path references,
    and inlines the enum of ``Described.color`` instead of writing it as a schema of its own.
    """
    template_path = write_template(tmp_path, template_described("From Config", oas_version=oas_version))
    config_path = tmp_path / "config.yaml"
    config_path.write_text(openapi_config_yaml(template=template_path, keep_unreferenced=True, inline_enums=True))

    result = CliRunner().invoke(cli, ["-C", str(config_path), input_path("openapi/schema_template_overrides.yaml")])

    assert result.exit_code == 0, result.output
    spec = yaml.safe_load(result.output)
    assert spec["info"]["title"] == "From Config"
    schemas = spec["components"]["schemas"]
    assert "Untouched" in schemas
    assert "ColorEnum" not in schemas
    assert schemas["Described"]["properties"]["color"]["enum"] == ["RED", "BLUE"]


def test_cli_explicit_template_overrides_config_file(input_path, tmp_path):
    """Test that ``-t`` on the command line takes precedence over ``template`` in the config file."""
    config_template = tmp_path / "config_template.yaml"
    config_template.write_text(template_described("From Config"))
    cli_template = tmp_path / "cli_template.yaml"
    cli_template.write_text(template_described("From CLI"))
    config_path = tmp_path / "config.yaml"
    config_path.write_text(openapi_config_yaml(template=str(config_template)))

    result = CliRunner().invoke(
        cli, ["-C", str(config_path), "-t", str(cli_template), input_path("openapi/schema_template_overrides.yaml")]
    )

    assert result.exit_code == 0, result.output
    spec = yaml.safe_load(result.output)
    assert spec["info"]["title"] == "From CLI"
    # -k and -e are left at their defaults, so the placeholder that no path references is pruned.
    assert "Untouched" not in spec["components"]["schemas"]


def test_cli_config_file_without_openapi_section_prints_generic_template(input_path, tmp_path):
    """Test that a config file without an ``openapi`` section changes nothing, so the generic template is printed."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text("generator_args:\n  java:\n    package: org.example\n")

    result = CliRunner().invoke(cli, ["-C", str(config_path), input_path("openapi/schema_template_overrides.yaml")])

    assert result.exit_code == 0, result.output
    assert "# TODO: remove this whole comment block after processing" in result.output
    assert "x-linkml-source: Described" in result.output


# The tests below create templates with --create-template from the expose and exclude settings.

EXPOSURE_ID = "https://w3id.org/linkml/tests/exposure"

# The settings most exposure tests create their template from: the core subset, Action added
# by name, Hazard excluded, and Risk's derived defaults replaced by explicit values.
EXPOSURE_SETTINGS = {
    "expose": {
        "subset": "core",
        "classes": {
            "Action": {},
            "Risk": {"path": "/risks", "operation_id": "list_risks", "summary": "Risks"},
        },
    },
    "exclude": ["Hazard"],
}


def create_template(schema_path: str, oas_version: str, **settings) -> dict:
    """Create a template from the exposure ``settings`` and parse it.

    :param schema_path: the LinkML schema to expose
    :param oas_version: the OpenAPI version the template declares
    :param settings: ``expose`` and ``exclude``, as the config file would carry them
    """
    return yaml.safe_load(OpenApiGenerator(schema_path, **settings).create_template(oas_version))


@pytest.fixture
def exposure_schema_path(input_path) -> str:
    return input_path("openapi/schema_exposure.yaml")


@pytest.fixture
def exposure_template(exposure_schema_path, oas_version) -> dict:
    """The template :data:`EXPOSURE_SETTINGS` creates, parsed."""
    return create_template(exposure_schema_path, oas_version, **EXPOSURE_SETTINGS)


def test_created_template_is_valid_for_its_version(exposure_template, oas_version):
    """Test that a created template validates, as it is, against the OpenAPI version it declares."""
    assert exposure_template["openapi"] == oas_version
    assert validate(exposure_template, cls=OAS_VALIDATORS[oas_version]) is None


def test_exposed_set_is_subset_plus_named_minus_excluded_abstract_and_mixin(exposure_template):
    """Test the exposed set: the subset's concrete classes, plus the named class, minus the excluded one.

    ``Entity`` (abstract) and ``Taggable`` (mixin) are in the core subset and must not be
    exposed. ``Hazard`` is in it and is excluded. ``Note`` is outside it and not named. The
    subset's members come first, then the named classes.
    """
    assert list(exposure_template["components"]["schemas"]) == ["Risk", "Action"]
    assert list(exposure_template["paths"]) == ["/risks", "/action"]


def test_placeholders_hold_structure_only(exposure_template):
    """Test that a placeholder holds ``type: object`` and the two bookkeeping keys, and nothing else.

    A description or title copied from the schema would drift from it. Both are generated when
    the template is instantiated.
    """
    for name, placeholder in exposure_template["components"]["schemas"].items():
        assert placeholder == {"type": "object", "x-linkml-schema": EXPOSURE_ID, "x-linkml-source": name}


def test_parameters_narrow_to_the_subset_slots_in_rank_order(exposure_template):
    """Test that a class's parameters are its induced slots in the subset, ordered by ``rank``.

    The core subset names ``hazards`` (rank 1), ``severity`` (rank 2) and the inherited ``id``
    (no rank), so ``count``, ``score``, ``active``, ``noted_on`` and the mixin's ``tag`` are left out.
    Each parameter holds structure only, typed as a string: ``hazards`` is a reference passed as
    an identifier, ``severity`` an enum passed as a value's text, ``id`` an identifier.
    """
    parameters = exposure_template["paths"]["/risks"]["get"]["parameters"]
    assert [p["name"] for p in parameters] == ["hazards", "severity", "id"]
    for parameter in parameters:
        assert parameter == {
            "in": "query",
            "name": parameter["name"],
            "required": False,
            "schema": {"type": "string"},
            "x-linkml-source": f"Risk.{parameter['name']}",
        }


def test_a_class_named_outside_the_subset_keeps_every_slot(exposure_template):
    """Test that the subset's slots narrow only the parameters of the classes in the subset.

    ``Action`` is named under ``expose.classes`` and is outside the core subset, so the subset
    says nothing about its slots. It keeps its own ``name`` and the inherited ``id``, although
    the core subset tags only ``id`` of the two.
    """
    parameters = exposure_template["paths"]["/action"]["get"]["parameters"]
    assert [p["x-linkml-source"] for p in parameters] == ["Action.name", "Action.id"]


# (slot, expected ``schema.type``) for every slot of Risk when no subset narrows them
PARAMETER_TYPE_CASES = [
    ("hazards", "string"),  # multivalued reference: one identifier per request
    ("severity", "string"),  # enum: the text of a permissible value
    ("count", "integer"),
    ("score", "number"),
    ("active", "boolean"),
    ("noted_on", "string"),  # date: a string, as the JSON Schema generator types it
    ("tag", "string"),  # inherited from the mixin
    ("id", "string"),  # inherited from the abstract parent
]


@pytest.mark.parametrize(("slot", "expected_type"), PARAMETER_TYPE_CASES)
def test_parameter_type_follows_the_slot_range(exposure_schema_path, oas_version, slot, expected_type):
    """Test that a parameter's ``schema.type`` follows the slot's range through its base type.

    The ``summary`` subset names classes only, so every induced slot of ``Risk`` becomes a
    parameter, and the cases cover each kind of type.
    """
    template = create_template(exposure_schema_path, oas_version, expose={"subset": "summary"})
    parameters = {p["x-linkml-source"]: p for p in template["paths"]["/risk"]["get"]["parameters"]}
    assert parameters[f"Risk.{slot}"]["schema"] == {"type": expected_type}


def test_a_subset_naming_no_slot_leaves_every_induced_slot(exposure_schema_path, oas_version):
    """Test that a subset with no slot members does not narrow the parameters, and rank still orders them."""
    template = create_template(exposure_schema_path, oas_version, expose={"subset": "summary"})
    sources = [p["x-linkml-source"] for p in template["paths"]["/risk"]["get"]["parameters"]]
    assert sources[:2] == ["Risk.hazards", "Risk.severity"]
    assert sorted(sources) == sorted(f"Risk.{slot}" for slot, _ in PARAMETER_TYPE_CASES)


def test_parameter_takes_the_slot_alias(tmp_path, exposure_schema_path, oas_version):
    """Test that a parameter is named as the payload names the slot, by its ``alias`` when it has one.

    ``noted_on`` has the alias ``notedOn``, which the generated schema uses for the property, so a
    client filters on the name it reads in a response. ``x-linkml-source`` keeps the slot name.
    """
    text = OpenApiGenerator(exposure_schema_path, expose={"subset": "summary"}).create_template(oas_version)
    parameters = yaml.safe_load(text)["paths"]["/risk"]["get"]["parameters"]
    assert {p["x-linkml-source"]: p["name"] for p in parameters}["Risk.noted_on"] == "notedOn"
    spec = yaml.safe_load(OpenApiGenerator(exposure_schema_path).serialize(write_template(tmp_path, text)))
    assert "notedOn" in spec["components"]["schemas"]["Risk"]["properties"]


def test_template_copies_no_linkml_field_values(exposure_schema_path, oas_version):
    """Test that no description, enum value or default from the schema reaches the template.

    Those values are generated at instantiation. Copied into the template, they would drift.
    """
    text = OpenApiGenerator(exposure_schema_path, **EXPOSURE_SETTINGS).create_template(oas_version)
    for linkml_value in ("a risk, the class every test exposes", "the hazards behind the risk", "low", "high"):
        assert linkml_value not in text


def test_explicit_entry_wins_over_derived_defaults(exposure_template):
    """Test that a class entry's path, operation id and summary take precedence over the derived defaults.

    ``Risk`` has an entry that sets all three. ``Action`` has an empty entry, so it gets
    ``/action``, ``list_action`` and ``Get Action``.
    """
    risk = exposure_template["paths"]["/risks"]["get"]
    assert (risk["operationId"], risk["summary"]) == ("list_risks", "Risks")
    action = exposure_template["paths"]["/action"]["get"]
    assert (action["operationId"], action["summary"]) == ("list_action", "Get Action")
    for name, operation in (("Risk", risk), ("Action", action)):
        response_schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
        assert response_schema == {"type": "array", "items": {"$ref": f"#/components/schemas/{name}"}}


def test_entry_description_is_the_operation_description(exposure_schema_path, oas_version):
    """Test that a class entry's ``description`` becomes its operation's, and that without one there is none.

    The class's description in the schema is never copied into the template, where it would drift.
    """
    template = create_template(
        exposure_schema_path,
        oas_version,
        expose={"classes": {"Risk": {"description": "Lists the risks, newest first"}, "Action": {}}},
    )
    risk = template["paths"]["/risk"]["get"]
    assert list(risk) == ["summary", "description", "operationId", "parameters", "responses"]
    assert risk["description"] == "Lists the risks, newest first"
    assert "description" not in template["paths"]["/action"]["get"]


def test_crud_false_gives_a_placeholder_without_an_endpoint(exposure_schema_path, oas_version):
    """Test that ``crud: false`` puts the class in ``components/schemas`` and gives it no path."""
    template = create_template(
        exposure_schema_path, oas_version, expose={"classes": {"Risk": {"crud": False}, "Action": {}}}
    )
    assert list(template["components"]["schemas"]) == ["Risk", "Action"]
    assert list(template["paths"]) == ["/action"]


def test_without_expose_every_concrete_class_is_exposed(exposure_schema_path, oas_version):
    """Test that without ``subset`` and ``classes``, every class that is neither abstract nor a mixin is exposed."""
    template = create_template(exposure_schema_path, oas_version)
    assert list(template["paths"]) == ["/risk", "/hazard", "/action", "/note"]


def test_exclude_accepts_a_bare_class_name(exposure_schema_path, oas_version):
    """Test that ``exclude: Hazard`` counts as a list of one, as the shared config code treats a scalar."""
    template = create_template(exposure_schema_path, oas_version, exclude="Hazard")
    assert list(template["paths"]) == ["/risk", "/action", "/note"]


@pytest.mark.parametrize("name", ["Entity", "Taggable"])
def test_a_named_abstract_or_mixin_class_is_exposed(tmp_path, exposure_schema_path, oas_version, name):
    """Test that the abstract and mixin filter applies to what a subset contributes, not to a named class.

    ``Entity`` is abstract and ``Taggable`` is a mixin. The core subset holds both and exposes
    neither. A class named under ``expose.classes`` is exposed even when it is abstract or a mixin,
    because a person chose it by name: a listing of an abstract class returns the records of its
    subclasses, and a schema may give a mixin records of its own. The created template
    instantiates on both versions.
    """
    text = OpenApiGenerator(exposure_schema_path, expose={"classes": {name: {}}}).create_template(oas_version)
    assert list(yaml.safe_load(text)["paths"]) == [f"/{name.lower()}"]
    spec = yaml.safe_load(OpenApiGenerator(exposure_schema_path).serialize(write_template(tmp_path, text)))
    assert list(spec["components"]["schemas"]) == [name]


def test_consumer_keys_in_a_class_entry_pass_through(exposure_schema_path, oas_version):
    """Test that a key the generator does not read, such as a server's routing setting, is left alone.

    A server that reads the same file may keep its own keys beside ``path``, such as a flag that
    adds filters of its own. A key that does not look like a misspelling of one of the
    generator's keys must not stop the template from being created.
    """
    template = create_template(exposure_schema_path, oas_version, expose={"classes": {"Risk": {"related": True}}})
    assert list(template["paths"]) == ["/risk"]


def test_info_comes_from_the_schema_metadata(exposure_template):
    """Test that ``info`` is the schema's title, version and description, so it cannot drift from them."""
    assert exposure_template["info"] == {
        "title": "The Exposure API",
        "version": "2.3.4",
        "description": "a schema whose classes an API exposes by subset and by name",
    }


def test_created_template_round_trips_with_no_dangling_ref(tmp_path, exposure_schema_path, oas_version):
    """Test the round trip: a created template instantiates into a valid document.

    ``serialize`` raises an error on a dangling ``$ref``, so a document it returns has none.
    Generated schemas replace the placeholders, and the enum that ``Risk.severity`` refers to is
    generated with them.
    """
    template_path = write_template(
        tmp_path, OpenApiGenerator(exposure_schema_path, **EXPOSURE_SETTINGS).create_template(oas_version)
    )
    spec = yaml.safe_load(OpenApiGenerator(exposure_schema_path).serialize(template_path))
    assert validate(spec, cls=OAS_VALIDATORS[oas_version]) is None
    schemas = spec["components"]["schemas"]
    assert sorted(schemas) == ["Action", "Risk", "SeverityEnum"]
    assert schemas["Risk"]["description"] == "a risk, the class every test exposes"
    assert "x-linkml-" not in str(schemas)


EXPOSURE_ERROR_CASES = [
    pytest.param({"expose": "Risk"}, "expected a YAML mapping at 'expose'", id="expose-scalar"),
    pytest.param({"expose": {"subsets": "core"}}, "unknown key 'subsets'", id="unknown-expose-key"),
    pytest.param({"expose": {"subset": "nope"}}, "declares no subset 'nope'", id="undeclared-subset"),
    pytest.param({"expose": {"classes": {"Nope": {}}}}, "no class 'Nope'", id="unknown-class"),
    pytest.param({"exclude": ["Nope"]}, "no class 'Nope'", id="unknown-excluded-class"),
    pytest.param(
        {"expose": {"classes": {"Risk": {}}}, "exclude": ["Risk"]},
        "Risk named both in expose.classes and in exclude",
        id="exposed-and-excluded",
    ),
    pytest.param({"expose": {"classes": {"Risk": {"crud": "yes"}}}}, "crud: expected bool", id="crud-not-bool"),
    pytest.param(
        {"expose": {"classes": {"Risk": {"description": ["Risks"]}}}},
        "description: expected str",
        id="description-not-str",
    ),
    pytest.param({"expose": {"classes": {"Risk": {"path": "risks"}}}}, "a path starts with '/'", id="path-no-slash"),
    pytest.param(
        {"expose": {"classes": {"Risk": {"operationId": "list_risks"}}}},
        "expose.classes.Risk.operationId: did you mean 'operation_id'?",
        id="openapi-spelling-of-a-key",
    ),
    pytest.param(
        {"expose": {"classes": {"Risk": {"summry": "Risks"}}}},
        "expose.classes.Risk.summry: did you mean 'summary'?",
        id="misspelt-key",
    ),
    pytest.param(
        {"expose": {"classes": {"Risk": {"path": "/x"}, "Action": {"path": "/x"}}}},
        "Risk and Action share the path /x",
        id="shared-path",
    ),
    pytest.param({"exclude": {"Risk": True}}, "exclude: expected a list of class names", id="exclude-mapping"),
]


@pytest.mark.parametrize(("settings", "message"), EXPOSURE_ERROR_CASES)
def test_malformed_exposure_settings_are_rejected(exposure_schema_path, settings, message):
    """Test that a mistake in the exposure settings is reported where it was made, before any output."""
    with pytest.raises(ValueError, match=re.escape(message)):
        OpenApiGenerator(exposure_schema_path, **settings).create_template()


def test_cli_create_template_reads_the_exposure_from_the_config_file(exposure_schema_path, tmp_path, oas_version):
    """Test that ``--create-template -C`` creates the template from the section's ``expose`` and ``exclude``.

    ``openapi_version`` is an option, so the config file sets it like any other option. The
    generator reads the exposure settings itself. The created template then instantiates through
    the same command with ``-t``.
    """
    config_path = tmp_path / "config.yaml"
    config_path.write_text(openapi_config_yaml(openapi_version=oas_version, **EXPOSURE_SETTINGS))

    result = CliRunner().invoke(cli, ["--create-template", "-C", str(config_path), exposure_schema_path])

    assert result.exit_code == 0, result.output
    template = yaml.safe_load(result.output)
    assert template["openapi"] == oas_version
    assert list(template["paths"]) == ["/risks", "/action"]

    template_path = write_template(tmp_path, result.output)
    result = CliRunner().invoke(cli, ["-t", template_path, "-C", str(config_path), exposure_schema_path])

    assert result.exit_code == 0, result.output
    assert validate(yaml.safe_load(result.output), cls=OAS_VALIDATORS[oas_version]) is None


def test_cli_malformed_expose_is_a_usage_error(exposure_schema_path, tmp_path):
    """Test that the command line reports a malformed ``expose`` as a usage error, not a traceback."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(openapi_config_yaml(expose={"subsets": "core"}))

    result = CliRunner().invoke(cli, ["--create-template", "-C", str(config_path), exposure_schema_path])

    assert result.exit_code == 2
    assert "expose: unknown key 'subsets'" in result.output


def test_cli_template_with_create_template_is_a_usage_error(exposure_schema_path, tmp_path):
    """Test that ``-t`` and ``--create-template`` given together on the command line are a usage error."""
    template_path = write_template(tmp_path, template_described("Existing"))

    result = CliRunner().invoke(cli, ["--create-template", "-t", template_path, exposure_schema_path])

    assert result.exit_code == 2
    assert "--template and --create-template cannot be given together" in result.output


def test_cli_config_file_names_the_template_it_creates(exposure_schema_path, tmp_path, oas_version):
    """Test that one config file both creates the template it names and then instantiates it.

    The template does not exist until ``--create-template`` writes it, so the first run must
    not read it. The second run, with ``-C`` alone, instantiates it.
    """
    template_path = tmp_path / "api-template.yaml"
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        openapi_config_yaml(template=str(template_path), openapi_version=oas_version, **EXPOSURE_SETTINGS)
    )

    result = CliRunner().invoke(cli, ["--create-template", "-C", str(config_path), exposure_schema_path])

    assert result.exit_code == 0, result.output
    template_path.write_text(result.output)
    result = CliRunner().invoke(cli, ["-C", str(config_path), exposure_schema_path])

    assert result.exit_code == 0, result.output
    spec = yaml.safe_load(result.output)
    assert list(spec["paths"]) == ["/risks", "/action"]
    assert validate(spec, cls=OAS_VALIDATORS[oas_version]) is None
