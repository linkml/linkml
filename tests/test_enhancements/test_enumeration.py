import logging
from pathlib import Path

import pytest
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator
from linkml.generators.yamlgen import YAMLGenerator


@pytest.mark.no_asserts
def test_evidence(input_path, snapshot):
    """Test evidence enumeration"""
    generated = PythonGenerator(
        Path(input_path("enumeration")) / "evidence.yaml",
        mergeimports=False,
    ).serialize()
    assert generated == snapshot(Path("enumeration") / "evidence.py")


@pytest.mark.parametrize(
    "file,error",
    [
        ("enum_name_error", '":" not allowed in identifier'),
        ("enum_class_name_error", "Overlapping enum and class names: test1, test2"),
        ("enum_type_name_error", "Overlapping type and enum names: test2"),
        ("enum_error_1", 'Enum: "error1" needs a code set to have a version'),
        ("enum_error_2", 'Enum: "error2" cannot have both version and tag'),
        ("enum_error_3", 'Enum: "error3" needs a code set to have a tag'),
        ("enum_error_4", 'Enum: "error4" needs a code set to have a formula'),
        ("enum_error_5", 'Enum: "error5" can have a formula or permissible values but not both'),
        ("enum_error_6a", 'Slot: "classError1__slot_1" enumerations cannot be inlined'),
        ("enum_error_6b", 'Slot: "classError1__slot_1" enumerations cannot be inlined'),
        ("enum_error_7", "Unknown PvFormulaOptions enumeration code: FOO"),
    ],
)
def test_enum_errors(file, error, input_path):
    with pytest.raises(ValueError, match=error):
        YAMLGenerator(
            (Path(input_path("enumeration")) / file).with_suffix(".yaml"),
            mergeimports=False,
            log_level=logging.INFO,
        ).serialize(validateonly=True)


@pytest.mark.parametrize(
    "file,warnings",
    [
        (
            "enum_name_overlaps",
            [
                "Overlapping subset and slot names: a random name",
                "Overlapping enum and slot names: a random name, a slot",
                "Overlapping subset and enum names: a random name, a subset",
            ],
        ),
    ],
)
def test_enum_warns(file, warnings, input_path, caplog):

    generator = YAMLGenerator(
        (Path(input_path("enumeration")) / file).with_suffix(".yaml"),
        mergeimports=False,
        log_level=logging.INFO,
    )
    generator.serialize(validateonly=True)
    for msg in warnings if isinstance(warnings, list) else [warnings]:
        assert any([msg in logmsg.message for logmsg in caplog.records])


@pytest.mark.xfail
def test_enum_valueerror(input_path):
    """Make sure that the link to the error is included in the output"""
    with pytest.raises(ValueError, 'alternatives.yaml", line '):
        YAMLGenerator(
            (Path(input_path("enumeration")) / "enum_error_7").with_suffix(".yaml"),
            mergeimports=False,
            log_level=logging.INFO,
        ).serialize(validateonly=True)


@pytest.mark.no_asserts
def test_enum_alternatives(input_path, snapshot):
    """test various variants on enum constraints"""
    schema_file = Path(input_path("enumeration")) / "alternatives.yaml"

    generated_yaml = YAMLGenerator(schema_file).serialize()
    generated_python = (PythonGenerator(schema_file, mergeimports=False).serialize(),)

    assert generated_yaml == snapshot(Path("enumeration") / "alternatives.yaml")
    assert generated_python[0] == snapshot(Path("enumeration") / "alternatives.py")


def test_notebook_model_1(input_path, snapshot):
    schema_path = Path(input_path("enumeration")) / "notebook_model_1.yaml"
    python_path = Path("enumeration") / "notebook_model_1.py"

    generated = PythonGenerator(schema_path, mergeimports=False, gen_classvars=False, gen_slots=False).serialize()

    assert generated == snapshot(python_path)

    module = compile_python(generated)
    c1 = module.PositionalRecord("my location", "a")
    assert c1.id == "my location"
    assert c1.position.code.text == "a"
    assert c1.position.code.description == "top"

    with pytest.raises(ValueError, match="Unknown OpenEnum enumeration code: z"):
        module.PositionalRecord("your location", "z")

    x = module.PositionalRecord("117493", "c")
    assert x.id == "117493"
    assert x.position.code.text == "c"
    assert x.position.code.description == "bottom"


@pytest.mark.no_asserts
def test_notebook_model_2(input_path, snapshot):
    schema_path = Path(input_path("enumeration")) / "notebook_model_2.yaml"
    python_path = Path("enumeration") / "notebook_model_2.py"

    generated = PythonGenerator(schema_path, mergeimports=False, gen_classvars=False, gen_slots=False).serialize()

    assert generated == snapshot(python_path)

    module = compile_python(generated)
    module.Sample(
        "Something",
        [module.UnusualEnumPatterns.M, module.UnusualEnumPatterns["% ! -- whoo"]],
    )


@pytest.mark.no_asserts
def test_notebook_model_3(input_path, snapshot):
    schema_path = Path(input_path("enumeration")) / "notebook_model_3.yaml"
    python_path = Path("enumeration") / "notebook_model_3.py"

    generated = PythonGenerator(schema_path, mergeimports=False, gen_classvars=False, gen_slots=False).serialize()

    assert generated == snapshot(python_path)

    module = compile_python(generated)
    module.FavoriteColor("Harold", module.Colors["2"])
    module.FavoriteColor("Donald", module.Colors["4"])


@pytest.mark.no_asserts
def test_notebook_model_4(input_path, snapshot):
    schema_path = Path(input_path("enumeration")) / "notebook_model_4.yaml"
    python_path = Path("enumeration") / "notebook_model_4.py"

    generated = PythonGenerator(schema_path, mergeimports=False, gen_classvars=False, gen_slots=False).serialize()

    assert generated == snapshot(python_path)

    module = compile_python(generated)
    module.FavoriteColor("Harold", module.Colors["2"])
    module.FavoriteColor("Donald", module.Colors["4"])
