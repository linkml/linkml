from enum import Enum

import pytest
from rdflib import RDFS, SKOS, Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import OWL, RDF

from linkml.generators.owlgen import MetadataProfile, OwlSchemaGenerator
from linkml.utils.schema_builder import SchemaBuilder
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.linkml_model.meta import PermissibleValue

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


class PermissibleValueURIMixture(Enum):
    USE_URIS = "use_uris"
    NO_URIS = "no_uris"
    MIXTURE = "mixture"


@pytest.mark.parametrize("default_permissible_value_type", ["owl:Class", "rdfs:Literal", "owl:NamedIndividual"])
@pytest.mark.parametrize(
    "pv_implements", [None, "owl:Class", "rdfs:Literal", "owl:NamedIndividual", ("owl:Class", "rdfs:Literal")]
)
@pytest.mark.parametrize("permissible_value_uri_mixture", [x for x in PermissibleValueURIMixture])
def test_permissible_values(
    default_permissible_value_type: str,
    pv_implements: str | None | tuple[str, str],
    permissible_value_uri_mixture: PermissibleValueURIMixture,
):
    """
    Test permissible value transformation to OWL representations.

    This test verifies how LinkML enums with permissible values are converted to OWL,
    testing different combinations of type mappings and URI configurations.

    OWL Mapping Strategy:
    - Enums can be represented as owl:unionOf (for classes) or owl:oneOf (for individuals/literals)
    - Permissible values can map to OWL Classes, Named Individuals, or Literals
    - The mapping depends on the `default_permissible_value_type` and per-PV `implements` settings

    Parameters
    ----------
    default_permissible_value_type : str
        Default OWL type for permissible values when not explicitly specified.
        Options: "owl:Class", "rdfs:Literal", "owl:NamedIndividual"
        - owl:Class: PVs become OWL classes, enum is owl:unionOf
        - rdfs:Literal: PVs become RDF literals, enum is owl:oneOf
        - owl:NamedIndividual: PVs become named individuals, enum is owl:oneOf

    pv_implements : Union[str, None, tuple[str, str]]
        Override type mapping per permissible value.
        - None: Use default_permissible_value_type for all PVs
        - str: Apply this type to all PVs (overrides default)
        - tuple: Apply first type to PVs with URIs, second to PVs without URIs

    permissible_value_uri_mixture : PermissibleValueURIMixture
        Controls whether PVs have URIs (meanings) assigned.
        - USE_URIS: All PVs have URIs
        - NO_URIS: No PVs have URIs
        - MIXTURE: Some PVs have URIs, some don't (tests mixed scenarios)

    Expected Behavior
    -----------------
    1. When PV type is owl:Class:
       - Enum becomes owl:unionOf of classes
       - PVs are URIRefs (not Literals)

    2. When PV type is rdfs:Literal:
       - Enum becomes owl:oneOf
       - PVs are RDF Literals

    3. When PV type is owl:NamedIndividual:
       - Enum becomes owl:oneOf
       - PVs are URIRefs (individuals)

    4. Mixed types (tuple implements):
       - Can have different types based on URI presence
       - May skip test if behavior is undefined

    Related Issues
    --------------
    - https://github.com/linkml/linkml/issues/1841 - Complex enum constraints in OWL
    - TODOs in owlgen.py lines 668, 929, 1186, 1205 - Enum mapping improvements
    """
    sb = SchemaBuilder()
    permissible_values = [
        PermissibleValue(text="1", description="pv 1"),
        PermissibleValue(text="2", description="pv 2"),
    ]
    if permissible_value_uri_mixture != PermissibleValueURIMixture.NO_URIS:
        permissible_values[0].meaning = "ex:value1"
        if permissible_value_uri_mixture == PermissibleValueURIMixture.USE_URIS:
            permissible_values[1].meaning = "ex:value2"
    if pv_implements:
        for pv in permissible_values:
            if isinstance(pv_implements, tuple):
                if pv.meaning:
                    pv.implements = [pv_implements[0]]
                else:
                    pv.implements = [pv_implements[1]]
            else:
                pv.implements = [pv_implements]
    sb.add_enum(
        "MyEnum",
        description="An enum",
        permissible_values=permissible_values,
    )
    sb.add_defaults()
    sb.add_prefix("schema", "http://schema.org/")
    sb.add_prefix("ex", "https://example.org/")
    schema = sb.schema
    gen = OwlSchemaGenerator(
        schema,
        mergeimports=False,
        default_permissible_value_type=default_permissible_value_type,
    )
    owl = gen.serialize()
    g = Graph()
    g.parse(data=owl)
    triples = list(g.triples((None, None, None)))
    disjunction_targets = {}
    for s, p, o in triples:
        if p in (OWL.oneOf, OWL.unionOf):
            # translate `o` from rdf list into python list
            from rdflib.collection import Collection

            disj_list = list(Collection(g, o))
            assert p not in disjunction_targets
            disjunction_targets[p] = disj_list
    if isinstance(pv_implements, tuple) and permissible_value_uri_mixture == PermissibleValueURIMixture.MIXTURE:
        pytest.skip("mixture of URIs and literals is undefined behavior")
    assert len(disjunction_targets) == 1
    disj_pred, disj_list = tuple(list(disjunction_targets.items())[0])
    assert len(disj_list) == 2
    from rdflib import Literal

    for pv in disj_list:
        expected_permissible_value_type = default_permissible_value_type
        if pv_implements:
            expected_permissible_value_type = pv_implements
        if expected_permissible_value_type == "owl:Class":
            assert disj_pred == OWL.unionOf
            assert not isinstance(pv, Literal)
            assert isinstance(pv, URIRef)
            # assert isinstance(pv, OWL.Class)
        elif expected_permissible_value_type == "rdfs:Literal":
            assert disj_pred == OWL.oneOf
            assert isinstance(pv, Literal)
        elif expected_permissible_value_type == "owl:NamedIndividual":
            assert disj_pred == OWL.oneOf
            assert isinstance(pv, URIRef)
        elif isinstance(expected_permissible_value_type, tuple):
            # mixture of URIs and literals
            assert isinstance(pv, URIRef) or isinstance(pv, Literal)
        else:
            raise AssertionError("all combinations must be accounted for")


def _restriction_values(g: Graph, predicate: URIRef) -> list:
    """Collect the objects of *predicate* across all OWL restriction nodes in *g*."""
    results = []
    for r in g.subjects(RDF.type, OWL.Restriction):
        for obj in g.objects(r, predicate):
            results.append(obj)
    return results


@pytest.mark.parametrize("skip_min_zero_cardinality_axioms", [True, False])
def test_skip_min_zero_cardinality_axioms(skip_min_zero_cardinality_axioms: bool) -> None:
    """Test that owl:minCardinality 0 axioms are suppressed when the flag is set.

    Non-required slots produce a minCardinality 0 restriction by default (vacuous).
    Required slots still produce minCardinality 1, which must never be suppressed.
    """
    sb = SchemaBuilder()
    sb.add_class(
        "MyClass",
        slots=[
            SlotDefinition("optional_slot", range="string"),
            SlotDefinition("required_slot", range="string", required=True),
        ],
    )
    sb.add_defaults()
    gen = OwlSchemaGenerator(
        sb.schema,
        mergeimports=False,
        metaclasses=False,
        type_objects=False,
        skip_min_zero_cardinality_axioms=skip_min_zero_cardinality_axioms,
    )
    g = Graph()
    g.parse(data=gen.serialize(), format="turtle")
    min_card_values = _restriction_values(g, OWL.minCardinality)
    if skip_min_zero_cardinality_axioms:
        assert Literal(0) not in min_card_values, "minCardinality 0 should be suppressed"
    else:
        assert Literal(0) in min_card_values, "minCardinality 0 should be present"
    # minCardinality 1 (required slot) must always be present
    assert Literal(1) in min_card_values, "minCardinality 1 must not be suppressed"


@pytest.mark.parametrize("skip_vacuous_local_range_axioms", [True, False])
def test_skip_vacuous_local_range_axioms(skip_vacuous_local_range_axioms: bool) -> None:
    """Test that vacuous owl:allValuesFrom restrictions are suppressed when the flag is set.

    A global slot receives a global rdfs:range axiom on the OWL property; an allValuesFrom
    with the same filler is therefore entailed (vacuous) and can be dropped.  An attribute
    slot (defined in class.attributes) has *no* global rdfs:range, so its allValuesFrom is
    the only range declaration and must never be suppressed.
    """
    sb = SchemaBuilder()
    sb.add_class("Target")
    sb.add_class("AttributeTarget")
    # Global slot — will get rdfs:range Target at property level; local allValuesFrom is vacuous.
    sb.add_slot(SlotDefinition("global_slot", range="Target"))
    sb.add_class("MyClass", slots=["global_slot"])
    # Attribute slot — stored in class.attributes, no global rdfs:range; allValuesFrom is essential.
    sb.schema.classes["MyClass"].attributes["attr_slot"] = SlotDefinition("attr_slot", range="AttributeTarget")
    sb.add_defaults()
    gen = OwlSchemaGenerator(
        sb.schema,
        mergeimports=False,
        metaclasses=False,
        type_objects=False,
        skip_vacuous_local_range_axioms=skip_vacuous_local_range_axioms,
    )
    g = Graph()
    g.parse(data=gen.serialize(), format="turtle")
    avf_values = _restriction_values(g, OWL.allValuesFrom)
    target_uri = EX.Target
    attr_target_uri = EX.AttributeTarget
    if skip_vacuous_local_range_axioms:
        assert target_uri not in avf_values, "vacuous allValuesFrom (global slot) should be suppressed"
    else:
        assert target_uri in avf_values, "allValuesFrom for global slot should be present"
    # Attribute slots carry the only range info — must never be suppressed.
    assert attr_target_uri in avf_values, "allValuesFrom for attribute slot must not be suppressed"
