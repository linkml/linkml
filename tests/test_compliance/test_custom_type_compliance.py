import sys

import pytest
from linkml_runtime.utils.formatutils import camelcase

from tests.test_compliance.helper import (
    JSON_SCHEMA,
    OWL,
    PYDANTIC,
    PYTHON_DATACLASSES,
    SHACL,
    SQL_DDL_SQLITE,
    ValidationBehavior,
    check_data,
    metamodel_schemaview,
    validated_schema,
)
from tests.test_compliance.test_compliance import CLASS_C, CORE_FRAMEWORKS, SLOT_S1


# TODO: consider merging into normal type test
@pytest.mark.parametrize("example_value", ["", None, 1, 1.1, "1", True, False])
@pytest.mark.parametrize("linkml_type", ["string", "integer", "float", "double", "boolean"])
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_typeof(framework, linkml_type, example_value):
    """
    Tests behavior of extended types.

    An extended type is a user defined type that inherits
    from a base type using type_of

    :param framework: all should support built-in types
    :param linkml_type: from the linkml metamodel
    :param example_value: value to check
    :return:
    """
    if framework == SHACL:
        pytest.skip("TODO: shaclgen does not support typeof")
    metamodel = metamodel_schemaview()
    ext_type = camelcase(f"my_{linkml_type}")
    type_elt = metamodel.get_type(linkml_type)
    type_py_cls = eval(type_elt.repr if type_elt.repr else type_elt.base)
    typ_py_name = type_py_cls.__name__
    # if linkml_type == "boolean" and framework == PYTHON_DATACLASSES:
    #    typ_py_name = "Union[bool, Bool]"
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "range": ext_type,
                    "_mappings": {
                        PYDANTIC: f"{SLOT_S1}: Optional[{typ_py_name}]",
                        PYTHON_DATACLASSES: f"{SLOT_S1}: Optional[Union[{typ_py_name}, {ext_type}]]",
                    },
                },
            }
        },
    }
    types = {
        ext_type: {
            "typeof": linkml_type,
        }
    }
    schema = validated_schema(
        test_typeof,
        linkml_type,
        framework,
        classes=classes,
        types=types,
        core_elements=["typeof"],
    )
    expected_behavior = None
    v = example_value
    is_valid = isinstance(v, (type_py_cls, type(None)))
    bool2int = isinstance(v, bool) and linkml_type == "integer"
    if bool2int:
        is_valid = False
    coerced = None
    if not is_valid:
        try:
            coerced = {SLOT_S1: type_py_cls(v)}
        except (ValueError, TypeError):
            pass
    # Pydantic coerces by default; see https://docs.pydantic.dev/latest/usage/types/strict_types/
    if coerced:
        if sys.version_info < (3, 10) and framework == PYDANTIC and linkml_type == "boolean" and isinstance(v, float):
            # On Python 3.9 and earlier, Pydantic will coerce floats to bools. This goes against
            # what their docs say should happen or why it only affects older Python version.
            expected_behavior = ValidationBehavior.COERCES
        elif linkml_type == "boolean" and not isinstance(v, int) and v != "1":
            pass
        else:
            if framework in [PYDANTIC, PYTHON_DATACLASSES]:
                expected_behavior = ValidationBehavior.COERCES
                if framework == PYTHON_DATACLASSES and bool2int:
                    expected_behavior = ValidationBehavior.INCOMPLETE
            elif framework == JSON_SCHEMA:
                if linkml_type in ["float", "double"] and isinstance(v, int):
                    expected_behavior = ValidationBehavior.ACCEPTS
    if framework == SQL_DDL_SQLITE:
        if not is_valid:
            # SQLite effectively coerces everything and has no type checking
            expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == OWL:
        # OWL validation currently depends on python dataclasses to make instances;
        # this coerces
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        f"{type(example_value).__name__}-{example_value}",
        framework,
        {SLOT_S1: example_value},
        is_valid,
        expected_behavior=expected_behavior,
        target_class=CLASS_C,
        coerced=coerced,
        description="pattern",
    )
