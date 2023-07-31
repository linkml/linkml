import pytest
import yaml


def test_yaml_load(input_path):
    """Test case to ensure that we are using the right
    signature for the yaml.load() method."""

    # load any random input YAML files from previous tests
    SCHEMA = input_path("issue_494/testme.yaml")

    # negative test case to check TypeError is raised
    # when we don't pass value to Loader argument
    with open(SCHEMA) as f:
        with pytest.raises(TypeError):
            yaml.load(stream=f)

    # compare results when we pass a value to the Loader
    # argument as expected
    expected_dict = {
        "id": "file://testmodel",
        "classes": {"annotation": {"description": "dummy", "abstract": True}},
    }
    with open(SCHEMA) as f:
        actual_dict = yaml.load(stream=f, Loader=yaml.Loader)

    assert actual_dict == expected_dict
