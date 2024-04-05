from pathlib import Path

import pytest

from linkml.generators.pythongen import PythonGenerator


@pytest.mark.no_asserts
def test_simple_example(input_path, snapshot):
    generated = PythonGenerator(
        Path(input_path("string_serialization")) / "simple_example.yaml", mergeimports=False
    ).serialize()
    assert generated == snapshot(Path("string_serialization") / "simple_example.py")
