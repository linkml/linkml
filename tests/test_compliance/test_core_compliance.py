"""Compliance tests for core constructs."""

import pytest
from _decimal import Decimal

from tests.test_compliance.helper import (
    JSON_SCHEMA,
    PYDANTIC,
    PYDANTIC_ROOT_CLASS,
    PYTHON_DATACLASSES,
    PYTHON_DATACLASSES_ROOT_CLASS,
    SQL_DDL_SQLITE,
    ValidationBehavior,
    check_data,
    metamodel_schemaview,
    validated_schema,
)
from tests.test_compliance.test_compliance import (
    CLASS_ANY,
    CLASS_C,
    CLASS_D,
    CORE_FRAMEWORKS,
    EXAMPLE_STRING_VALUE_1,
    EXAMPLE_STRING_VALUE_2,
    EXAMPLE_STRING_VALUE_3,
    SLOT_S1,
    SLOT_S2,
    SLOT_S3,
)


@pytest.mark.parametrize(
    "description,object,is_valid",
    [
        ("object may be empty", {}, True),
        (
            "not all attributes need to be specified",
            {
                SLOT_S1: EXAMPLE_STRING_VALUE_1,
            },
            True,
        ),
        (
            "all attributes can be specified",
            {
                SLOT_S1: EXAMPLE_STRING_VALUE_1,
                SLOT_S2: EXAMPLE_STRING_VALUE_2,
            },
            True,
        ),
        (
            "attributes not in the class are not allowed",
            {
                SLOT_S1: EXAMPLE_STRING_VALUE_1,
                SLOT_S2: EXAMPLE_STRING_VALUE_2,
                SLOT_S3: EXAMPLE_STRING_VALUE_3,
            },
            False,
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_attributes(framework, description, object, is_valid):
    """
    Tests basic behavior of attributes.

    :param framework: all should support attributes
    :param description: description of the test data
    :param object: object to check
    :param is_valid: whether the object is valid
    :return:
    """
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "_mappings": {
                        PYDANTIC: "s1: Optional[str] = Field(None)",
                        PYTHON_DATACLASSES: "s1: Optional[str] = None",
                    }
                },
                SLOT_S2: {},
            },
            "_mappings": {
                PYDANTIC: f"class C({PYDANTIC_ROOT_CLASS}):",
                PYTHON_DATACLASSES: f"@dataclass\nclass C({PYTHON_DATACLASSES_ROOT_CLASS}):",
                JSON_SCHEMA: {
                    "$defs": {
                        "C": {
                            "additionalProperties": False,
                            "description": "",
                            "properties": {
                                "s1": {"type": "string"},
                                "s2": {"type": "string"},
                            },
                            "title": "C",
                            "type": "object",
                        }
                    }
                },
            },
        },
    }
    schema = validated_schema(test_attributes, "attributes", framework, classes=classes)
    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        object,
        is_valid,
        target_class=CLASS_C,
        description="pattern",
    )


@pytest.mark.parametrize("example_value", ["", None, 1, 1.1, "1", True, False])
@pytest.mark.parametrize("linkml_type", ["string", "integer", "float", "double", "boolean"])
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_type_range(framework, linkml_type, example_value):
    """
    Tests behavior of built-in types.

    TODO: additional types

    - decimal
    - date types
    - curies and uris

    :param framework: all should support built-in types
    :param linkml_type: from the linkml metamodel
    :param example_value: value to check
    :return:
    """
    Decimal("1.2")  ## TODO
    metamodel = metamodel_schemaview()
    type_elt = metamodel.get_type(linkml_type)
    type_py_cls = eval(type_elt.repr if type_elt.repr else type_elt.base)
    typ_py_name = type_py_cls.__name__
    if linkml_type == "boolean" and framework == PYTHON_DATACLASSES:
        typ_py_name = "Union[bool, Bool]"
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "range": linkml_type,
                    "_mappings": {
                        PYDANTIC: f"{SLOT_S1}: Optional[{typ_py_name}]",
                        PYTHON_DATACLASSES: f"{SLOT_S1}: Optional[{typ_py_name}]",
                    },
                },
            }
        },
    }
    schema = validated_schema(test_type_range, linkml_type, framework, classes=classes)
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
        if linkml_type == "boolean" and not isinstance(v, int) and v != "1":
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


@pytest.mark.parametrize(
    "data_name,value",
    [
        ("sv", "x"),
        ("list2", ["x", "y"]),
    ],
)
@pytest.mark.parametrize("required", [False, True])
@pytest.mark.parametrize("multivalued", [False, True])
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_cardinality(framework, multivalued, required, data_name, value):
    """
    Tests cardinality (required, multivalued) behavior.

    :param framework: all should support cardinality
    :param multivalued: corresponds to linkml:multivalued
    :param required: corresponds to linkml:required
    :param data_name: name of the test data
    :param value: value to check
    :return:
    """
    choices = {
        (PYDANTIC, False, False): "Optional[str] = Field(None)",
        (PYDANTIC, False, True): "str = Field(...)",
        (PYDANTIC, True, False): "Optional[List[str]] = Field(default_factory=list)",
        (PYDANTIC, True, True): "List[str] = Field(default_factory=list)",
        # TODO: values
        (PYTHON_DATACLASSES, False, False): "",
        (PYTHON_DATACLASSES, False, True): "",
        (PYTHON_DATACLASSES, True, False): "",
        (PYTHON_DATACLASSES, True, True): "",
    }
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "required": required,
                    "multivalued": multivalued,
                    "_mappings": {
                        PYDANTIC: choices[(PYDANTIC, multivalued, required)],
                        PYTHON_DATACLASSES: choices[(PYTHON_DATACLASSES, multivalued, required)],
                    },
                },
            }
        }
    }
    schema = validated_schema(
        test_cardinality, f"MV{multivalued}_REQ{required}", framework, classes=classes
    )
    coerced = None
    is_valid = True
    list2scalar = False
    if multivalued and not isinstance(value, list):
        coerced = [value]
    if not multivalued and isinstance(value, list):
        is_valid = False
        list2scalar = True
        # coerced = value[0] ## TODO
    if coerced:
        is_valid = False
        coerced = {SLOT_S1: coerced}
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if coerced and framework == PYTHON_DATACLASSES:
        expected_behavior = ValidationBehavior.COERCES
    if list2scalar and framework == PYTHON_DATACLASSES:
        # dc will cast a list to a string serialization.
        # TODO: consider this a valid coercion?
        expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == SQL_DDL_SQLITE:
        if not is_valid:
            # SQLite effectively coerces everything and has no type checking
            expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        # f"{value}",
        data_name,
        framework,
        {SLOT_S1: value},
        is_valid,
        expected_behavior=expected_behavior,
        target_class=CLASS_C,
        coerced=coerced,
        description="pattern",
    )


@pytest.mark.parametrize("use_default_range", [False, True])
@pytest.mark.parametrize(
    "data_name,value,is_valid",
    [("int", 1, True), ("str", "abc", False), ("obj", {SLOT_S2: "abc"}, True)],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_any_of(framework, data_name, value, is_valid, use_default_range):
    """
    Tests behavior of any_of.

    :param framework:
    :param data_name:
    :param value:
    :param is_valid:
    :param use_default_range:
    :return:
    """
    classes = {
        CLASS_D: {
            "attributes": {
                SLOT_S2: {
                    "range": "string",
                },
            },
        },
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "any_of": [
                        {
                            "range": CLASS_D,
                        },
                        {"range": "integer"},
                    ],
                    "_mappings": {
                        PYDANTIC: f"{SLOT_S1}: Optional[Union[D, int]]",
                    },
                },
            },
        },
    }
    if use_default_range:
        default_range = "string"
        classes[CLASS_ANY] = {
            "class_uri": "linkml:Any",
        }
        classes[CLASS_C]["attributes"][SLOT_S1]["range"] = CLASS_ANY
    else:
        default_range = None
    schema = validated_schema(
        test_any_of, f"DR{default_range}", framework, classes=classes, default_range=default_range
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework in [PYTHON_DATACLASSES, SQL_DDL_SQLITE]:
        expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == JSON_SCHEMA and use_default_range:
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        data_name,
        framework,
        {SLOT_S1: value},
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description=f"validity {is_valid} check for value {value}",
    )
