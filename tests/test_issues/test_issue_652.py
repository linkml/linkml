import json

import pytest

from linkml.generators.jsonschemagen import JsonSchemaGenerator


@pytest.mark.jsonschemagen
def test_issue_652_scenario1(input_path):
    """
    Generate JSON Schema in default mode, where range class
    descendants are not included
    """
    output = JsonSchemaGenerator(input_path("issue_652.yaml"), include_range_class_descendants=False).serialize()

    issue_jsonschema = json.loads(output)
    prop4_def = issue_jsonschema["$defs"]["NamedThing"]["properties"]["prop4"]
    assert prop4_def["anyOf"][0]["$ref"] == "#/$defs/C1"


@pytest.mark.jsonschemagen
def test_issue_652_scenario2(input_path):
    """
    Generate JSON Schema where descendants of range class
    are included for the type of a property
    """
    output = JsonSchemaGenerator(input_path("issue_652.yaml"), include_range_class_descendants=True).serialize()

    issue_jsonschema = json.loads(output)
    prop4_def = issue_jsonschema["$defs"]["NamedThing"]["properties"]["prop4"]
    assert "anyOf" in prop4_def
    assert len(prop4_def["anyOf"]) == 4
    assert {"$ref": "#/$defs/C1"} in prop4_def["anyOf"]
    assert {"$ref": "#/$defs/C2"} in prop4_def["anyOf"]
    assert {"$ref": "#/$defs/C3"} in prop4_def["anyOf"]
