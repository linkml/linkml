import pytest

from linkml.generators.pythongen import PythonGenerator


@pytest.mark.pythongen
def test_prefix(input_path, snapshot):
    output = PythonGenerator(input_path("issue_107.yaml")).serialize()
    assert output == snapshot("issue_107.py")
