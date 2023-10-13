"""Tests for annotation compliance.

Note these tests differ from other compliance tests in that
there is no instance data to test.
"""

import pytest

from tests.test_compliance.helper import (
    validated_schema,
)
from tests.test_compliance.test_compliance import CLASS_C, CORE_FRAMEWORKS, SLOT_S1


@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_annotation(framework):
    """
    Tests behavior of annotations.

    See: `<https://w3id.org/linkml/annotations>_`

    Note annotations do not affect data, so
    there is no instance data accompanying this test

    :param framework: some frameworks like sqlite do not support annotations
    :param annotation_name: name of the annotation
    :param annotation_desc: description of the annotation
    :param pvs: permissible values
    :param value: value to check
    :param include_meaning: whether to include the meaning in the annotation
    :return:
    """
    classes = {
        "MetaclassM": {
            "attributes": {
                "metaslot": {},
            }
        },
        CLASS_C: {
            "attributes": {
                SLOT_S1: {},
                "annotations": {},
            },
            "annotations": {},
            "instantiates": ["MetaclassM"],
        },
    }

    _schema = validated_schema(
        test_annotation,
        "annotation",
        framework,
        classes=classes,
        core_elements=["annotations"],
    )
    # TODO: test compliance with metaclasses
