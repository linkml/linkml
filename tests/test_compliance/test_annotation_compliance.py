"""Tests for annotation compliance.

Note these tests differ from other compliance tests in that
there is no instance data to test.
"""

from copy import copy
from typing import Any, Dict, Optional, Union

import pytest
import rdflib

from tests.test_compliance.helper import (
    OWL,
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import CLASS_C, CORE_FRAMEWORKS, SLOT_S1

# use rdflib to create a namespace
EX = rdflib.Namespace("http://example.org/")


@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
@pytest.mark.parametrize(
    "name,slot_annotations,class_annotations",
    [
        ("empty", {}, {}),
        ("slot_num", {"foo": 1}, {}),
        ("slot_str", {"foo": "v1"}, {}),
        ("slot_nested_obj", {"foo": {"bar": "v1"}}, {}),
        ("class_num", {}, {"foo": 1}),
        ("class_str", {}, {"foo": "v1"}),
        ("class_nested_obj", {}, {"foo": {"bar": "v1"}}),
        ("class_list_nested_obj", {}, {"foo": [1, {"bar": "v1"}]}),
        ("slot_incomplete", {"foo": None}, None),
        ("class_incomplete", None, {"foo": None}),
    ],
)
@pytest.mark.parametrize("is_valid", [True, False])
@pytest.mark.parametrize("expand", [True, False])
def test_annotation(
    framework: str,
    name: str,
    slot_annotations: Optional[Dict[str, Any]],
    class_annotations: Optional[Dict[str, Any]],
    expand: Optional[Union[bool, str]],
    is_valid: bool,
):
    """
    Tests behavior of annotations.

    See: https://w3id.org/linkml/annotations

    Note annotations do not affect data, so
    there is no instance data accompanying this test suite.

    LinkML 1.6 introduced the "instantiates" metaslot which
    can be used to impose structure on annotations. However, this
    is not yet implemented.

    :param framework: some frameworks like sqlite do not support annotations
    :param name: name of the test
    :param slot_annotations: slot annotations
    :param class_annotations: class annotations
    :param is_valid: whether the schema is valid
    :return:
    """

    def anns(tvs: Optional[dict]) -> Optional[dict]:
        if tvs is None:
            return None
        if expand:
            if expand == "partial":
                return {k: {"value": v if v else {}} for k, v in tvs.items()}
            else:
                return {k: {"tag": k, **{"value": v if v else {}}} for k, v in tvs.items()}
        else:
            return tvs

    is_nested = "nested" in name

    # expected triples in OWL serialization
    triples = []

    def onode(v: Any):
        if isinstance(v, dict):
            return rdflib.BNode()
        else:
            return rdflib.Literal(v)

    if class_annotations:
        for k, v in class_annotations.items():
            if v:
                triples.append((EX[CLASS_C], EX[k], onode(v)))
    if slot_annotations:
        for k, v in slot_annotations.items():
            if v:
                triples.append((EX[SLOT_S1], EX[k], onode(v)))

    if is_valid:
        class_annotations = copy(class_annotations) or {}
        class_annotations["class_metaslot"] = "..."
    if not is_valid:
        pytest.skip("TODO: test invalid annotations")
    print(triples if "nested" not in name else None)
    classes = {
        "MetaclassM": {
            "attributes": {
                "class_metaslot": {
                    "required": True,
                },
            }
        },
        CLASS_C: {
            "attributes": {
                SLOT_S1: {
                    "annotations": anns(slot_annotations),
                }
            },
            "annotations": anns(class_annotations),
            "instantiates": ["MetaclassM"],
            "_mappings": {
                OWL: triples if "nested" not in name else None,
            },
        },
    }

    if is_nested and not expand:
        pytest.skip("TODO: https://github.com/linkml/linkml/issues/2191")

    schema = validated_schema(
        test_annotation,
        name,
        framework,
        classes=classes,
        core_elements=["annotations"],
    )
    check_data(
        schema,
        "null_data",
        framework,
        {SLOT_S1: "foo"},
        True,
        target_class=CLASS_C,
        expected_behavior=ValidationBehavior.IMPLEMENTS,
        description="trivial data test, mainly serves to check there is no edge case issues",
    )
