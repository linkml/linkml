"""Tests for pattern slots and use of regular expressions as constraints."""

# TODO: structured patterns

import re

import pytest

from tests.test_compliance.helper import (
    JSON_SCHEMA,
    OWL,
    PANDERA_POLARS_CLASS,
    PYDANTIC,
    PYTHON_DATACLASSES,
    SHACL,
    SQL_DDL_SQLITE,
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import CLASS_C, CLASS_D, CORE_FRAMEWORKS, SLOT_ID, SLOT_S1


@pytest.mark.parametrize(
    "schema_name,range,pattern,data_name,value",
    [
        ("complete_match", "string", r"^\S+$", "no_ws", "ab"),
        ("complete_match", "string", r"^\S+$", "ws", "a b"),
        ("partial_match", "string", r"ab", "partial_ab", "abcd"),
        ("partial_match", "string", r"ab", "complete_ab", "ab"),
        ("partial_match", "string", r"ab", "ws", "a b"),
        ("partial_match_curie", "uriorcurie", r".*ab.*", "partial_ab_curie", "X:ab"),
        ("full_match_int", "integer", r"^12$", "full_match_int", 12),
        ("full_match_int", "integer", r"^12$", "non_full_match_int", 123),
        ("full_match_D", CLASS_D, r"^X:1$", "full_match_ref", "X:1"),
        ("full_match_D", CLASS_D, r"^X:1$", "non_full_match_ref", "X:12"),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_pattern(framework, range, schema_name, pattern, data_name, value):
    """
    Tests behavior of pattern slots.

    Pattern slots allow for regular expression constraints.

    Note: Currently not supported for validation by python frameworks.

    :param framework: not supported by python dataclasses
    :param schema_name: the name reflects which constraints are implemented
    :param pattern: regular expression
    :param value: value to check
    :return:
    """
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "pattern": pattern,
                    "range": range,
                },
            }
        }
    }
    if range == CLASS_D:
        classes[CLASS_D] = {
            "attributes": {
                SLOT_ID: {
                    "identifier": True,
                    "range": "uriorcurie",
                },
            }
        }
    prefixes = {
        "X": "http://example.org/",
    }
    if framework == PANDERA_POLARS_CLASS and range == CLASS_D:
        pytest.skip("PanderaGen does not implement class ranged slots.")
    schema = validated_schema(
        test_pattern, schema_name, framework, classes=classes, prefixes=prefixes, core_elements=["pattern"]
    )
    implementation_status = ValidationBehavior.IMPLEMENTS
    is_valid = bool(re.match(pattern, str(value)))
    if framework in [PYTHON_DATACLASSES, SQL_DDL_SQLITE]:
        if not is_valid:
            implementation_status = ValidationBehavior.INCOMPLETE
    if range == "integer" and not is_valid and framework in [PYDANTIC, JSON_SCHEMA]:
        implementation_status = ValidationBehavior.INCOMPLETE
    if range == "integer" and framework == PANDERA_POLARS_CLASS:
        implementation_status = ValidationBehavior.INCOMPLETE
    if framework == OWL:
        pytest.skip("Hermit reasoning over xsd regular expressions is broken")
    if framework == SHACL and range == CLASS_D:
        pytest.skip("SHACL correctly notices integrity violations, but that's not the subject of this test")
    check_data(
        schema,
        data_name,
        framework,
        {SLOT_S1: value},
        is_valid,
        expected_behavior=implementation_status,
        target_class=CLASS_C,
        description=f"matching {value} to {pattern} expected={is_valid}",
    )


# pattern is {word}{ws}{word} and defined in settings above
@pytest.mark.parametrize(
    "interpolated,partial_match,value,is_valid",
    [
        (True, False, "abc def", True),
        (True, False, "abc", False),
        (True, False, "abc def ghi", False),
        (True, True, "abc def ghi", True),
        (False, False, "abc def", False),
        (False, True, "abc def", False),
        (False, False, "{word}{ws}{word}", True),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
@pytest.mark.skip(reason="https://github.com/linkml/linkml/issues/1557")
def test_structured_pattern(framework, interpolated, partial_match, value: str, is_valid):
    """
    Tests behavior of structured pattern slots.

    Pattern slots allow for regular expression constraints.
    Currently not supported for validation by python frameworks.

    :param framework: one of CORE_FRAMEWORKS collection above, not supported by python dataclasses
    :param interpolated: whether the pattern is interpolated
    :param partial_match: whether the pattern is a partial match
    :param value: value to check
    :param is_valid: whether the value is valid
    :return:

    Examples:
    (True, False, "abc def", True)
    Interpolation is enabled, and partial matching is disabled.
    The string "abc def" should exactly match the interpolated pattern {word}{ws}{word} - 'word' and 'ws' defined below
    (which translates to something like [a-zA-Z]+\s+[a-zA-Z]+), and this is expected to be valid.

    (True, False, "abc", False)
    Similar settings as the first, but "abc" does not meet the {word}{ws}{word} pattern since
    there's no whitespace or second word. Expected to be invalid.

    (True, False, "abc def ghi", False)
    Again, partial matching is not allowed, and "abc def ghi" exceeds the {word}{ws}{word} pattern
    because it has an extra word. Expected to be invalid.

    """
    settings = {
        "word": r"[a-zA-Z]+",
        "ws": r"\s+",
    }
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "structured_pattern": {
                        "syntax": "{word}{ws}{word}",
                        "interpolated": interpolated,
                        "partial_match": partial_match,
                    },
                },
            }
        }
    }
    schema = validated_schema(
        test_structured_pattern,
        f"INT{interpolated}_PM{partial_match}",
        framework,
        classes=classes,
        settings=settings,
        core_elements=["structured_pattern"],
    )
    implementation_status = ValidationBehavior.IMPLEMENTS
    if framework in [PYDANTIC, PYTHON_DATACLASSES, SQL_DDL_SQLITE]:
        if not is_valid:
            implementation_status = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        value.replace(" ", "_"),
        framework,
        {SLOT_S1: value},
        is_valid,
        expected_behavior=implementation_status,
        target_class=CLASS_C,
        description=f"matching {value}",
    )


@pytest.mark.parametrize(
    "value,is_valid",
    [
        ("FOO:1", True),
        ("schema:Person", True),
        ("BAR:1", False),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_id_prefix(framework, value, is_valid):
    """
    Tests behavior of id_prefix slots.

    Note: currently id_prefix is only a recommendation, see:
    https://github.com/linkml/linkml/issues/194

    :param framework:
    :param value:
    :param is_valid:
    :return:
    """
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_ID: {
                    "identifier": True,
                    "range": "uriorcurie",
                },
                SLOT_S1: {},
            },
            "id_prefixes": [
                "schema",
                "FOO",
            ],
        }
    }
    schema = validated_schema(
        test_id_prefix,
        "default",
        framework,
        classes=classes,
        prefixes={
            "FOO": "http://example.org/foo/",
            "schema": "http://schema.org/",
        },
        core_elements=["id_prefix"],
    )
    # https://github.com/linkml/linkml/issues/194
    implementation_status = (
        ValidationBehavior.INCOMPLETE,
        "See https://github.com/linkml/linkml/issues/194",
    )
    check_data(
        schema,
        value,
        framework,
        {SLOT_ID: value, SLOT_S1: "..."},
        is_valid,
        expected_behavior=implementation_status,
        target_class=CLASS_C,
        description=f"matching {value} to id_prefixes expected={is_valid}",
    )
