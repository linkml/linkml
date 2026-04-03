import yaml
from openapi_spec_validator import OpenAPIV30SpecValidator, validate

from linkml.generators.openapigen import OpenApiGenerator


def gen_openapi_spec(head_path, kitchen_sink_path):
    openapigen = OpenApiGenerator(kitchen_sink_path)
    return openapigen.serialize(head_path)


def test_openapi(input_path, kitchen_sink_path):
    """Test if generation succeeds without failure and returns valid YAML."""
    head_path = str(input_path("openapi/spec-head.openapi.yaml"))
    openapi_spec = gen_openapi_spec(head_path, kitchen_sink_path)
    # ensure that valid YAML has been generated
    assert yaml.safe_load(openapi_spec)
    # ensure that valid OpenAPI spec has been generated
    assert validate(yaml.safe_load(openapi_spec), cls=OpenAPIV30SpecValidator) is None


def test_resources_presence_and_absence(input_path, kitchen_sink_path):
    head_path = str(input_path("openapi/spec-head.openapi.yaml"))
    openapi_spec = gen_openapi_spec(head_path, kitchen_sink_path)
    openapi_spec_yaml = yaml.safe_load(openapi_spec)
    # ensure expected resource schemas are present
    assert "MarriageEvent" in openapi_spec_yaml["components"]["schemas"].keys()
    assert "MedicalEvent" in openapi_spec_yaml["components"]["schemas"].keys()
    assert "DiagnosisConcept" in openapi_spec_yaml["components"]["schemas"].keys()
    assert "Person" in openapi_spec_yaml["components"]["schemas"].keys()
    # ensure unneeded resource schemas as not present
    assert "AnyOfSimpleType" not in openapi_spec_yaml["components"]["schemas"].keys()
