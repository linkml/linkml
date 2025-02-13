"""
Tests for implements compliance.
"""

import pytest

from tests.test_compliance.helper import (
    validated_schema,
)
from tests.test_compliance.test_compliance import CLASS_C, CLASS_D, CORE_FRAMEWORKS, SLOT_S1, SLOT_S2, SLOT_S3

SLOT_S1_REF = f"ex:{SLOT_S1}"
SLOT_S2_REF = f"ex:{SLOT_S2}"


@pytest.mark.parametrize(
    "parent_atts,child_atts,satisfiable",
    [
        ({}, {}, True),
        ({SLOT_S1: {}}, {SLOT_S3: {"implements": [f"ex:{SLOT_S1}"]}}, True),
        ({SLOT_S1: {"required": True}}, {SLOT_S3: {"implements": [SLOT_S1_REF]}}, False),
        ({SLOT_S1: {"multivalued": True}}, {SLOT_S3: {"implements": [SLOT_S1_REF]}}, False),
        ({SLOT_S1: {"required": True}}, {SLOT_S3: {"required": True, "implements": [SLOT_S1_REF]}}, True),
        ({SLOT_S1: {"multivalued": True}}, {SLOT_S3: {"multivalued": True, "implements": [SLOT_S1_REF]}}, True),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_implements(framework, parent_atts, child_atts, satisfiable):
    """
    Tests behavior of implements.

    :param framework: some frameworks like sqlite do not support annotations
    :param annotation_name: name of the annotation
    :param annotation_desc: description of the annotation
    :param pvs: permissible values
    :param value: value to check
    :param include_meaning: whether to include the meaning in the annotation
    :return:
    """
    if not satisfiable:
        pytest.skip("Satisfiability check not implemented")
    prefix = "ex"
    classes = {
        CLASS_C: {
            "attributes": parent_atts,
        },
        CLASS_D: {
            "implements": [f"{prefix}:{CLASS_C}"],
            "attributes": child_atts,
        },
    }
    _schema = validated_schema(
        test_implements,
        "default",
        framework,
        unsatisfiable=not satisfiable,
        classes=classes,
        core_elements=["implements"],
    )
