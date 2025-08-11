import logging
from pathlib import Path

import pytest
from curies import Converter
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, SKOS, XSD

from linkml_runtime import DataNotFoundError, MappingError
from linkml_runtime.dumpers import rdflib_dumper, yaml_dumper
from linkml_runtime.linkml_model import Prefix
from linkml_runtime.loaders import rdflib_loader, yaml_loader
from linkml_runtime.utils.schemaview import SchemaView
from tests.test_loaders_dumpers import INPUT_DIR, OUTPUT_DIR
from tests.test_loaders_dumpers.models.node_object import NodeObject, Triple
from tests.test_loaders_dumpers.models.personinfo import Address, Container, Organization, OrganizationType, Person
from tests.test_loaders_dumpers.models.personinfo_test_issue_429 import Container as Container_429
from tests.test_loaders_dumpers.models.phenopackets import (
    MetaData,
    OntologyClass,
    Phenopacket,
    PhenotypicFeature,
    Resource,
)

logger = logging.getLogger(__name__)


INPUT_PATH = Path(INPUT_DIR)
OUTPUT_PATH = Path(OUTPUT_DIR)

SCHEMA = INPUT_PATH / "personinfo.yaml"
DATA = INPUT_PATH / "example_personinfo_data.yaml"
DATA_TTL = INPUT_PATH / "example_personinfo_data.ttl"
OUT = OUTPUT_PATH / "example_personinfo_data.ttl"
DATA_ROUNDTRIP = OUTPUT_PATH / "example_personinfo_data.roundtrip-rdf.yaml"
UNMAPPED_ROUNDTRIP = OUTPUT_PATH / "example_personinfo_data.unmapped-preds.yaml"

# Test TTL files
UNMAPPED_PREDICATES_TTL = INPUT_PATH / "unmapped_predicates_test.ttl"
UNMAPPED_TYPE_TTL = INPUT_PATH / "unmapped_type_test.ttl"
ENUM_UNION_TYPE_TTL = INPUT_PATH / "enum_union_type_test.ttl"
BLANK_NODE_TTL = INPUT_PATH / "blank_node_test.ttl"


# see https://github.com/linkml/linkml/issues/429
SCHEMA_429 = INPUT_PATH / "personinfo_test_issue_429.yaml"
DATA_429 = INPUT_PATH / "example_personinfo_test_issue_429_data.yaml"
OUT_429 = OUTPUT_PATH / "example_personinfo_test_issue_429_data.ttl"

ORCID = Namespace("https://orcid.org/")
personinfo = Namespace("https://w3id.org/linkml/examples/personinfo/")
SDO = Namespace("http://schema.org/")

PREFIX_MAP = {
    "CODE": "http://example.org/code/",
    "ROR": "http://example.org/ror/",
    "P": "http://example.org/P/",
    "GEO": "http://example.org/GEO/",
}


P = Namespace("http://example.org/P/")
ROR = Namespace("http://example.org/ror/")
CODE = Namespace("http://example.org/code/")
INFO = Namespace("https://w3id.org/linkml/examples/personinfo/")
SDO = Namespace("http://schema.org/")
GSSO = Namespace("http://purl.obolibrary.org/obo/GSSO_")
HP = Namespace("http://purl.obolibrary.org/obo/HP_")
SYMP = Namespace("http://purl.obolibrary.org/obo/SYMP_")
WD = Namespace("http://www.wikidata.org/entity/")


@pytest.fixture
def issue_429_graph():
    """Create RDF graph for issue 429 testing."""
    view = SchemaView(str(SCHEMA_429))
    container = yaml_loader.load(str(DATA_429), target_class=Container_429)
    rdflib_dumper.dump(container, schemaview=view, to_file=str(OUT_429))
    g = Graph()
    g.parse(str(OUT_429), format="ttl")
    return g


@pytest.mark.parametrize("prefix_map", [PREFIX_MAP, Converter.from_prefix_map(PREFIX_MAP)])
def test_rdflib_dumper(prefix_map):
    """Test the RDFLib dumper functionality."""
    view = SchemaView(str(SCHEMA))
    container = yaml_loader.load(str(DATA), target_class=Container)
    _check_objs(view, container)
    rdflib_dumper.dump(container, schemaview=view, to_file=str(OUT), prefix_map=prefix_map)
    g = Graph()
    g.parse(str(OUT), format="ttl")

    assert (P["001"], RDF.type, SDO.Person) in g
    assert (P["001"], SDO.name, Literal("fred bloggs")) in g
    assert (P["001"], SDO.email, Literal("fred.bloggs@example.com")) in g
    assert (P["001"], INFO.age_in_years, Literal(33)) in g
    assert (P["001"], SDO.gender, GSSO["000371"]) in g
    assert (P["001"], INFO.depicted_by, Literal("https://example.org/pictures/fred.jpg", datatype=XSD.anyURI)) in g
    assert (P["001"], INFO.depicted_by, Literal("https://example.org/pictures/fred.jpg", datatype=XSD.string)) not in g
    assert (CODE["D0001"], RDF.type, INFO.DiagnosisConcept) in g
    assert (CODE["D0001"], RDF.type, INFO.DiagnosisConcept) in g
    assert (CODE["D0001"], SKOS.exactMatch, HP["0002315"]) in g
    assert (CODE["D0001"], SKOS.exactMatch, WD.Q86) in g
    assert (CODE["D0001"], SKOS.exactMatch, SYMP["0000504"]) in g
    assert (CODE["D0001"], SKOS.exactMatch, Literal(HP["0002315"])) not in g
    [container] = g.subjects(RDF.type, INFO.Container)
    assert (container, INFO.organizations, ROR["1"]) in g
    assert (container, INFO.organizations, ROR["2"]) in g
    assert (container, INFO.persons, P["001"]) in g
    assert (container, INFO.persons, P["002"]) in g
    container: Container = rdflib_loader.load(str(OUT), target_class=Container, schemaview=view, prefix_map=prefix_map)
    _check_objs(view, container)


@pytest.mark.parametrize("prefix_map", [PREFIX_MAP, Converter.from_prefix_map(PREFIX_MAP)])
def test_enums(prefix_map):
    """Test enum handling in RDFLib dumper."""
    view = SchemaView(str(SCHEMA))
    org1type1 = OrganizationType("non profit")  ## no meaning declared
    org1type2 = OrganizationType("charity")  ## meaning URI is declared
    assert not org1type1.meaning
    assert org1type2.meaning
    org1 = Organization("ROR:1", categories=[org1type1, org1type2])
    print(org1.categories)
    g = rdflib_dumper.as_rdf_graph(org1, schemaview=view, prefix_map=prefix_map)
    print(g)
    cats = list(g.objects(ROR["1"], INFO["categories"]))
    print(cats)
    assert sorted(cats) == sorted([Literal("non profit"), URIRef("https://example.org/bizcodes/001")])
    orgs = rdflib_loader.from_rdf_graph(g, target_class=Organization, schemaview=view)
    assert len(orgs) == 1
    [org1x] = orgs
    catsx = org1x.categories
    print(catsx)
    assert sorted([org1type1, org1type2], key=str) == sorted(catsx, key=str)


def test_undeclared_prefix_raises_error():
    """Test that undeclared prefixes raise exceptions."""
    view = SchemaView(str(SCHEMA))
    org1 = Organization("foo")  # not a CURIE or URI
    with pytest.raises(Exception):
        rdflib_dumper.as_rdf_graph(org1, schemaview=view)
    org1 = Organization("http://example.org/foo/o1")
    rdflib_dumper.as_rdf_graph(org1, schemaview=view)


def test_base_prefix():
    """Test base prefix functionality."""
    view = SchemaView(str(SCHEMA))
    view.schema.prefixes["_base"] = Prefix("_base", "http://example.org/")
    org1 = Organization("foo")  # not a CURIE or URI
    g = rdflib_dumper.as_rdf_graph(org1, schemaview=view)
    assert (URIRef("http://example.org/foo"), RDF.type, SDO.Organization) in g


@pytest.mark.parametrize("prefix_map", [PREFIX_MAP, Converter.from_prefix_map(PREFIX_MAP)])
def test_rdflib_loader(prefix_map):
    """
    tests loading from an RDF graph
    """
    view = SchemaView(str(SCHEMA))
    container: Container = rdflib_loader.load(
        str(DATA_TTL), target_class=Container, schemaview=view, prefix_map=prefix_map
    )
    _check_objs(view, container)
    yaml_dumper.dump(container, to_file=str(DATA_ROUNDTRIP))


@pytest.mark.parametrize("prefix_map", [PREFIX_MAP, Converter.from_prefix_map(PREFIX_MAP)])
def test_unmapped_predicates(prefix_map):
    """
    By default, the presence of predicates in rdf that have no mapping to slots
    should raise a MappingError
    """
    view = SchemaView(str(SCHEMA))
    # default behavior is to raise error on unmapped predicates
    with pytest.raises(MappingError):
        rdflib_loader.load(str(UNMAPPED_PREDICATES_TTL), target_class=Person, schemaview=view, prefix_map=prefix_map)
    # called can explicitly allow unmapped predicates to be dropped
    person: Person = rdflib_loader.load(
        str(UNMAPPED_PREDICATES_TTL),
        target_class=Person,
        schemaview=view,
        prefix_map=prefix_map,
        ignore_unmapped_predicates=True,
    )
    assert person.id == "P:001"
    assert person.age_in_years == 33
    assert str(person.gender) == "cisgender man"
    yaml_dumper.dump(person, to_file=str(UNMAPPED_ROUNDTRIP))


@pytest.mark.parametrize("prefix_map", [PREFIX_MAP, Converter.from_prefix_map(PREFIX_MAP)])
def test_any_of_enum(prefix_map):
    """
    Tests https://github.com/linkml/linkml/issues/1023
    """
    view = SchemaView(str(SCHEMA))
    # default behavior is to raise error on unmapped predicates
    person = rdflib_loader.load(str(ENUM_UNION_TYPE_TTL), target_class=Person, schemaview=view, prefix_map=prefix_map)
    assert person.id == "P:001"
    assert person.age_in_years == 33
    yaml_dumper.dump(person, to_file=str(UNMAPPED_ROUNDTRIP))
    cases = [
        ("P:002", "COWORKER_OF"),
        ("P:003", "BEST_FRIEND_OF"),
    ]
    tups = []
    for r in person.has_interpersonal_relationships:
        tups.append((r.related_to, r.type))
    assert sorted(cases) == sorted(tups)


@pytest.mark.parametrize("prefix_map", [PREFIX_MAP, Converter.from_prefix_map(PREFIX_MAP)])
def test_unmapped_type(prefix_map):
    """
    If a type cannot be mapped then no objects will be returned by load/from_rdf_graph
    """
    view = SchemaView(str(SCHEMA))
    # default behavior is to raise error on unmapped predicates
    with pytest.raises(DataNotFoundError):
        rdflib_loader.load(str(UNMAPPED_TYPE_TTL), target_class=Person, schemaview=view, prefix_map=prefix_map)
    graph = Graph()
    graph.parse(str(UNMAPPED_TYPE_TTL), format="ttl")
    objs = rdflib_loader.from_rdf_graph(graph, target_class=Person, schemaview=view, prefix_map=prefix_map)
    assert len(objs) == 0


@pytest.mark.parametrize("prefix_map", [PREFIX_MAP, Converter.from_prefix_map(PREFIX_MAP)])
def test_blank_node(prefix_map):
    """
    blank nodes should be retrievable
    """
    view = SchemaView(str(SCHEMA))
    address: Address = rdflib_loader.load(
        str(BLANK_NODE_TTL),
        target_class=Address,
        schemaview=view,
        prefix_map=prefix_map,
        ignore_unmapped_predicates=True,
    )
    assert address.city == "foo city"
    ttl = rdflib_dumper.dumps(address, schemaview=view)
    print(ttl)
    g = Graph()
    g.parse(data=ttl, format="ttl")
    INFO = Namespace("https://w3id.org/linkml/examples/personinfo/")
    SDO = Namespace("http://schema.org/")
    [bn] = g.subjects(RDF.type, SDO.PostalAddress)
    assert (bn, RDF.type, SDO.PostalAddress) in g
    assert (bn, INFO.city, Literal("foo city")) in g
    assert (bn, INFO.street, Literal("1 foo street")) in g


def _check_objs(view: SchemaView, container: Container):
    """Helper function to check container objects."""
    persons = container.persons
    orgs = container.organizations.values()
    [p1] = [p for p in persons if p.id == "P:001"]
    [p2] = [p for p in persons if p.id == "P:002"]
    [o1] = [o for o in orgs if o.id == "ROR:1"]
    [o2] = [o for o in orgs if o.id == "ROR:2"]
    o1cats = [c.code.text for c in o1.categories]
    o2cats = [c.code.text for c in o2.categories]
    assert p1.name == "fred bloggs"
    assert p2.name == "joe schmö"
    assert p1.age_in_years == 33
    assert p1.gender.code.text == "cisgender man"
    assert p2.gender.code.text == "transgender man"
    assert sorted(o1cats) == sorted(["non profit", "charity"])
    assert sorted(o2cats) == sorted(["shell company"])
    p2: Person
    emp = p2.has_employment_history[0]
    assert emp.started_at_time == "2019-01-01"
    assert emp.is_current == True
    assert emp.employed_at == o1.id
    frel = p2.has_familial_relationships[0]
    assert frel.related_to == p1.id
    # TODO: check PV vs PVText
    assert str(frel.type) == "SIBLING_OF"
    med = p2.has_medical_history[0]
    assert med.in_location == "GEO:1234"
    assert med.diagnosis.id == "CODE:D0001"
    assert med.diagnosis.name == "headache"
    assert med.diagnosis.code_system == "CODE:D"


def test_edge_cases():
    """
    Tests various edge cases:

     - unprocessed triples (triples that cannot be reached via root objects)
     - mismatch between expected range categories (Type vs Class) and value (Literal vs Node)
     - complex range expressions (e.g. modeling a range as being EITHER string OR object
    """
    # schema with following characterics:
    #  - reified triples
    #  - object has a complex union range (experimental new feature)
    view = SchemaView(str(INPUT_PATH / "complex_range_example.yaml"))
    graph = Graph()
    taxon_prefix_map = {
        "NCBITaxon": "http://purl.obolibrary.org/obo/NCBITaxon_",
        "RO": "http://purl.obolibrary.org/obo/RO_",
    }
    # this graph has the following characteristics
    #  - blank nodes to represent statements
    #  - some triples not reachable from roots
    #  - implicit schema with complex ranges (rdf:object has range of either node or literal)
    graph.parse(str(INPUT_PATH / "bacteria-taxon-class.ttl"), format="ttl")
    objs = rdflib_loader.from_rdf_graph(
        graph,
        target_class=NodeObject,
        schemaview=view,
        cast_literals=False,  ## strict
        allow_unprocessed_triples=True,  ## known issue
        prefix_map=taxon_prefix_map,
    )
    [obj] = objs
    for x in obj.statements:
        assert x.subject is None
        assert x.predicate is not None
        assert x.object is not None
        logger.info(f"  x={x}")
    # ranges that are objects are contracted
    assert Triple(subject=None, predicate="rdfs:subClassOf", object="owl:Thing") in obj.statements
    assert Triple(subject=None, predicate="rdfs:subClassOf", object="NCBITaxon:1") in obj.statements
    # string ranges
    assert Triple(subject=None, predicate="rdfs:label", object="Bacteria") in obj.statements
    with pytest.raises(ValueError):
        rdflib_loader.from_rdf_graph(
            graph,
            target_class=NodeObject,
            schemaview=view,
            cast_literals=False,
            allow_unprocessed_triples=False,
            prefix_map=taxon_prefix_map,
        )
        logger.error("Passed unexpectedly: there are known to be unreachable triples")
    # removing complex range, object has a range of string
    view.schema.slots["object"].exactly_one_of = []
    view.set_modified()
    rdflib_loader.from_rdf_graph(
        graph,
        target_class=NodeObject,
        schemaview=view,
        cast_literals=True,  ## required to pass
        allow_unprocessed_triples=True,
        prefix_map=taxon_prefix_map,
    )
    with pytest.raises(ValueError):
        rdflib_loader.from_rdf_graph(
            graph,
            target_class=NodeObject,
            schemaview=view,
            cast_literals=False,
            allow_unprocessed_triples=True,
            prefix_map=taxon_prefix_map,
        )
        logger.error("Passed unexpectedly: rdf:object is known to have a mix of literals and nodes")


@pytest.mark.parametrize("prefix_map", [PREFIX_MAP, Converter.from_prefix_map(PREFIX_MAP)])
def test_phenopackets(prefix_map):
    """Test phenopackets functionality."""
    view = SchemaView(str(INPUT_PATH / "phenopackets" / "phenopackets.yaml"))
    test_label = "test label"
    with pytest.raises(ValueError):
        c = OntologyClass(id="NO_SUCH_PREFIX:1", label=test_label)
        rdflib_dumper.dumps(c, view)
    cases = [
        ("HP:1", "http://purl.obolibrary.org/obo/HP_1", None),
        (
            "FOO:1",
            "http://example.org/FOO_1",
            {"FOO": "http://example.org/FOO_", "@base": "http://example.org/base/"},
        ),
    ]
    for id, expected_uri, test_prefix_map in cases:
        c = OntologyClass(id=id, label=test_label)
        ttl = rdflib_dumper.dumps(c, view, prefix_map=test_prefix_map)
        g = Graph()
        g.parse(data=ttl, format="ttl")
        assert len(g) == 2
        assert Literal(test_label) in list(g.objects(URIRef(expected_uri))), (
            f"Expected label {test_label} for {expected_uri} in {ttl}"
        )
        pf = PhenotypicFeature(type=c)
        pkt = Phenopacket(
            id="id with spaces",
            metaData=MetaData(resources=[Resource(id="id with spaces")]),
            phenotypicFeatures=[pf],
        )
        ttl = rdflib_dumper.dumps(pkt, view, prefix_map=prefix_map)
        g = Graph()
        g.parse(data=ttl, format="ttl")
        assert Literal(test_label) in list(g.objects(URIRef(expected_uri))), (
            f"Expected label {test_label} for {expected_uri} in {ttl}"
        )
        if test_prefix_map and "@base" in test_prefix_map:
            resource_uri = URIRef(test_prefix_map["@base"] + "id%20with%20spaces")
            assert len(list(g.objects(resource_uri))) == 1


def test_rdf_output(issue_429_graph):
    """Test RDF output for issue 429."""
    g = issue_429_graph
    assert (ORCID["1234"], RDF.type, SDO.Person) in g
    assert (ORCID["1234"], personinfo.full_name, Literal("Clark Kent")) in g
    assert (ORCID["1234"], personinfo.age, Literal("32")) in g
    assert (ORCID["1234"], personinfo.phone, Literal("555-555-5555")) in g
    assert (ORCID["4567"], RDF.type, SDO.Person) in g
    assert (ORCID["4567"], personinfo.full_name, Literal("Lois Lane")) in g
    assert (ORCID["4567"], personinfo.age, Literal("33")) in g
    assert (ORCID["4567"], personinfo.phone, Literal("555-555-5555")) in g


def test_output_prefixes():
    """Test output prefixes for issue 429."""
    with open(str(OUT_429), encoding="UTF-8") as file:
        file_string = file.read()
    prefixes = ["prefix ORCID:", "prefix personinfo:", "prefix sdo:", "sdo:Person", "personinfo:age", "ORCID:1234"]
    for prefix in prefixes:
        assert prefix in file_string
