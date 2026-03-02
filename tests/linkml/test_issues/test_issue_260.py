import pytest

from linkml.generators.pythongen import PythonGenerator


@pytest.mark.pythongen
def test_local_imports(input_path, snapshot):
    """Check the local import behavior"""
    test_dir = "issue_260"

    output = PythonGenerator(
        input_path(f"{test_dir}/issue_260a.yaml"),
        mergeimports=False,
    ).serialize()
    assert output == snapshot(f"{test_dir}/issue_260a.py")

    output = PythonGenerator(
        input_path(f"{test_dir}/issue_260b.yaml"),
        mergeimports=False,
    ).serialize()
    assert output == snapshot(f"{test_dir}/issue_260b.py")

    output = PythonGenerator(
        input_path(f"{test_dir}/issue_260c.yaml"),
        mergeimports=False,
    ).serialize()
    assert output == snapshot(f"{test_dir}/issue_260c.py")

    output = PythonGenerator(
        input_path(f"{test_dir}/issue_260.yaml"),
        mergeimports=False,
    ).serialize()
    assert output == snapshot(f"{test_dir}/issue_260.py")
