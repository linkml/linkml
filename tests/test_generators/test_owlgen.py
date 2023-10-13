from linkml_runtime.linkml_model import SlotDefinition
from rdflib import RDFS, SKOS, Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import OWL, RDF

from linkml.generators.owlgen import MetadataProfile, OwlSchemaGenerator
from linkml.utils.schema_builder import SchemaBuilder

SYMP = Namespace("http://purl.obolibrary.org/obo/SYMP_")
KS = Namespace("https://w3id.org/linkml/tests/kitchen_sink/")
LINKML = Namespace("https://w3id.org/linkml/")
BIZ = Namespace("https://example.org/bizcodes/")


def test_owlgen(kitchen_sink_path):
    """tests generation of owl schema-style ontologies"""
    owl = OwlSchemaGenerator(
        kitchen_sink_path,
        mergeimports=False,
        metaclasses=False,
        type_objects=False,
        ontology_uri_suffix=".owl.ttl",
    ).serialize()
    g = Graph()
    g.parse(data=owl, format="turtle")
    owl_classes = list(g.subjects(RDF.type, OWL.Class))
    assert len(owl_classes) > 10
    for c in owl_classes:
        types = list(g.objects(c, RDF.type))
        assert types == [OWL.Class]
    assert KS.MedicalEvent in owl_classes
    # test that enums are treated as classes
    assert KS.EmploymentEventType in owl_classes
    owl_object_properties = list(g.subjects(RDF.type, OWL.ObjectProperty))
    assert len(owl_object_properties) > 10
    for p in owl_object_properties:
        types = list(g.objects(p, RDF.type))
        assert types == [OWL.ObjectProperty]
    owl_datatype_properties = list(g.subjects(RDF.type, OWL.DatatypeProperty))
    assert len(owl_datatype_properties) > 10
    for p in owl_datatype_properties:
        types = list(g.objects(p, RDF.type))
        assert types == [OWL.DatatypeProperty]
    # check that definitions are present, and use the default profile
    assert Literal("A person, living or dead") in g.objects(KS.Person, SKOS.definition)
    # test enums
    enum_bnode = list(g.objects(KS.EmploymentEventType, OWL.unionOf))[0]
    coll = Collection(g, enum_bnode)
    assert [BIZ["001"], BIZ["002"], BIZ["003"], BIZ["004"]] == list(coll)
    assert BIZ["001"] in owl_classes


def test_rdfs_profile(kitchen_sink_path):
    owl = OwlSchemaGenerator(
        kitchen_sink_path,
        mergeimports=False,
        metaclasses=False,
        type_objects=False,
        metadata_profile=MetadataProfile.rdfs,
        ontology_uri_suffix=".owl.ttl",
    ).serialize(mergeimports=False)
    g = Graph()
    g.parse(data=owl, format="turtle")
    owl_classes = list(g.subjects(RDF.type, OWL.Class))
    for c in owl_classes:
        # check not using the default metadata profile
        assert list(g.objects(c, SKOS.definition)) == []
    # check that definitions are present, and use the RDFS profile
    assert Literal("A person, living or dead") in g.objects(KS.Person, RDFS.comment)


def test_definition_uris():
    """
    Tests behavior of assigning URIs to classes and slots

    In future this will be paramterizable as per:
    https://github.com/linkml/linkml/issues/932
    """
    sb = SchemaBuilder()
    sb.add_class(
        "MyPerson",
        class_uri="schema:Person",
        slots=[SlotDefinition("name", slot_uri="schema:name")],
    )
    sb.add_defaults()
    sb.add_prefix("schema", "http://schema.org/")
    schema = sb.schema
    gen = OwlSchemaGenerator(schema, mergeimports=False, metaclasses=False, type_objects=False)
    owl = gen.serialize()
    g = Graph()
    g.parse(data=owl)
    triples = list(g.triples((None, None, None)))
    expected = [
        (
            URIRef("http://example.org/test-schema/MyPerson"),
            URIRef("http://www.w3.org/2004/02/skos/core#exactMatch"),
            URIRef("http://schema.org/Person"),
        )
    ]
    for t in expected:
        assert t in triples


def test_equivalent_uris():
    """
    Test behavior of asserting owl:equivalentClass between a class
    and its corresponding class_uri
    """
    sb = SchemaBuilder()
    sb.add_class(
        "MyPerson",
        class_uri="schema:Person",
        slots=[SlotDefinition("name", slot_uri="schema:name")],
    )
    sb.add_defaults()
    sb.add_prefix("schema", "http://schema.org/")
    schema = sb.schema
    gen = OwlSchemaGenerator(
        schema=schema,
        mergeimports=False,
        metaclasses=False,
        type_objects=False,
        assert_equivalent_classes=True,
    )
    owl = gen.serialize()
    graph = Graph()
    graph.parse(data=owl)
    assert (
        URIRef("http://example.org/test-schema/MyPerson"),
        OWL.equivalentClass,
        URIRef("http://schema.org/Person"),
    ) in graph
