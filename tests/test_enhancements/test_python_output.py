import re
from pathlib import Path
from types import ModuleType

import pytest
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator


class NonStr:
    def __init__(self, v) -> None:
        self.v = v

    def __str__(self) -> str:
        return self.v


@pytest.fixture(scope="module")
def python_types(input_path) -> ModuleType:
    generated = PythonGenerator(
        Path(input_path("python_generation")) / "python_types.yaml", mergeimports=False
    ).serialize()
    mod = compile_python(generated)
    return mod


def test_python_types_snapshot(input_path, snapshot):
    generated = PythonGenerator(
        Path(input_path("python_generation")) / "python_types.yaml", mergeimports=False
    ).serialize()
    assert generated == snapshot(Path("python_generation") / "python_types.py")


@pytest.mark.strcmp
@pytest.mark.parametrize(
    "cls_name,args,argv,expected,err",
    [
        [
            "Strings",
            ("s1", "s2", "s3", "s4"),
            {},
            "Strings(mand_string='s1', mand_multi_string=['s2'], opt_string='s3', opt_multi_string=['s4'])",
            None,
        ],
        [
            "Strings",
            ("s1", ["s21", "s22"], "s3", ["s41", "s42"]),
            {},
            (
                "Strings(mand_string='s1', mand_multi_string=['s21', 's22'], "
                "opt_string='s3', opt_multi_string=['s41', 's42'])"
            ),
            None,
        ],
        [
            "Strings",
            ("s1", ["s21", "s22"], None, None),
            {},
            "Strings(mand_string='s1', mand_multi_string=['s21', 's22'], opt_string=None, opt_multi_string=[])",
            None,
        ],
        [
            "Strings",
            (NonStr("s1"), NonStr("s2"), NonStr("s3"), NonStr("s4")),
            {},
            "Strings(mand_string='s1', mand_multi_string=['s2'], opt_string='s3', opt_multi_string=['s4'])",
            None,
        ],
        [
            "Strings",
            (
                NonStr("s1"),
                [NonStr("s21"), NonStr("s22")],
                NonStr("s3"),
                [NonStr("s41"), "s42"],
            ),
            {},
            (
                "Strings(mand_string='s1', mand_multi_string=['s21', 's22'], "
                "opt_string='s3', opt_multi_string=['s41', 's42'])"
            ),
            None,
        ],
        ["Strings", (), {}, "mand_string must be supplied", ValueError],
        ["Strings", ("s1",), {}, "mand_multi_string must be supplied", ValueError],
        ["Strings", ("s1", []), {}, "mand_multi_string must be supplied", ValueError],
        [
            "Booleans",
            ("True", "false", 1, [1, 0, True, False]),
            {},
            (
                "Booleans(mand_boolean=True, mand_multi_boolean=[False], opt_boolean=True, "
                "opt_multi_boolean=[True, False, True, False])"
            ),
            None,
        ],
        [
            "Integers",
            ("17", -2, 12 + 3, [42, "17"]),
            {},
            "Integers(mand_integer=17, mand_multi_integer=[-2], opt_integer=15, opt_multi_integer=[42, 17])",
            None,
        ],
        [
            "Integers",
            ("17e", 1, 2, 3),
            {},
            "invalid literal for int() with base 10: '17e'",
            ValueError,
        ],
    ],
)
def test_python_types(cls_name, args, argv, expected, err, python_types):
    cls = getattr(python_types, cls_name)
    if err:
        with pytest.raises(err, match=re.escape(expected)):
            cls(*args, **argv)
    else:
        inst = cls(*args, **argv)
        assert str(inst) == expected


@pytest.mark.no_asserts
def test_python_complex_ranges(input_path, snapshot):
    """description"""

    generated = PythonGenerator(
        Path(input_path("python_generation")) / "python_complex_ranges.yaml", mergeimports=False
    ).serialize()
    assert generated == snapshot(Path("python_generation") / "python_complex_ranges.py")


@pytest.mark.no_asserts
def test_python_lists_and_keys(input_path, snapshot):
    """description"""

    generated = PythonGenerator(
        Path(input_path("python_generation")) / "python_lists_and_keys.yaml", mergeimports=False
    ).serialize()
    assert generated == snapshot(Path("python_generation") / "python_lists_and_keys.py")
