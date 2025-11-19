import pytest
from jsonasobj2 import as_json
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator


@pytest.mark.pythongen
def test_issue_python_ordering(input_path, snapshot):
    """Make sure that types are generated as part of the output"""
    output = PythonGenerator(input_path("issue_134.yaml")).serialize()
    assert output == snapshot("issue_134.py")

    module = compile_python(output)
    e = module.E("id:1")
    b = module.B("id:2")
    e.has_b = b

    json_output = as_json(e)
    assert json_output == snapshot("issue_134.json")
