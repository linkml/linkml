import pytest
from pathlib import Path

from linkml import LOCAL_MODEL_YAML_FILES
from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.utils.compile_python import compile_python


@pytest.mark.parametrize("model", LOCAL_MODEL_YAML_FILES)
def test_models_python(model, snapshot):
    generated = PythonGenerator(model).serialize()
    # ensure valid python
    compile_python(generated, "test")
    output_file = Path(model).with_suffix(".py").name
    assert generated == snapshot(output_file)
