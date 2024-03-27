import pytest

from tests.test_compliance.helper import (
    OWL,
    PYTHON_DATACLASSES,
    SQL_DDL_SQLITE,
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import (
    CLASS_C,
    CLASS_CONTAINER,
    CLASS_D,
    CORE_FRAMEWORKS,
    SLOT_ID,
    SLOT_S1,
    SLOT_S2,
    SLOT_S3,
)


@pytest.mark.parametrize("additional_slot_values", [None, "v1"])
@pytest.mark.parametrize(
    "description,ids,is_valid",
    [
        ("no_duplicates", ["P:1", "P:2"], True),
        ("duplicates", ["P:1", "P:1"], False),
        ("empty", [], True),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_identifier(framework, description, ids, is_valid, additional_slot_values):
    """
    Tests basic behavior of identifiers.

    This test constructs a container class, with a list of objects of class C.
    C has an identifier slot, and a slot with additional values.

    :param framework: all should support attributes
    :param description: description of the test data
    :param ids: list of C ids in collection
    :param is_valid: whether the constructed object is valid
    :param additional_slot_values: additional slot values
    :return:
    """
    classes = {
        CLASS_CONTAINER: {
            "attributes": {
                "entities": {
                    "range": CLASS_C,
                    "multivalued": True,
                    "inlined": True,
                    "inlined_as_list": True,
                },
            },
        },
        CLASS_C: {
            "attributes": {
                SLOT_ID: {
                    "identifier": True,
                },
                SLOT_S1: {},
            },
        },
    }
    prefixes = {
        "P": "http://example.org/P/",
    }
    schema = validated_schema(
        test_identifier, "default", framework, classes=classes, core_elements=["identifier"], prefixes=prefixes
    )
    obj = {"entities": [{"id": id, SLOT_S1: additional_slot_values} for id in ids]}
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if not is_valid and framework != PYTHON_DATACLASSES:
        expected_behavior = ValidationBehavior.INCOMPLETE
    if not additional_slot_values:
        pytest.skip("issues with dataclasses where object is empty except for plain id")
    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        obj,
        is_valid,
        target_class=CLASS_CONTAINER,
        expected_behavior=expected_behavior,
        description=description,
    )


@pytest.mark.parametrize("consider_nulls_inequal", [False, True])
@pytest.mark.parametrize(
    "description,objects,is_valid,is_valid_if_nulls_inequal",
    [
        ("trivial", [], True, True),
        (
            "neq",
            [
                (None, None, None),
                (None, None, None),
            ],
            True,
            False,
        ),
        (
            "neq2",
            [
                ("x1", None, None),
                ("x1", None, None),
            ],
            True,
            False,
        ),
        (
            "no_duplicates",
            [
                ("x1", "y1", "z1"),
                ("x2", "y2", "z2"),
                ("x3", "y3", "z3"),
            ],
            True,
            True,
        ),
        (
            "duplicates_main",
            [
                ("x1", "y1", "z1"),
                ("x1", "y1", "z2"),
                ("x3", "y3", "z3"),
            ],
            False,
            False,
        ),
        (
            "duplicates_secondary",
            [
                ("x1", "y1", "z1"),
                ("x1", "y2", "z1"),
                ("x3", "y3", "z3"),
            ],
            False,
            False,
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_unique_keys(framework, description, objects, is_valid, is_valid_if_nulls_inequal, consider_nulls_inequal):
    """
    Tests unique keys

    """
    classes = {
        CLASS_CONTAINER: {
            "attributes": {
                "entities": {
                    "range": CLASS_C,
                    "multivalued": True,
                    "inlined": True,
                    "inlined_as_list": True,
                },
            },
        },
        CLASS_C: {
            "attributes": {
                SLOT_S1: {},
                SLOT_S2: {},
                SLOT_S3: {},
            },
            "unique_keys": {
                "main": {
                    "unique_key_slots": [SLOT_S1, SLOT_S2],
                    "consider_nulls_inequal": consider_nulls_inequal,
                },
                "secondary": {
                    "unique_key_slots": [SLOT_S1, SLOT_S3],
                    "consider_nulls_inequal": consider_nulls_inequal,
                },
            },
            "_mappings": {
                SQL_DDL_SQLITE: f"UNIQUE ({SLOT_S1}, {SLOT_S2})",
                OWL: (
                    "@prefix ex: <http://example.org/> ."
                    "@prefix owl: <http://www.w3.org/2002/07/owl#> ."
                    "ex:C owl:hasKey (ex:s1 ex:s2) , (ex:s1 ex:s3) ."
                ),
            },
        },
    }
    schema = validated_schema(
        test_unique_keys,
        f"NIE{consider_nulls_inequal}",
        framework,
        classes=classes,
        core_elements=["identifier"],
    )
    obj = {"entities": [{SLOT_S1: s1, SLOT_S2: s2, SLOT_S3: s3} for s1, s2, s3 in objects]}
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if not is_valid:
        if framework == SQL_DDL_SQLITE:
            # SQLite and most RDBMSs treats nulls as inequal
            if not consider_nulls_inequal:
                expected_behavior = ValidationBehavior.IMPLEMENTS
            else:
                expected_behavior = ValidationBehavior.INCOMPLETE
        elif framework == OWL:
            # TODO: by its open world nature, OWL will not consider clashes to be a violation
            # unless Unique Name Assumptions are explicitly asserted. This is currently outside
            # of the scope of the limited OWL support in this test suite.
            expected_behavior = ValidationBehavior.INCOMPLETE
        else:
            # only supported in SQL backends
            expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        obj,
        is_valid,
        target_class=CLASS_CONTAINER,
        expected_behavior=expected_behavior,
        description=description,
    )


D_INST_1 = {SLOT_ID: "ex:d1", SLOT_S3: "t"}
D_INST_2 = {SLOT_ID: "ex:d2", SLOT_S3: "t"}


@pytest.mark.parametrize(
    "schema_name,d_has_id,s1def,s2def,ddl,valid_objs,invalid_objs",
    [
        (
            "s1_ref",
            True,
            {"range": CLASS_D},
            {"range": "integer"},
            "UNIQUE (s1, s2)",
            [
                ("ex:d1", 5),
                ("ex:d1", 4),
            ],
            [
                ("ex:d1", 5),
                ("ex:d1", 5),
            ],
        ),
        (
            "s1_inlined",
            True,
            {"range": CLASS_D, "inlined": True},
            {"range": "integer"},
            "UNIQUE (s1_id, s2)",
            [
                (D_INST_1, 5),
                (D_INST_2, 5),
            ],
            [
                (D_INST_1, 5),
                (D_INST_1, 5),
            ],
        ),
        (
            "s1_multivalued",
            True,
            {"range": "integer", "multivalued": True},
            {"range": "integer"},
            "",
            [
                ([1, 2], 5),
                ([1, 3], 5),
            ],
            [
                ([1, 2], 5),
                ([1, 2], 5),
            ],
        ),
        (
            "s1_multivalued_ref",
            True,
            {"range": CLASS_D, "multivalued": True},
            {"range": "integer"},
            "",
            [
                (["ex:d1", "ex:d2"], 5),
                (["ex:d1"], 5),
            ],
            [
                (["ex:d1"], 5),
                (["ex:d1"], 5),
            ],
        ),
        (
            "s1_multivalued_inlined",
            False,
            {"range": CLASS_D, "multivalued": True, "inlined_as_list": True},
            {"range": "integer"},
            "",
            [
                ([D_INST_1, D_INST_2], 5),
                ([D_INST_1], 5),
            ],
            [
                ([D_INST_1], 5),
                ([D_INST_1], 5),
            ],
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_inlined_unique_keys(framework, schema_name, d_has_id, s1def, s2def, ddl, valid_objs, invalid_objs):
    """
    Tests unique keys where some slots may be inlined

    """
    consider_nulls_inequal = True
    is_inlined = s1def.get("inlined_as_list", False) or s1def.get("inlined", False)
    d_is_top_level = s1def["range"] == CLASS_D and not is_inlined
    classes = {
        CLASS_CONTAINER: {
            "attributes": {
                "entities": {
                    "range": CLASS_C,
                    "multivalued": True,
                    "inlined": True,
                    "inlined_as_list": True,
                },
            },
        },
        CLASS_C: {
            "attributes": {
                SLOT_S1: s1def,
                SLOT_S2: s2def,
            },
            "unique_keys": {
                "main": {
                    "unique_key_slots": [SLOT_S1, SLOT_S2],
                    "consider_nulls_inequal": consider_nulls_inequal,
                },
            },
            "_mappings": {
                SQL_DDL_SQLITE: ddl,
                # OWL: (
                #    "@prefix ex: <http://example.org/> ."
                #    "@prefix owl: <http://www.w3.org/2002/07/owl#> ."
                #    "ex:C owl:hasKey (ex:s1 ex:s2) , (ex:s1 ex:s3) ."
                # ),
            },
        },
        CLASS_D: {
            "attributes": {
                SLOT_ID: {
                    "identifier": d_has_id,
                },
                SLOT_S3: {},
            },
        },
    }
    if d_is_top_level:
        classes[CLASS_CONTAINER]["attributes"]["d_entities"] = {
            "range": CLASS_D,
            "multivalued": True,
            "inlined": True,
            "inlined_as_list": True,
        }
    schema = validated_schema(
        test_inlined_unique_keys,
        schema_name,
        framework,
        classes=classes,
        core_elements=["unique_keys", "inlined"],
    )
    for is_valid, objects in [(True, valid_objs), (False, invalid_objs)]:
        if objects is None:
            continue
        obj = {"entities": [{SLOT_S1: s1, SLOT_S2: s2} for s1, s2 in objects]}
        if d_is_top_level:
            obj["d_entities"] = [D_INST_1, D_INST_2]
        expected_behavior = ValidationBehavior.IMPLEMENTS
        if not is_valid:
            if framework == SQL_DDL_SQLITE:
                # SQLite and most RDBMSs treats nulls as inequal
                if not consider_nulls_inequal:
                    expected_behavior = ValidationBehavior.IMPLEMENTS
                else:
                    expected_behavior = ValidationBehavior.INCOMPLETE
            elif framework == OWL:
                # TODO: by its open world nature, OWL will not consider clashes to be a violation
                # unless Unique Name Assumptions are explicitly asserted. This is currently outside
                # of the scope of the limited OWL support in this test suite.
                expected_behavior = ValidationBehavior.INCOMPLETE
            else:
                # only supported in SQL backends
                expected_behavior = ValidationBehavior.INCOMPLETE
        if framework == SQL_DDL_SQLITE and schema_name == "s1_multivalued_ref":
            # TODO: bug in SQLA for this case
            # AttributeError: 'DId' object has no attribute '_sa_instance_state'
            # https://github.com/linkml/linkml/issues/1160
            expected_behavior = ValidationBehavior.INCOMPLETE
        check_data(
            schema,
            f"V{is_valid}",
            framework,
            obj,
            is_valid,
            target_class=CLASS_CONTAINER,
            expected_behavior=expected_behavior,
            description=f"Expected validity={is_valid}",
        )
