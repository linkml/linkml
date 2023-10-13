from linkml_runtime import SchemaView


def test_something(input_path):
    sv = SchemaView(input_path("issue_756.yaml"))
    assert sv.schema.name == "test"  # add assertion here
