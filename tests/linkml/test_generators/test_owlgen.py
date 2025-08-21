import pytest
from linkml_runtime.linkml_model import SlotDefinition
from rdflib import RDFS, SKOS, Graph, Literal, Namespace
from rdflib.collection import Collection
from rdflib.namespace import OWL, RDF

from linkml.generators.owlgen import MetadataProfile, OwlSchemaGenerator
from linkml.utils.schema_builder import SchemaBuilder

SYMP = Namespace("http://purl.obolibrary.org/obo/SYMP_")
KS = Namespace("https://w3id.org/linkml/tests/kitchen_sink/")
LINKML = Namespace("https://w3id.org/linkml/")
BIZ = Namespace("https://example.org/bizcodes/")
EX = Namespace("http://example.org/test-schema/")
SCHEMA = Namespace("http://schema.org/")


@pytest.mark.parametrize(
    "metaclasses,type_objects",
    [
        (False, False),
        (True, False),
        (False, True),
        (True, True),
    ],
)
def test_owlgen(kitchen_sink_path, metaclasses, type_objects):
    """tests generation of owl schema-style ontologies"""
    owl = OwlSchemaGenerator(
        kitchen_sink_path,
        mergeimports=False,
        metaclasses=metaclasses,
        type_objects=type_objects,
        ontology_uri_suffix=".owl.ttl",
    ).serialize()
    g = Graph()
    g.parse(data=owl, format="turtle")
    owl_classes = list(g.subjects(RDF.type, OWL.Class))
    assert len(owl_classes) > 10
    for c in owl_classes:
        types = list(g.objects(c, RDF.type))
        assert OWL.Class in types
        if metaclasses:
            # TODO: make this stricter;
            # ClassDefinitions should be of type ClassDefinition
            # PVs should be of the enum type
            assert len(types) == 2
        else:
            assert len(types) == 1
    assert KS.MedicalEvent in owl_classes
    # test that enums are treated as classes
    assert KS.EmploymentEventType in owl_classes
    owl_object_properties = list(g.subjects(RDF.type, OWL.ObjectProperty))
    assert len(owl_object_properties) > 10
    for p in owl_object_properties:
        types = list(g.objects(p, RDF.type))
        assert OWL.ObjectProperty in types
        if metaclasses:
            assert len(types) == 2
        else:
            assert len(types) == 1
    owl_datatype_properties = list(g.subjects(RDF.type, OWL.DatatypeProperty))
    if type_objects:
        assert owl_datatype_properties == []
    else:
        assert len(owl_datatype_properties) > 10
    for p in owl_datatype_properties:
        types = list(g.objects(p, RDF.type))
        assert OWL.DatatypeProperty in types
        if metaclasses:
            assert len(types) == 2
        else:
            assert len(types) == 1
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


@pytest.mark.parametrize(
    "description,metadata_profiles,use_native_uris,metaclasses,assert_equivalent_classes,expected",
    [
        (
            "default is model (native) URIs and SKOS for matches",
            [],
            True,
            False,
            False,
            [
                (
                    EX.MyPerson,
                    RDFS.label,
                    Literal("MyPerson"),
                ),
                (
                    EX.MyPerson,
                    SKOS.definition,
                    Literal("A person"),
                ),
                (
                    EX.MyPerson,
                    SKOS.exactMatch,
                    SCHEMA.Person,
                ),
                (
                    EX.name,
                    RDFS.label,
                    Literal("name"),
                ),
            ],
        ),
        (
            "non-native_uris",
            [],
            False,
            False,
            False,
            [
                (
                    SCHEMA.Person,
                    RDFS.label,
                    Literal("MyPerson"),
                ),
                (
                    SCHEMA.Person,
                    SKOS.exactMatch,
                    EX.MyPerson,
                ),
                (
                    SCHEMA.name,
                    RDFS.label,
                    Literal("name"),
                ),
            ],
        ),
        (
            "native_uris and OWL for matches",
            [],
            True,
            False,
            True,
            [
                (
                    EX.MyPerson,
                    RDFS.label,
                    Literal("MyPerson"),
                ),
                (
                    EX.MyPerson,
                    OWL.equivalentClass,
                    SCHEMA.Person,
                ),
            ],
        ),
        (
            "RDFS profile",
            [MetadataProfile.rdfs],
            True,
            False,
            False,
            [
                (
                    EX.MyPerson,
                    RDFS.label,
                    Literal("MyPerson"),
                ),
                (
                    EX.MyPerson,
                    RDFS.comment,
                    Literal("A person"),
                ),
                (
                    EX.MyPerson,
                    SKOS.exactMatch,
                    SCHEMA.Person,
                ),
            ],
        ),
    ],
)
def test_definition_uris(
    description, metadata_profiles, use_native_uris, metaclasses, assert_equivalent_classes, expected
):
    """
    Tests behavior of assigning URIs to classes and slots.
    """
    sb = SchemaBuilder()
    sb.add_class(
        "MyPerson",
        class_uri="schema:Person",
        description="A person",
        slots=[SlotDefinition("name", slot_uri="schema:name")],
    )
    sb.add_defaults()
    sb.add_prefix("schema", "http://schema.org/")
    schema = sb.schema
    gen = OwlSchemaGenerator(
        schema,
        metadata_profiles=metadata_profiles,
        mergeimports=False,
        metaclasses=metaclasses,
        type_objects=False,
        use_native_uris=use_native_uris,
        assert_equivalent_classes=assert_equivalent_classes,
    )
    owl = gen.serialize()
    print(owl)
    g = Graph()
    g.parse(data=owl)
    triples = list(g.triples((None, None, None)))
    for t in expected:
        assert t in triples
    if metadata_profiles == [MetadataProfile.rdfs]:
        owl_classes = list(g.subjects(RDF.type, OWL.Class))
        for c in owl_classes:
            # check not using the default metadata profile
            assert list(g.objects(c, SKOS.definition)) == []
