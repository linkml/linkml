import pytest
from jsonasobj2 import as_json
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator


@pytest.mark.pythongen
def test_issue_113(input_path, snapshot):
    """Make sure that types are generated as part of the output"""
    output = PythonGenerator(input_path("issue_113.yaml")).serialize()
    assert output == snapshot("issue_113.py")

    module = compile_python(output)
    example = module.TestClass(test_attribute_2="foo")
    assert hasattr(example, "test_attribute_2")
    assert hasattr(example, "test_attribute_1")
    example.wiible = "foo"
    example.test_attribute_1 = "foo"
    example.test_attribute_2 = "foo"

    example_json = as_json(example)
    assert example_json == snapshot("issue_113.json")
