import pytest
import yaml.constructor

from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader
from tests.test_issues.environment import env


def test_issue_1040_file_name() -> None:
    """issue_1040.yaml has a parsing error is confusing as all getout when accompanied by a stack
    trace.  We use this to make sure that the file name gets in correctly."""
    with pytest.raises(yaml.constructor.ConstructorError, match='"issue_1040.yaml"'):
        yaml_loader.load(env.input_path("issue_1040.yaml"), SchemaDefinition)
