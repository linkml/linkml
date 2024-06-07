"""Compliance tests for core constructs."""

import sys
import unicodedata
from _decimal import Decimal

import pytest
from linkml_runtime.utils.formatutils import underscore
from pydantic.version import VERSION as PYDANTIC_VERSION

from tests.test_compliance.helper import (
    JSON_SCHEMA,
    OWL,
    PYDANTIC,
    PYDANTIC_ROOT_CLASS,
    PYTHON_DATACLASSES,
    PYTHON_DATACLASSES_ROOT_CLASS,
    SHACL,
    SHEX,
    SQL_DDL_POSTGRES,
    SQL_DDL_SQLITE,
    ValidationBehavior,
    check_data,
    metamodel_schemaview,
    validated_schema,
)
from tests.test_compliance.test_compliance import (
    CLASS_ANY,
    CLASS_C,
    CORE_FRAMEWORKS,
    EXAMPLE_STRING_VALUE_1,
    EXAMPLE_STRING_VALUE_2,
    EXAMPLE_STRING_VALUE_3,
    SLOT_ID,
    SLOT_S1,
    SLOT_S2,
    SLOT_S3,
)

IS_PYDANTIC_V1 = PYDANTIC_VERSION[0] == "1"


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

    Known issues:

    - None. This is core behavior all frameworks MUST support.

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
                        PYDANTIC: "s1: Optional[str] = Field(None",
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
    schema = validated_schema(test_attributes, "attributes", framework, classes=classes, core_elements=["attributes"])
    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        object,
        is_valid,
        target_class=CLASS_C,
        description="pattern",
    )


@pytest.mark.parametrize("example_value", ["", None, 1, 1.1, "1", True, False, Decimal("5.4")])
@pytest.mark.parametrize("linkml_type", ["string", "integer", "float", "double", "boolean"])
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_type_range(framework, linkml_type, example_value):
    """
    Tests behavior of built-in types.

    This test will check the cross-product of a set of example values again schemas where the
    expected type for these values varies.

    Known issues:

    - Many frameworks **coerce** values to the correct type.

    TODO: additional types

    - decimal
    - date types
    - curies and uris

    :param framework: all should support built-in types
    :param linkml_type: from the linkml metamodel
    :param example_value: value to check
    :return:
    """
    if isinstance(example_value, Decimal):
        pytest.skip("Decimal not supported by YAML - https://github.com/yaml/pyyaml/issues/255")
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
    schema = validated_schema(test_type_range, linkml_type, framework, classes=classes, core_elements=["range"])
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
            elif framework in [OWL, SHACL, SHEX]:
                # OWL validation currently depends on python dataclasses to make instances;
                # this coerces
                expected_behavior = ValidationBehavior.INCOMPLETE
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
    "name,range,minimum,maximum,value,valid",
    [
        ("integer", "integer", 1, 10, 5, True),
        ("integer", "integer", 1, 10, 15, False),
        ("float", "float", 1.5, 10.5, 1.6, True),
        ("float", "float", 1.5, 10.5, 1.4, False),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_min_max_values(framework, name, range, minimum, maximum, value, valid):
    """
    Tests behavior of min/max values.

    :param framework:
    :param name:
    :param range:
    :param minimum:
    :param maximum:
    :param value:
    :param valid:
    :return:
    """
    if isinstance(value, Decimal):
        pytest.skip("Decimal not supported by YAML - https://github.com/yaml/pyyaml/issues/255")
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "range": range,
                    "minimum_value": minimum,
                    "maximum_value": maximum,
                },
            }
        },
    }
    schema = validated_schema(
        test_min_max_values, name, framework, classes=classes, core_elements=["minimum_value", "maximum_value"]
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework in [SQL_DDL_SQLITE, PYTHON_DATACLASSES] or (framework == PYDANTIC and IS_PYDANTIC_V1):
        if not valid:
            expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        f"{type(value).__name__}-{value}",
        framework,
        {SLOT_S1: value},
        valid,
        expected_behavior=expected_behavior,
        target_class=CLASS_C,
        coerced=False,
        description="min-max values",
    )


@pytest.mark.parametrize("example_value", ["", None, 1, 1.1, "1", True, False, Decimal("5.4"), {}, {"foo": 1}])
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_any_type(framework, example_value):
    """
    Tests linkml:Any.

    :param framework: all should support built-in types
    :param example_value: value to check
    :return:
    """
    if isinstance(example_value, Decimal):
        pytest.skip("Decimal not supported by YAML - https://github.com/yaml/pyyaml/issues/255")
    if framework in [SQL_DDL_SQLITE, SQL_DDL_POSTGRES]:
        pytest.skip("TODO: add support in sqlgen")
    classes = {
        CLASS_ANY: {
            "class_uri": "linkml:Any",
        },
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "range": "Any",
                    "_mappings": {
                        # PYDANTIC: f"{SLOT_S1}: Optional[Any]",
                        # PYTHON_DATACLASSES: f"{SLOT_S1}: Optional[Any]",
                    },
                },
            }
        },
    }
    schema = validated_schema(test_any_type, "linkml_any", framework, classes=classes, core_elements=["Any"])
    expected_behavior = ValidationBehavior.IMPLEMENTS
    check_data(
        schema,
        f"{type(example_value).__name__}-{example_value}",
        framework,
        {SLOT_S1: example_value},
        True,
        expected_behavior=expected_behavior,
        target_class=CLASS_C,
        exclude_rdf=True,
        description=f"linkml:Any with {example_value}",
    )


@pytest.mark.parametrize(
    "linkml_type,example_value,is_valid",
    [
        ("uri", "http://example.org/x/1", True),
        ("uri", "X 1", False),
        ("uriorcurie", "X:1", True),
        ("uriorcurie", "X.Y:1", True),
        ("uriorcurie", "X 1", False),
        ("uriorcurie", "X 1:1", False),
        # ("uriorcurie", "X:1 2", False),
        ("curie", "X:1", True),
        ("curie", "X.Y:A1", True),
        ("curie", "X 1", False),
        ("curie", "X 1:A1", False),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_uri_types(framework, linkml_type, example_value, is_valid):
    """
    Tests behavior of uri and uriorcurie.

    :param framework: all should support built-in types
    :param linkml_type: from the linkml metamodel
    :param example_value: value to check
    :param is_valid: whether the value is valid
    :return:
    """
    if example_value == "X:1":
        if framework in [PYTHON_DATACLASSES, SHACL, SHEX, OWL, SQL_DDL_SQLITE]:
            pytest.skip("Incorrectly flagged as invalid")
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "range": linkml_type,
                },
            }
        },
    }
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if not is_valid and framework in [PYDANTIC, JSON_SCHEMA]:
        expected_behavior = ValidationBehavior.INCOMPLETE
    schema = validated_schema(
        test_uri_types,
        linkml_type,
        framework,
        classes=classes,
        core_elements=["uri", "uriorcurie"],
    )
    check_data(
        schema,
        ensafeify(f"{example_value}-{example_value}"),
        framework,
        {SLOT_S1: example_value},
        is_valid,
        expected_behavior=expected_behavior,
        target_class=CLASS_C,
        description="uris and curies",
    )


@pytest.mark.parametrize(
    "linkml_type,example_value,is_valid",
    [
        ("date", "Friday", False),
        ("date", "2021", False),
        ("date", "20210101", False),
        ("datetime", "Friday", False),
        ("time", "Friday", False),
        ("date", "2021-01-01", True),
        ("date", "2021-01-01+06:00", True),
        ("datetime", "2021-01-01", False),
        ("datetime", "2002-05-30T09:00:00", True),
        ("datetime", "2002-05-30T09:00:00Z", True),
        ("datetime", "2002-05-30T09:00:00+06:00", True),
        ("time", "09:00:00", True),
        ("time", "09:00:00.5", True),
        ("time", "09:00:00Z", True),
        ("duration", "P5Y2M10DT15H", True),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_date_types(framework, linkml_type, example_value, is_valid):
    """
    Tests behavior of date types.

    Known issues:

    - xsd:dates allow for time zone offsets, but this isn't supported in all frameworks

    See also:

    - `<https://stackoverflow.com/questions/20264146/json-schema-date-time-does-not-check-correctly>`_

    :param framework: all should support built-in types
    :param linkml_type: from the linkml metamodel
    :param example_value: value to check
    :param is_valid: whether the value is valid
    :return:
    """
    if linkml_type == "duration":
        pytest.skip("duration not yet supported")
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "range": linkml_type,
                },
            }
        },
    }
    coerced = False
    expected_behavior = ValidationBehavior.IMPLEMENTS
    schema = validated_schema(
        test_date_types,
        linkml_type,
        framework,
        classes=classes,
        core_elements=["range", "TypeDefinition"],
    )
    if framework == SQL_DDL_SQLITE:
        # SQLite Date type only accepts Python date objects as input
        expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == PYTHON_DATACLASSES:
        if linkml_type == "datetime" and example_value == "2021-01-01":
            expected_behavior = ValidationBehavior.COERCES
        if linkml_type == "time" and "." in example_value and is_valid:
            expected_behavior = ValidationBehavior.FALSE_POSITIVE
    if framework == PYDANTIC:
        if not IS_PYDANTIC_V1 and linkml_type == "datetime" and example_value == "2021-01-01":
            expected_behavior = ValidationBehavior.COERCES
        if linkml_type == "time" and is_valid is False:
            expected_behavior = ValidationBehavior.INCOMPLETE
        if linkml_type == "date" and is_valid is False and example_value.startswith("2021"):
            expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == JSON_SCHEMA:
        # RFC3339 requires either Z or time zone offset
        if (
            linkml_type in ["time", "datetime"]
            and is_valid
            and "Z" not in example_value
            and "+06:00" not in example_value
        ):
            expected_behavior = ValidationBehavior.FALSE_POSITIVE
        if linkml_type == "date" and "+" in example_value and is_valid:
            expected_behavior = ValidationBehavior.FALSE_POSITIVE
    if ("+" in example_value or "Z" in example_value) and is_valid:
        if framework in [PYDANTIC, PYTHON_DATACLASSES]:
            expected_behavior = ValidationBehavior.FALSE_POSITIVE
    if framework in [OWL, SHACL, SHEX]:
        # OWL validation currently depends on python dataclasses to make instances;
        # this coerces;
        if not is_valid:
            expected_behavior = ValidationBehavior.INCOMPLETE
        else:
            # TODO: investigate this, hermit issue?
            expected_behavior = ValidationBehavior.FALSE_POSITIVE
    check_data(
        schema,
        ensafeify(f"times-{example_value}-{example_value}"),
        framework,
        {SLOT_S1: example_value},
        is_valid,
        expected_behavior=expected_behavior,
        target_class=CLASS_C,
        coerced=coerced,
        description="uris and curies",
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
        (PYDANTIC, False, False): "Optional[str] = Field(None",
        (PYDANTIC, False, True): "str = Field(...",
        (PYDANTIC, True, False): "Optional[List[str]] = Field(default_factory=list",
        (PYDANTIC, True, True): "List[str] = Field(default_factory=list",
        # TODO: values
        (PYTHON_DATACLASSES, False, False): "",
        (PYTHON_DATACLASSES, False, True): "",
        (PYTHON_DATACLASSES, True, False): "",
        (PYTHON_DATACLASSES, True, True): "",
        (SHEX, False, False): " ?",
        (SHEX, False, True): "",
        (SHEX, True, False): "*",
        (SHEX, True, True): " +",
    }
    shacl = (
        "@prefix ex: <http://example.org/> ."
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."
        "@prefix sh: <http://www.w3.org/ns/shacl#> ."
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> ."
        "ex:C a sh:NodeShape ;"
        "sh:closed true ;"
        "sh:ignoredProperties ( rdf:type ) ;"
        "sh:property [ sh:datatype xsd:string ;"
        f"    {'sh:maxCount 1 ;' if not multivalued else ''}"
        f"    {'sh:minCount 1 ;' if required else ''}"
        "    sh:nodeKind sh:Literal ;"
        "    sh:order 0 ;"
        "    sh:path ex:s1 ] ;"
        "sh:targetClass ex:C ."
    )
    shex = (
        "< C > CLOSED {"
        f"  (  $ < C_tes > < s1 > @ < String >{choices[(SHEX, multivalued, required)]} ;"
        "    rdf:type[< C >] ?"
        "  )"
        "}"
    )
    owl_mv = "" if multivalued else "[ a owl:Restriction ; owl:maxCardinality 1 ; owl:onProperty ex:s1 ],"
    owl = (
        "@prefix ex: <http://example.org/> ."
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."
        "@prefix sh: <http://www.w3.org/ns/shacl#> ."
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> ."
        "@prefix owl: <http://www.w3.org/2002/07/owl#> ."
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> ."
        "ex:C a owl:Class ;"
        'rdfs:label "C" ;'
        "rdfs:subClassOf [ a owl:Restriction ;"
        f"    owl:minCardinality {1 if required else 0} ;"
        "    owl:onProperty ex:s1 ],"
        f"{owl_mv}"
        "    [ a owl:Restriction ;"
        "    owl:allValuesFrom xsd:string ;"
        "   owl:onProperty ex:s1 ] ."
    )
    sql_nullable = "NOT NULL" if required else ""
    if not multivalued:
        sqlite = 'CREATE TABLE "C" (' f"  id INTEGER NOT NULL," f"  s1 TEXT {sql_nullable}," "  PRIMARY KEY (id)" ");"
    else:
        sqlite = (
            'CREATE TABLE "C_s1" ('
            '   "C_id" INTEGER,'
            f"   s1 TEXT {sql_nullable},"
            '   PRIMARY KEY ("C_id", s1),'
            '   FOREIGN KEY("C_id") REFERENCES "C" (id)'
            ");"
        )

    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "required": required,
                    "multivalued": multivalued,
                    "_mappings": {
                        PYDANTIC: choices[(PYDANTIC, multivalued, required)],
                        PYTHON_DATACLASSES: choices[(PYTHON_DATACLASSES, multivalued, required)],
                        SHACL: shacl,
                        SHEX: shex,
                        OWL: owl,
                        SQL_DDL_SQLITE: sqlite,
                        SQL_DDL_POSTGRES: sqlite.replace("id INTEGER", "id SERIAL"),
                    },
                },
            }
        }
    }
    schema = validated_schema(
        test_cardinality,
        f"MV{multivalued}_REQ{required}",
        framework,
        classes=classes,
        core_elements=["required", "multivalued"],
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
    if framework == OWL:
        if not is_valid:
            # OWL is open world
            expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == SHACL:
        if not is_valid:
            if multivalued and not isinstance(value, list):
                # RDF does not distinguish between singletons and single values
                expected_behavior = ValidationBehavior.INCOMPLETE
        if not multivalued and isinstance(value, list):
            # RDF does not distinguish between singletons and single values
            expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        data_name,
        framework,
        {SLOT_S1: value},
        is_valid,
        expected_behavior=expected_behavior,
        target_class=CLASS_C,
        coerced=coerced,
        description="cardinality",
    )


@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
@pytest.mark.parametrize("required_asserted", [None, True])
@pytest.mark.parametrize(
    "data_name,instance,is_valid",
    [
        ("empty", {}, False),
        ("present", {SLOT_ID: "x"}, True),
    ],
)
def test_identifier_is_required(framework, required_asserted, data_name, instance, is_valid):
    """
    Tests that when identifiers are specified they are treated as required.

    :param framework:
    :param required_asserted:
    :param data_name:
    :param instance:
    :param is_valid:
    :return:
    """
    if framework == SHACL:
        pytest.skip("TODO: @base CURIEs")
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_ID: {
                    "identifier": True,
                    "required": required_asserted,
                },
                SLOT_S1: {},
            }
        }
    }
    schema = validated_schema(
        test_identifier_is_required,
        f"requiredEQ_{required_asserted}",
        framework,
        classes=classes,
        core_elements=["identifier", "required"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    check_data(
        schema,
        data_name,
        framework,
        instance,
        is_valid,
        expected_behavior=expected_behavior,
        target_class=CLASS_C,
        # coerced=coerced,
        description="identifier implies required",
    )


def ensafeify(name: str):
    """
    Converts a string to a safe label for use in file names and NCNames.

    :param name:
    :return:
    """
    safe_label = ""
    for char in name:
        if char.isalpha() or char.isnumeric() or char == "_":
            safe_label += char
        else:
            safe_label += underscore(unicodedata.name(char))
    return safe_label


@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
@pytest.mark.parametrize(
    "class_name,safe_class_name,slot_name,safe_slot_name,type_name",
    [
        ("C", "C", "s1", "s1", "T1"),
        ("C", "C", "S1", "S1", "t1"),
        ("c", "C", "S1", "S1", "t1"),
        ("C", "C", "s 1", "s_1", "t 1"),
        ("C", "C", "1s", "1s", "T1"),
    ],
)
def test_non_standard_names(framework, class_name, safe_class_name, slot_name, safe_slot_name, type_name):
    """
    Tests that non-standard class and slot names are handled gracefully.

    :param framework:
    :param class_name:
    :param safe_class_name:
    :param slot_name:
    :param safe_slot_name:
    :param type_name:
    :return:
    """
    classes = {
        class_name: {
            "attributes": {
                slot_name: {
                    "range": type_name,
                },
                # SLOT_S1: {
                #    "range": class_name,
                # }
            }
        }
    }
    types = {
        type_name: {
            "typeof": "string",
        },
    }
    name = ensafeify(f"ClassNameEQ_{class_name}__SlotNameEQ_{slot_name}__TypeNameEQ_{type_name}")
    schema = validated_schema(test_cardinality, name, framework, classes=classes, types=types, core_elements=["name"])
    expected_behavior = ValidationBehavior.IMPLEMENTS
    instance = {
        safe_slot_name: "x",
    }
    exclude_rdf = False
    if slot_name.startswith("1"):
        if framework in [PYTHON_DATACLASSES, PYDANTIC, SQL_DDL_SQLITE]:
            expected_behavior = ValidationBehavior.INCOMPLETE
        exclude_rdf = True
    if class_name == "c" and framework in [JSON_SCHEMA, SHACL]:
        pytest.skip("TODO: causes schemaview error")
    check_data(
        schema,
        "test",
        framework,
        instance,
        True,
        expected_behavior=expected_behavior,
        target_class=safe_class_name,
        # coerced=coerced,
        description="nom-standard names are allowed",
        exclude_rdf=exclude_rdf,
    )


@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
@pytest.mark.parametrize(
    "enum_name,pv_name",
    [
        ("E", "s1"),
        ("E", "S1"),
        ("e", "S1"),
        ("e 1", "S1"),
        ("E", "s 1"),
        ("E", "1s"),
        ("E", " "),
        ("E", "'"),
        ("E[x]", "[x]"),
        ("E", "[x]"),
    ],
)
def test_non_standard_num_names(framework, enum_name, pv_name):
    """
    Tests that non-standard enum and permissible value names are handled gracefully.

    :param framework:
    :param enum_name:
    :param pv_name:
    :return:
    """
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "range": enum_name,
                },
            }
        }
    }
    enums = {
        enum_name: {
            "permissible_values": {
                pv_name: {},
            },
        },
    }
    name = ensafeify(f"EN{enum_name}_PV{pv_name}")
    schema = validated_schema(
        test_non_standard_num_names,
        name,
        framework,
        classes=classes,
        enums=enums,
        core_elements=["name"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    instance = {
        SLOT_S1: pv_name,
    }
    exclude_rdf = False
    if "[" in enum_name and framework in [PYDANTIC, SQL_DDL_SQLITE, PYTHON_DATACLASSES, OWL, SHACL]:
        # TODO: need to escape []s
        expected_behavior = ValidationBehavior.INCOMPLETE
        exclude_rdf = True
    if pv_name == " " and framework == PYDANTIC:
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        "test",
        framework,
        instance,
        True,
        expected_behavior=expected_behavior,
        target_class=CLASS_C,
        # coerced=coerced,
        description="nom-standard enum/pv names are allowed",
        exclude_rdf=exclude_rdf,
    )
