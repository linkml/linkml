import pytest
import yaml
from openapi_spec_validator import OpenAPIV30SpecValidator, OpenAPIV31SpecValidator, validate

from linkml.generators.openapigen import OpenApiGenerator


def gen_openapi_spec(head_path, kitchen_sink_path, openapi_version="3.0.3"):
    openapigen = OpenApiGenerator(kitchen_sink_path, openapi_version=openapi_version)
    return openapigen.serialize(head_path)


@pytest.fixture
def openapi_spec_v303(input_path, kitchen_sink_path):
    head_path = str(input_path("openapi/spec-head.openapi.yaml"))
    openapigen = OpenApiGenerator(kitchen_sink_path, openapi_version="3.0.3")
    return yaml.safe_load(openapigen.serialize(head_path))


@pytest.fixture
def openapi_spec_v310(input_path, kitchen_sink_path):
    head_path = str(input_path("openapi/spec-head-v31.openapi.yaml"))
    openapigen = OpenApiGenerator(kitchen_sink_path, openapi_version="3.1.0")
    return yaml.safe_load(openapigen.serialize(head_path))


def test_openapi_v303(input_path, kitchen_sink_path):
    """Test if v3.0.3 generation succeeds and returns valid OpenAPI."""
    head_path = str(input_path("openapi/spec-head.openapi.yaml"))
    openapi_spec = gen_openapi_spec(head_path, kitchen_sink_path, openapi_version="3.0.3")
    parsed = yaml.safe_load(openapi_spec)
    assert parsed
    assert validate(parsed, cls=OpenAPIV30SpecValidator) is None


def test_openapi_v310(input_path, kitchen_sink_path):
    """Test if v3.1.0 generation succeeds and returns valid OpenAPI."""
    head_path = str(input_path("openapi/spec-head-v31.openapi.yaml"))
    openapi_spec = gen_openapi_spec(head_path, kitchen_sink_path, openapi_version="3.1.0")
    parsed = yaml.safe_load(openapi_spec)
    assert parsed
    assert validate(parsed, cls=OpenAPIV31SpecValidator) is None


def test_openapi_missing_template(kitchen_sink_path):
    """Test that serialize raises ValueError when no template file is provided."""
    with pytest.raises(ValueError, match="An OpenAPI template file is required"):
        OpenApiGenerator(kitchen_sink_path).serialize()


# --- v3.0.3 specific tests ---


def test_openapi_v303_no_defs_references(openapi_spec_v303):
    """Test that all $defs references are converted to components/schemas."""
    for schema in openapi_spec_v303["components"]["schemas"].values():
        assert "#/$defs/" not in str(schema)


def test_openapi_v303_const_to_enum_conversion(openapi_spec_v303):
    """Test that const values are converted to single-item enum arrays."""
    person = openapi_spec_v303["components"]["schemas"]["Person"]
    assert person["properties"]["species_name"]["enum"] == ["human"]
    assert person["properties"]["stomach_count"]["enum"] == [1]
    assert "const" not in person["properties"]["species_name"]
    assert "const" not in person["properties"]["stomach_count"]


def test_openapi_v303_class_level_title_stripped(openapi_spec_v303):
    """Test that class-level title (redundant with dict key) is removed but property-level description preserved."""
    person = openapi_spec_v303["components"]["schemas"]["Person"]
    assert "title" not in person
    assert person["properties"]["age_in_years"]["description"] == "number of years since birth"


def test_openapi_v303_nullable_type_conversion(openapi_spec_v303):
    """Test that nullable type arrays are converted to anyOf."""
    emp_event = openapi_spec_v303["components"]["schemas"]["EmploymentEvent"]
    assert "anyOf" in emp_event["properties"]["type"]
    assert "type" not in emp_event["properties"]["type"] or not isinstance(
        emp_event["properties"]["type"]["type"], list
    )


# --- v3.1.0 specific tests ---


def test_openapi_v310_no_defs_references(openapi_spec_v310):
    """Test that all $defs references are converted to components/schemas."""
    for schema in openapi_spec_v310["components"]["schemas"].values():
        assert "#/$defs/" not in str(schema)


def test_openapi_v310_no_linkml_meta(openapi_spec_v310):
    """Test that linkml_meta annotations are stripped from v3.1.0 output."""
    for schema in openapi_spec_v310["components"]["schemas"].values():
        assert "linkml_meta" not in str(schema)


def test_openapi_v310_preserves_const(openapi_spec_v310):
    """Test that const values are preserved as-is (valid in OpenAPI 3.1.0)."""
    person = openapi_spec_v310["components"]["schemas"]["Person"]
    species_name = person["properties"]["species_name"]
    if "anyOf" in species_name:
        const_branches = [b for b in species_name["anyOf"] if "const" in b]
        assert len(const_branches) > 0, "const should be present in anyOf branches for v3.1.0"
    else:
        assert "const" in species_name, "const should be preserved in v3.1.0"


def test_openapi_v310_class_level_title_stripped(openapi_spec_v310):
    """Test that class-level title is removed but property-level description preserved."""
    person = openapi_spec_v310["components"]["schemas"]["Person"]
    assert "title" not in person
    assert person["properties"]["age_in_years"]["description"] == "number of years since birth"


def test_openapi_v310_nullable_uses_anyof(openapi_spec_v310):
    """Test that nullable fields use anyOf (Pydantic v2 native representation)."""
    emp_event = openapi_spec_v310["components"]["schemas"]["EmploymentEvent"]
    type_prop = emp_event["properties"]["type"]
    assert "anyOf" in type_prop


# --- shared tests ---


def test_openapi_v303_resources_presence_and_absence(openapi_spec_v303):
    assert "MarriageEvent" in openapi_spec_v303["components"]["schemas"]
    assert "MedicalEvent" in openapi_spec_v303["components"]["schemas"]
    assert "DiagnosisConcept" in openapi_spec_v303["components"]["schemas"]
    assert "Person" in openapi_spec_v303["components"]["schemas"]
    assert "AnyOfSimpleType" not in openapi_spec_v303["components"]["schemas"]


def test_openapi_v310_resources_presence_and_absence(openapi_spec_v310):
    assert "MarriageEvent" in openapi_spec_v310["components"]["schemas"]
    assert "MedicalEvent" in openapi_spec_v310["components"]["schemas"]
    assert "DiagnosisConcept" in openapi_spec_v310["components"]["schemas"]
    assert "Person" in openapi_spec_v310["components"]["schemas"]
    assert "AnyOfSimpleType" not in openapi_spec_v310["components"]["schemas"]
