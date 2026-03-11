"""Compliance tests for subproperty_of slot constraint.

Tests that generators correctly constrain slot values to descendants of the
referenced slot when subproperty_of is set.
"""

import pytest

from tests.linkml.test_compliance.helper import (
    JSON_SCHEMA,
    PYDANTIC,
    SHACL,
    SHEX,
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.linkml.test_compliance.test_compliance import CORE_FRAMEWORKS

# Slot names for the hierarchy
SLOT_RELATED_TO = "related_to"
SLOT_CAUSES = "causes"
SLOT_DIRECTLY_CAUSES = "directly_causes"
SLOT_TREATS = "treats"
SLOT_UNRELATED = "unrelated_slot"
SLOT_PREDICATE = "predicate"

# Class names
CLASS_ASSOCIATION = "Association"


@pytest.mark.parametrize(
    "description,predicate_value,is_valid",
    [
        # Root predicate is valid
        ("root_predicate", "related_to", True),
        # Direct child is valid
        ("child_predicate_causes", "causes", True),
        # Another direct child is valid
        ("child_predicate_treats", "treats", True),
        # Grandchild is valid
        ("grandchild_predicate", "directly_causes", True),
        # Unrelated slot is invalid
        ("unrelated_slot", "unrelated_slot", False),
        # Non-existent value is invalid
        ("nonexistent", "not_a_real_predicate", False),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_subproperty_of_value_constraint(framework, description, predicate_value, is_valid):
    """
    Tests that subproperty_of constrains slot values to descendants.

    Creates a schema with:
    - Slot hierarchy: related_to -> causes -> directly_causes
                                 -> treats
    - A predicate slot with subproperty_of: related_to
    - Association class using the predicate slot

    Valid values should include any slot in the is_a hierarchy.
    Invalid values should be rejected.

    :param framework: generator to test
    :param description: name of test case
    :param predicate_value: value to test
    :param is_valid: whether the value should be accepted
    """
    slots = {
        # Slot hierarchy
        SLOT_RELATED_TO: {"description": "Root predicate slot"},
        SLOT_CAUSES: {"is_a": SLOT_RELATED_TO},
        SLOT_DIRECTLY_CAUSES: {"is_a": SLOT_CAUSES},
        SLOT_TREATS: {"is_a": SLOT_RELATED_TO},
        SLOT_UNRELATED: {"description": "Unrelated slot"},
    }
    classes = {
        CLASS_ASSOCIATION: {
            "tree_root": True,
            "attributes": {
                SLOT_PREDICATE: {
                    "range": "string",
                    "subproperty_of": SLOT_RELATED_TO,
                },
            },
        },
    }
    schema = validated_schema(
        test_subproperty_of_value_constraint,
        f"pred_{description}",
        framework,
        slots=slots,
        classes=classes,
        core_elements=["subproperty_of"],
    )

    # Expected behavior varies by framework
    # Only pydantic, jsonschema, shacl, and shex implement subproperty_of
    if framework in [PYDANTIC, JSON_SCHEMA, SHACL, SHEX]:
        expected_behavior = ValidationBehavior.IMPLEMENTS
    else:
        expected_behavior = ValidationBehavior.INCOMPLETE

    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        {SLOT_PREDICATE: predicate_value},
        is_valid,
        target_class=CLASS_ASSOCIATION,
        expected_behavior=expected_behavior,
        description=description,
    )


@pytest.mark.parametrize(
    "description,range_type,predicate_value,is_valid",
    [
        # String range - slot name
        ("string_range_valid", "string", "causes", True),
        ("string_range_invalid", "string", "not_a_slot", False),
        # uriorcurie range - CURIE format
        ("curie_range_valid", "uriorcurie", "ex:causes", True),
        ("curie_range_root", "uriorcurie", "ex:related_to", True),
        ("curie_range_invalid", "uriorcurie", "ex:not_a_slot", False),
    ],
)
@pytest.mark.parametrize("framework", [PYDANTIC, JSON_SCHEMA])
def test_subproperty_of_range_formatting(framework, description, range_type, predicate_value, is_valid):
    """
    Tests that subproperty_of values are formatted according to range type.

    When range is:
    - string: values should be slot names (e.g., "causes")
    - uriorcurie: values should be CURIEs (e.g., "ex:causes")

    :param framework: generator to test
    :param description: name of test case
    :param range_type: type of the slot range
    :param predicate_value: value to test
    :param is_valid: whether the value should be accepted
    """
    slots = {
        SLOT_RELATED_TO: {"slot_uri": "ex:related_to"},
        SLOT_CAUSES: {"is_a": SLOT_RELATED_TO, "slot_uri": "ex:causes"},
        SLOT_TREATS: {"is_a": SLOT_RELATED_TO, "slot_uri": "ex:treats"},
    }
    classes = {
        CLASS_ASSOCIATION: {
            "tree_root": True,
            "attributes": {
                SLOT_PREDICATE: {
                    "range": range_type,
                    "subproperty_of": SLOT_RELATED_TO,
                },
            },
        },
    }
    schema = validated_schema(
        test_subproperty_of_range_formatting,
        f"range_{description}",
        framework,
        slots=slots,
        classes=classes,
        prefixes={"ex": "https://example.org/"},
        core_elements=["subproperty_of"],
    )

    check_data(
        schema,
        description.replace(" ", "_"),
        framework,
        {SLOT_PREDICATE: predicate_value},
        is_valid,
        target_class=CLASS_ASSOCIATION,
        expected_behavior=ValidationBehavior.IMPLEMENTS,
        description=description,
    )


@pytest.mark.parametrize("framework", [PYDANTIC, JSON_SCHEMA, SHACL, SHEX])
def test_subproperty_of_deep_hierarchy(framework):
    """
    Tests that subproperty_of includes all descendants at any depth.

    Creates a 4-level hierarchy:
    - root -> level1 -> level2 -> level3

    All levels should be valid values.

    :param framework: generator to test
    """
    slots = {
        "root": {},
        "level1": {"is_a": "root"},
        "level2": {"is_a": "level1"},
        "level3": {"is_a": "level2"},
        "other": {},  # Not in hierarchy
    }
    classes = {
        CLASS_ASSOCIATION: {
            "tree_root": True,
            "attributes": {
                SLOT_PREDICATE: {
                    "range": "string",
                    "subproperty_of": "root",
                },
            },
        },
    }
    schema = validated_schema(
        test_subproperty_of_deep_hierarchy,
        "deep_hierarchy",
        framework,
        slots=slots,
        classes=classes,
        core_elements=["subproperty_of"],
    )

    # All hierarchy levels should be valid
    for level in ["root", "level1", "level2", "level3"]:
        check_data(
            schema,
            f"valid_{level}",
            framework,
            {SLOT_PREDICATE: level},
            True,
            target_class=CLASS_ASSOCIATION,
            expected_behavior=ValidationBehavior.IMPLEMENTS,
            description=f"valid_{level}",
        )

    # Slot outside hierarchy should be invalid
    check_data(
        schema,
        "invalid_other",
        framework,
        {SLOT_PREDICATE: "other"},
        False,
        target_class=CLASS_ASSOCIATION,
        expected_behavior=ValidationBehavior.IMPLEMENTS,
        description="invalid_other",
    )


@pytest.mark.parametrize("framework", [PYDANTIC, JSON_SCHEMA])
def test_subproperty_of_slot_usage_narrowing(framework):
    """
    Tests that slot_usage can narrow the subproperty_of constraint.

    Creates:
    - Base Association with predicate subproperty_of: related_to
    - CausalAssociation with slot_usage narrowing to subproperty_of: causes

    CausalAssociation should only accept causes and its descendants,
    not other related_to descendants like treats.

    :param framework: generator to test
    """
    slots = {
        SLOT_RELATED_TO: {},
        SLOT_CAUSES: {"is_a": SLOT_RELATED_TO},
        SLOT_DIRECTLY_CAUSES: {"is_a": SLOT_CAUSES},
        SLOT_TREATS: {"is_a": SLOT_RELATED_TO},
        SLOT_PREDICATE: {
            "range": "string",
            "subproperty_of": SLOT_RELATED_TO,
        },
    }
    classes = {
        CLASS_ASSOCIATION: {
            "slots": [SLOT_PREDICATE],
        },
        "CausalAssociation": {
            "is_a": CLASS_ASSOCIATION,
            "tree_root": True,
            "slot_usage": {
                SLOT_PREDICATE: {
                    "subproperty_of": SLOT_CAUSES,
                },
            },
        },
    }
    schema = validated_schema(
        test_subproperty_of_slot_usage_narrowing,
        "slot_usage_narrowing",
        framework,
        slots=slots,
        classes=classes,
        core_elements=["subproperty_of", "slot_usage"],
    )

    # causes and directly_causes should be valid for CausalAssociation
    for value in [SLOT_CAUSES, SLOT_DIRECTLY_CAUSES]:
        check_data(
            schema,
            f"valid_{value}",
            framework,
            {SLOT_PREDICATE: value},
            True,
            target_class="CausalAssociation",
            expected_behavior=ValidationBehavior.IMPLEMENTS,
            description=f"valid_{value}",
        )

    # treats should be invalid for CausalAssociation (not under causes)
    check_data(
        schema,
        "invalid_treats",
        framework,
        {SLOT_PREDICATE: SLOT_TREATS},
        False,
        target_class="CausalAssociation",
        expected_behavior=ValidationBehavior.IMPLEMENTS,
        description="invalid_treats",
    )


@pytest.mark.parametrize("framework", [PYDANTIC, JSON_SCHEMA])
def test_subproperty_of_multivalued(framework):
    """
    Tests that subproperty_of works correctly with multivalued slots.

    :param framework: generator to test
    """
    slots = {
        SLOT_RELATED_TO: {},
        SLOT_CAUSES: {"is_a": SLOT_RELATED_TO},
        SLOT_TREATS: {"is_a": SLOT_RELATED_TO},
    }
    classes = {
        CLASS_ASSOCIATION: {
            "tree_root": True,
            "attributes": {
                "predicates": {
                    "range": "string",
                    "multivalued": True,
                    "subproperty_of": SLOT_RELATED_TO,
                },
            },
        },
    }
    schema = validated_schema(
        test_subproperty_of_multivalued,
        "multivalued",
        framework,
        slots=slots,
        classes=classes,
        core_elements=["subproperty_of"],
    )

    # All valid values in list
    check_data(
        schema,
        "all_valid",
        framework,
        {"predicates": [SLOT_RELATED_TO, SLOT_CAUSES, SLOT_TREATS]},
        True,
        target_class=CLASS_ASSOCIATION,
        expected_behavior=ValidationBehavior.IMPLEMENTS,
        description="all_valid",
    )

    # One invalid value in list
    check_data(
        schema,
        "one_invalid",
        framework,
        {"predicates": [SLOT_CAUSES, "invalid_slot"]},
        False,
        target_class=CLASS_ASSOCIATION,
        expected_behavior=ValidationBehavior.IMPLEMENTS,
        description="one_invalid",
    )


@pytest.mark.parametrize("framework", [PYDANTIC])
def test_subproperty_of_class_range(framework):
    """
    Tests that subproperty_of does not override class range with Literal type.

    When a slot has subproperty_of AND range pointing to a class,
    the class range should take priority. The subproperty_of Literal
    expansion only applies to string-like ranges (string, uri, uriorcurie).

    Regression test for https://github.com/linkml/linkml/issues/3184
    """
    slots = {
        "mayHaveAbility": {"range": "Ability", "multivalued": True},
        "mayHaveHiddenAbility": {
            "is_a": "mayHaveAbility",
            "range": "Ability",
            "multivalued": True,
            "subproperty_of": "mayHaveAbility",
        },
    }
    classes = {
        "Ability": {
            "attributes": {
                "name": {"range": "string", "identifier": True},
            },
        },
        "Species": {
            "tree_root": True,
            "slots": ["mayHaveAbility", "mayHaveHiddenAbility"],
        },
    }
    schema = validated_schema(
        test_subproperty_of_class_range,
        "class_range",
        framework,
        slots=slots,
        classes=classes,
        core_elements=["subproperty_of"],
    )

    # Ability has an identifier slot, so Pydantic represents references as strings.
    # With the fix, mayHaveHiddenAbility accepts any valid Ability identifier string.
    # Without the fix, it would only accept Literal["mayHaveAbility"].
    check_data(
        schema,
        "valid_ability_ref",
        framework,
        {"mayHaveAbility": ["Overgrow"], "mayHaveHiddenAbility": ["Chlorophyll"]},
        True,
        target_class="Species",
        expected_behavior=ValidationBehavior.IMPLEMENTS,
        description="valid_ability_ref",
    )

    # Verify mayHaveAbility itself also works (parent slot, no subproperty_of issue)
    check_data(
        schema,
        "valid_parent_slot",
        framework,
        {"mayHaveAbility": ["Overgrow", "Blaze"]},
        True,
        target_class="Species",
        expected_behavior=ValidationBehavior.IMPLEMENTS,
        description="valid_parent_slot",
    )
