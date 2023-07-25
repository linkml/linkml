import re

import pytest

from tests.test_compliance.helper import (
    metamodel_schemaview,
    validated_schema,
    _check_data,
    ValidationBehavior,
    PYDANTIC_ROOT_CLASS,
    PYTHON_DATACLASSES_ROOT_CLASS,
    PYDANTIC,
    PYTHON_DATACLASSES,
    JSON_SCHEMA,
)

CLASS_CONTAINER = "Container"
CLASS_C = "C"
CLASS_D = "D"
SLOT_S1 = "s1"
SLOT_S2 = "s2"
SLOT_S3 = "s3"
SLOT_S4 = "s4"
SLOT_ID = "id"
EXAMPLE_STRING_VALUE_1 = "foo"
EXAMPLE_STRING_VALUE_2 = "bar"
EXAMPLE_STRING_VALUE_3 = "fuz"

CORE_FRAMEWORKS = [PYTHON_DATACLASSES, PYDANTIC, JSON_SCHEMA]


@pytest.mark.parametrize("data", ["flat", "nested"])
@pytest.mark.parametrize("foreign_key", [0, "FK"])
@pytest.mark.parametrize("multivalued", [0, "MV"])
@pytest.mark.parametrize("inlined_as_list", [0, "IAL"])
@pytest.mark.parametrize("inlined", [0, "INL"])
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_inlined(framework, inlined, inlined_as_list, multivalued, foreign_key, data):
    """
    Tests behavior of inlined slots.

    :param framework:
    :param inlined:
    :param inlined_as_list:
    :param multivalued:
    :param foreign_key:
    :return:
    """
    inlined = bool(inlined)
    inlined_as_list = bool(inlined_as_list)
    multivalued = bool(multivalued)
    foreign_key = bool(foreign_key)
    schema_name = f"INL{inlined}_IAL{inlined_as_list}_MV{multivalued}_FK{foreign_key}"
    entailed_inlined = inlined or inlined_as_list or not foreign_key
    inconsistent_combo = inlined_as_list and not multivalued
    py_def_map = {
        (PYDANTIC, False, False, False, False): "D",
        (PYDANTIC, False, False, False, True): "str",
        (PYDANTIC, False, False, True, False): "List[D]",
        (PYDANTIC, False, False, True, True): "List[str]",
        (PYDANTIC, False, True, False, False): "D",  # odd but valid combo
        (PYDANTIC, False, True, False, True): "D",  # odd but valid combo
        (PYDANTIC, False, True, True, False): "List[D]",
        # (PYDANTIC, False, True, True, True): "List[str]", ## TODO check this one
        (PYDANTIC, True, False, False, False): "D",
        (PYDANTIC, True, False, False, True): "D",
        (PYDANTIC, True, False, True, False): "List[D]",
        (PYDANTIC, True, False, True, True): "Dict[str, D]",
        (PYDANTIC, True, True, False, False): "D",  # odd but valid combo
        # (PYDANTIC, True, True, False, True): "str",  ## TODO check this one
        (PYDANTIC, True, True, True, False): "List[D]",
        (PYDANTIC, True, True, True, True): "List[D]",
        (PYTHON_DATACLASSES, False, False, False, False): 'Union[dict, "D"]',
        (PYTHON_DATACLASSES, False, False, False, True): "Union[str, DId]",
        (
            PYTHON_DATACLASSES,
            False,
            False,
            True,
            False,
        ): 'Union[Union[dict, "D"], List[Union[dict, "D"]]]',
        (
            PYTHON_DATACLASSES,
            False,
            False,
            True,
            True,
        ): "Union[Union[str, DId], List[Union[str, DId]]]",
        (PYTHON_DATACLASSES, False, True, False, False): 'Union[dict, "D"]',  # odd but valid combo
        (PYTHON_DATACLASSES, False, True, False, True): 'Union[dict, "D"]',  # odd but valid combo
        (
            PYTHON_DATACLASSES,
            False,
            True,
            True,
            False,
        ): 'Union[Union[dict, "D"], List[Union[dict, "D"]]]',
        (
            PYTHON_DATACLASSES,
            False,
            True,
            True,
            True,
        ): 'Union[Dict[Union[str, DId], Union[dict, "D"]], List[Union[dict, "D"]]]',
        (PYTHON_DATACLASSES, True, False, False, False): 'Union[dict, "D"]',
        (PYTHON_DATACLASSES, True, False, False, True): 'Union[dict, "D"]',
        (
            PYTHON_DATACLASSES,
            True,
            False,
            True,
            False,
        ): 'Union[Union[dict, "D"], List[Union[dict, "D"]]]',
        (
            PYTHON_DATACLASSES,
            True,
            False,
            True,
            True,
        ): 'Union[Dict[Union[str, DId], Union[dict, "D"]], List[Union[dict, "D"]]]',
        (PYTHON_DATACLASSES, True, True, False, False): 'Union[dict, "D"]',  # odd but valid combo
        (PYTHON_DATACLASSES, True, True, False, True): 'Union[dict, "D"]',
        (
            PYTHON_DATACLASSES,
            True,
            True,
            True,
            False,
        ): 'Union[Union[dict, "D"], List[Union[dict, "D"]]]',
        (
            PYTHON_DATACLASSES,
            True,
            True,
            True,
            True,
        ): 'Union[Dict[Union[str, DId], Union[dict, "D"]], List[Union[dict, "D"]]]',
    }
    tpl = (framework, inlined, inlined_as_list, multivalued, foreign_key)
    if tpl in py_def_map:
        py_def = py_def_map[tpl]
        py_def = f"Optional[{py_def}]"
    else:
        py_def = "Optional"
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "inlined": inlined,
                    "inlined_as_list": inlined_as_list,
                    "multivalued": multivalued,
                    "range": CLASS_D,
                    "_mappings": {
                        PYDANTIC: f"{SLOT_S1}: {py_def}",
                        PYTHON_DATACLASSES: f"{SLOT_S1}: {py_def}",
                    },
                },
            },
        },
        CLASS_D: {
            "attributes": {
                SLOT_ID: {
                    "identifier": foreign_key,
                },
                SLOT_S2: {},
                SLOT_S3: {},
            },
        },
    }
    schema = validated_schema(test_type_range, schema_name, framework, classes=classes)
    implementation_status = ValidationBehavior.IMPLEMENTS
    coerced = None
    id_val = "X:1"
    if data == "flat":
        inst = {
            SLOT_S1: id_val,
        }
        is_valid = False if entailed_inlined or multivalued else True
        if not is_valid:
            if entailed_inlined:
                if foreign_key and multivalued and not inlined_as_list:
                    coerced = {SLOT_S1: {id_val: {SLOT_ID: id_val}}}
                elif foreign_key and multivalued and inlined_as_list:
                    coerced = {SLOT_S1: [{SLOT_ID: id_val}]}
                elif foreign_key and not multivalued:
                    coerced = {SLOT_S1: {SLOT_ID: id_val}}
            else:
                if not multivalued:
                    raise AssertionError
                if foreign_key:
                    coerced = {SLOT_S1: [id_val]}
                else:
                    raise AssertionError
    elif data == "nested":
        inst = {
            SLOT_S1: {
                SLOT_ID: id_val,
                SLOT_S2: EXAMPLE_STRING_VALUE_2,
                SLOT_S3: EXAMPLE_STRING_VALUE_3,
            }
        }
        is_valid = entailed_inlined and not multivalued
        if framework == JSON_SCHEMA:
            if inlined and not inlined_as_list and multivalued and foreign_key:
                # TODO: json-schema generation appears incorrect here
                implementation_status = ValidationBehavior.INCOMPLETE
    else:
        raise AssertionError(f"Unknown data type {data}")
    if not is_valid and framework == PYTHON_DATACLASSES:
        implementation_status = ValidationBehavior.COERCES
    _check_data(
        schema,
        data,
        framework,
        inst,
        is_valid,
        coerced=coerced,
        expected_behavior=implementation_status,
        target_class=CLASS_C,
        description=f"s1 entailed inlined: {entailed_inlined}",
    )


@pytest.mark.parametrize(
    "schema_name,pattern,data_name,value",
    [
        ("complete_match", r"^\S+$", "no_ws", "ab"),
        ("complete_match", r"^\S+$", "ws", "a b"),
        ("partial_match", r"ab", "partial_ab", "abcd"),
        ("partial_match", r"ab", "complete_ab", "ab"),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_pattern(framework, schema_name, pattern, data_name, value):
    """
    Tests behavior of pattern slots.

    :param framework:
    :param name:
    :param pattern:
    :param value:
    :return:
    """
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "pattern": pattern,
                },
            }
        }
    }
    schema = validated_schema(test_type_range, schema_name, framework, classes=classes)
    implementation_status = ValidationBehavior.IMPLEMENTS
    is_valid = bool(re.match(pattern, value))
    if framework != JSON_SCHEMA:
        if not is_valid:
            implementation_status = ValidationBehavior.INCOMPLETE
    _check_data(
        schema,
        data_name,
        framework,
        {SLOT_S1: value},
        is_valid,
        expected_behavior=implementation_status,
        target_class=CLASS_C,
        description=f"pattern",
    )


@pytest.mark.parametrize("example_value", ["", None, 1, 1.1, "1", True, False])
@pytest.mark.parametrize("linkml_type", ["string", "integer", "float", "boolean"])
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_type_range(framework, linkml_type, example_value):
    """
    Tests behavior of built-in types.

    :param metamodel:
    :param example_atomic_values:
    :param linkml_type:
    :return:
    """
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
    print(f"v={v}, coerced={coerced}")
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
                if linkml_type == "float" and isinstance(v, int):
                    expected_behavior = ValidationBehavior.ACCEPTS

    _check_data(
        schema,
        f"{type(example_value).__name__}-{example_value}",
        framework,
        {SLOT_S1: example_value},
        is_valid,
        expected_behavior=expected_behavior,
        target_class=CLASS_C,
        coerced=coerced,
        description=f"pattern",
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
        # dc will cast a list to a string
        expected_behavior = ValidationBehavior.INCOMPLETE
    _check_data(
        schema,
        # f"{value}",
        data_name,
        framework,
        {SLOT_S1: value},
        is_valid,
        expected_behavior=expected_behavior,
        target_class=CLASS_C,
        coerced=coerced,
        description=f"pattern",
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
    _check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        object,
        is_valid,
        target_class=CLASS_C,
        description=f"pattern",
    )
