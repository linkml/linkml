from io import StringIO
from pathlib import Path

import pytest
import yaml
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator


def test_pattern_1(input_path, snapshot):
    """Test the pattern enhancement"""
    device = "/dev/tty.Bluetooth-Incoming-Port"
    label = "AbCd0123-1111-FF10-AAF1-A1B2C3D4A1B2C3D4A1B2C3D4"
    generated = PythonGenerator(
        Path(input_path("issue_pattern")) / "pattern_1.yaml",
        mergeimports=False,
    ).serialize()

    assert generated == snapshot(Path("issue_pattern") / "pattern_1.py")

    d1_test = f"""
    device: {device}
    label: {label}
    """

    module = compile_python(generated)
    d1 = yaml.load(StringIO(d1_test), yaml.loader.SafeLoader)
    dev1 = module.DiskDevice(**d1)
    assert dev1.label == label
    assert dev1.device == device


@pytest.mark.xfail
def test_pattern_exception(input_path):
    """
    Python models should validate patterns, but currently they don't
    """
    generated = PythonGenerator(
        Path(input_path("issue_pattern")) / "pattern_1.yaml",
        mergeimports=False,
    ).serialize()
    module = compile_python(generated)

    with pytest.raises(Exception):
        module.DiskDevice(device="hey", label="invalid")
