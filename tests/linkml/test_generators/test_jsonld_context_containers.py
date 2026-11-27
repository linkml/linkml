"""``--fix-multivalue-containers`` gives each multivalued slot the JSON-LD container that keeps its data.

- A slot inlined as a dict keyed by the range's ``identifier`` is an id map
  (JSON-LD 1.1 §4.6.3): each key is the IRI of its node.
- A slot inlined as a dict keyed by the range's ``key`` is a property-based index
  map (§4.6.1.1): each key is the value of the key slot.
- A slot with ``list_elements_ordered`` is a list (§4.3.1), which keeps the order.
- Any other multivalued slot is a set.

Without the option no container is emitted.
"""

import json

import pytest
from rdflib import RDF, Graph, Literal, URIRef
from rdflib.collection import Collection

from linkml.generators.jsonldcontextgen import ContextGenerator

EX = "https://example.org/"

SCHEMA = """
id: https://example.org/d
name: d
prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/
imports: [linkml:types]
default_prefix: ex
default_range: string
slots:
  id:
    identifier: true
  code:
    key: true
  name:
  tags:
    multivalued: true
  steps:
    multivalued: true
    list_elements_ordered: true
  people_dict:
    range: Person
    multivalued: true
    inlined: true
    inlined_as_list: false
  people_list:
    range: Person
    multivalued: true
    inlined_as_list: true
  codes_dict:
    range: Coded
    multivalued: true
    inlined: true
    inlined_as_list: false
  ordered_people_dict:
    range: Person
    multivalued: true
    inlined: true
    inlined_as_list: false
    list_elements_ordered: true
classes:
  Person:
    slots: [id, name]
  Coded:
    slots: [code, name]
  Container:
    slots: [id, tags, steps, people_dict, people_list, codes_dict, ordered_people_dict]
"""


def _context(**kwargs) -> dict:
    return json.loads(ContextGenerator(SCHEMA, **kwargs).serialize())["@context"]


@pytest.mark.parametrize(
    "slot,container",
    [
        ("tags", {"@container": "@set"}),
        ("steps", {"@container": "@list"}),
        ("people_list", {"@container": "@set"}),
        ("people_dict", {"@container": "@id"}),
        ("ordered_people_dict", {"@container": "@id"}),
        ("codes_dict", {"@container": "@index", "@index": EX + "code"}),
    ],
)
def test_container(slot, container):
    """Each multivalued slot gets the container for its form."""
    term = _context(fix_multivalue_containers=True)[slot]
    assert {k: v for k, v in term.items() if k in ("@container", "@index")} == container


@pytest.mark.parametrize("slot", ["tags", "steps", "people_list", "people_dict", "codes_dict"])
def test_no_container_without_the_option(slot):
    """The default output has no containers."""
    term = _context()[slot]
    assert "@container" not in term
    assert "@index" not in term


def _graph(data: dict) -> Graph:
    """Parse *data* as JSON-LD with the generated context."""
    doc = {"@context": _context(fix_multivalue_containers=True), "id": "ex:c1", **data}
    return Graph().parse(data=json.dumps(doc), format="json-ld")


def test_id_map_keeps_identifiers():
    """The keys of a dict keyed by identifier are the IRIs of the nodes."""
    graph = _graph({"people_dict": {"ex:P1": {"name": "Alice"}}})
    assert (URIRef(EX + "c1"), URIRef(EX + "people_dict"), URIRef(EX + "P1")) in graph
    assert (URIRef(EX + "P1"), URIRef(EX + "name"), Literal("Alice")) in graph


def test_index_map_keeps_keys():
    """The keys of a dict keyed by a key slot are the values of that slot."""
    graph = _graph({"codes_dict": {"A1": {"name": "first"}}})
    (node,) = graph.objects(URIRef(EX + "c1"), URIRef(EX + "codes_dict"))
    assert (node, URIRef(EX + "code"), Literal("A1")) in graph
    assert (node, URIRef(EX + "name"), Literal("first")) in graph


def test_list_keeps_order():
    """An ordered slot is an RDF list in the order of the data."""
    graph = _graph({"steps": ["b", "a"]})
    (head,) = graph.objects(URIRef(EX + "c1"), URIRef(EX + "steps"))
    assert (head, RDF.first, None) in graph
    assert list(Collection(graph, head)) == [Literal("b"), Literal("a")]
