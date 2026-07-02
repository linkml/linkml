"""Tests for ``rdf:List`` serialization of ordered multivalued slots.

When a multivalued slot declares ``list_elements_ordered: true`` the RDF dumper
emits an ``rdf:List`` (``rdf:first``/``rdf:rest``) instead of flat triples, so that
element order becomes part of the RDF semantics and survives canonicalization.
The loader reads such lists back into an ordered Python list.

See https://github.com/linkml/linkml/issues/3531
"""

from pathlib import Path

import pytest
from rdflib import Graph, URIRef
from rdflib.namespace import RDF

from linkml_runtime.dumpers.rdflib_dumper import RDFLibDumper
from linkml_runtime.loaders.rdflib_loader import RDFLibLoader
from linkml_runtime.utils.schemaview import SchemaView
from tests.linkml_runtime.test_loaders_dumpers.models import ordered_list as model

SCHEMA = Path(__file__).parent / "models" / "ordered_list.yaml"

SCOPE_URI = URIRef("http://example.org/scope")
SCOPE = ["latitude", "longitude", "easting", "northing", "depth", "sampling_notes"]
# deliberately not in lexical order, so a canonicalizing sort would reorder them
ITEM_NAMES = ["ex:zeta", "ex:mu", "ex:alpha"]


@pytest.fixture
def schemaview() -> SchemaView:
    return SchemaView(str(SCHEMA))


@pytest.fixture
def dumper() -> RDFLibDumper:
    return RDFLibDumper()


@pytest.fixture
def loader() -> RDFLibLoader:
    return RDFLibLoader()


def _graph(ttl: str) -> Graph:
    g = Graph()
    g.parse(data=ttl, format="turtle")
    return g


def test_ordered_literals_emit_rdf_list(schemaview, dumper):
    """An ordered literal slot is serialized as an ``rdf:List``, not flat triples."""
    obj = model.ColumnDesc(atom="ex:sampled_data", scope=SCOPE)
    g = _graph(dumper.dumps(obj, schemaview=schemaview))
    # exactly one rdf:first per element, terminating in rdf:nil
    assert len(list(g.triples((None, RDF.first, None)))) == len(SCOPE)
    assert (None, RDF.rest, RDF.nil) in g
    # the scope predicate points at a single list head, not at the values directly
    scope_objs = list(g.objects(None, RDF.first))
    assert {str(o) for o in scope_objs} == set(SCOPE)


def test_ordered_literals_round_trip_preserves_order(schemaview, dumper, loader):
    """dump -> load preserves the original (non-lexical) order of an ordered slot."""
    obj = model.ColumnDesc(atom="ex:sampled_data", scope=SCOPE)
    ttl = dumper.dumps(obj, schemaview=schemaview)
    loaded = loader.loads(ttl, target_class=model.ColumnDesc, schemaview=schemaview)
    assert loaded.scope == SCOPE


def test_canonical_output_is_stable_across_runs(schemaview, dumper):
    """The RDFC-1.0 canonicalizer yields identical output across repeated dumps."""
    obj = model.ColumnDesc(atom="ex:sampled_data", scope=SCOPE)
    assert dumper.dumps(obj, schemaview=schemaview) == dumper.dumps(obj, schemaview=schemaview)


def test_ordered_objects_round_trip_preserves_order(schemaview, dumper, loader):
    """Ordered lists of class-ranged (inlined) objects preserve order on round trip."""
    obj = model.ColumnDesc(
        atom="ex:sampled_data",
        items=[model.Item(name) for name in ITEM_NAMES],
    )
    g = _graph(dumper.dumps(obj, schemaview=schemaview))
    assert len(list(g.triples((None, RDF.first, None)))) == len(ITEM_NAMES)
    loaded = loader.loads(
        dumper.dumps(obj, schemaview=schemaview), target_class=model.ColumnDesc, schemaview=schemaview
    )
    assert [item.name for item in loaded.items] == ITEM_NAMES


@pytest.mark.parametrize(
    "scope",
    [
        pytest.param([], id="empty"),
        pytest.param(["only"], id="single"),
        pytest.param(SCOPE, id="many"),
    ],
)
def test_ordered_list_round_trip_sizes(schemaview, dumper, loader, scope):
    """Empty, single-element, and multi-element ordered lists all round trip."""
    obj = model.ColumnDesc(atom="ex:sampled_data", scope=scope)
    ttl = dumper.dumps(obj, schemaview=schemaview)
    loaded = loader.loads(ttl, target_class=model.ColumnDesc, schemaview=schemaview)
    assert loaded.scope == scope


def test_empty_ordered_list_emits_nothing(schemaview, dumper):
    """An empty ordered list emits no triples for the slot (matching unordered empties)."""
    obj = model.ColumnDesc(atom="ex:sampled_data", scope=[])
    g = _graph(dumper.dumps(obj, schemaview=schemaview))
    # no list spine and no scope arc at all
    assert list(g.triples((None, RDF.first, None))) == []
    assert list(g.triples((None, SCOPE_URI, None))) == []


def test_non_schema_none_attribute_is_skipped(schemaview, dumper):
    """A python attribute that is not a schema slot must not be resolved when it is None.

    Regression for #3531: the dumper resolves each slot once per attribute; it must skip
    value-less attributes *before* resolving, since an element can carry python attributes
    (defaults, cross-schema instances) that have no slot definition.
    """
    obj = model.ColumnDesc(atom="ex:sampled_data", scope=["latitude"])
    obj.not_a_slot = None  # present in vars() but absent from the schema
    g = _graph(dumper.dumps(obj, schemaview=schemaview))  # must not raise
    assert list(g.triples((None, SCOPE_URI, None)))  # real slot still emitted


def test_unordered_slot_stays_flat(schemaview, dumper):
    """A multivalued slot without ``list_elements_ordered`` keeps flat-triple output."""
    obj = model.ColumnDesc(atom="ex:sampled_data", tags=["b", "a", "c"])
    g = _graph(dumper.dumps(obj, schemaview=schemaview))
    assert list(g.triples((None, RDF.first, None))) == []
    tag_values = {str(o) for o in g.objects() if str(o) in {"a", "b", "c"}}
    assert tag_values == {"a", "b", "c"}


def test_ordered_inlined_as_dict_round_trip_preserves_order(schemaview, dumper, loader):
    """Ordered inlined-as-dict slots also serialize as an ``rdf:List`` and preserve order.

    Regression for the dict form of #3531: the dumper previously gated the ``rdf:List``
    branch on ``isinstance(v_or_list, list)``, so a dict-backed collection fell through to
    flat, order-losing triples -- even though the loader and ``gen-shacl`` already treat
    the same slot as ordered.
    """
    obj = model.ColumnDesc(
        atom="ex:sampled_data",
        items_by_id=[model.Item(name) for name in ITEM_NAMES],
    )
    g = _graph(dumper.dumps(obj, schemaview=schemaview))
    # emitted as an rdf:List (one rdf:first per element), not flat triples
    assert len(list(g.triples((None, RDF.first, None)))) == len(ITEM_NAMES)
    loaded = loader.loads(
        dumper.dumps(obj, schemaview=schemaview), target_class=model.ColumnDesc, schemaview=schemaview
    )
    assert [item.name for item in loaded.items_by_id.values()] == ITEM_NAMES
