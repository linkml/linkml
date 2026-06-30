import logging
import os
from enum import Enum

import pytest
from rdflib import RDFS, SKOS, BNode, Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import OWL, RDF

from linkml import METAMODEL_CONTEXT_URI
from linkml.generators.owlgen import MetadataProfile, OwlSchemaGenerator
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.linkml_model.meta import (
    AnonymousClassExpression,
    AnonymousSlotExpression,
    ClassRule,
    PermissibleValue,
)
from linkml_runtime.utils.schema_builder import SchemaBuilder

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


def test_rule_none_of_ignores_empty_slot_expression() -> None:
    """Issue 3358: empty ``none_of`` operands in rules must not crash OWL generation."""

    sb = SchemaBuilder()
    sb.add_slot(SlotDefinition("object_category", range="string"))
    sb.add_slot(SlotDefinition("object_source", range="string"))
    sb.add_class("MappingRule", tree_root=True, slots=["object_category", "object_source"])
    sb.add_defaults()
    sb.schema.classes["MappingRule"].rules = [
        ClassRule(
            preconditions=AnonymousClassExpression(
                slot_conditions={
                    "object_category": SlotDefinition(
                        "object_category",
                        none_of=[AnonymousSlotExpression()],
                    )
                }
            ),
            postconditions=AnonymousClassExpression(
                slot_conditions={
                    "object_source": SlotDefinition(
                        "object_source",
                        equals_string="source",
                    )
                }
            ),
        )
    ]

    owl = OwlSchemaGenerator(
        sb.schema,
        mergeimports=False,
        metaclasses=False,
        type_objects=False,
    ).serialize()
    g = Graph()
    g.parse(data=owl, format="turtle")

    assert (EX.MappingRule, RDF.type, OWL.Class) in g
    assert list(g.objects(None, OWL.complementOf)) == []
    assert list(g.objects(None, OWL.datatypeComplementOf)) == []


@pytest.mark.network
def test_issue_388_attribute_slot_uri_conflicts_stay_disambiguated_in_owl(input_path):
    """Ambiguous attribute URIs should keep the minimal shared OWL identity."""
    generated_owl = OwlSchemaGenerator(
        input_path("linkml_issue_388.yaml"),
        metaclasses=False,
        skip_vacuous_min_zero_cardinality_axioms=False,
        skip_vacuous_local_range_axioms=False,
        consolidate_cardinality_axioms=False,
    ).serialize(context=[METAMODEL_CONTEXT_URI])

    owl_graph = Graph()
    owl_graph.parse(data=generated_owl, format="turtle")
    this_a = URIRef("https://example.org/this/a")
    assert len(list(owl_graph.triples((this_a, None, None)))) == 1


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


# ---------------------------------------------------------------------------
# Helpers for abstract covering-axiom tests
# ---------------------------------------------------------------------------


def _build_abstract_schema() -> SchemaBuilder:
    """Return a SchemaBuilder with Animal (abstract) -> Dog, Cat subclasses."""
    sb = SchemaBuilder()
    sb.add_class("Animal", abstract=True)
    sb.add_class("Dog", is_a="Animal")
    sb.add_class("Cat", is_a="Animal")
    sb.add_defaults()
    return sb


def _input_path(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), "input", name)


def _literal_values_in_complement_filler(g: Graph) -> set[str]:
    """Return all literal values inside datatypeComplementOf owl:oneOf fillers.

    Produces: neg_expr owl:datatypeComplementOf [a rdfs:Datatype; owl:oneOf ("Red")].
    We traverse: datatypeComplementOf -> filler -> owl:oneOf -> RDF list -> literals.
    """
    values: set[str] = set()
    for filler in g.objects(None, OWL.datatypeComplementOf):
        for list_node in g.objects(filler, OWL.oneOf):
            for v in Collection(g, list_node):
                if isinstance(v, Literal):
                    values.add(str(v))
    return values


def _union_members(g: Graph, cls_uri: URIRef) -> set[URIRef] | None:
    """Return the set of URIRefs in the owl:unionOf covering axiom for *cls_uri*.

    Returns ``None`` when no such axiom exists.
    """
    for obj in g.objects(cls_uri, RDFS.subClassOf):
        if not isinstance(obj, BNode):
            continue
        for union_list in g.objects(obj, OWL.unionOf):
            return set(Collection(g, union_list))
    return None


def _owl_graph(sb: SchemaBuilder, **gen_kwargs) -> Graph:
    gen = OwlSchemaGenerator(sb.schema, mergeimports=False, metaclasses=False, type_objects=False, **gen_kwargs)
    g = Graph()
    g.parse(data=gen.serialize(), format="turtle")
    return g


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_abstract_class_gets_union_of_subclasses_by_default():
    """Abstract classes emit rdfs:subClassOf owl:unionOf(subclasses) by default."""
    g = _owl_graph(_build_abstract_schema())
    members = _union_members(g, EX.Animal)
    assert members is not None, "No union-of covering axiom found for Animal"
    assert members == {EX.Dog, EX.Cat}


def test_skip_flag_suppresses_union_of_axiom():
    """Setting skip_abstract_class_as_unionof_subclasses=True omits the covering axiom."""
    g = _owl_graph(_build_abstract_schema(), skip_abstract_class_as_unionof_subclasses=True)
    assert _union_members(g, EX.Animal) is None


def test_non_abstract_class_does_not_get_union_of_axiom():
    """Concrete (non-abstract) classes never receive a union-of covering axiom."""
    sb = SchemaBuilder()
    sb.add_class("Vehicle")
    sb.add_class("Car", is_a="Vehicle")
    sb.add_class("Bike", is_a="Vehicle")
    sb.add_defaults()
    g = _owl_graph(sb)
    assert _union_members(g, EX.Vehicle) is None


def test_abstract_class_without_subclasses_gets_no_union_of_axiom():
    """An abstract class with no direct subclasses emits no union-of axiom."""
    sb = SchemaBuilder()
    sb.add_class("Orphan", abstract=True)
    sb.add_defaults()
    g = _owl_graph(sb)
    assert _union_members(g, EX.Orphan) is None


def test_abstract_class_with_no_children_emits_info(caplog):
    """An abstract class with no children emits an info message about missing coverage.

    When an abstract class has zero subclasses, no covering axiom can be
    generated.  An info message alerts users that the class hierarchy is
    incomplete — this is not a warning because abstract leaf classes are
    a normal pattern in base schemas designed for downstream extension.

    See: mgskjaeveland's review on linkml/linkml#3309.
    See: matentzn's review on linkml/linkml#3309.
    """
    sb = SchemaBuilder()
    sb.add_class("Orphan", abstract=True)
    sb.add_defaults()

    with caplog.at_level(logging.INFO, logger="linkml.generators.owlgen"):
        g = _owl_graph(sb)

    # No covering axiom emitted
    assert _union_members(g, EX.Orphan) is None

    # An info message must be logged (not a warning)
    assert any("has no children" in msg for msg in caplog.messages), (
        "Expected an info message about abstract class with no children"
    )
    assert any("No covering axiom" in msg for msg in caplog.messages), (
        "Info message should mention that no covering axiom will be generated"
    )


def test_no_children_info_suppressed_by_skip_flag(caplog):
    """When --skip-abstract-class-as-unionof-subclasses is set, no info for zero children."""
    sb = SchemaBuilder()
    sb.add_class("Orphan", abstract=True)
    sb.add_defaults()

    with caplog.at_level(logging.INFO, logger="linkml.generators.owlgen"):
        _owl_graph(sb, skip_abstract_class_as_unionof_subclasses=True)

    assert not any("has no children" in msg for msg in caplog.messages)


def test_abstract_class_with_single_child_emits_warning(caplog):
    """An abstract class with one child still gets a covering axiom but emits a warning.

    Per OWL 2 semantics, the covering axiom with a single child creates an
    equivalence (Parent ≡ Child).  This is logically correct but may surprise
    users who plan to extend the ontology later.  The generator should warn
    and recommend ``--skip-abstract-class-as-unionof-subclasses``.

    See: W3C OWL 2 Primer §4.2 — bidirectional rdfs:subClassOf = equivalence.
    See: mgskjaeveland's review on linkml/linkml#3309.
    """
    sb = SchemaBuilder()
    sb.add_class("GrandParent")
    sb.add_class("Parent", is_a="GrandParent", abstract=True)
    sb.add_class("Child", is_a="Parent")
    sb.add_defaults()

    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        g = _owl_graph(sb)

    # Covering axiom IS still emitted (single child → equivalence is OWL-correct).
    # With one child, _union_of returns the child URI directly (no owl:unionOf wrapper),
    # so the covering axiom materialises as Parent rdfs:subClassOf Child.
    # Combined with Child rdfs:subClassOf Parent (from is_a), this is the equivalence.
    assert (EX.Parent, RDFS.subClassOf, EX.Child) in g, (
        "Covering axiom should produce Parent rdfs:subClassOf Child for single-child case"
    )
    assert (EX.Child, RDFS.subClassOf, EX.Parent) in g
    assert (EX.Parent, RDFS.subClassOf, EX.GrandParent) in g

    # But a warning must be logged
    assert any("only 1 direct child" in msg for msg in caplog.messages), (
        "Expected a warning about single-child covering axiom creating equivalence"
    )
    assert any("--skip-abstract-class-as-unionof-subclasses" in msg for msg in caplog.messages), (
        "Warning should recommend the skip flag"
    )


def test_single_child_warning_suppressed_by_skip_flag(caplog):
    """When --skip-abstract-class-as-unionof-subclasses is set, no warning is emitted.

    The skip flag suppresses covering axioms entirely, so the single-child
    equivalence case never arises.
    """
    sb = SchemaBuilder()
    sb.add_class("Parent", abstract=True)
    sb.add_class("Child", is_a="Parent")
    sb.add_defaults()

    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        g = _owl_graph(sb, skip_abstract_class_as_unionof_subclasses=True)

    # No covering axiom emitted
    assert (EX.Parent, RDFS.subClassOf, EX.Child) not in g
    # No warning either
    assert not any("only 1 direct child" in msg for msg in caplog.messages)


def test_multiple_children_no_warning(caplog):
    """An abstract class with 2+ children must NOT emit a warning.

    The covering axiom is a proper union (not a degenerate equivalence),
    so no warning is needed.
    """
    sb = SchemaBuilder()
    sb.add_class("Animal", abstract=True)
    sb.add_class("Dog", is_a="Animal")
    sb.add_class("Cat", is_a="Animal")
    sb.add_defaults()

    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        g = _owl_graph(sb)

    # Covering axiom emitted (proper union)
    members = _union_members(g, EX.Animal)
    assert members == {EX.Dog, EX.Cat}

    # No warning about children count
    assert not any("has no children" in msg for msg in caplog.messages)
    assert not any("only 1 direct child" in msg for msg in caplog.messages)


def test_non_abstract_class_no_warning(caplog):
    """A non-abstract class must NOT emit covering axiom warnings.

    Covering axioms only apply to abstract classes.  Concrete classes
    should be silently skipped regardless of child count.
    """
    sb = SchemaBuilder()
    sb.add_class("Parent")  # not abstract
    sb.add_class("Child", is_a="Parent")
    sb.add_defaults()

    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        g = _owl_graph(sb)

    # No covering axiom for non-abstract class
    assert _union_members(g, EX.Parent) is None
    assert (EX.Parent, RDFS.subClassOf, EX.Child) not in g

    # No warning either
    assert not any("has no children" in msg for msg in caplog.messages)
    assert not any("only 1 direct child" in msg for msg in caplog.messages)


def test_abstract_class_with_only_mixin_children_emits_info(caplog):
    """An abstract class whose only children are via mixins (not is_a) gets the no-children info.

    The covering axiom only considers direct is_a children (not mixins).
    If an abstract class has mixin children but no is_a children, it should
    log an info message about having no children for covering axiom purposes.
    """
    sb = SchemaBuilder()
    sb.add_class("Base", abstract=True)
    sb.add_class("MixinChild", mixins=["Base"])
    sb.add_defaults()

    with caplog.at_level(logging.INFO, logger="linkml.generators.owlgen"):
        g = _owl_graph(sb)

    assert _union_members(g, EX.Base) is None
    assert any("has no children" in msg for msg in caplog.messages), (
        "Abstract class with only mixin children should log info about no is_a children"
    )


@pytest.mark.parametrize("skip", [False, True])
def test_union_of_axiom_only_covers_direct_children(skip: bool):
    """Union-of axiom lists only direct is_a children, not grandchildren.

    Schema: Animal (abstract) <- Dog <- Poodle
            Animal (abstract) <- Cat
    Expected union: {Dog, Cat} — Poodle is NOT included.
    """
    sb = SchemaBuilder()
    sb.add_class("Animal", abstract=True)
    sb.add_class("Dog", is_a="Animal")
    sb.add_class("Poodle", is_a="Dog")
    sb.add_class("Cat", is_a="Animal")
    sb.add_defaults()
    g = _owl_graph(sb, skip_abstract_class_as_unionof_subclasses=skip)
    if skip:
        assert _union_members(g, EX.Animal) is None
    else:
        members = _union_members(g, EX.Animal)
        assert members == {EX.Dog, EX.Cat}, f"Expected {{Dog, Cat}}, got {members}"


def _restriction_values(g: Graph, predicate: URIRef) -> list:
    """Collect the objects of *predicate* across all OWL restriction nodes in *g*."""
    results = []
    for r in g.subjects(RDF.type, OWL.Restriction):
        for obj in g.objects(r, predicate):
            results.append(obj)
    return results


@pytest.mark.parametrize("skip_vacuous_min_zero_cardinality_axioms", [True, False])
def test_skip_vacuous_min_zero_cardinality_axioms(skip_vacuous_min_zero_cardinality_axioms: bool) -> None:
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
        skip_vacuous_min_zero_cardinality_axioms=skip_vacuous_min_zero_cardinality_axioms,
    )
    g = Graph()
    g.parse(data=gen.serialize(), format="turtle")
    min_card_values = _restriction_values(g, OWL.minCardinality)
    if skip_vacuous_min_zero_cardinality_axioms:
        assert Literal(0) not in min_card_values, "minCardinality 0 should be suppressed"
    else:
        assert Literal(0) in min_card_values, "minCardinality 0 should be present"
    # required + non-multivalued → min=1, max=1 (consolidation is off by default)
    assert Literal(1) in min_card_values, "minCardinality 1 for required slot must not be suppressed"


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


@pytest.mark.parametrize("enum_inherits_as_subclass_of", [True, False])
def test_enum_inherits_as_subclass_of(enum_inherits_as_subclass_of: bool) -> None:
    """Test that enum inherits relationships are translated to rdfs:subClassOf when the flag is set.

    With the flag enabled, a child enum that lists a parent in its inherits field should
    be asserted as a subclass of that parent in the generated OWL. With the flag disabled
    (the default), no such axiom should be emitted.
    """
    sb = SchemaBuilder()
    sb.add_enum("ParentEnum", permissible_values=["A", "B"])
    sb.add_enum("ChildEnum", permissible_values=["A"], inherits=["ParentEnum"])
    sb.add_defaults()
    gen = OwlSchemaGenerator(
        sb.schema,
        mergeimports=False,
        metaclasses=False,
        type_objects=False,
        enum_inherits_as_subclass_of=enum_inherits_as_subclass_of,
    )
    g = Graph()
    g.parse(data=gen.serialize(), format="turtle")
    subclass_axiom = (EX.ChildEnum, RDFS.subClassOf, EX.ParentEnum)
    if enum_inherits_as_subclass_of:
        assert subclass_axiom in g
    else:
        assert subclass_axiom not in g


@pytest.mark.parametrize(
    "slot_kwargs,consolidate,expected_exact,expected_min,expected_max",
    [
        pytest.param(
            {"required": True},
            True,
            1,
            None,
            None,
            id="required-non-multivalued-collapses-to-cardinality-1",
        ),
        pytest.param(
            {"required": True},
            False,
            None,
            1,
            1,
            id="required-non-multivalued-no-consolidation",
        ),
        pytest.param(
            {"required": True, "multivalued": True},
            False,
            None,
            1,
            None,
            id="required-multivalued-min-1-no-max",
        ),
        pytest.param(
            {},
            False,
            None,
            0,
            1,
            id="optional-non-multivalued-min-0-max-1",
        ),
        pytest.param(
            {"multivalued": True},
            False,
            None,
            0,
            None,
            id="optional-multivalued-min-0-no-max",
        ),
        pytest.param(
            {"minimum_cardinality": 2, "multivalued": True},
            False,
            None,
            2,
            None,
            id="explicit-minimum-cardinality",
        ),
        pytest.param(
            {"maximum_cardinality": 5, "multivalued": True},
            False,
            None,
            0,
            5,
            id="explicit-maximum-cardinality",
        ),
        pytest.param(
            {"minimum_cardinality": 2, "maximum_cardinality": 5, "multivalued": True},
            False,
            None,
            2,
            5,
            id="explicit-min-max-different",
        ),
        pytest.param(
            {"minimum_cardinality": 3, "maximum_cardinality": 3, "multivalued": True},
            True,
            3,
            None,
            None,
            id="explicit-min-equals-max-collapses-to-cardinality",
        ),
        pytest.param(
            {"minimum_cardinality": 3, "maximum_cardinality": 3, "multivalued": True},
            False,
            None,
            3,
            3,
            id="explicit-min-equals-max-no-consolidation",
        ),
    ],
)
def test_slot_cardinality_axioms(
    slot_kwargs: dict,
    consolidate: bool,
    expected_exact: int | None,
    expected_min: int | None,
    expected_max: int | None,
) -> None:
    """Test that OWL cardinality axioms are generated correctly from slot properties.

    Covers minimum_cardinality, maximum_cardinality, required, and multivalued,
    including the optimisation where min==max is collapsed to a single
    owl:cardinality restriction instead of separate min/max restrictions.
    """
    sb = SchemaBuilder()
    sb.add_class(
        "MyClass",
        slots=[SlotDefinition("my_slot", range="string", **slot_kwargs)],
    )
    sb.add_defaults()
    gen = OwlSchemaGenerator(
        sb.schema,
        mergeimports=False,
        metaclasses=False,
        type_objects=False,
        consolidate_cardinality_axioms=consolidate,
    )
    g = Graph()
    g.parse(data=gen.serialize(), format="turtle")

    exact_values = _restriction_values(g, OWL.cardinality)
    min_values = _restriction_values(g, OWL.minCardinality)
    max_values = _restriction_values(g, OWL.maxCardinality)

    if expected_exact is not None:
        assert Literal(expected_exact) in exact_values
        assert not min_values, f"expected no owl:minCardinality when min==max, got {min_values}"
        assert not max_values, f"expected no owl:maxCardinality when min==max, got {max_values}"
    else:
        assert not exact_values, f"expected no owl:cardinality, got {exact_values}"
        if expected_min is not None:
            assert Literal(expected_min) in min_values
        else:
            assert not min_values, f"expected no owl:minCardinality, got {min_values}"
        if expected_max is not None:
            assert Literal(expected_max) in max_values
        else:
            assert not max_values, f"expected no owl:maxCardinality, got {max_values}"


@pytest.mark.parametrize(
    "num_children,children_are_mutually_disjoint,expect_axiom",
    [
        (3, True, True),  # flag set, multiple children → axiom emitted
        (1, True, False),  # flag set, single child → axiom suppressed
        (3, False, False),  # flag not set → no axiom
    ],
)
def test_children_are_mutually_disjoint(
    num_children: int, children_are_mutually_disjoint: bool, expect_axiom: bool
) -> None:
    """Test that children_are_mutually_disjoint emits owl:AllDisjointClasses for direct subclasses.

    The axiom should be emitted only when the flag is True and at least two children exist.
    """
    sb = SchemaBuilder()
    sb.add_class("Animal", children_are_mutually_disjoint=children_are_mutually_disjoint)
    child_names = [f"Child{i}" for i in range(num_children)]
    for name in child_names:
        sb.add_class(name, is_a="Animal")
    sb.add_defaults()
    gen = OwlSchemaGenerator(sb.schema, mergeimports=False, metaclasses=False, type_objects=False)
    owl = gen.serialize()
    g = Graph()
    g.parse(data=owl, format="turtle")
    disjoint_nodes = list(g.subjects(RDF.type, OWL.AllDisjointClasses))
    if not expect_axiom:
        assert disjoint_nodes == []
    else:
        assert len(disjoint_nodes) == 1
        members_node = list(g.objects(disjoint_nodes[0], OWL.members))[0]
        members = set(Collection(g, members_node))
        assert members == {EX[name] for name in child_names}


# equals_string on an enum-ranged slot (is_literal=None) must not silently
# drop the constraint; it should produce an owl:oneOf expression with a Literal.


def test_equals_string_enum_none_of_no_crash():
    """Regression: gen-owl on owlgen/slot_conditions.yaml must not raise an AssertionError.

    The bug was that equals_string on an enum-ranged slot produced is_literal=None,
    which caused the constraint to be dropped, leaving None in the expression list
    and ultimately triggering rdflib's assertion inside graph.add().
    """
    owl = OwlSchemaGenerator(_input_path("owlgen/slot_conditions.yaml")).serialize()
    g = Graph()
    g.parse(data=owl, format="turtle")
    # Schema parses without error and the Item class is present.
    assert any(str(s).endswith("Item") for s, _, _ in g.triples((None, RDF.type, OWL.Class)))


def test_equals_string_enum_slot_emits_one_of_literal():
    """equals_string on an enum-ranged slot must produce an owl:oneOf with a Literal.

    Before the fix, is_literal=None caused a warning and the expression was skipped.
    After the fix, the value is treated like equals_string_in (single-item list).
    """
    owl = OwlSchemaGenerator(_input_path("owlgen/slot_conditions.yaml")).serialize()
    g = Graph()
    g.parse(data=owl, format="turtle")
    assert "Red" in _literal_values_in_complement_filler(g), (
        "Expected owl:oneOf with literal 'Red' for equals_string on enum-ranged slot"
    )


def test_equals_string_enum_produces_complement_expression():
    """A none_of rule using equals_string on an enum slot must produce a complement axiom.

    The complement (owl:complementOf / owl:datatypeComplementOf) wraps the oneOf
    expression, expressing "value is not Red".
    """
    owl = OwlSchemaGenerator(_input_path("owlgen/slot_conditions.yaml")).serialize()
    g = Graph()
    g.parse(data=owl, format="turtle")
    # There must be at least one owl:datatypeComplementOf or owl:complementOf triple.
    complement_triples = list(g.triples((None, OWL.datatypeComplementOf, None))) + list(
        g.triples((None, OWL.complementOf, None))
    )
    assert complement_triples, "Expected an owl:complementOf/datatypeComplementOf axiom from none_of rule"


# _complement_of_union_of must handle None operands gracefully


def test_complement_of_union_of_filters_none(caplog):
    """_complement_of_union_of([None]) must return None and log a warning, not crash.

    Without the guard, [None] is passed to _union_of which propagates None into
    graph.add(), raising an AssertionError from rdflib.
    """
    import logging

    gen = OwlSchemaGenerator(_input_path("owlgen/slot_conditions.yaml"))
    gen.as_graph()  # initialises self.graph

    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        result = gen._complement_of_union_of([None])

    assert result is None, "_complement_of_union_of([None]) should return None"
    assert any("None" in rec.message or "complement" in rec.message.lower() for rec in caplog.records), (
        "Expected a warning about unresolvable complement operands"
    )


@pytest.mark.parametrize(
    "exprs,expect_none",
    [
        ([None], True),
        ([None, None], True),
    ],
)
def test_complement_of_union_of_all_none_returns_none(exprs, expect_none):
    """_complement_of_union_of with only None operands must return None without crashing."""
    gen = OwlSchemaGenerator(_input_path("owlgen/slot_conditions.yaml"))
    gen.as_graph()
    result = gen._complement_of_union_of(exprs)
    assert (result is None) == expect_none


def test_complement_of_union_of_mixed_none_filters_silently():
    """_complement_of_union_of with some valid and some None operands uses only valid ones."""
    from rdflib import BNode

    gen = OwlSchemaGenerator(_input_path("owlgen/slot_conditions.yaml"))
    gen.as_graph()
    valid_node = URIRef("http://example.org/Foo")
    result = gen._complement_of_union_of([None, valid_node])
    # Should succeed and return a BNode (the complement expression).
    assert result is not None
    assert isinstance(result, BNode)
