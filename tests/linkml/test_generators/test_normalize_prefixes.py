"""Tests for the --normalize-prefixes flag across all generators.

Verifies that non-standard prefix aliases (e.g. ``sdo`` for ``https://schema.org/``)
are normalised to well-known names (e.g. ``schema``) consistently in OWL, SHACL,
and JSON-LD context output.

References:
- prefix.cc — community consensus RDF prefix registry
- rdflib 7.x curated default namespace bindings
- W3C Turtle §2.4 — prefix declarations are syntactic sugar
"""

import json
import logging
import re
import textwrap

import pytest

# ── Shared test schema ──────────────────────────────────────────────

SCHEMA_SDO = textwrap.dedent("""\
    id: https://example.org/test
    name: test_normalize
    default_prefix: ex
    prefixes:
      ex: https://example.org/
      linkml: https://w3id.org/linkml/
      sdo: https://schema.org/
    imports:
      - linkml:types
    classes:
      Person:
        class_uri: sdo:Person
        attributes:
          full_name:
            range: string
            slot_uri: sdo:name
""")

SCHEMA_DCE = textwrap.dedent("""\
    id: https://example.org/test
    name: test_normalize_dce
    default_prefix: ex
    prefixes:
      ex: https://example.org/
      linkml: https://w3id.org/linkml/
      dce: http://purl.org/dc/elements/1.1/
    imports:
      - linkml:types
    classes:
      Record:
        class_uri: ex:Record
        attributes:
          title:
            range: string
            slot_uri: dce:title
""")

# HTTP variant — linkml-runtime historically binds schema: http://schema.org/
# while rdflib (and the W3C) prefer https://schema.org/.  The normalize flag
# must handle both.
SCHEMA_HTTP_SDO = textwrap.dedent("""\
    id: https://example.org/test
    name: test_http_schema
    default_prefix: ex
    prefixes:
      ex: https://example.org/
      linkml: https://w3id.org/linkml/
      sdo: http://schema.org/
    imports:
      - linkml:types
    classes:
      Place:
        class_uri: sdo:Place
        attributes:
          geo:
            range: string
            slot_uri: sdo:geo
""")

# Collision scenario: user declares 'foaf' for a custom namespace AND 'myfoaf'
# for http://xmlns.com/foaf/0.1/.  Normalisation must NOT clobber the user's 'foaf'.
# Uses 'foaf' instead of 'schema' because 'schema' is declared in linkml:types,
# which causes a SchemaLoader merge conflict before normalisation even runs.
SCHEMA_COLLISION = textwrap.dedent("""\
    id: https://example.org/test
    name: test_collision
    default_prefix: ex
    prefixes:
      ex: https://example.org/
      linkml: https://w3id.org/linkml/
      foaf: https://something-else.org/
      myfoaf: http://xmlns.com/foaf/0.1/
    imports:
      - linkml:types
    classes:
      Agent:
        class_uri: myfoaf:Agent
        attributes:
          label:
            range: string
            slot_uri: myfoaf:name
""")


def _write_schema(tmp_path, content: str, name: str = "schema.yaml") -> str:
    """Write schema content to a temporary file and return its path as string."""
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return str(p)


def _turtle_prefixes(ttl: str) -> dict[str, str]:
    """Extract @prefix declarations from Turtle output → {prefix: namespace}."""
    result = {}
    for m in re.finditer(r"@prefix\s+(\w+):\s+<([^>]+)>", ttl):
        result[m.group(1)] = m.group(2)
    return result


# ── OWL Generator Tests ─────────────────────────────────────────────


def test_owl_sdo_normalised_to_schema(tmp_path):
    """sdo → schema when --normalize-prefixes is active."""
    from linkml.generators.owlgen import OwlSchemaGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_SDO)
    ttl = OwlSchemaGenerator(schema_path, normalize_prefixes=True).serialize()
    pfx = _turtle_prefixes(ttl)
    assert "schema" in pfx, f"Expected 'schema' prefix in OWL output, got: {sorted(pfx)}"
    assert pfx["schema"] == "https://schema.org/"
    assert "sdo" not in pfx, "Non-standard 'sdo' prefix should be removed"


def test_owl_flag_off_preserves_original(tmp_path):
    """Without the flag, schema-declared prefix names are preserved."""
    from linkml.generators.owlgen import OwlSchemaGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_SDO)
    ttl = OwlSchemaGenerator(schema_path, normalize_prefixes=False).serialize()
    pfx = _turtle_prefixes(ttl)
    assert "sdo" in pfx, "With flag off, original prefix 'sdo' must be preserved"


def test_owl_dce_normalised_to_dc(tmp_path):
    """dce → dc for http://purl.org/dc/elements/1.1/ in graph bindings.

    Note: rdflib's Turtle serializer only emits @prefix declarations for
    namespaces actually used in triples.  Since the OWL generator may not
    produce triples using dc:elements URIs for simple attribute schemas,
    we verify the graph's namespace bindings directly.
    """
    from linkml.generators.owlgen import OwlSchemaGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_DCE)
    gen = OwlSchemaGenerator(schema_path, normalize_prefixes=True)
    graph = gen.as_graph()
    bound = {str(p): str(n) for p, n in graph.namespaces()}
    assert "dc" in bound, f"Expected 'dc' in graph bindings, got: {sorted(bound)}"
    assert bound["dc"] == "http://purl.org/dc/elements/1.1/"


def test_owl_custom_prefix_not_affected(tmp_path):
    """Domain-specific prefixes (e.g. 'ex') are not touched by normalisation."""
    from linkml.generators.owlgen import OwlSchemaGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_SDO)
    ttl = OwlSchemaGenerator(schema_path, normalize_prefixes=True).serialize()
    pfx = _turtle_prefixes(ttl)
    assert "ex" in pfx, "Custom prefix 'ex' must survive normalisation"
    assert pfx["ex"] == "https://example.org/"


def test_owl_http_schema_org_normalised(tmp_path):
    """http://schema.org/ (HTTP variant) also normalises to 'schema'.

    The linkml-runtime historically binds ``schema: http://schema.org/``
    while the W3C and rdflib prefer ``https://schema.org/``.  Both
    variants must be recognised by the static well-known prefix map.
    """
    from linkml.generators.owlgen import OwlSchemaGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_HTTP_SDO)
    ttl = OwlSchemaGenerator(schema_path, normalize_prefixes=True).serialize()
    pfx = _turtle_prefixes(ttl)
    assert "schema" in pfx, f"Expected 'schema' prefix for http://schema.org/, got: {sorted(pfx)}"
    assert "sdo" not in pfx


def test_owl_no_schema1_from_runtime_http_binding(tmp_path):
    """Runtime-injected ``schema: http://schema.org/`` must not create ``schema1``.

    The linkml metamodel (types.yaml) declares ``schema: http://schema.org/``
    (HTTP).  When a user schema declares ``sdo: https://schema.org/`` (HTTPS),
    normalisation must clean up *both* variants so the output never contains
    auto-generated suffixed prefixes like ``schema1``.
    """
    from linkml.generators.owlgen import OwlSchemaGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_SDO)
    ttl = OwlSchemaGenerator(schema_path, normalize_prefixes=True).serialize()
    pfx = _turtle_prefixes(ttl)
    suffixed = [p for p in pfx if re.match(r"schema\d+", p)]
    assert not suffixed, (
        f"Auto-generated suffixed prefix(es) {suffixed} found — runtime http://schema.org/ binding was not cleaned up"
    )


# ── SHACL Generator Tests ───────────────────────────────────────────


def test_shacl_sdo_normalised_to_schema(tmp_path):
    """sdo → schema when --normalize-prefixes is active."""
    from linkml.generators.shaclgen import ShaclGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_SDO)
    ttl = ShaclGenerator(schema_path, normalize_prefixes=True).serialize()
    pfx = _turtle_prefixes(ttl)
    assert "schema" in pfx, f"Expected 'schema' prefix in SHACL output, got: {sorted(pfx)}"
    assert pfx["schema"] == "https://schema.org/"
    assert "sdo" not in pfx, "Non-standard 'sdo' prefix should be removed"


def test_shacl_flag_off_preserves_original(tmp_path):
    """Without the flag, schema-declared prefix names are preserved."""
    from linkml.generators.shaclgen import ShaclGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_SDO)
    ttl = ShaclGenerator(schema_path, normalize_prefixes=False).serialize()
    pfx = _turtle_prefixes(ttl)
    assert "sdo" in pfx, "With flag off, original prefix 'sdo' must be preserved"


def test_shacl_dce_normalised_to_dc(tmp_path):
    """dce → dc for http://purl.org/dc/elements/1.1/."""
    from linkml.generators.shaclgen import ShaclGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_DCE)
    ttl = ShaclGenerator(schema_path, normalize_prefixes=True).serialize()
    pfx = _turtle_prefixes(ttl)
    assert "dc" in pfx, f"Expected 'dc' prefix in SHACL output, got: {sorted(pfx)}"
    assert pfx["dc"] == "http://purl.org/dc/elements/1.1/"
    assert "dce" not in pfx, "Non-standard 'dce' prefix should be removed"


def test_shacl_custom_prefix_not_affected(tmp_path):
    """Domain-specific prefixes (e.g. 'ex') are not touched by normalisation.

    Note: rdflib only emits @prefix for namespaces used in triples.
    We verify graph bindings directly.
    """
    from linkml.generators.shaclgen import ShaclGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_SDO)
    gen = ShaclGenerator(schema_path, normalize_prefixes=True)
    graph = gen.as_graph()
    bound = {str(p): str(n) for p, n in graph.namespaces()}
    assert "ex" in bound, f"Custom prefix 'ex' must survive in graph bindings, got: {sorted(bound)}"
    assert bound["ex"] == "https://example.org/"


def test_shacl_http_schema_org_normalised(tmp_path):
    """http://schema.org/ (HTTP variant) also normalises to 'schema'."""
    from linkml.generators.shaclgen import ShaclGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_HTTP_SDO)
    ttl = ShaclGenerator(schema_path, normalize_prefixes=True).serialize()
    pfx = _turtle_prefixes(ttl)
    assert "schema" in pfx, f"Expected 'schema' prefix for http://schema.org/, got: {sorted(pfx)}"
    assert "sdo" not in pfx


def test_shacl_no_schema1_from_runtime_http_binding(tmp_path):
    """Runtime-injected ``schema: http://schema.org/`` must not create ``schema1``.

    Same scenario as the OWL test: linkml:types imports bring in
    ``schema: http://schema.org/`` while the user schema has
    ``sdo: https://schema.org/``.  Phase 2 of normalisation must
    clean up the orphaned HTTP binding.
    """
    from linkml.generators.shaclgen import ShaclGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_SDO)
    ttl = ShaclGenerator(schema_path, normalize_prefixes=True).serialize()
    pfx = _turtle_prefixes(ttl)
    suffixed = [p for p in pfx if re.match(r"schema\d+", p)]
    assert not suffixed, (
        f"Auto-generated suffixed prefix(es) {suffixed} found — runtime http://schema.org/ binding was not cleaned up"
    )


# ── JSON-LD Context Generator Tests ─────────────────────────────────


def test_context_http_schema_org_normalised(tmp_path):
    """http://schema.org/ (HTTP variant) normalises to 'schema' in JSON-LD context.

    This covers the edge case where linkml-runtime's ``schema: http://schema.org/``
    conflicts with rdflib's ``schema: https://schema.org/``.  The stale binding
    must be removed and replaced with the correct one.
    """
    from linkml.generators.jsonldcontextgen import ContextGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_HTTP_SDO)
    ctx = json.loads(ContextGenerator(schema_path, normalize_prefixes=True).serialize())["@context"]
    assert "schema" in ctx, "HTTP schema.org should normalise to 'schema'"
    assert "sdo" not in ctx, "Non-standard 'sdo' should be removed"
    # The namespace URI must match the schema-declared one (http, not https)
    schema_val = ctx["schema"]
    if isinstance(schema_val, dict):
        schema_val = schema_val.get("@id", "")
    assert schema_val == "http://schema.org/", f"Namespace URI must be preserved: got {schema_val}"


# ── Static Prefix Map Tests ─────────────────────────────────────────


def test_well_known_prefix_map_returns_dict():
    from linkml.utils.generator import well_known_prefix_map

    wk = well_known_prefix_map()
    assert isinstance(wk, dict)
    assert len(wk) >= 29, f"Expected ≥29 entries, got {len(wk)}"


def test_well_known_prefix_map_schema_https():
    from linkml.utils.generator import well_known_prefix_map

    wk = well_known_prefix_map()
    assert wk["https://schema.org/"] == "schema"


def test_well_known_prefix_map_schema_http_variant():
    """Both http and https schema.org must map to 'schema'."""
    from linkml.utils.generator import well_known_prefix_map

    wk = well_known_prefix_map()
    assert wk["http://schema.org/"] == "schema"


def test_well_known_prefix_map_dc_elements():
    from linkml.utils.generator import well_known_prefix_map

    wk = well_known_prefix_map()
    assert wk["http://purl.org/dc/elements/1.1/"] == "dc"


def test_well_known_prefix_map_returns_copy():
    """Callers should not be able to mutate the internal map."""
    from linkml.utils.generator import well_known_prefix_map

    wk1 = well_known_prefix_map()
    wk1["http://example.org/"] = "test"
    wk2 = well_known_prefix_map()
    assert "http://example.org/" not in wk2


def test_well_known_prefix_map_matches_rdflib_defaults():
    """The static map must be a superset of rdflib's current defaults.

    This test documents the relationship: if rdflib adds new defaults in
    a future version, this test will flag them for inclusion.
    """
    from rdflib import Graph as RdfGraph

    from linkml.utils.generator import well_known_prefix_map

    wk = well_known_prefix_map()
    rdflib_map = {str(ns): str(pfx) for pfx, ns in RdfGraph().namespaces() if str(pfx)}
    missing = {ns: pfx for ns, pfx in rdflib_map.items() if ns not in wk}
    assert not missing, f"Static map missing rdflib defaults: {missing}"


# ── Cross-Generator Consistency Tests ────────────────────────────────


def test_all_generators_normalise_sdo_to_schema(tmp_path):
    """OWL, SHACL, and JSON-LD context must all use 'schema' for schema.org."""
    from linkml.generators.jsonldcontextgen import ContextGenerator
    from linkml.generators.owlgen import OwlSchemaGenerator
    from linkml.generators.shaclgen import ShaclGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_SDO)

    owl_ttl = OwlSchemaGenerator(schema_path, normalize_prefixes=True).serialize()
    shacl_ttl = ShaclGenerator(schema_path, normalize_prefixes=True).serialize()
    ctx = json.loads(ContextGenerator(schema_path, normalize_prefixes=True).serialize())["@context"]

    owl_pfx = _turtle_prefixes(owl_ttl)
    shacl_pfx = _turtle_prefixes(shacl_ttl)

    assert "schema" in owl_pfx, "OWL must use 'schema'"
    assert "schema" in shacl_pfx, "SHACL must use 'schema'"
    assert "schema" in ctx, "JSON-LD context must use 'schema'"

    assert "sdo" not in owl_pfx, "OWL must not have 'sdo'"
    assert "sdo" not in shacl_pfx, "SHACL must not have 'sdo'"
    assert "sdo" not in ctx, "JSON-LD context must not have 'sdo'"


# ── Prefix Collision Tests ────────────────────────────────────────────


@pytest.mark.parametrize(
    "generator_cls,generator_module",
    [
        ("OwlSchemaGenerator", "linkml.generators.owlgen"),
        ("ShaclGenerator", "linkml.generators.shaclgen"),
    ],
    ids=["owl", "shacl"],
)
def test_graph_generator_collision_skips_rename(tmp_path, caplog, generator_cls, generator_module):
    """Graph generators: myfoaf must NOT be renamed to 'foaf' when user claims that name."""
    import importlib

    mod = importlib.import_module(generator_module)
    cls = getattr(mod, generator_cls)

    schema_path = _write_schema(tmp_path, SCHEMA_COLLISION)
    with caplog.at_level(logging.WARNING):
        gen = cls(schema_path, normalize_prefixes=True)
        graph = gen.as_graph()
    bound = {str(p): str(n) for p, n in graph.namespaces()}
    assert "myfoaf" in bound, "Non-standard 'myfoaf' must remain when collision prevents renaming"
    assert bound["myfoaf"] == "http://xmlns.com/foaf/0.1/"
    assert "collision" in caplog.text.lower(), f"Expected collision warning, got: {caplog.text}"


def test_context_collision_preserves_user_prefix(tmp_path, caplog):
    """JSON-LD: user's 'foaf: https://something-else.org/' must survive."""
    from linkml.generators.jsonldcontextgen import ContextGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_COLLISION)
    with caplog.at_level(logging.WARNING):
        ctx = json.loads(ContextGenerator(schema_path, normalize_prefixes=True).serialize())["@context"]
    # User's 'foaf' binding preserved
    foaf_val = ctx.get("foaf")
    if isinstance(foaf_val, dict):
        foaf_val = foaf_val.get("@id", "")
    assert foaf_val == "https://something-else.org/", f"User's 'foaf' binding must be preserved, got: {foaf_val}"
    # myfoaf must remain (not renamed to foaf)
    assert "myfoaf" in ctx, "Non-standard 'myfoaf' must remain when collision prevents renaming"
    # Warning emitted
    assert "collision" in caplog.text.lower(), f"Expected collision warning, got: {caplog.text}"


# ── JSONLDGenerator Flag Forwarding Tests ─────────────────────────────


def test_jsonld_generator_forwards_normalize_prefixes(tmp_path):
    """JSONLDGenerator must pass normalize_prefixes to embedded ContextGenerator.

    Without forwarding, the inline @context in JSON-LD output would keep
    non-standard prefix aliases even when --normalize-prefixes is set.
    """
    from linkml.generators.jsonldgen import JSONLDGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_SDO)
    out = JSONLDGenerator(schema_path, normalize_prefixes=True).serialize()
    parsed = json.loads(out)
    # The @context may be a list; find the dict entry
    ctx = parsed.get("@context", {})
    if isinstance(ctx, list):
        for item in ctx:
            if isinstance(item, dict):
                ctx = item
                break
    assert "sdo" not in ctx, "normalize_prefixes not forwarded: 'sdo' still in embedded @context"


# ── Phase 2 HTTP/HTTPS Overwrite Bug Tests ────────────────────────────


def test_phase2_does_not_overwrite_https_with_http(tmp_path):
    """When Phase 1 binds schema → https://schema.org/, Phase 2 must not
    overwrite it with http://schema.org/ from the runtime metamodel.

    Reproduction: linkml:types imports bring schema: http://schema.org/
    (HTTP) while the user schema has sdo: https://schema.org/ (HTTPS).
    Phase 1 normalises sdo → schema (HTTPS).  Phase 2 must not then
    rebind schema → http://schema.org/ when it encounters the runtime
    HTTP binding.
    """
    from linkml.generators.owlgen import OwlSchemaGenerator

    schema_path = _write_schema(tmp_path, SCHEMA_SDO)
    gen = OwlSchemaGenerator(schema_path, normalize_prefixes=True)
    graph = gen.as_graph()
    bound = {str(p): str(n) for p, n in graph.namespaces()}
    assert "schema" in bound, f"Expected 'schema' in bindings, got: {sorted(bound)}"
    # MUST be HTTPS (from the user's schema), not HTTP (from runtime)
    assert bound["schema"] == "https://schema.org/", (
        f"Phase 2 overwrote HTTPS with HTTP: schema bound to {bound['schema']}"
    )


def test_normalize_graph_prefixes_phase2_guard():
    """Direct unit test for the Phase 2 guard in normalize_graph_prefixes.

    Simulates the exact scenario: Phase 1 binds schema → https://schema.org/,
    then Phase 2 encounters schema1 → http://schema.org/ and must NOT rebind.
    """
    from rdflib import Graph, Namespace, URIRef

    from linkml.utils.generator import normalize_graph_prefixes

    g = Graph(bind_namespaces="none")
    # Simulate Phase 1 result
    g.bind("schema", Namespace("https://schema.org/"))
    # Simulate runtime-injected HTTP variant (would appear as schema1)
    g.bind("schema1", Namespace("http://schema.org/"))
    # Add a triple so the graph isn't empty
    g.add((URIRef("https://example.org/s"), URIRef("https://schema.org/name"), URIRef("https://example.org/o")))

    normalize_graph_prefixes(g, {"sdo": "https://schema.org/"})

    bound = {str(p): str(n) for p, n in g.namespaces()}
    assert bound.get("schema") == "https://schema.org/", f"Phase 2 guard failed: schema bound to {bound.get('schema')}"


def test_empty_schema_no_crash(tmp_path):
    """A schema with no custom prefixes must not crash normalize_graph_prefixes."""
    from linkml.generators.owlgen import OwlSchemaGenerator

    (tmp_path / "empty.yaml").write_text(
        textwrap.dedent("""\
            id: https://example.org/empty
            name: empty
            default_prefix: ex
            prefixes:
              linkml: https://w3id.org/linkml/
              ex: https://example.org/
            imports:
              - linkml:types
        """),
        encoding="utf-8",
    )
    # Should not raise
    gen = OwlSchemaGenerator(str(tmp_path / "empty.yaml"), normalize_prefixes=True)
    ttl = gen.serialize()
    assert len(ttl) > 0
