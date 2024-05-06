from pathlib import Path

import pytest
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.yamlutils import from_yaml

from linkml.generators.pythongen import PythonGenerator


@pytest.mark.xfail
def test_template_basics(input_path, snapshot):
    """Test the basics of a string template"""
    generated = PythonGenerator(
        Path(input_path("string_template")) / "templated_classes.yaml", mergeimports=False
    ).serialize()
    assert generated == snapshot(Path("string_template") / "templated_classes.py")

    module = compile_python(generated)
    inst = module.FirstClass("Sam Sneed", 42, "Male")
    assert "Sam Sneed - a 42 year old Male" == str(inst)
    inst2 = module.FirstClass.parse("Jillian Johnson - a 93 year old female")
    assert "FirstClass(name='Jillian Johnson', age=93, gender='female')" == repr(inst2)
    assert "Jillian Johnson - a 93 year old female" == str(inst2)
    with open(Path(input_path("string_template")) / "jones.yaml") as yf:
        inst3 = from_yaml(yf, module.FirstClass)
    assert "Freddy Buster Jones - a 11 year old Undetermined" == str(inst3)
