from linkml.utils.schemaloader import SchemaLoader

# Issue #206 - SchemaLoader needs to do a yaml_loader.load early on


def test_class_list(input_path):
    """SchemaLoader should be monotonic - metamodel test"""
    schema = SchemaLoader(input_path("issue_206.yaml")).resolve()
    assert list(schema.classes) == ["Entity"]
    assert schema.classes["Entity"].slots == ["entity__id", "entity__description"]
