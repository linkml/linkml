import pytest
from linkml_runtime.utils.schemaview import SchemaView

from linkml.utils.datautils import infer_root_class


def test_jsonschema_validation(input_path):
    """Test case that tries to infer the target class for a schema
    that has a local import and doesn't explicitly specify the
    target class"""
    SCHEMA = input_path("issue_494/slot_usage_example.yaml")
    sv = SchemaView(schema=SCHEMA)

    with pytest.raises(
        RuntimeError,
        match="Multiple potential target "
        r"classes found: \['annotation', 'Container'\]. "
        "Please specify a target using --target-class "
        "or by adding tree_root: true to the relevant class in the schema",
    ):
        # infer target_class rather than explicit specification
        infer_root_class(sv)
