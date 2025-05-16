import pytest

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.pythongen import PythonGenerator


@pytest.mark.jsonschemagen
@pytest.mark.pythongen
def test_issue_120(input_path, snapshot):
    """Courses not inlining"""
    output = PythonGenerator(input_path("issue_120.yaml")).serialize()
    assert output == snapshot("issue_120.py")

    output = JsonSchemaGenerator(input_path("issue_120.yaml")).serialize()
    assert output == snapshot("issue_120.json")
