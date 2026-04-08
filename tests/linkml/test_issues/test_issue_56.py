import pytest

from linkml.generators.pythongen import PythonGenerator


@pytest.mark.xfail
def test_slot_subclass(input_path, snapshot):
    """Test slot domain as superclass of parent"""
    output = PythonGenerator(input_path("issue_56_good.yaml")).serialize()
    assert output == snapshot("issue_56_good.py")

    with pytest.raises(Exception):
        PythonGenerator(input_path("issue_56_bad.yaml")).serialize()
