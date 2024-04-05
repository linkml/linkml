from pathlib import Path

import pytest
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator
from tests import LOCAL_MODEL_YAML_NO_META


@pytest.mark.parametrize("model", LOCAL_MODEL_YAML_NO_META)
def test_models_python(model, snapshot):
    generated = PythonGenerator(model).serialize()
    # ensure valid python
    compile_python(generated, "test")
    output_file = Path(model).with_suffix(".py").name
    assert generated == snapshot(output_file)
