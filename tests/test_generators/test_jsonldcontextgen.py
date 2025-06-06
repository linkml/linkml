import json

import pytest

from linkml.generators import ContextGenerator, JSONLDGenerator
from tests.utils.compare_jsonld_context import CompareJsonldContext
from tests.utils.validate_jsonld_context import RdfExpectations


def test_jsonld_context_integration(kitchen_sink_path, snapshot_path):
    jsonld_context = ContextGenerator(kitchen_sink_path).serialize()

    CompareJsonldContext.compare_with_snapshot(jsonld_context, snapshot_path("kitchen_sink.jsonld"))


def test_no_default_namespace_prefix(input_path, snapshot_path):
    jsonld_context = ContextGenerator(str(input_path("jsonld_context_no_default_namespace_prefix.yaml"))).serialize()

    CompareJsonldContext.compare_with_snapshot(jsonld_context, snapshot_path("no_default_namespace_prefix.jsonld"))


def test_class_uri_prefix(input_path, snapshot_path):
    jsonld_context = ContextGenerator(str(input_path("jsonld_context_class_uri_prefix.yaml"))).serialize()

    CompareJsonldContext.compare_with_snapshot(jsonld_context, snapshot_path("class_uri_prefix.jsonld"))


def test_inlined_external_types(input_path, snapshot_path):
    jsonld_context = ContextGenerator(str(input_path("jsonld_context_inlined_external_types.yaml"))).serialize()

    CompareJsonldContext.compare_with_snapshot(jsonld_context, snapshot_path("context_inlined_external_types.jsonld"))


@pytest.mark.parametrize(
    "schema",
    [
        pytest.param(
            "jsonld_context_class_uri_prefix.yaml",
            marks=pytest.mark.xfail(reason="Bug linkml#2677: class_uri and slot_uri not used for element URIs"),
        ),
        pytest.param(
            "jsonld_context_inlined_external_types.yaml",
            marks=pytest.mark.xfail(reason="Bug linkml#2679: unexpected example.org URI"),
        ),
        pytest.param(
            "jsonld_context_no_default_namespace_prefix.yaml",
            marks=pytest.mark.xfail(reason="Bug linkml#2677: class_uri and slot_uri not used for element URIs"),
        ),
    ],
)
def test_expected_rdf(input_path, schema):
    schema_path = input_path(schema)
    # generate the JSON-LD document
    output = JSONLDGenerator(schema_path).serialize()
    rdf_expects = RdfExpectations(schema_path, json.loads(output))
    rdf_expects.check_expectations()
