"""Tests for deterministic generator output.

When ``deterministic=True``, generators must produce byte-identical output
across multiple invocations. This ensures version-controlled artifacts don't
show spurious diffs from blank-node relabeling or dict-ordering instability.

Generators must also produce **isomorphic** output — the deterministic
serialization must encode the same RDF graph as non-deterministic mode.
"""

import json
import time
from pathlib import Path

import pytest
from rdflib import Graph
from rdflib.compare import isomorphic

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.shaclgen import ShaclGenerator

# Deterministic Turtle requires pyoxigraph >= 0.4.0 (for Dataset/canonicalize).
# When an older version is present (e.g. pulled in by morph-kgc), skip these tests.
_has_pyoxigraph = False
try:
    import pyoxigraph

    _has_pyoxigraph = hasattr(pyoxigraph, "Dataset")
except ImportError:
    pass

pytestmark = pytest.mark.skipif(not _has_pyoxigraph, reason="pyoxigraph >= 0.4.0 required for deterministic tests")

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
    """When deterministic=True, JSON list elements should be sorted.

    Lists under JSON-LD structural keys (``@context``, ``@list``, ``imports``,
    etc.) are exempt because their ordering carries semantic meaning.
    """
    out = generator_cls(SCHEMA, deterministic=True).serialize()
    parsed = json.loads(out)

    # JSON-LD keys whose array values carry ordering semantics.
    _ORDERED_KEYS = {"@context", "@list", "@graph", "@set", "imports"}

    def _check_sorted_lists(obj, path="root", parent_key=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                _check_sorted_lists(v, f"{path}.{k}", parent_key=k)
        elif isinstance(obj, list):
            if parent_key not in _ORDERED_KEYS:
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


def test_wl_handles_structurally_similar_bnodes():
    """Blank nodes with identical local structure but different named neighbours
    must receive different WL signatures and thus different stable labels.

    This tests the core WL property: two BNodes that differ only in their
    connected named nodes (URIs/literals) must be distinguishable.
    """
    from rdflib import BNode, Graph, Namespace, URIRef

    from linkml.utils.generator import deterministic_turtle

    RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
    OWL_RESTRICTION = URIRef("http://www.w3.org/2002/07/owl#Restriction")
    OWL_ON_PROP = URIRef("http://www.w3.org/2002/07/owl#onProperty")
    OWL_ALL_VALUES = URIRef("http://www.w3.org/2002/07/owl#allValuesFrom")

    EX = Namespace("http://example.org/")
    g = Graph()

    # Two restrictions with same structure but different property URIs
    r1 = BNode()
    g.add((r1, RDF_TYPE, OWL_RESTRICTION))
    g.add((r1, OWL_ON_PROP, EX.alpha))
    g.add((r1, OWL_ALL_VALUES, EX.Target1))

    r2 = BNode()
    g.add((r2, RDF_TYPE, OWL_RESTRICTION))
    g.add((r2, OWL_ON_PROP, EX.beta))
    g.add((r2, OWL_ALL_VALUES, EX.Target2))

    RDFS_SUBCLASS = URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf")
    g.add((EX.MyClass, RDFS_SUBCLASS, r1))
    g.add((EX.MyClass, RDFS_SUBCLASS, r2))

    # Must be deterministic across runs
    out1 = deterministic_turtle(g)
    out2 = deterministic_turtle(g)
    assert out1 == out2, "WL-based serializer is not deterministic for similar BNodes"

    # Both restrictions must appear (not collapsed)
    assert "alpha" in out1
    assert "beta" in out1


def test_deterministic_turtle_no_bnodes():
    """Graphs with no blank nodes should still produce sorted, deterministic output."""
    from rdflib import Graph, Literal, Namespace
    from rdflib.namespace import RDFS

    from linkml.utils.generator import deterministic_turtle

    EX = Namespace("http://example.org/")
    g = Graph()
    g.add((EX.B, RDFS.label, Literal("B")))
    g.add((EX.A, RDFS.label, Literal("A")))

    out1 = deterministic_turtle(g)
    out2 = deterministic_turtle(g)
    assert out1 == out2

    # A should appear before B (sorted)
    a_pos = out1.find("example.org/A")
    b_pos = out1.find("example.org/B")
    assert a_pos < b_pos, "Triples should be sorted: A before B"


@pytest.mark.xfail(
    reason=(
        "Collection sorting (owl:oneOf, sh:in) in deterministic mode intentionally "
        "reorders RDF list triples for canonical output. The resulting graph is "
        "semantically equivalent (OWL/SHACL interpret these as unordered sets) but "
        "not RDF-isomorphic because rdf:first/rdf:rest chains encode ordering."
    ),
    strict=True,
)
@pytest.mark.parametrize(
    "generator_cls",
    [OwlSchemaGenerator, ShaclGenerator],
    ids=["owl", "shacl"],
)
def test_deterministic_turtle_is_isomorphic(generator_cls):
    """Deterministic output is NOT RDF-isomorphic to non-deterministic output.

    This documents the trade-off identified in linkml/linkml#3295 review:
    deterministic mode sorts Collection inputs (owl:oneOf, sh:in,
    sh:ignoredProperties) to produce canonical RDF list ordering.  Since RDF
    Collections encode order via rdf:first/rdf:rest triples, the sorted graph
    is structurally different from the insertion-order graph — even though the
    OWL/SHACL semantics are identical (these Collections represent sets).

    The test is marked xfail(strict=True) so that it:
    - Documents the known, intentional non-isomorphism
    - Alerts maintainers if the behaviour changes (strict xfail fails on pass)
    """
    out_det = generator_cls(SCHEMA, deterministic=True).serialize()
    out_nondet = generator_cls(SCHEMA, deterministic=False).serialize()

    g_det = Graph()
    g_det.parse(data=out_det, format="turtle")

    g_nondet = Graph()
    g_nondet.parse(data=out_nondet, format="turtle")

    assert len(g_det) == len(g_nondet), (
        f"Triple count mismatch: deterministic={len(g_det)}, non-deterministic={len(g_nondet)}"
    )
    assert isomorphic(g_det, g_nondet), (
        f"{generator_cls.__name__}: deterministic output is NOT isomorphic "
        "to non-deterministic output — the serialization changed the graph"
    )


@pytest.mark.parametrize(
    "generator_cls",
    [OwlSchemaGenerator, ShaclGenerator],
    ids=["owl", "shacl"],
)
def test_non_deterministic_output_unchanged(generator_cls):
    """Non-deterministic output must still produce valid RDF.

    Ensures that changes for deterministic mode don't break default behavior.
    """
    out = generator_cls(SCHEMA, deterministic=False).serialize()
    assert len(out) > 100, "Output suspiciously short"
    g = Graph()
    g.parse(data=out, format="turtle")
    assert len(g) > 50, f"Graph has too few triples ({len(g)})"


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
def test_non_deterministic_produces_valid_output(generator_cls, kwargs):
    """All generators must produce valid output in non-deterministic mode."""
    out = generator_cls(SCHEMA, deterministic=False, **kwargs).serialize()
    assert len(out) > 100, f"{generator_cls.__name__} output suspiciously short"


@pytest.mark.xfail(
    reason=(
        "Collection sorting in deterministic mode produces non-isomorphic RDF "
        "(different rdf:first/rdf:rest triples). See test_deterministic_turtle_is_isomorphic."
    ),
    strict=True,
)
@pytest.mark.parametrize(
    "generator_cls",
    [OwlSchemaGenerator, ShaclGenerator],
    ids=["owl", "shacl"],
)
def test_deterministic_kitchen_sink_isomorphic(generator_cls):
    """Isomorphism check on the complex kitchen_sink schema.

    Expected to fail for the same reason as test_deterministic_turtle_is_isomorphic:
    Collection sorting changes the RDF structure while preserving OWL/SHACL semantics.
    """
    out_det = generator_cls(KITCHEN_SINK, deterministic=True).serialize()
    out_nondet = generator_cls(KITCHEN_SINK, deterministic=False).serialize()

    g_det = Graph()
    g_det.parse(data=out_det, format="turtle")

    g_nondet = Graph()
    g_nondet.parse(data=out_nondet, format="turtle")

    assert isomorphic(g_det, g_nondet), (
        f"{generator_cls.__name__}: kitchen_sink deterministic output is NOT isomorphic to non-deterministic output"
    )


@pytest.mark.skipif(False, reason="does not require pyoxigraph")
def test_expression_sort_key_is_stable():
    """``_expression_sort_key`` must produce stable, content-based keys.

    LinkML anonymous expressions inherit ``YAMLRoot.__repr__()``, which
    formats objects using **field values** (not memory addresses).
    The ``_expression_sort_key`` helper relies on this for deterministic
    ordering of ``any_of`` / ``all_of`` / ``none_of`` members.

    This test verifies that:
    1. Two distinct objects with identical fields produce the same key.
    2. Objects with different fields produce different keys.
    3. Sorting is stable across repeated calls.
    """
    from linkml.generators.owlgen import _expression_sort_key
    from linkml_runtime.linkml_model.meta import AnonymousClassExpression, AnonymousSlotExpression

    # Two distinct objects with identical content → same key
    a1 = AnonymousClassExpression(is_a="Parent")
    a2 = AnonymousClassExpression(is_a="Parent")
    assert a1 is not a2
    assert _expression_sort_key(a1) == _expression_sort_key(a2)

    # Different content → different keys
    b = AnonymousClassExpression(is_a="Child")
    assert _expression_sort_key(a1) != _expression_sort_key(b)

    # Sorting stability: same order every time
    items = [b, a1, a2]
    for _ in range(5):
        result = sorted(items, key=_expression_sort_key)
        # "Child" < "Parent" alphabetically, so b comes first
        assert _expression_sort_key(result[0]) == _expression_sort_key(b)
        assert _expression_sort_key(result[1]) == _expression_sort_key(result[2])  # a1, a2 together

    # Slot expressions work too
    s1 = AnonymousSlotExpression(range="string")
    s2 = AnonymousSlotExpression(range="integer")
    assert _expression_sort_key(s1) != _expression_sort_key(s2)
    order1 = sorted([s2, s1], key=_expression_sort_key)
    order2 = sorted([s1, s2], key=_expression_sort_key)
    assert [_expression_sort_key(x) for x in order1] == [_expression_sort_key(x) for x in order2]
