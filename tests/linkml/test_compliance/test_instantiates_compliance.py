"""
Tests for annotation compliance.

 - TODO: dynamic annotations
"""

import pytest

from tests.test_compliance.helper import (
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import CLASS_C, CORE_FRAMEWORKS, SLOT_S1


@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_instantiates(framework):
    """
    Tests behavior of instantiation.

    :param framework: some frameworks like sqlite do not support annotations
    :param annotation_name: name of the annotation
    :param annotation_desc: description of the annotation
    :param pvs: permissible values
    :param value: value to check
    :param include_meaning: whether to include the meaning in the annotation
    :return:
    """
    classes = {
        CLASS_C: {
            "attributes": {
                SLOT_S1: {},
            },
            "annotations": {
                "annotation_A": "foo",
                # "annotation_B": {"subslot": "bar"},
            },
        },
    }

    schema = validated_schema(
        test_instantiates,
        "default",
        framework,
        classes=classes,
        core_elements=["instantiates", "annotations"],
    )
    check_data(
        schema,
        "default",
        framework,
        {},
        True,
        target_class=CLASS_C,
        description="annotation",
    )
