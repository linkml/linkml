from linkml.generators.jsonschemagen import JsonSchemaGenerator
from tests import DEFAULT_LOG_LEVEL


def test_json_schema_with_materialized_patterns(input_path, snapshot):
    """Ensure JSON Schema generation correctly materializes structured patterns."""
    json_schema = JsonSchemaGenerator(
        input_path("issue_2499.yaml"), log_level=DEFAULT_LOG_LEVEL, materialize_patterns=True
    ).serialize()
    assert json_schema == snapshot("issue_2499.json")
