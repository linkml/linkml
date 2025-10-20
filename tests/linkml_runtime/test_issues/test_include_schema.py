from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml_runtime.loaders import yaml_loader
from tests.test_issues.environment import env

# https://github.com/linkml/linkml/issues/3


def test_include_schema():
    """
    Test for GitHub issue #3: include_schema.yaml produces a Python exception on an uncaught error

    This is a regression test to ensure schema inclusion works without throwing exceptions.
    """
    # Load schema file - this should not raise an exception
    inp = yaml_loader.load(env.input_path("include_schema.yaml"), SchemaDefinition)

    # Verify the schema was loaded successfully
    assert inp is not None
    assert isinstance(inp, SchemaDefinition)
