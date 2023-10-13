import pytest

from linkml.generators.pythongen import PythonGenerator


@pytest.mark.skip("issue_38.yaml clinical profile conflicts with latest Biolink Model")
def test_python_import(input_path, snapshot):
    """Import generates for biolink-model"""
    python = PythonGenerator(
        input_path("issue_38.yaml"),
        importmap=input_path("biolink-model-importmap.json"),
    ).serialize()
    assert python == snapshot("issue_38.py")
