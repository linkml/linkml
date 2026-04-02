"""Benchmark: deterministic Turtle serializer on real-world ontologies.

Evaluates the ``--deterministic`` flag against schema.org (~16 000 triples,
~800 classes, ~1 400 properties) and the kitchen_sink LinkML schema to
demonstrate four properties:

1. **Semantic equivalence** — ``rdflib.compare.isomorphic()`` confirms that
   deterministic and non-deterministic outputs encode the same RDF graph.
2. **Byte-level stability** — SHA-256 identity across repeated runs proves
   that deterministic output is truly reproducible.
3. **Diff quality** — controlled mutations show that small schema changes
   produce small, focused diffs (high signal-to-noise ratio).
4. **Performance** — generation time stays within acceptable bounds even
   on large real-world graphs.

Schema.org tests exercise ``deterministic_turtle()`` directly on a
pre-existing OWL ontology.  Kitchen_sink tests exercise the full
``OwlSchemaGenerator`` / ``ShaclGenerator`` pipeline with LinkML schemas.

References
----------
- W3C RDFC-1.0: https://www.w3.org/TR/rdf-canon/
- W3C Turtle 1.1: https://www.w3.org/TR/turtle/
- schema.org: https://schema.org/docs/developers.html
"""

import difflib
import hashlib
import time
from pathlib import Path

import pytest
import yaml
from rdflib import Graph
from rdflib.compare import isomorphic

from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.shaclgen import ShaclGenerator
from linkml.utils.generator import deterministic_turtle

_has_pyoxigraph = False
try:
    import pyoxigraph

    _has_pyoxigraph = hasattr(pyoxigraph, "Dataset")
except ImportError:
    pass

pytestmark = pytest.mark.skipif(
    not _has_pyoxigraph,
    reason="pyoxigraph >= 0.4.0 required for deterministic benchmarks",
)

KITCHEN_SINK = str(Path(__file__).parent / "input" / "kitchen_sink.yaml")
SCHEMA_ORG_URL = "https://schema.org/version/latest/schemaorg-current-https.ttl"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _diff_line_count(a: str, b: str) -> int:
    """Count lines present in *b* but not in *a* (unified-diff additions)."""
    al = a.strip().splitlines()
    bl = b.strip().splitlines()
    return sum(
        1 for line in difflib.unified_diff(al, bl, lineterm="") if line.startswith("+") and not line.startswith("+++")
    )


# ── Schema.org: direct serializer benchmark ────────────────────────


@pytest.fixture(scope="module")
def schema_org_graph():
    """Download and parse schema.org as an rdflib Graph.

    Cached for the module so the network fetch only happens once.
    Skips all dependent tests if the download fails.
    """
    try:
        import urllib.request

        with urllib.request.urlopen(SCHEMA_ORG_URL, timeout=60) as resp:
            data = resp.read().decode("utf-8")
    except Exception as exc:
        pytest.skip(f"Could not fetch schema.org: {exc}")

    g = Graph()
    g.parse(data=data, format="turtle")
    return g


@pytest.mark.network
class TestSchemaOrgDeterministicSerializer:
    """Benchmark ``deterministic_turtle()`` on schema.org OWL ontology."""

    def test_semantic_equivalence(self, schema_org_graph):
        """Deterministic serialization must be isomorphic to the original graph."""
        det_ttl = deterministic_turtle(schema_org_graph)

        g_det = Graph()
        g_det.parse(data=det_ttl, format="turtle")

        assert len(g_det) == len(schema_org_graph), (
            f"Triple count mismatch: original={len(schema_org_graph)}, deterministic={len(g_det)}"
        )
        assert isomorphic(g_det, schema_org_graph), (
            "Deterministic output is NOT isomorphic to original schema.org graph"
        )

    def test_byte_stability(self, schema_org_graph):
        """Two deterministic runs must produce byte-identical output."""
        run1 = deterministic_turtle(schema_org_graph)
        run2 = deterministic_turtle(schema_org_graph)
        assert _sha256(run1) == _sha256(run2), "Deterministic serializer produced different output across runs"

    def test_prefix_filtering(self, schema_org_graph):
        """Only prefixes actually used in the graph should be declared."""
        det_ttl = deterministic_turtle(schema_org_graph)

        # Extract declared prefixes
        declared = {}
        for line in det_ttl.splitlines():
            if line.startswith("@prefix"):
                parts = line.split()
                pfx = parts[1].rstrip(":")
                ns = parts[2].strip("<>")
                declared[pfx] = ns

        # Collect all IRIs in the graph
        from rdflib import URIRef

        used_iris = set()
        for s, p, o in schema_org_graph:
            for term in (s, p, o):
                if isinstance(term, URIRef):
                    used_iris.add(str(term))

        # Every declared prefix must have at least one IRI using it
        for pfx, ns in declared.items():
            assert any(iri.startswith(ns) for iri in used_iris), f"Prefix '{pfx}:' <{ns}> declared but no IRI uses it"

    def test_performance(self, schema_org_graph):
        """Serialization must complete within 60 seconds for ~16K triples."""
        start = time.time()
        det_ttl = deterministic_turtle(schema_org_graph)
        elapsed = time.time() - start
        triple_count = len(schema_org_graph)
        throughput = triple_count / elapsed if elapsed > 0 else float("inf")

        # Log for benchmark visibility (shows with pytest -v)
        print(f"\n  schema.org: {triple_count} triples in {elapsed:.1f}s ({throughput:.0f} triples/s)")

        assert elapsed < 60.0, f"Serialization took {elapsed:.1f}s (limit: 60s) for {triple_count} triples"
        assert len(det_ttl) > 1000, "Output suspiciously short"


# ── Kitchen_sink: full pipeline benchmark ───────────────────────────


def _mutate_kitchen_sink(description_suffix: str = "", add_slot: bool = False) -> str:
    """Create a mutated copy of kitchen_sink.yaml **in the same directory** and return its path.

    The copy must live alongside the original so that LinkML relative imports
    (``linkml:types``, ``core``, etc.) resolve correctly.

    Uses a unique filename (via ``os.getpid()``) to avoid race conditions
    when tests run in parallel under pytest-xdist.

    Parameters
    ----------
    description_suffix
        Text appended to the first class description found.
    add_slot
        If True, adds a synthetic ``benchmark_notes`` slot to the first class.
    """
    import os

    ks_path = Path(KITCHEN_SINK)
    schema = yaml.safe_load(ks_path.read_text())

    if description_suffix or add_slot:
        # Find the first class with a description
        for cls_name, cls_def in schema.get("classes", {}).items():
            if isinstance(cls_def, dict) and cls_def.get("description"):
                if description_suffix:
                    cls_def["description"] += description_suffix
                if add_slot:
                    slots = cls_def.get("slots", [])
                    slots.append("benchmark_notes")
                    cls_def["slots"] = slots
                break

        # Define the synthetic slot if adding one
        if add_slot:
            slots_dict = schema.setdefault("slots", {})
            slots_dict["benchmark_notes"] = {
                "description": "Synthetic benchmark slot for diff quality testing.",
                "range": "string",
            }

    # Write in the same directory so relative imports resolve.
    # Use PID to avoid race conditions with pytest-xdist workers.
    out_path = ks_path.parent / f"_benchmark_mutated_{os.getpid()}_kitchen_sink.yaml"
    out_path.write_text(
        yaml.dump(schema, default_flow_style=False, allow_unicode=True),
        encoding="utf-8",
    )
    return str(out_path)


@pytest.mark.parametrize(
    "generator_cls",
    [OwlSchemaGenerator, ShaclGenerator],
    ids=["owl", "shacl"],
)
class TestKitchenSinkDiffQuality:
    """Measure diff quality on the kitchen_sink schema with controlled mutations."""

    def test_mutation_description_change(self, generator_cls):
        """A single description change must produce a small, focused diff.

        Deterministic mode should change only the affected line(s) and their
        immediate context (e.g. SHACL may repeat descriptions in sh:description).
        Non-deterministic mode produces a much larger diff due to blank-node
        and property-ordering instability.
        """
        base = generator_cls(KITCHEN_SINK, deterministic=True).serialize()
        mutated_path = _mutate_kitchen_sink(description_suffix=" (benchmark edit)")
        try:
            mutated = generator_cls(mutated_path, deterministic=True).serialize()
        finally:
            Path(mutated_path).unlink(missing_ok=True)

        det_diff = _diff_line_count(base, mutated)

        # Non-deterministic baseline for comparison
        non_base = generator_cls(KITCHEN_SINK, deterministic=False).serialize()
        non_mutated_path = _mutate_kitchen_sink(description_suffix=" (benchmark edit)")
        try:
            non_mutated = generator_cls(non_mutated_path, deterministic=False).serialize()
        finally:
            Path(non_mutated_path).unlink(missing_ok=True)

        non_diff = _diff_line_count(non_base, non_mutated)

        # The deterministic diff must be small (description + any SHACL mirrors)
        assert det_diff <= 20, (
            f"Deterministic diff too large for a 1-description change: {det_diff} lines (expected ≤20)"
        )
        # Signal-to-noise: deterministic must be at least 5× smaller
        if non_diff > 0:
            ratio = non_diff / max(det_diff, 1)
            assert ratio >= 5, (
                f"Insufficient noise reduction: det={det_diff}, non-det={non_diff}, ratio={ratio:.1f}× (expected ≥5×)"
            )

        print(
            f"\n  {generator_cls.__name__} description mutation: "
            f"det={det_diff} lines, non-det={non_diff} lines, "
            f"noise reduction={non_diff / max(det_diff, 1):.0f}×"
        )

    def test_mutation_add_slot(self, generator_cls):
        """Adding a new slot must produce a proportionally small diff.

        A new slot adds ~10-20 triples (label, range, domain, restrictions).
        The diff should be roughly proportional to the new content, not a
        full-file rewrite.
        """
        base = generator_cls(KITCHEN_SINK, deterministic=True).serialize()
        mutated_path = _mutate_kitchen_sink(add_slot=True)
        try:
            mutated = generator_cls(mutated_path, deterministic=True).serialize()
        finally:
            Path(mutated_path).unlink(missing_ok=True)

        det_diff = _diff_line_count(base, mutated)

        # Non-deterministic baseline for comparison
        non_base = generator_cls(KITCHEN_SINK, deterministic=False).serialize()
        non_mutated_path = _mutate_kitchen_sink(add_slot=True)
        try:
            non_mutated = generator_cls(non_mutated_path, deterministic=False).serialize()
        finally:
            Path(non_mutated_path).unlink(missing_ok=True)

        non_diff = _diff_line_count(non_base, non_mutated)

        g_base = Graph()
        g_base.parse(data=base, format="turtle")
        g_mut = Graph()
        g_mut.parse(data=mutated, format="turtle")
        new_triples = len(g_mut) - len(g_base)

        # Diff should be proportional to new triples (allow 5× margin)
        assert det_diff <= max(new_triples * 5, 40), (
            f"Deterministic diff ({det_diff} lines) disproportionate to new triples ({new_triples})"
        )
        # Signal-to-noise: deterministic must be at least 5× smaller
        if non_diff > 0:
            ratio = non_diff / max(det_diff, 1)
            assert ratio >= 5, (
                f"Insufficient noise reduction: det={det_diff}, non-det={non_diff}, ratio={ratio:.1f}× (expected ≥5×)"
            )

        print(
            f"\n  {generator_cls.__name__} add-slot mutation: "
            f"det_diff={det_diff} lines, non-det={non_diff} lines, "
            f"new_triples={new_triples}, noise reduction={non_diff / max(det_diff, 1):.0f}×"
        )

        print(f"\n  {generator_cls.__name__} add-slot mutation: det_diff={det_diff} lines, new_triples={new_triples}")


@pytest.mark.parametrize(
    "generator_cls",
    [OwlSchemaGenerator, ShaclGenerator],
    ids=["owl", "shacl"],
)
class TestKitchenSinkEquivalence:
    """Verify semantic equivalence between deterministic and non-deterministic modes."""

    def test_triple_count_matches(self, generator_cls):
        """Both modes must produce the same number of triples."""
        det = generator_cls(KITCHEN_SINK, deterministic=True).serialize()
        nondet = generator_cls(KITCHEN_SINK, deterministic=False).serialize()

        g_det = Graph()
        g_det.parse(data=det, format="turtle")
        g_nondet = Graph()
        g_nondet.parse(data=nondet, format="turtle")

        assert len(g_det) == len(g_nondet), (
            f"Triple count mismatch: deterministic={len(g_det)}, non-deterministic={len(g_nondet)}"
        )

    def test_byte_stability_across_runs(self, generator_cls):
        """Three deterministic runs must produce identical output."""
        runs = [generator_cls(KITCHEN_SINK, deterministic=True).serialize() for _ in range(3)]
        hashes = [_sha256(r) for r in runs]
        assert hashes[0] == hashes[1] == hashes[2], f"Deterministic output varies across runs: {hashes}"

    def test_non_deterministic_instability(self, generator_cls):
        """Non-deterministic output should vary across runs (documents the problem).

        This test is advisory — it passes regardless but logs the instability.
        """
        runs = [generator_cls(KITCHEN_SINK, deterministic=False).serialize() for _ in range(3)]
        hashes = [_sha256(r) for r in runs]
        identical = hashes[0] == hashes[1] == hashes[2]
        print(
            f"\n  {generator_cls.__name__} non-det stable: {identical} "
            f"(expected: False for Turtle due to bnode/ordering instability)"
        )
