"""Tests for deterministic generator output.

When ``deterministic=True``, generators must produce byte-identical output
across multiple invocations. This ensures version-controlled artifacts don't
show spurious diffs from blank-node relabeling or dict-ordering instability.
"""

import json
import time
from pathlib import Path

import pytest

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.shaclgen import ShaclGenerator

SCHEMA = str(Path(__file__).parent / "input" / "personinfo.yaml")


@pytest.mark.parametrize(
    "generator_cls,kwargs",
    [
        (OwlSchemaGenerator, {}),
        (ShaclGenerator, {}),
        (ContextGenerator, {}),
        (JSONLDGenerator, {}),
    ],
    ids=["owl", "shacl", "context", "jsonld"],
)
def test_deterministic_output_is_identical_across_runs(generator_cls, kwargs):
    """Generate output twice with deterministic=True and verify identity."""
    out1 = generator_cls(SCHEMA, deterministic=True, **kwargs).serialize()
    out2 = generator_cls(SCHEMA, deterministic=True, **kwargs).serialize()
    # JSONLDGenerator embeds a generation_date timestamp — normalize it
    if generator_cls is JSONLDGenerator:
        import re

        ts_re = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")
        out1 = ts_re.sub("TIMESTAMP", out1)
        out2 = ts_re.sub("TIMESTAMP", out2)
    assert out1 == out2, f"{generator_cls.__name__} produced different output across runs"
    assert len(out1) > 100, "Output suspiciously short — generator may have failed silently"


@pytest.mark.parametrize(
    "generator_cls",
    [ContextGenerator, JSONLDGenerator],
    ids=["context", "jsonld"],
)
def test_deterministic_json_has_sorted_keys(generator_cls):
    """When deterministic=True, JSON dict keys should be sorted at all levels.

    For the ContextGenerator, @context keys use grouped ordering (prefixes
    before term entries) — each group is sorted, but not globally.
    """
    out = generator_cls(SCHEMA, deterministic=True).serialize()
    parsed = json.loads(out)

    is_context_gen = generator_cls is ContextGenerator

    def _check_sorted_keys(obj, path="root"):
        if isinstance(obj, dict):
            keys = list(obj.keys())
            # Context generator groups @context keys: @-directives, prefixes, terms
            if is_context_gen and path == "root.@context":
                at_keys = [k for k in keys if k.startswith("@")]
                prefix_keys = [k for k in keys if not k.startswith("@") and isinstance(obj[k], str)]
                term_keys = [k for k in keys if not k.startswith("@") and not isinstance(obj[k], str)]
                assert at_keys == sorted(at_keys), f"@-keys not sorted: {at_keys}"
                assert prefix_keys == sorted(prefix_keys), f"Prefix keys not sorted: {prefix_keys}"
                assert term_keys == sorted(term_keys), f"Term keys not sorted: {term_keys}"
            else:
                assert keys == sorted(keys), f"Keys not sorted at {path}: {keys}"
            for k, v in obj.items():
                _check_sorted_keys(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                _check_sorted_keys(item, f"{path}[{i}]")

    _check_sorted_keys(parsed)


@pytest.mark.parametrize(
    "generator_cls",
    [ContextGenerator, JSONLDGenerator],
    ids=["context", "jsonld"],
)
def test_deterministic_json_lists_are_sorted(generator_cls):
    """When deterministic=True, JSON list elements should be sorted."""
    out = generator_cls(SCHEMA, deterministic=True).serialize()
    parsed = json.loads(out)

    def _check_sorted_lists(obj, path="root"):
        if isinstance(obj, dict):
            for k, v in obj.items():
                _check_sorted_lists(v, f"{path}.{k}")
        elif isinstance(obj, list):
            str_items = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in obj]
            assert str_items == sorted(str_items), f"List not sorted at {path}"
            for i, item in enumerate(obj):
                _check_sorted_lists(item, f"{path}[{i}]")

    _check_sorted_lists(parsed)


@pytest.mark.parametrize(
    "generator_cls",
    [OwlSchemaGenerator, ShaclGenerator],
    ids=["owl", "shacl"],
)
def test_deterministic_turtle_preserves_at_prefix(generator_cls):
    """deterministic_turtle must produce standard @prefix, not SPARQL PREFIX."""
    out = generator_cls(SCHEMA, deterministic=True).serialize()
    assert "@prefix" in out, "Output uses non-standard prefix syntax"
    assert "PREFIX " not in out, "Output uses SPARQL PREFIX instead of Turtle @prefix"


def test_deterministic_turtle_performance():
    """Deterministic OWL generation must complete within 10 seconds for personinfo.

    The Weisfeiler-Lehman approach is O(n log n), so this should easily pass.
    The previous canon=True approach was exponential and failed this test
    for graphs above ~250 triples.
    """
    start = time.time()
    out = OwlSchemaGenerator(SCHEMA, deterministic=True).serialize()
    elapsed = time.time() - start
    assert elapsed < 10.0, f"Deterministic generation took {elapsed:.1f}s (limit: 10s)"
    assert len(out) > 100, "Output suspiciously short"


def test_shacl_closed_ignored_properties_deterministic():
    """sh:ignoredProperties in closed shapes must be deterministic.

    ``_build_ignored_properties`` collects inherited slots into a set; without
    explicit sorting this produces different ``rdf:first``/``rdf:rest`` chains
    on each run.  With ``deterministic=True`` (and sorted Collection inputs)
    the output must be byte-identical.
    """
    runs = [ShaclGenerator(SCHEMA, deterministic=True, closed=True).serialize() for _ in range(3)]
    assert runs[0] == runs[1] == runs[2], "sh:ignoredProperties ordering differs across runs"
    assert "sh:ignoredProperties" in runs[0], "Expected closed shapes with sh:ignoredProperties"


def test_shacl_enum_in_deterministic():
    """sh:in RDF lists for enums must be deterministic.

    ``_build_enum_constraint`` iterates ``enum.permissible_values.items()``
    (dict iteration order) into a ``Collection``.  Without sorting, the
    ``rdf:first``/``rdf:rest`` chain varies across runs.
    """
    runs = [ShaclGenerator(SCHEMA, deterministic=True).serialize() for _ in range(3)]
    assert runs[0] == runs[1] == runs[2], "sh:in enum list ordering differs across runs"
    assert "sh:in" in runs[0], "Expected sh:in constraints for enums"


def test_owl_enum_one_of_deterministic():
    """owl:oneOf RDF lists for enums must be deterministic.

    ``_boolean_expression`` feeds ``pv_uris`` (from ``permissible_values``)
    into a ``Collection``.  Without sorting, ``owl:oneOf`` list ordering varies.
    """
    runs = [OwlSchemaGenerator(SCHEMA, deterministic=True).serialize() for _ in range(3)]
    assert runs[0] == runs[1] == runs[2], "owl:oneOf enum list ordering differs across runs"


KITCHEN_SINK = str(Path(__file__).parent / "input" / "kitchen_sink.yaml")


def test_deterministic_large_schema():
    """End-to-end idempotency on a complex schema (kitchen_sink).

    Exercises many code paths simultaneously: closed shapes, enums, imports,
    class hierarchies, and mixed ranges.
    """
    owl1 = OwlSchemaGenerator(KITCHEN_SINK, deterministic=True).serialize()
    owl2 = OwlSchemaGenerator(KITCHEN_SINK, deterministic=True).serialize()
    assert owl1 == owl2, "OWL output differs across runs for kitchen_sink"
    assert len(owl1) > 500, "kitchen_sink output suspiciously short"

    shacl1 = ShaclGenerator(KITCHEN_SINK, deterministic=True).serialize()
    shacl2 = ShaclGenerator(KITCHEN_SINK, deterministic=True).serialize()
    assert shacl1 == shacl2, "SHACL output differs across runs for kitchen_sink"
    assert len(shacl1) > 500, "kitchen_sink output suspiciously short"


def test_deterministic_context_preserves_jsonld_structure():
    """Deterministic JSON-LD context must preserve conventional structure.

    JSON-LD contexts have a conventional layout:
    1. ``comments`` block first (metadata)
    2. ``@context`` block second, with prefixes grouped before term entries

    ``deterministic_json()`` would scramble this by sorting all keys
    uniformly.  The context generator must use JSON-LD-aware ordering.
    """
    out = ContextGenerator(SCHEMA, deterministic=True, metadata=True).serialize()
    parsed = json.loads(out)

    # Top-level key order: "comments" before "@context"
    top_keys = list(parsed.keys())
    assert "comments" in top_keys, "Expected 'comments' block with metadata=True"
    assert top_keys.index("comments") < top_keys.index("@context"), (
        f"'comments' should precede '@context', got: {top_keys}"
    )

    # Inside @context: @-directives, then prefixes (str values), then terms (dict values)
    ctx = parsed["@context"]
    ctx_keys = list(ctx.keys())

    at_keys = [k for k in ctx_keys if k.startswith("@")]
    prefix_keys = [k for k in ctx_keys if not k.startswith("@") and isinstance(ctx[k], str)]
    term_keys = [k for k in ctx_keys if not k.startswith("@") and not isinstance(ctx[k], str)]

    # Verify grouping: all @-keys before all prefix keys before all term keys
    last_at = max(ctx_keys.index(k) for k in at_keys) if at_keys else -1
    first_prefix = min(ctx_keys.index(k) for k in prefix_keys) if prefix_keys else len(ctx_keys)
    last_prefix = max(ctx_keys.index(k) for k in prefix_keys) if prefix_keys else -1
    first_term = min(ctx_keys.index(k) for k in term_keys) if term_keys else len(ctx_keys)

    assert last_at < first_prefix, "@-directives must come before prefixes"
    assert last_prefix < first_term, "Prefixes must come before term entries"

    # Verify each group is sorted internally
    assert at_keys == sorted(at_keys), f"@-directives not sorted: {at_keys}"
    assert prefix_keys == sorted(prefix_keys), f"Prefixes not sorted: {prefix_keys}"
    assert term_keys == sorted(term_keys), f"Term entries not sorted: {term_keys}"


def test_non_deterministic_is_default():
    """Verify that ``deterministic`` defaults to False."""
    gen = OwlSchemaGenerator(SCHEMA)
    assert gen.deterministic is False
