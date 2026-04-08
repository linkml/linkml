from linkml.utils.schemaloader import SchemaLoader


def test_slot_usage_range(input_path):
    """Test to make the absolute minimal model work"""
    schema = SchemaLoader(input_path("issue_213.yaml")).resolve()
    assert schema.slots["my slot"].range == "string"
