"""
Tests for annotation compliance.

 - TODO: dynamic annotations
"""

import pytest

from tests.test_compliance.helper import (
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import CLASS_C, CORE_FRAMEWORKS, SLOT_S1


@pytest.mark.parametrize("include_meaning", [True, False])
@pytest.mark.parametrize("value", ["A", "C", "schema:A"])
@pytest.mark.parametrize(
    "annotation_name,annotation_desc,pvs",
    [
        ("annotation_A", "basic_annotation", [("A", "schema:A", "An A"), ("B", "schema:B", "A B")]),
        (
            "annotation_B",
            "curies_annotation",
            [("schema:A", "schema:A", "An A"), ("schema:B", "schema:B", "A B")],
        ),
        (
            "annotation_C",
            "ws_annotation",
            [("A B", "schema:AB", "An A B"), ("B-%", "schema:Bpct", "A B%")],
        ),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
@pytest.mark.skip(reason="TODO:  annotations")
def test_annotation(framework, annotation_name, annotation_desc, pvs, value, include_meaning):
    """
    Tests behavior of annotations.

    :param framework: some frameworks like sqlite do not support annotations
    :param annotation_name: name of the annotation
    :param annotation_desc: description of the annotation
    :param pvs: permissible values
    :param value: value to check
    :param include_meaning: whether to include the meaning in the annotation
    :return:
    """
    classes = {
        CLASS_C: {"attributes": {SLOT_S1: {}, "annotations": {}}},
    }

    schema = validated_schema(
        test_annotation,
        f"{annotation_name}_M{include_meaning}",
        framework,
        classes=classes,
        core_elements=["annotations"],
    )
    is_valid = value in [pv[0] for pv in pvs]
    expected_behavior = ValidationBehavior.IMPLEMENTS
    check_data(
        schema,
        value.replace(":", "_").replace(" ", "_"),
        framework,
        {SLOT_S1: value},
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description="annotation",
    )
