from jsonasobj2 import loads

from linkml.generators.jsonschemagen import JsonSchemaGenerator


def test_issue_202(input_path, snapshot):
    output = JsonSchemaGenerator(input_path("issue_202.yaml")).serialize()
    assert output == snapshot("issue_202.json.schema")

    json_schema = loads(output)
    assert json_schema["$defs"].GeospatialDDCoordLocation.properties.latitude.type == "number"
