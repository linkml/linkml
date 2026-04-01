import json

import pytest
from jsonasobj2 import as_json

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.utils.compile_python import compile_python

pytestmark = pytest.mark.pythongen


def test_imported_type_is_emitted_once(input_path):
    """Imported LinkML types should remain available in generated Python."""
    python = PythonGenerator(input_path("issue_121.yaml")).serialize()

    type_import_lines = [
        line for line in python.splitlines() if line.startswith("from linkml_runtime.linkml_model.types ")
    ]
    assert type_import_lines == ["from linkml_runtime.linkml_model.types import String"]

    module = compile_python(python)

    biosample = module.Biosample(depth="test")
    assert biosample.depth == "test"
    assert json.loads(as_json(biosample)) == {"depth": "test"}

    imported = module.ImportedClass()
    assert json.loads(as_json(imported)) == {}
