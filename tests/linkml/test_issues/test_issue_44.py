import pytest

from linkml.generators.pythongen import PythonGenerator


@pytest.mark.pythongen
def test_multiple_postinit(input_path, snapshot):
    """Generate postinit code for a multi-occurring element"""
    output = PythonGenerator(input_path("issue_44.yaml"), emit_metadata=False).serialize()
    assert output == snapshot("issue_44.py")
