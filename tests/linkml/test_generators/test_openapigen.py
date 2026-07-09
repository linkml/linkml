import pytest
import yaml
from openapi_spec_validator import OpenAPIV30SpecValidator, OpenAPIV31SpecValidator, validate
from referencing.exceptions import PointerToNowhere

from linkml.generators.openapigen import OpenApiGenerator


def gen_openapi_spec(head_path, kitchen_sink_path):
    openapigen = OpenApiGenerator(kitchen_sink_path)
    return openapigen.serialize(head_path)


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


@pytest.mark.parametrize(
    "templating",
    [
        ("openapi/spec-head-v30.openapi.yaml", OpenAPIV30SpecValidator),
        ("openapi/spec-head-v31.openapi.yaml", OpenAPIV31SpecValidator),
    ],
)
def test_openapi_no_defs_references(openapi_spec):
    """Test that all $defs references are converted to components/schemas."""
    for schema in openapi_spec["components"]["schemas"].values():
        assert "#/$defs/" not in str(schema)


@pytest.mark.parametrize(
    "templating",
    [
        ("openapi/spec-head-v31.openapi.yaml", OpenAPIV31SpecValidator),
    ],
)
def test_openapi_v31_no_linkml_meta(openapi_spec):
    for schema in openapi_spec["components"]["schemas"].values():
        assert "linkml_meta" not in str(schema)


@pytest.mark.parametrize(
    "templating",
    [
        ("openapi/spec-head-v30.openapi.yaml", OpenAPIV30SpecValidator),
    ],
)
def test_openapi_v30_const_to_enum_conversion(openapi_spec):
    """Test that const values are converted to single-item enum arrays (OpenAPI 3.1.0)."""
    person = openapi_spec["components"]["schemas"]["Person"]
    print(person)
    assert person["properties"]["species_name"]["enum"] == ["human"]
    assert person["properties"]["stomach_count"]["enum"] == [1]
    assert "const" not in person["properties"]["species_name"]
    assert "const" not in person["properties"]["stomach_count"]


@pytest.mark.parametrize(
    "templating",
    [
        ("openapi/spec-head-v31.openapi.yaml", OpenAPIV31SpecValidator),
    ],
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


@pytest.mark.parametrize(
    "templating",
    [
        ("openapi/spec-head-v30.openapi.yaml", OpenAPIV30SpecValidator),
        ("openapi/spec-head-v31.openapi.yaml", OpenAPIV31SpecValidator),
    ],
)
def test_openapi_class_level_title_stripped(openapi_spec):
    """Test that class-level title (redundant with dict key) is removed but property-level description preserved."""
    person = openapi_spec["components"]["schemas"]["Person"]
    assert "title" not in person
    assert person["properties"]["age_in_years"]["description"] == "number of years since birth"


@pytest.mark.parametrize(
    "templating",
    [
        ("openapi/spec-head-v30.openapi.yaml", OpenAPIV30SpecValidator),
        ("openapi/spec-head-v31.openapi.yaml", OpenAPIV31SpecValidator),
    ],
)
def test_openapi_nullable_type_conversion(openapi_spec):
    """Test that nullable type arrays are converted to anyOf."""
    emp_event = openapi_spec["components"]["schemas"]["EmploymentEvent"]
    assert "anyOf" in emp_event["properties"]["type"]
    assert "type" not in emp_event["properties"]["type"] or not isinstance(
        emp_event["properties"]["type"]["type"], list
    )


@pytest.mark.parametrize(
    "templating",
    [
        ("openapi/spec-head-v30.openapi.yaml", OpenAPIV30SpecValidator),
        ("openapi/spec-head-v31.openapi.yaml", OpenAPIV31SpecValidator),
    ],
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
