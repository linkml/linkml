import json

from linkml.generators.jsonschemagen import JsonSchemaGenerator


def test_required_property_json_schema(input_path):
    """Check that the xsd:dateTime format is per ISO 8601 standards."""

    json_schema_str = JsonSchemaGenerator(
        input_path("issue_433_fixed.yaml"),
        top_class="PhysicalSampleRecord",
    ).serialize()

    json_schema_dict = json.loads(json_schema_str)

    # check if the required key is part of the dictionary
    assert "required" in json_schema_dict

    # valdiate the values that show up in the required property
    assert sorted(json_schema_dict["required"]) == [
        "id",
        "label",
        "sampleidentifier",
    ]
