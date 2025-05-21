import pytest
from jsonasobj2 import as_json
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator


@pytest.mark.pythongen
def test_issue_121(input_path, snapshot):
    """Make sure that types are generated as part of the output"""
    python = PythonGenerator(input_path("issue_121.yaml")).serialize()
    assert python == snapshot("issue_121.py")

    has_includes = False
    for line in python.split("\n"):
        if line.startswith("from linkml_runtime.linkml_model.types "):
            assert line == "from linkml_runtime.linkml_model.types import String"
            has_includes = True
    assert has_includes
    module = compile_python(python)

    example = module.Biosample(depth="test")
    assert hasattr(example, "depth")
    assert example.depth == "test"

    example2 = module.ImportedClass()

    example_json = as_json(example)
    assert example_json == snapshot("issue_121_1.json")

    example_json_2 = as_json(example2)
    assert example_json_2 == snapshot("issue_121_2.json")
