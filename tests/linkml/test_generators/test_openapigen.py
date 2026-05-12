import pytest
import yaml
from openapi_spec_validator import OpenAPIV30SpecValidator, validate

from linkml.generators.openapigen import OpenApiGenerator


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


def test_resources_presence_and_absence(openapi_spec):
    # ensure expected resource schemas are present
    assert "MarriageEvent" in openapi_spec["components"]["schemas"].keys()
    assert "MedicalEvent" in openapi_spec["components"]["schemas"].keys()
    assert "DiagnosisConcept" in openapi_spec["components"]["schemas"].keys()
    assert "Person" in openapi_spec["components"]["schemas"].keys()
    # ensure unneeded resource schemas are not present
    assert "AnyOfSimpleType" not in openapi_spec["components"]["schemas"].keys()
