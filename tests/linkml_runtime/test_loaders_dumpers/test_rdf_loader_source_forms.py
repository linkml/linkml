"""Reproduction tests for RDFLoader.

``RDFLoader.load`` documents its ``source`` as "a URL, a file name, an RDF string, an open
handle or an existing graph", and accepts a ``contexts`` argument to shape the result into
``target_class``. None of that currently works: every source form raises, and ``contexts`` is
never read.

**These tests are expected to FAIL.** Each asserts the *documented* behaviour, so each one
fails. They are left un-``xfail``-ed - to show failure - they turn green as loader is fixed.

The only existing coverage, ``test_loaders.py::test_rdf_loader``, cannot catch any of this: it
is disabled with an unconditional ``@pytest.mark.skip``, also needing the local docker.
These tests read the context from the local fixture tree instead.
"""

from pathlib import Path

from pydantic import BaseModel
from rdflib import Graph

from linkml_runtime.loaders import RDFLoader
from tests.linkml_runtime.test_loaders_dumpers import INPUT_DIR, LD_11_DIR
from tests.linkml_runtime.test_loaders_dumpers.models.termci_schema import Package

TTL_FILE = str(Path(INPUT_DIR) / "obo_sample.ttl")
JSONLD_FILE = str(Path(INPUT_DIR) / "obo_sample.jsonld")
CONTEXT_FILE = str(Path(LD_11_DIR) / "termci_schema_inlined.context.jsonld")

# obo_sample.ttl holds one ConceptSystem (the OBO namespace) with two concepts
EXPECTED_NAMESPACE = "http://purl.obolibrary.org/obo/"
EXPECTED_PREFIX = "OBO"
EXPECTED_CODES = {"C147557", "C147796"}


def assert_obo_sample(package: object) -> None:
    """Assert the loaded object is the Package that obo_sample.ttl describes.

    Checking the slot values (not just the type) is what catches an unapplied ``contexts``:
    without a context the graph keeps full predicate URIs as keys, so no slot is populated.
    """
    assert isinstance(package, Package)
    assert len(package.system) == 1
    system = package.system[0]
    assert system.namespace == EXPECTED_NAMESPACE
    assert system.prefix == EXPECTED_PREFIX
    assert {concept.code for concept in system.contents} == EXPECTED_CODES


# FAILS WITH: NameError: name 'json' is not defined - json is never imported
def test_load_from_file_name_turtle():
    """A turtle file name is the most basic documented source form."""
    assert_obo_sample(RDFLoader().load(TTL_FILE, Package, contexts=CONTEXT_FILE, fmt="turtle"))


# FAILS WITH: NameError: name 'json' is not defined - json is never imported
def test_load_from_rdf_string_turtle():
    """An RDF string is a documented source form."""
    rdf = Path(TTL_FILE).read_text()
    assert_obo_sample(RDFLoader().load(rdf, Package, contexts=CONTEXT_FILE, fmt="turtle"))


# FAILS WITH: NameError: name 'json' is not defined - json is never imported
def test_load_from_open_handle_turtle():
    """An open file handle is a documented source form."""
    with Path(TTL_FILE).open() as handle:
        assert_obo_sample(RDFLoader().load(handle, Package, contexts=CONTEXT_FILE, fmt="turtle"))


# FAILS WITH: AttributeError: 'str' object has no attribute 'pop' - a json-ld string is never
#   json.loads()ed, because the `isinstance(data, str)` branch only parses when fmt != 'json-ld'
def test_load_from_file_name_jsonld():
    """fmt='json-ld' needs no RDF parsing, yet it is the form that breaks soonest.

    NOTE: this one needs a fixture fix as well as a loader fix. ``obo_sample.jsonld`` and
    ``obo_sample.ttl`` are meant to be the same data, but the root node is typed
    ``termci:Package`` in the turtle and ``termci:dict`` in the JSON-LD. ``termci:dict`` is not
    a class in the termci schema, so nothing can select that node by type. Repairing the loader
    leaves this failing with ``TypeError: Package.__init__() got an unexpected keyword argument
    'http://www.w3.org/2004/02/skos/core#broader'``, because the loader falls back to the first
    node in the graph - a skos:Concept.
    """
    assert_obo_sample(RDFLoader().load(JSONLD_FILE, Package, contexts=CONTEXT_FILE, fmt="json-ld"))


# FAILS WITH: NameError: name 'pyld_jsonld_from_rdflib_graph' is not defined - the helper is called but
#   never defined or imported (linkml#3722)
def test_load_from_rdflib_graph():
    """An existing rdflib Graph is a documented source form.

    This is the path reported in linkml#3722. No test has ever exercised it, which is why the
    undefined name survived.
    """
    graph = Graph()
    graph.parse(TTL_FILE, format="turtle")
    assert_obo_sample(RDFLoader().load(graph, Package, contexts=CONTEXT_FILE))


# FAILS WITH: AttributeError: class_name - the type check reads target_class.class_name, which only exists
#   on generated YAMLRoot dataclasses, never on pydantic BaseModel targets
def test_load_into_pydantic_basemodel_target():
    """``target_class`` is typed ``type[BaseModel | YAMLRoot]``, so BaseModel must work.

    A dict source is used to reach the type check directly, past the source-parsing bugs above.
    """

    class PydanticPackage(BaseModel):
        marker: str = ""

    source = {"@type": "https://hotecosystem.org/termci/Package", "marker": "loaded"}
    result = RDFLoader().load(source, PydanticPackage, fmt="json-ld")
    assert isinstance(result, PydanticPackage)
    assert result.marker == "loaded"


# FAILS WITH: AttributeError: 'str' object has no attribute 'pop' - the json-ld string is never parsed,
#   which masks the graph-array bug behind it: once the parsing and NameError bugs are fixed this input
#   instead raises TypeError: pop expected at most 1 argument, got 2, because both arms of the `if not
#   isinstance(data, dict)` guard assign `data` unchanged, so a list reaches list.pop('@type', None)
def test_load_graph_array_without_contexts():
    """A graph array must be reduced to the target class's node even with no ``contexts``.

    The graph-array defect cannot be observed in isolation on an unfixed tree - every route to
    it (turtle parsing, json-ld parsing) raises first. That layering is why the one-line #3722
    fix was not the end of it.
    """
    source = """[
      {"@id": "_:b0", "@type": "https://hotecosystem.org/termci/Other", "system": {}},
      {"@id": "_:b1", "@type": "https://hotecosystem.org/termci/Package",
       "system": {"http://example.org/ns1": {"namespace": "http://example.org/ns1", "prefix": "ex"}}}
    ]"""
    result = RDFLoader().load(source, Package, fmt="json-ld")
    assert isinstance(result, Package)
    assert [system.namespace for system in result.system] == ["http://example.org/ns1"]
