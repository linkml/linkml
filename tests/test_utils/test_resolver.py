from linkml.utils.schemaloader import SchemaLoader


def test_default_range(input_path):
    """Validate default slot range settings"""
    schema = SchemaLoader(input_path("resolver1.yaml")).resolve()
    assert {"s1": "t1", "s2": "t2"} == {slot.name: slot.range for slot in schema.slots.values()}
    schema = SchemaLoader(input_path("resolver2.yaml")).resolve()
    assert {"s1": "string", "s2": "t2"} == {slot.name: slot.range for slot in schema.slots.values()}


def test_type_uri(input_path):
    """Validate type URI's and the fact that they aren't inherited"""
    schema = SchemaLoader(input_path("resolver2.yaml")).resolve()
    assert {
        "string": "xsd:string",
        "t1": "xsd:string",
        "t2": "xsd:int",
        "t3": "xsd:string",
    } == {t.name: t.uri for t in schema.types.values()}
