import pytest

from linkml.generators.pythongen import PythonGenerator


@pytest.mark.pythongen
def test_issue_106(input_path, snapshot):
    output = PythonGenerator(input_path("issue_106.yaml")).serialize()
    assert output == snapshot("issue_106.py")
