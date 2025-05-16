import pytest

from tests.test_compliance.helper import (
    JSON_SCHEMA,
    OWL,
    PANDERA_POLARS_CLASS,
    PYDANTIC,
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
    SLOT_KEY,
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
    if framework == PANDERA_POLARS_CLASS:
        pytest.skip("PanderaGen does not implement class ranged slots.")
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
    if framework == PANDERA_POLARS_CLASS:
        pytest.skip("PanderaGen does not implement class ranged slots.")
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
    if framework == PANDERA_POLARS_CLASS:
        pytest.skip("PanderaGen does not implement class ranged slots.")
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
        if framework == PANDERA_POLARS_CLASS:
            expected_behavior = ValidationBehavior.INCOMPLETE
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


@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
@pytest.mark.parametrize(
    "is_local,data_name,objs,is_valid",
    [
        (
            True,
            "t1",
            [
                {
                    SLOT_ID: "ex:1",
                    SLOT_S2: [
                        {SLOT_KEY: "ex:1v1", SLOT_S3: "..."},
                        {SLOT_KEY: "ex:1v2", SLOT_S3: "..."},
                    ],
                },
                {
                    SLOT_ID: "ex:2",
                    SLOT_S2: [
                        {SLOT_KEY: "ex:2v1", SLOT_S3: "..."},
                        {SLOT_KEY: "ex:2v2", SLOT_S3: "..."},
                    ],
                },
            ],
            True,
        ),
        (
            True,
            "t2",
            [
                {
                    SLOT_ID: "ex:1",
                    SLOT_S2: [
                        {SLOT_KEY: "ex:1v1", SLOT_S3: "..."},
                        {SLOT_KEY: "ex:1v2", SLOT_S3: "..."},
                    ],
                },
                {
                    SLOT_ID: "ex:2",
                    SLOT_S2: [
                        {SLOT_KEY: "ex:2v1", SLOT_S3: "COPY_1"},
                        {SLOT_KEY: "ex:2v1", SLOT_S3: "COPY_2"},
                    ],
                },
            ],
            False,
        ),
        (
            True,
            "t3_unique_per_container",
            [
                {
                    SLOT_ID: "ex:1",
                    SLOT_S2: [
                        {SLOT_KEY: "ex:v1", SLOT_S3: "..."},
                        {SLOT_KEY: "ex:v2", SLOT_S3: "..."},
                    ],
                },
                {
                    SLOT_ID: "ex:2",
                    SLOT_S2: [
                        {SLOT_KEY: "ex:v1", SLOT_S3: "COPY_1"},
                        {SLOT_KEY: "ex:v2", SLOT_S3: "COPY_2"},
                    ],
                },
            ],
            True,
        ),
        (
            False,
            "t3_unique_per_container",
            [
                {
                    SLOT_ID: "ex:1",
                    SLOT_S2: [
                        {SLOT_KEY: "ex:v1", SLOT_S3: "..."},
                        {SLOT_KEY: "ex:v2", SLOT_S3: "..."},
                    ],
                },
                {
                    SLOT_ID: "ex:2",
                    SLOT_S2: [
                        {SLOT_KEY: "ex:v1", SLOT_S3: "COPY_1"},
                        {SLOT_KEY: "ex:v2", SLOT_S3: "COPY_2"},
                    ],
                },
            ],
            False,
        ),
        (False, "t10", [{SLOT_ID: "ex:1", SLOT_S1: "..."}], True),
    ],
)
def test_nested_key(framework, is_local, data_name, objs, is_valid):
    """
        Tests behavior of keys where the key is nested within another object.

        Identifiers should be globally unique, but keys are only required to be unique within the object
        that holds them.

        For example, given a list of students where each student has a list of exam results; the following structure
        is valid if `name` in the `Exam` class is a key:

        ```yaml
        students:
          - id: S1
            exam_results:
              - name: MATH
                score: 100
              - name: ENG
                score: 90
          - id: S2
            exam_results:
              - name: MATH
                score: 81
              - name: ENG
                score: 76
        ```

        This should NOT be valid if `name` is an identifier (because it is not globally unique; there is more
        than one student with an exam named "MATH").

        The intent is more obvious if the exam results are not inlined_as_list:

        ```yaml
        students:
          - id: S1
            exam_results:
              MATH:
                score: 100
              ENG:
                score: 90
          - id: S2
            exam_results:
              MATH:
                score: 81
              ENG:
                score: 76
        ```

        A schema for this might be something like:

        ```yaml
        classes:
          Student:
            attributes:
              id:
                identifier: true
              full_name:
              # other atts here
              exam_results:
                range: ExamResult
                  inlined: true
                  inlined_as_list: true
          ExamResult:
            attributes:
              name:
                key: true
              score:
                range: integer
              additional_notes:
        ```

        Note that when a relational model is created it SHOULD create a unique key from the combination of the
        key and the parent object's identifier:

        ```yaml
        CREATE TABLE "student" (
            id TEXT NOT NULL,
            full_name TEXT,
            PRIMARY KEY (id)
        );
        CREATE TABLE "exam_result" (
            "student_id" TEXT,
            FOREIGN KEY("student_id") REFERENCES "student" (id),
            name TEXT NOT NULL,
            additional_notes TEXT,
            PRIMARY KEY (student_id, name),
        );
        ```
    ➜

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
                    "range": "uriorcurie",
                    "identifier": True,
                },
                SLOT_S1: {},
                SLOT_S2: {
                    "range": CLASS_D,
                    "inlined": True,
                    "inlined_as_list": True,
                    "multivalued": True,
                },
            },
        },
        CLASS_D: {
            "attributes": {
                SLOT_KEY: {
                    "range": "uriorcurie",
                    "key": is_local,
                    "identifier": not is_local,
                },
                SLOT_S3: {},
            },
        },
    }
    if framework == PANDERA_POLARS_CLASS:
        pytest.skip("PanderaGen does not implement class slots.")
    schema = validated_schema(
        test_nested_key,
        f"is_local{is_local}",
        framework,
        classes=classes,
        core_elements=["key"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if not is_valid:
        if framework in [PYDANTIC, JSON_SCHEMA]:
            expected_behavior = ValidationBehavior.INCOMPLETE
        if data_name == "t3_unique_per_container" and framework == PYTHON_DATACLASSES:
            expected_behavior = ValidationBehavior.INCOMPLETE
    if framework == PANDERA_POLARS_CLASS:
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        data_name,
        framework,
        {"entities": objs},
        is_valid,
        target_class=CLASS_CONTAINER,
        expected_behavior=expected_behavior,
        description=f"Expected validity={is_valid}",
    )
