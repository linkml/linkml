from linkml.utils.schemaloader import SchemaLoader


def test_inherited_slot(input_path):
    """Validate default slot range settings"""
    schema = SchemaLoader(input_path("inherited_slots.yaml")).resolve()
    assert "same as" in schema.classes["named thing"].slots
