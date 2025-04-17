import json

import pytest
import rdflib
from deepdiff import DeepDiff
from pyld import jsonld as pyjsonld
from pyld.jsonld import JsonLdError
from rdflib import compare as rdf_graph_cmp

from linkml.generators import ContextGenerator, JSONLDGenerator
from tests.utils.compare_jsonld_context import CompareJsonldContext

# flag combinations that are unique,
# considering that flags are to be considered as 2 item tuples
flag_combinations = [
    (True, True, True, False),
    (True, True, False, True),
    (False, False, True, True),
    (True, False, False, True),
]


def test_jsonld_context_integration(kitchen_sink_path, snapshot_path):
    jsonld_context = ContextGenerator(kitchen_sink_path).serialize()

    CompareJsonldContext.compare_with_snapshot(jsonld_context, snapshot_path("kitchen_sink.context.jsonld"))


def test_no_default_namespace_prefix(input_path, snapshot_path):
    jsonld_context = ContextGenerator(str(input_path("jsonld_context_no_default_namespace_prefix.yaml"))).serialize()

    CompareJsonldContext.compare_with_snapshot(
        jsonld_context, snapshot_path("no_default_namespace_prefix.context.jsonld")
    )


def test_class_uri_prefix(input_path, snapshot_path):
    jsonld_context = ContextGenerator(str(input_path("jsonld_context_class_uri_prefix.yaml"))).serialize()

    CompareJsonldContext.compare_with_snapshot(jsonld_context, snapshot_path("class_uri_prefix.context.jsonld"))


def test_inlined_external_types(input_path, snapshot_path):
    jsonld_context = ContextGenerator(str(input_path("jsonld_context_inlined_external_types.yaml"))).serialize()

    CompareJsonldContext.compare_with_snapshot(jsonld_context, snapshot_path("inlined_external_types.context.jsonld"))


@pytest.mark.parametrize(
    "schema",
    [
        "jsonld_context_class_uri_prefix.yaml",
        "jsonld_context_inlined_external_types.yaml",
        "jsonld_context_no_default_namespace_prefix.yaml",
    ],
)
@pytest.mark.parametrize(
    "model_1, prefixes_1, model_2, prefixes_2",
    flag_combinations,
)
def test_isomorphism(input_path, schema, model_1, prefixes_1, model_2, prefixes_2):
    """Check that resulting graph is isomorphic.
    Check it first with expanded JSON-LD and then with RDF."""
    schema = input_path(schema)

    # generate the JSON-LD document
    output = JSONLDGenerator(schema, context=()).serialize(context=())
    jsonld_doc = json.loads(output)

    # generate both context combinations
    output = ContextGenerator(schema, model=model_1, prefixes=prefixes_1, emit_metadata=False).serialize(
        model=model_1, prefixes=prefixes_1, emit_metadata=False
    )
    context_1 = json.loads(output)
    output = ContextGenerator(schema, model=model_2, prefixes=prefixes_2, emit_metadata=False).serialize(
        model=model_2, prefixes=prefixes_2, emit_metadata=False
    )
    context_2 = json.loads(output)

    # generate compact JSON-LD for both combinations
    # context fetching from URL is flacky, tring twice before failing
    try:
        jsonld_compact_1 = pyjsonld.compact(jsonld_doc, context_1)
    except JsonLdError:
        jsonld_compact_1 = pyjsonld.compact(jsonld_doc, context_1)
    try:
        jsonld_compact_2 = pyjsonld.compact(jsonld_doc, context_2)
    except JsonLdError:
        jsonld_compact_2 = pyjsonld.compact(jsonld_doc, context_2)

    # and expand all JSON-LD
    jsonld_expand_1 = pyjsonld.expand(jsonld_compact_1)
    jsonld_expand_2 = pyjsonld.expand(jsonld_compact_2)

    # and assert all expanded are equal
    jsonld_diffs = DeepDiff(jsonld_expand_1, jsonld_expand_2)
    assert not jsonld_diffs

    #
    g_1 = rdflib.Graph().parse(data=jsonld_compact_1, format="json-ld")
    g_2 = rdflib.Graph().parse(data=jsonld_compact_2, format="json-ld")
    assert rdf_graph_cmp.isomorphic(g_1, g_2)


@pytest.mark.parametrize(
    "schema",
    [
        "jsonld_context_class_uri_prefix.yaml",
        "jsonld_context_inlined_external_types.yaml",
        "jsonld_context_no_default_namespace_prefix.yaml",
    ],
)
@pytest.mark.parametrize(
    "model_1, prefixes_1, model_2, prefixes_2",
    flag_combinations,
)
def test_compact_diffs(input_path, schema, model_1, prefixes_1, model_2, prefixes_2):
    """Check that compact JSON-LD differs as expected."""
    schema = input_path(schema)

    # generate the JSON-LD document
    output = JSONLDGenerator(schema, context=()).serialize(context=())
    open("tmp/doc.class.ld.json", "w+").write(output)
    jsonld_doc = json.loads(output)

    # generate both context combinations
    output = ContextGenerator(schema, model=model_1, prefixes=prefixes_1, emit_metadata=False).serialize(
        model=model_1, prefixes=prefixes_1, emit_metadata=False
    )
    flags = ""
    if model_1:
        flags = flags + "t"
    else:
        flags = flags + "f"
    if prefixes_1:
        flags = flags + "t"
    else:
        flags = flags + "f"
    open(f"tmp/context_{flags}.class.ld.json", "w+").write(output)
    context_1 = json.loads(output)
    output = ContextGenerator(schema, model=model_2, prefixes=prefixes_2, emit_metadata=False).serialize(
        model=model_2, prefixes=prefixes_2, emit_metadata=False
    )
    flags = ""
    if model_2:
        flags = flags + "t"
    else:
        flags = flags + "f"
    if prefixes_2:
        flags = flags + "t"
    else:
        flags = flags + "f"
    open(f"tmp/context_{flags}.class.ld.json", "w+").write(output)
    context_2 = json.loads(output)

    # generate compact JSON-LD for both combinations
    # context fetching from URL is flacky, tring twice before failing
    try:
        jsonld_compact_1 = pyjsonld.compact(jsonld_doc, context_1)
    except JsonLdError:
        jsonld_compact_1 = pyjsonld.compact(jsonld_doc, context_1)
    try:
        jsonld_compact_2 = pyjsonld.compact(jsonld_doc, context_2)
    except JsonLdError:
        jsonld_compact_2 = pyjsonld.compact(jsonld_doc, context_2)

    # if "prefixes" flag active, then CURIEs, otherwise URIs
    if prefixes_1:
        assert "linkml:classes" in jsonld_compact_1.keys()
    else:
        assert "https://w3id.org/linkml/classes" in jsonld_compact_1.keys()
    if prefixes_2:
        assert "linkml:classes" in jsonld_compact_2.keys()
    else:
        assert "https://w3id.org/linkml/classes" in jsonld_compact_2.keys()

    # switching only the "model" flag, but keeping "prefixes",
    # the model terms will be missing in the context
    jsonld_diffs = DeepDiff(jsonld_compact_1, jsonld_compact_2)
    if (model_1 and prefixes_1) and (not model_2 and prefixes_2):
        assert list(jsonld_diffs.keys()) == ["dictionary_item_removed"]
        for item in jsonld_diffs["dictionary_item_removed"]:
            assert item.startswith("root['@context']")
    # switching only the "model" flag, but keeping "no-prefixes",
    # the model terms will be missing in the context
    elif (model_1 and not prefixes_1) and (not model_2 and not prefixes_2):
        assert list(jsonld_diffs.keys()) == ["values_changed"]
        assert list(jsonld_diffs["values_changed"].keys()) == ["root['@context']"]
    # switching the "prefixes" flag creates multiple differences
    # in the JSON-LD document body because of CURIEs vs. URIs differences
    # apart from changes in the context
    else:
        assert list(jsonld_diffs.keys()) == ["values_changed"]
        assert list(jsonld_diffs["values_changed"].keys()) == ["root"]
