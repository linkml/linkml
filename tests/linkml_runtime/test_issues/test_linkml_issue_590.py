from linkml_runtime.utils.schemaview import SchemaView
from tests.test_issues.environment import env

SCHEMA = env.input_path("test_linkml_issue_590.yaml")


def test_issue_590() -> None:
    """Test that get_slot() returns attribute not top level slot."""
    sv = SchemaView(SCHEMA)
    # check that multivalued is set to False as in schema
    assert sv.get_slot("a").multivalued is False
