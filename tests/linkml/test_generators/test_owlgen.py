import logging
import os
from enum import Enum

import pytest
from rdflib import RDFS, SKOS, BNode, Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import OWL, RDF, XSD

from linkml import METAMODEL_CONTEXT_URI
from linkml.generators.owlgen import MetadataProfile, OwlSchemaGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.linkml_model.meta import (
    AnonymousClassExpression,
    AnonymousSlotExpression,
    ClassRule,
    PermissibleValue,
)
from linkml_runtime.utils.compile_python import compile_python
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


@pytest.mark.parametrize(
    ("partial_match", "expected_pattern"),
    [
        (False, r"[a-z]+"),
        (True, r".*([a-z]+).*"),
    ],
)
def test_as_graph_materializes_xsd_structured_patterns(partial_match: bool, expected_pattern: str) -> None:
    """Translate structured patterns without modifying the source schema."""
    generator = OwlSchemaGenerator(
        f"""
id: https://example.org/pattern
name: pattern
prefixes:
  ex: https://example.org/
default_prefix: ex
settings:
  word: "[a-z]+"
slots:
  value:
    structured_pattern:
      syntax: "{{word}}"
      interpolated: true
      partial_match: {str(partial_match).lower()}
classes:
  C:
    slots:
      - value
"""
    )
    value_slot = generator.schemaview.get_slot("value")

    assert value_slot.pattern is None

    graph = generator.as_graph()

    patterns = list(graph.objects(None, XSD.pattern))
    assert Literal(expected_pattern) in patterns, patterns
    assert value_slot.pattern is None


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


def test_add_root_classes_declares_grouping_classes() -> None:
    """``add_root_classes`` must declare the metamodel grouping classes it references.

    Regression test for https://github.com/linkml/linkml/issues/3605. With ``add_root_classes``,
    enums, classes, and permissible values are made ``rdfs:subClassOf`` ``linkml:EnumDefinition`` /
    ``linkml:ClassDefinition`` / ``linkml:PermissibleValue``. Previously those parents were never
    declared as ``owl:Class``, so RDF-only consumers (such as OLS) treated them as dangling
    references and dropped the grouping. Each referenced grouping class must now be declared as an
    ``owl:Class`` with an ``rdfs:label`` sourced from the metamodel.
    """
    sb = SchemaBuilder()
    sb.add_class("Person")
    sb.add_enum("StatusEnum", permissible_values=["active", "inactive"])
    sb.add_defaults()

    owl = OwlSchemaGenerator(
        sb.schema,
        add_root_classes=True,
        metaclasses=False,
        type_objects=False,
    ).serialize()
    g = Graph()
    g.parse(data=owl, format="turtle")

    for grouping_uri in (LINKML.EnumDefinition, LINKML.ClassDefinition, LINKML.PermissibleValue):
        assert (grouping_uri, RDF.type, OWL.Class) in g, f"{grouping_uri} not declared as owl:Class"
        assert next(g.objects(grouping_uri, RDFS.label), None) is not None, f"{grouping_uri} missing rdfs:label"


def test_add_root_classes_declares_mixin_grouping_class() -> None:
    """The ``mixins_as_expressions`` path must declare its synthetic mixin grouping class.

    Companion to :func:`test_add_root_classes_declares_grouping_classes`, covering the branch a
    root mixin takes when ``mixins_as_expressions`` is set. Such a class is made
    ``rdfs:subClassOf`` the synthetic ``ClassDefinition#Mixin`` grouping class; that grouping class
    must itself be declared as an ``owl:Class`` with an ``rdfs:label`` so RDF-only consumers (such
    as OLS) keep the grouping rather than treating it as a dangling reference.
    """
    from linkml_runtime.linkml_model.meta import ClassDefinition as MetaClassDefinition

    sb = SchemaBuilder()
    sb.add_class(MetaClassDefinition("RootMixin", mixin=True))
    sb.add_defaults()

    owl = OwlSchemaGenerator(
        sb.schema,
        add_root_classes=True,
        mixins_as_expressions=True,
        metaclasses=False,
        type_objects=False,
    ).serialize()
    g = Graph()
    g.parse(data=owl, format="turtle")

    mixin_grouping_uri = URIRef(str(MetaClassDefinition.class_class_uri) + "#Mixin")
    assert (mixin_grouping_uri, RDF.type, OWL.Class) in g, "mixin grouping class not declared as owl:Class"
    assert (mixin_grouping_uri, RDFS.label, Literal("mixin")) in g, "mixin grouping class missing rdfs:label 'mixin'"


def test_grouping_classes_not_declared_without_add_root_classes() -> None:
    """Grouping-class declarations are emitted only when ``add_root_classes`` is set."""
    sb = SchemaBuilder()
    sb.add_class("Person")
    sb.add_enum("StatusEnum", permissible_values=["active", "inactive"])
    sb.add_defaults()

    owl = OwlSchemaGenerator(
        sb.schema,
        add_root_classes=False,
        metaclasses=False,
        type_objects=False,
    ).serialize()
    g = Graph()
    g.parse(data=owl, format="turtle")

    assert (LINKML.EnumDefinition, RDF.type, OWL.Class) not in g


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
    gen_kwargs = {"metaclasses": False, "type_objects": False, **gen_kwargs}
    gen = OwlSchemaGenerator(sb.schema, mergeimports=False, **gen_kwargs)
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


def _ontology_iris(g: Graph) -> set[URIRef]:
    """Return the IRIs declared as owl:Ontology in the graph."""
    return set(g.subjects(RDF.type, OWL.Ontology))


@pytest.mark.parametrize("suffix", [None, "", ".owl", ".owl.ttl"])
def test_ontology_uri_suffix_is_appended_to_ontology_iri(suffix: str | None) -> None:
    """The ontology IRI is the schema id followed by ``ontology_uri_suffix`` (#569)."""
    sb = _build_abstract_schema()
    g = _owl_graph(sb, ontology_uri_suffix=suffix)
    assert _ontology_iris(g) == {URIRef(f"{sb.schema.id}{suffix or ''}")}


@pytest.mark.parametrize(
    "args,expected_suffix",
    [
        ([], ".owl.ttl"),
        (["--ontology-uri-suffix", ".owl"], ".owl"),
        (["--ontology-uri-suffix", ""], ""),
    ],
)
def test_cli_ontology_uri_suffix(kitchen_sink_path, args: list[str], expected_suffix: str) -> None:
    """``gen-owl --ontology-uri-suffix`` changes the ontology IRI, and defaults to ``.owl.ttl`` (#569)."""
    from click.testing import CliRunner

    from linkml.generators.owlgen import cli

    result = CliRunner().invoke(cli, [str(kitchen_sink_path), *args])
    assert result.exit_code == 0, result.output
    g = Graph()
    g.parse(data=result.output, format="turtle")
    assert _ontology_iris(g) == {URIRef(f"https://w3id.org/linkml/tests/kitchen_sink{expected_suffix}")}


def _unit_schema(permissible_values: list[PermissibleValue], **enum_kwargs) -> SchemaBuilder:
    """Return a SchemaBuilder with a class Thing whose slot unit ranges over UnitEnum."""
    sb = SchemaBuilder()
    sb.add_enum("UnitEnum", permissible_values=permissible_values, **enum_kwargs)
    sb.add_slot("unit", range="UnitEnum")
    sb.add_class("Thing", slots=["unit"])
    sb.add_defaults()
    return sb


@pytest.mark.parametrize("type_objects", [False, True])
@pytest.mark.parametrize("declared_on", ["generator", "enum", "permissible_values"])
def test_enum_of_literals_is_a_datatype(declared_on: str, type_objects: bool) -> None:
    """An enum whose permissible values are all literals is a datatype, and its slots are data properties.

    OWL 2 DL does not let an IRI be both a class and a datatype (§5.8.1), and the datatype
    is defined as an enumeration of its literals (§9.4).
    """
    literal = ["rdfs:Literal"]
    pvs = [PermissibleValue(text=t, implements=literal if declared_on == "permissible_values" else []) for t in "mk"]
    sb = _unit_schema(pvs, implements=literal if declared_on == "enum" else [])
    gen_kwargs = {"default_permissible_value_type": "rdfs:Literal"} if declared_on == "generator" else {}
    g = _owl_graph(sb, type_objects=type_objects, **gen_kwargs)
    assert set(g.objects(EX.UnitEnum, RDF.type)) == {RDFS.Datatype}
    [data_range] = g.objects(EX.UnitEnum, OWL.equivalentClass)
    assert isinstance(data_range, BNode)
    assert (data_range, RDF.type, RDFS.Datatype) in g
    assert set(Collection(g, g.value(data_range, OWL.oneOf))) == {Literal("m"), Literal("k")}
    assert set(g.objects(EX.unit, RDF.type)) == {OWL.DatatypeProperty}


@pytest.mark.parametrize(
    "permissible_values",
    [[], [PermissibleValue(text="m"), PermissibleValue(text="k", implements=["owl:NamedIndividual"])]],
    ids=["no_values", "mixed_values"],
)
def test_enum_not_only_of_literals_stays_a_class(permissible_values: list[PermissibleValue]) -> None:
    """Only an enum with permissible values, all of them literals, is a datatype."""
    g = _owl_graph(_unit_schema(permissible_values, implements=["rdfs:Literal"]))
    assert set(g.objects(EX.UnitEnum, RDF.type)) == {OWL.Class}
    assert set(g.objects(EX.unit, RDF.type)) == {OWL.ObjectProperty}


@pytest.mark.parametrize(
    "parent",
    [{"is_a": "LengthEnum"}, {"mixins": ["LengthEnum"]}, {"inherits": ["LengthEnum"]}],
    ids=["is_a", "mixins", "inherits"],
)
def test_enum_of_literals_has_no_parents(caplog, parent: dict) -> None:
    """OWL 2 has no subtype axiom for datatypes, so the parents of a datatype enum are not emitted."""
    sb = _unit_schema([PermissibleValue(text="m")], **parent)
    sb.add_enum("LengthEnum", permissible_values=["m", "km"])
    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        g = _owl_graph(
            sb, default_permissible_value_type="rdfs:Literal", add_root_classes=True, enum_inherits_as_subclass_of=True
        )
    assert not set(g.objects(EX.UnitEnum, RDFS.subClassOf))
    assert not set(g.objects(EX.LengthEnum, RDFS.subClassOf))
    assert "Enum 'UnitEnum' is a datatype in OWL, so its parent enums are not emitted" in caplog.messages


@pytest.mark.parametrize("mixins_as_expressions", [False, True])
def test_class_enum_has_no_datatype_parents(caplog, mixins_as_expressions: bool) -> None:
    """An enum that stays a class does not get a datatype enum as parent: no IRI is both (§5.8.1)."""
    sb = SchemaBuilder()
    sb.add_enum("LengthEnum", permissible_values=["m", "km"])
    sb.add_enum("AnyUnit", inherits=["LengthEnum"])
    sb.add_enum("SubLength", is_a="LengthEnum")
    sb.add_enum("MixLength", mixins=["LengthEnum"])
    sb.add_defaults()
    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        g = _owl_graph(
            sb,
            default_permissible_value_type="rdfs:Literal",
            enum_inherits_as_subclass_of=True,
            mixins_as_expressions=mixins_as_expressions,
        )
    assert set(g.objects(EX.LengthEnum, RDF.type)) == {RDFS.Datatype}
    assert not set(g.subject_predicates(EX.LengthEnum))
    for child in ("AnyUnit", "SubLength", "MixLength"):
        assert set(g.objects(EX[child], RDF.type)) == {OWL.Class}
        assert (
            f"Enum {child!r} is a class in OWL and its parent 'LengthEnum' is a datatype, so that parent is not emitted"
            in caplog.messages
        )


@pytest.mark.parametrize("default_range", [None, "string"])
@pytest.mark.parametrize("type_objects", [False, True])
@pytest.mark.parametrize("refined_in", ["subclass", "subclass_of_narrowing_parent", "class_expression"])
def test_refined_slot_of_enum_of_literals_keeps_its_range(
    refined_in: str, type_objects: bool, default_range: str | None
) -> None:
    """A slot of such an enum, refined without a range, is restricted to the enum, a data range.

    A subclass ``slot_usage`` keeps the range its parent gives, the ``slot_conditions`` of a class
    expression the range of the slot. The default range, or ``owl:Thing`` without one, is a class
    with ``type_objects`` or without a default range, which a data property cannot have (§5.8.1).
    """
    sb = _unit_schema([PermissibleValue(text=t) for t in "mk"])
    required = {"unit": {"required": True}}
    if refined_in == "class_expression":
        sb.add_class("Thing", slots=["unit"], any_of=[{"slot_conditions": required}], replace_if_present=True)
    else:
        if refined_in == "subclass_of_narrowing_parent":
            sb.add_enum("AnyUnitEnum", permissible_values=["m", "k", "mm"])
            sb.schema.slots["unit"].range = "AnyUnitEnum"
            sb.add_class("Thing", slots=["unit"], slot_usage={"unit": {"range": "UnitEnum"}}, replace_if_present=True)
        sb.add_class("Child", is_a="Thing", slot_usage=required)
    sb.schema.default_range = default_range
    g = _owl_graph(sb, default_permissible_value_type="rdfs:Literal", type_objects=type_objects)
    restrictions = set(g.subjects(OWL.onProperty, EX.unit))
    assert {g.value(r, OWL.allValuesFrom) for r in restrictions} - {None} == {EX.UnitEnum}
    assert set(g.objects(EX.unit, RDF.type)) == {OWL.DatatypeProperty}


def test_slot_of_enum_of_literals_or_a_class_stays_an_object_property() -> None:
    """With type_objects, a slot that ranges over an enum of literals and a class stays an object property."""
    sb = _unit_schema([PermissibleValue(text="m")])
    sb.add_slot("unit_or_thing", any_of=[{"range": "UnitEnum"}, {"range": "Thing"}])
    sb.add_class("Thing", slots=["unit", "unit_or_thing"], replace_if_present=True)
    g = _owl_graph(sb, default_permissible_value_type="rdfs:Literal", type_objects=True)
    assert set(g.objects(EX.unit, RDF.type)) == {OWL.DatatypeProperty}
    assert set(g.objects(EX.unit_or_thing, RDF.type)) == {OWL.ObjectProperty}


@pytest.mark.parametrize("type_objects", [False, True])
def test_slot_of_enums_of_literals_and_types(type_objects: bool) -> None:
    """A slot of an enum of literals and a type with literal values is a data property.

    With type_objects, the type is a class, and the slots stay object properties. Without, the
    enum as the range of ``unit_and_text`` would make it an object property, and ``unit_or_text``,
    which has no range and no class uses, would be one by default. The values of ``uriorcurie``
    are IRIs, so ``unit_or_iri`` stays one.
    """
    sb = _unit_schema([PermissibleValue(text="m")])
    sb.add_slot("unit_and_text", range="UnitEnum", any_of=[{"range": "string"}])
    sb.add_slot("unit_or_text", any_of=[{"range": "UnitEnum"}, {"range": "string"}])
    sb.add_slot("unit_or_iri", any_of=[{"range": "UnitEnum"}, {"range": "uriorcurie"}])
    sb.add_class("Thing", slots=["unit", "unit_and_text"], replace_if_present=True)
    sb.schema.default_range = None
    g = _owl_graph(sb, default_permissible_value_type="rdfs:Literal", type_objects=type_objects)
    expected = {OWL.ObjectProperty} if type_objects else {OWL.DatatypeProperty}
    assert set(g.objects(EX.unit_and_text, RDF.type)) == expected
    assert set(g.objects(EX.unit_or_text, RDF.type)) == expected
    assert set(g.objects(EX.unit_or_iri, RDF.type)) == {OWL.ObjectProperty}


@pytest.mark.parametrize("type_objects", [False, True])
@pytest.mark.parametrize(
    "default_range,unit,some_unit",
    [
        ("UnitEnum", OWL.DatatypeProperty, OWL.DatatypeProperty),
        ("Thing", OWL.ObjectProperty, OWL.ObjectProperty),
        (None, OWL.ObjectProperty, OWL.DatatypeProperty),
    ],
    ids=["enum", "class", "none"],
)
def test_default_range_and_members_of_enums_of_literals(
    default_range: str | None, unit: URIRef, some_unit: URIRef, type_objects: bool
) -> None:
    """The ranges of a slot include those of ``all_members`` and ``has_member``, and the default range.

    A restriction on a slot gets the default range if neither its ``range`` nor its expressions
    give one; ``has_member`` gives a restriction of its own, and ``range_expression`` a class
    expression if it has slot conditions. A slot without any range keeps the kind it has
    without enums of literals.
    """
    sb = SchemaBuilder()
    sb.add_enum("UnitEnum", permissible_values=["m", "k"])
    sb.add_slot("unit")
    sb.add_slot("all_units", multivalued=True, all_members={"range": "UnitEnum"})
    sb.add_slot("some_unit", multivalued=True, has_member={"range": "UnitEnum"})
    sb.add_slot("units_of_things", range="UnitEnum", multivalued=True, all_members={"range": "Thing"})
    sb.add_slot("units_and_a_thing", range="UnitEnum", multivalued=True, has_member={"range": "Thing"})
    with_units = {"slot_conditions": {"units_of_things": {"range": "UnitEnum"}}}
    sb.add_slot("thing_with_units", range_expression={"any_of": [with_units]})
    sb.add_slot(
        "units_and_a_thing_with_units", range="UnitEnum", multivalued=True, has_member={"range_expression": with_units}
    )
    sb.add_slot("units_without_expression", range="UnitEnum", range_expression={})
    sb.add_class("Thing", slots=["unit", "all_units", "some_unit", "units_of_things", "units_and_a_thing"])
    sb.add_defaults()
    sb.schema.default_range = default_range
    g = _owl_graph(sb, default_permissible_value_type="rdfs:Literal", type_objects=type_objects)
    assert set(g.objects(EX.unit, RDF.type)) == {unit}
    assert set(g.objects(EX.all_units, RDF.type)) == {OWL.DatatypeProperty}
    assert set(g.objects(EX.units_without_expression, RDF.type)) == {OWL.DatatypeProperty}
    assert set(g.objects(EX.some_unit, RDF.type)) == {some_unit}
    for slot in ("units_of_things", "units_and_a_thing", "thing_with_units", "units_and_a_thing_with_units"):
        assert set(g.objects(EX[slot], RDF.type)) == {OWL.ObjectProperty}, slot
    if default_range == "UnitEnum":
        assert {g.value(r, OWL.allValuesFrom) for r in g.subjects(OWL.onProperty, EX.unit)} - {None} == {EX.UnitEnum}


def test_slot_narrowed_to_an_enum_of_literals_is_a_data_property() -> None:
    """A slot without a range that a class narrows to such an enum is a data property, as for a type."""
    sb = SchemaBuilder()
    sb.add_enum("UnitEnum", permissible_values=["m", "k"])
    sb.add_slot("unit")
    sb.add_class("Thing", slots=["unit"], slot_usage={"unit": {"range": "UnitEnum"}})
    sb.add_defaults()
    sb.schema.default_range = None
    g = _owl_graph(sb, default_permissible_value_type="rdfs:Literal")
    assert set(g.objects(EX.unit, RDF.type)) == {OWL.DatatypeProperty}


def test_condition_on_an_undeclared_slot_keeps_the_default_range() -> None:
    """A class expression can name a slot that is not declared, which has no enum to restrict it to."""
    sb = _unit_schema([PermissibleValue(text="m")])
    sb.add_class(
        "Thing", slots=["unit"], any_of=[{"slot_conditions": {"other": {"required": True}}}], replace_if_present=True
    )
    g = _owl_graph(sb, default_permissible_value_type="rdfs:Literal")
    assert {g.value(r, OWL.allValuesFrom) for r in g.subjects(OWL.onProperty, EX.other)} - {None} == {XSD.string}


@pytest.mark.parametrize("default_range", [None, "string"])
@pytest.mark.parametrize("type_objects", [False, True])
def test_boolean_expressions_over_enums_of_literals_are_data_ranges(
    type_objects: bool, default_range: str | None
) -> None:
    """``any_of`` over datatype enums is a union of data ranges (§7.2), ``none_of`` a complement (§7.3).

    A slot whose ranges are all such enums is a data property in every mode, also if no class uses it.
    """
    sb = SchemaBuilder()
    sb.add_enum("UnitEnum", permissible_values=["m", "k"])
    sb.add_enum("SizeEnum", permissible_values=["S", "L"])
    sb.add_slot("unit_or_size", any_of=[{"range": "UnitEnum"}, {"range": "SizeEnum"}])
    sb.add_slot("not_unit", none_of=[{"range": "UnitEnum"}])
    sb.add_slot("unused", any_of=[{"range": "UnitEnum"}, {"range": "SizeEnum"}])
    sb.add_class("Thing", slots=["unit_or_size", "not_unit"])
    sb.add_defaults()
    sb.schema.default_range = default_range
    g = _owl_graph(sb, default_permissible_value_type="rdfs:Literal", type_objects=type_objects)
    unions = set(g.subjects(OWL.unionOf, None))
    assert unions
    assert all((union, RDF.type, RDFS.Datatype) in g for union in unions)
    assert set(g.subjects(OWL.datatypeComplementOf, EX.UnitEnum))
    assert not set(g.subjects(OWL.complementOf, None))
    for slot in ("unit_or_size", "not_unit", "unused"):
        assert set(g.objects(EX[slot], RDF.type)) == {OWL.DatatypeProperty}


_LITERAL_ENUM_SCHEMA = """
id: https://example.org/units
name: units
prefixes:
  linkml: https://w3id.org/linkml/
  rdfs: http://www.w3.org/2000/01/rdf-schema#
  ex: https://example.org/units/
default_prefix: ex
default_range: string
imports:
  - linkml:types
enums:
  UnitEnum:
    implements:
      - rdfs:Literal
    permissible_values:
      m:
      cm:
slots:
  id:
    identifier: true
    range: uriorcurie
  unit:
    range: UnitEnum
classes:
  Measurement:
    slots: [id, unit]
"""


@pytest.mark.parametrize("type_objects", [False, True])
def test_dumped_value_of_enum_of_literals_is_in_its_datatype(type_objects: bool) -> None:
    """The RDF dumper writes a permissible value without a meaning as a literal. In OWL, its slot
    is a data property (OWL 2 §5.4), whose range is the enum's datatype, an enumeration that holds
    this literal (§7.4), so the data that LinkML writes fits the ontology."""
    module = compile_python(PythonGenerator(_LITERAL_ENUM_SCHEMA).serialize())
    data = rdflib_dumper.as_rdf_graph(module.Measurement(id="ex:r1", unit="cm"), SchemaView(_LITERAL_ENUM_SCHEMA))
    owl = Graph().parse(
        data=OwlSchemaGenerator(_LITERAL_ENUM_SCHEMA, type_objects=type_objects, metaclasses=False).serialize(),
        format="turtle",
    )
    ex = Namespace("https://example.org/units/")
    [value] = data.objects(ex.r1, ex.unit)
    assert value == Literal("cm")
    assert set(owl.objects(ex.unit, RDF.type)) == {OWL.DatatypeProperty}
    assert owl.value(ex.unit, RDFS.range) == ex.UnitEnum
    [data_range] = owl.objects(ex.UnitEnum, OWL.equivalentClass)
    assert value in set(Collection(owl, owl.value(data_range, OWL.oneOf)))


def _all_values_from(g: Graph, slot: str) -> set:
    """Return the fillers of the ``owl:allValuesFrom`` restrictions on *slot*."""
    return {g.value(r, OWL.allValuesFrom) for r in g.subjects(OWL.onProperty, EX[slot])} - {None}


def test_slot_of_classes_is_an_object_property_with_their_union_as_range() -> None:
    """A slot whose ranges are all classes is an object property, also if the default range is a type.

    Its range is the union of the classes (OWL 2 §8.1.2, §9.2.6). A subclass that refines it
    without a range restricts it to ``owl:Thing``, as no datatype, such as the default range,
    fills an object property restriction (§8.2.2), and so it does a slot of an enum that is a class.
    """
    sb = SchemaBuilder()
    sb.add_class("Wheel")
    sb.add_class("Door")
    sb.add_enum("KindEnum", permissible_values=["scalar", "vector"])
    sb.add_slot("part", multivalued=True, any_of=[{"range": "Wheel"}, {"range": "Door"}])
    sb.add_slot("kind", range="KindEnum")
    sb.add_class("Car", slots=["part", "kind"])
    sb.add_class("Truck", is_a="Car", slot_usage={"part": {"required": True}, "kind": {"required": True}})
    sb.add_defaults()
    g = _owl_graph(sb)
    assert set(g.objects(EX.part, RDF.type)) == {OWL.ObjectProperty}
    fillers = _all_values_from(g, "part")
    unions = set(g.objects(EX.part, RDFS.range)) | {f for f in fillers if isinstance(f, BNode)}
    assert len(unions) == 2
    for union in unions:
        assert set(Collection(g, g.value(union, OWL.unionOf))) == {EX.Wheel, EX.Door}
    assert fillers - unions == {OWL.Thing}
    assert _all_values_from(g, "kind") == {EX.KindEnum, OWL.Thing}


@pytest.mark.parametrize("default_range", [None, "string"])
@pytest.mark.parametrize(
    "ranges",
    [["float", "Quantity"], ["UnitEnum", "Quantity"], ["UnitEnum", "KindEnum"]],
    ids=["type_and_class", "enum_of_literals_and_class", "enum_of_literals_and_class_enum"],
)
def test_slot_of_literals_and_nodes_has_no_range(caplog, ranges: list[str], default_range: str | None) -> None:
    """A slot that ranges over both literals and nodes, in its ``any_of`` or with its ``has_member``,
    is an object property without a range, and gen-owl warns about it once, not in each class.

    Neither an object nor a data property has both (OWL 2 §5.3, §5.4, §5.8.1), so the values of
    the slot are not restricted, also where a subclass refines it without a range. A subclass that
    narrows it to nodes restricts it, and its cardinalities stay.
    """
    sb = SchemaBuilder()
    sb.add_enum("UnitEnum", permissible_values=["m", "k"], implements=["rdfs:Literal"])
    sb.add_enum("KindEnum", permissible_values=["scalar", "vector"])
    sb.add_class("Quantity")
    sb.add_slot("speed", any_of=[{"range": r} for r in ranges])
    sb.add_slot("readings", range=ranges[0], multivalued=True, has_member={"range": ranges[1]})
    sb.add_class("Vehicle", slots=["speed", "readings"])
    sb.add_class("Car", is_a="Vehicle", slot_usage={"speed": {"required": True}})
    sb.add_class("Train", is_a="Vehicle", slot_usage={"speed": {"range": ranges[1]}})
    sb.add_defaults()
    sb.schema.default_range = default_range
    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        g = _owl_graph(sb)
    for slot in ("speed", "readings"):
        assert set(g.objects(EX[slot], RDF.type)) == {OWL.ObjectProperty}, slot
        assert not set(g.objects(EX[slot], RDFS.range)), slot
        message = (
            f"Slot {slot!r} ranges over both literals and nodes, which neither an object nor a data "
            "property can have, so it has no range and its values are not restricted"
        )
        assert caplog.messages.count(message) == 1, slot
    assert not [m for m in caplog.messages if m.startswith("In class")]
    assert _all_values_from(g, "speed") == {EX[ranges[1]]}
    assert not _all_values_from(g, "readings")
    assert not set(g.subjects(OWL.someValuesFrom))
    assert not {u for u in g.subjects(OWL.unionOf) if isinstance(u, BNode)}
    assert Literal(1) in {g.value(r, OWL.minCardinality) for r in g.subjects(OWL.onProperty, EX.speed)}


def test_branch_without_a_range_has_the_range_of_the_slot(caplog) -> None:
    """A branch of ``any_of`` without a range, such as one with only a ``pattern``, has the range
    of the expression it is in, or else of the slot, which a class that refines the slot takes
    from the slot, or else the default range.

    So a slot with a branch of an enum that is a class and a branch of only a pattern over the
    default range, a type, ranges over literals and nodes, and has no range, also if the branch is
    in another expression. A slot with such branches in an expression whose range is a class, or
    that a class refines with them where its range is a class, ranges over nodes.
    """
    sb = SchemaBuilder()
    sb.add_enum("LicenseEnum", permissible_values=["MIT", "Apache-2.0"])
    sb.add_class("Agent")
    sb.add_class("Person", is_a="Agent")
    sb.add_slot("license", any_of=[{"range": "LicenseEnum"}, {"pattern": "^LicenseRef-"}])
    sb.add_slot("rights", any_of=[{"range": "Agent"}, {"any_of": [{"range": "LicenseEnum"}, {"pattern": "^x"}]}])
    sb.add_slot("author", any_of=[{"range": "Agent", "any_of": [{"range": "Person"}, {"pattern": "^X"}]}])
    sb.add_slot("holder", range="Agent")
    sb.add_class("Package", slots=["license", "rights", "author", "holder"])
    sb.add_class("Book", is_a="Package", slot_usage={"holder": {"any_of": [{"range": "Person"}, {"pattern": "^O"}]}})
    sb.add_defaults()
    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        g = _owl_graph(sb)
    for name in ("license", "rights"):
        assert set(g.objects(EX[name], RDF.type)) == {OWL.ObjectProperty}
        assert not set(g.objects(EX[name], RDFS.range))
        assert not _all_values_from(g, name)
    for name in ("author", "holder"):
        assert set(g.objects(EX[name], RDF.type)) == {OWL.ObjectProperty}
        assert not [message for message in caplog.messages if repr(name) in message]


def test_class_expression_that_owl_cannot_state_is_left_out(caplog) -> None:
    """A class expression with a condition on a slot that ranges over both literals and nodes,
    which neither an object nor a data property can have, is left out where leaving out only the
    condition could make an axiom stronger: the ``any_of`` or ``exactly_one_of`` that it is an
    operand of, a rule with it in its preconditions or its postconditions, and a classification
    rule with it.

    Of ``all_of`` and ``none_of``, only that operand is left out, which makes the axiom weaker,
    also where the condition is in an expression in the operand. A slot whose ``range_expression``
    has such a condition, also that of its ``has_member``, of its ``all_members`` or of a branch
    of its ``any_of``, has no range, and its values are not restricted.
    """
    sb = SchemaBuilder()
    sb.add_class("Quantity")
    sb.add_class("Base")
    sb.add_class("Sub", is_a="Base")
    sb.add_slot("speed", any_of=[{"range": "float"}, {"range": "Quantity"}])
    sb.add_slot("part", range="Base")
    fast = {"slot_conditions": {"speed": {"minimum_value": 3}}}
    narrow = {"slot_conditions": {"part": {"range": "Sub"}}}
    sb.add_slot("fast_part", range="Base", range_expression=fast)
    sb.add_slot("fast_parts", range="Base", multivalued=True, has_member={"range_expression": fast})
    sb.add_slot("fast_or_sub", any_of=[{"range": "Sub"}, {"range": "Base", "range_expression": fast}])
    sb.add_slot("fast_list", range="Base", multivalued=True, all_members={"range_expression": fast})
    sb.add_class("Vehicle", slots=["speed", "part"], any_of=[fast, narrow])
    sb.add_class("Car", slots=["speed", "part"], none_of=[fast, narrow])
    sb.add_class("Van", slots=["speed", "part"], exactly_one_of=[fast, narrow])
    sb.add_class("Tram", slots=["speed", "part"], all_of=[{"any_of": [fast, narrow]}])
    sb.add_class(
        "Truck",
        slots=["speed", "part"],
        rules=[{"preconditions": fast, "postconditions": narrow}, {"preconditions": narrow, "postconditions": fast}],
    )
    sb.add_class(
        "Bike", slots=["speed", "part"], classification_rules=[{"slot_conditions": {**fast["slot_conditions"]}}]
    )
    sb.add_class("Garage", slots=["fast_part", "fast_parts", "fast_or_sub", "fast_list"])
    sb.add_defaults()
    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        g = _owl_graph(sb)
    assert not set(g.subjects(XSD.minInclusive))
    assert not set(g.subjects(OWL.someValuesFrom))
    assert len(set(g.subjects(OWL.allValuesFrom, EX.Sub))) == 1
    assert not set(g.objects(EX.Bike, OWL.equivalentClass))
    reason = "slot 'speed' ranges over both literals and nodes, which neither an object nor a data property can have"
    for name in ("fast_part", "fast_parts", "fast_or_sub", "fast_list"):
        assert not set(g.objects(EX[name], RDFS.range)), name
        assert not _all_values_from(g, name), name
        message = (
            f"Slot {name!r} ranges over a class expression in which {reason}, so it has no range and its values "
            "are not restricted"
        )
        assert message in caplog.messages
    for message in (
        f"The any_of of class 'Vehicle' is not emitted, since in one of its operands {reason}",
        f"An operand of the none_of of class 'Car' is not emitted, since in it {reason}",
        f"The exactly_one_of of class 'Van' is not emitted, since in one of its operands {reason}",
        f"An operand of the all_of of class 'Tram' is not emitted, since in it {reason}",
        f"A rule of class 'Truck' is not emitted, since in it {reason}",
        f"A classification rule of class 'Bike' is not emitted, since in it {reason}",
    ):
        assert message in caplog.messages


@pytest.mark.parametrize("default_range", [None, "string"])
def test_values_that_a_property_cannot_have_are_not_restricted(caplog, default_range: str | None) -> None:
    """Where a slot ranges over values that its property cannot have, literals for an object
    property or nodes for a data property (OWL 2 §5.3, §5.4), its values are not restricted,
    with a warning: where a class narrows it, for an attribute, and for the range of a slot
    that implements a property role, which has that role also without a range, with or
    without a default range.
    """
    sb = SchemaBuilder()
    sb.add_enum("UnitEnum", permissible_values=["m", "k"], implements=["rdfs:Literal"])
    sb.add_class("Quantity")
    sb.add_slot("speed", any_of=[{"range": "float"}, {"range": "Quantity"}])
    sb.add_slot("unit", any_of=[{"range": "UnitEnum"}, {"range": "Quantity"}])
    sb.add_slot("label", range="string")
    sb.add_slot("amount", range="Quantity", implements=["owl:DatatypeProperty"])
    sb.add_slot("weight", implements=["owl:DatatypeProperty"])
    sb.add_class("Vehicle", slots=["speed", "unit", "label", "amount", "weight"])
    sb.add_class(
        "Car",
        is_a="Vehicle",
        slot_usage={
            "speed": {"range": "float"},
            "unit": {"range": "UnitEnum"},
            "label": {"range": "Quantity"},
            "weight": {"range": "Quantity"},
        },
    )
    sb.add_class("Sensor", attributes={"reading": {"any_of": [{"range": "float"}, {"range": "Quantity"}]}})
    sb.add_defaults()
    sb.schema.default_range = default_range
    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        g = _owl_graph(sb)
    for name in ("speed", "unit", "amount", "reading"):
        assert not _all_values_from(g, name), name
    assert EX.Quantity not in _all_values_from(g, "weight")
    assert _all_values_from(g, "label") == {XSD.string}
    assert set(g.objects(EX.amount, RDF.type)) == {OWL.DatatypeProperty}
    assert not set(g.objects(EX.amount, RDFS.range))
    literals = "ranges over literals, but it is an object property, so its values there are not restricted"
    nodes = "ranges over nodes, but it is a data property, so its values there are not restricted"
    for message in (
        f"In class 'Car', slot 'speed' {literals}",
        f"In class 'Car', slot 'unit' {literals}",
        f"In class 'Car', slot 'label' {nodes}",
        f"In class 'Car', slot 'weight' {nodes}",
        "In class 'Sensor', slot 'reading' ranges over both literals and nodes, which neither an object nor a data "
        "property can have, so its values there are not restricted",
        "Slot 'amount' ranges over nodes, but it is a data property, so it has no range and its values are not "
        "restricted",
    ):
        assert caplog.messages.count(message) == 1, message


@pytest.mark.parametrize("default_range", [None, "string"])
def test_slot_has_the_kind_of_the_range_it_inherits(default_range: str | None) -> None:
    """A slot without a range inherits that of its nearest ancestor through ``is_a`` and its
    mixins, as ``SchemaView.induced_slot`` gives it, and so a sub-property has the kind of its
    super-property (OWL 2 §9.2.1, §9.3.1) instead of that of the default range."""
    sb = SchemaBuilder()
    sb.add_class("Person")
    sb.add_slot("ref", range="Person")
    sb.add_slot("owner", is_a="ref")
    sb.add_slot("previous_owner", is_a="owner")
    sb.add_slot("holder", mixins=["ref"])
    sb.add_slot("size", range="integer")
    sb.add_slot("width", is_a="size")
    sb.add_slot("reference", range="uriorcurie")
    sb.add_slot("homepage", is_a="reference")
    # a nearer ancestor's range comes first
    sb.add_slot("label", is_a="ref", range="string")
    sb.add_slot("short_label", is_a="label")
    sb.add_class(
        "Car",
        slots=["owner", "previous_owner", "holder", "width", "short_label", "homepage"],
        slot_usage={"owner": {"required": True}},
    )
    sb.add_defaults()
    sb.schema.default_range = default_range
    g = _owl_graph(sb)
    for prop in (EX.ref, EX.owner, EX.previous_owner, EX.holder, EX.reference, EX.homepage):
        assert set(g.objects(prop, RDF.type)) == {OWL.ObjectProperty}, prop
    for prop in (EX.size, EX.width, EX.short_label):
        assert set(g.objects(prop, RDF.type)) == {OWL.DatatypeProperty}, prop
    # the fillers of a class's restrictions have the kind of the property
    expected = {
        EX.owner: {OWL.Thing, EX.Person},
        EX.previous_owner: {OWL.Thing, EX.Person},
        EX.holder: {OWL.Thing, EX.Person},
        EX.width: {XSD.integer},
        EX.short_label: {XSD.string},
        EX.homepage: {OWL.Thing},
    }
    for prop, fillers in expected.items():
        restrictions = [r for r in g.objects(EX.Car, RDFS.subClassOf) if (r, OWL.onProperty, prop) in g]
        assert {g.value(r, OWL.allValuesFrom) for r in restrictions} - {None} <= fillers, prop


def test_attribute_of_several_classes_has_the_kind_of_its_definitions(caplog) -> None:
    """An attribute that several classes define has the kind of property that their definitions
    give, not that of the slot without a range that SchemaView gives for its name alone, so a
    subclass that narrows it to literals does not restrict it. Where its definitions, also that of
    a slot of its name, give different kinds, it has no single kind, and each class restricts it
    to its range.
    """
    sb = SchemaBuilder()
    sb.add_class("Person")
    sb.add_class("Dimensions")
    sb.add_slot("size", range="float")
    sb.add_class("Car", attributes={"owner": {"range": "Person"}, "size": {"range": "Dimensions"}})
    sb.add_class("Boat", slots=["size"], attributes={"owner": {"range": "Person"}})
    sb.add_class("Yacht", is_a="Boat", slot_usage={"owner": {"range": "string"}})
    sb.add_defaults()
    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        g = _owl_graph(sb)
    assert set(g.objects(EX.owner, RDF.type)) == {OWL.ObjectProperty}
    expected = {
        (EX.Car, EX.owner): {EX.Person},
        (EX.Boat, EX.owner): {EX.Person},
        (EX.Yacht, EX.owner): set(),
        (EX.Car, EX.size): {EX.Dimensions},
        (EX.Boat, EX.size): {XSD.float},
    }
    for (cls, prop), fillers in expected.items():
        restrictions = [r for r in g.objects(cls, RDFS.subClassOf) if (r, OWL.onProperty, prop) in g]
        assert {g.value(r, OWL.allValuesFrom) for r in restrictions} - {None} == fillers, (cls, prop)
    assert [message for message in caplog.messages if "not restricted" in message] == [
        "In class 'Yacht', slot 'owner' ranges over literals, but it is an object property, so its values there are "
        "not restricted"
    ]


@pytest.mark.parametrize(
    "slot",
    [
        {"any_of": [{"range": "float"}, {"range": "Typo"}]},
        {"range": "float", "multivalued": True, "has_member": {"range": "Typo"}},
    ],
    ids=["any_of", "has_member"],
)
def test_unknown_range_is_an_error(slot: dict) -> None:
    """A range that is no class, enum or type is an error, also beside a range of literals."""
    sb = SchemaBuilder()
    sb.add_slot("speed", **slot)
    sb.add_class("Vehicle", slots=["speed"])
    sb.add_defaults()
    with pytest.raises(ValueError, match="Unknown range Typo"):
        _owl_graph(sb)


@pytest.mark.parametrize(
    "ranges", [["integer", "boolean"], ["MissingValueEnum", "VitalStatusEnum"]], ids=["types", "enums_of_literals"]
)
def test_any_of_with_range_any_has_the_ranges_of_its_operands(caplog, ranges: list[str]) -> None:
    """A slot whose range is ``linkml:Any`` and further constrained by ``any_of`` ranges over its
    operands, so over data ranges it is a data property with their union as range (OWL 2 §7.2).

    ``linkml:Any`` is the class URI of the range, whatever its name, and a slot of that range
    alone is an object property.
    """
    sb = SchemaBuilder()
    sb.add_enum("MissingValueEnum", permissible_values=["INVALID", "NOT_PROVIDED"], implements=["rdfs:Literal"])
    sb.add_enum("VitalStatusEnum", permissible_values=["LIVING", "DECEASED"], implements=["rdfs:Literal"])
    sb.add_class("Anything", class_uri="linkml:Any")
    sb.add_slot("status", range="Anything", any_of=[{"range": r} for r in ranges])
    sb.add_slot("note", range="Anything")
    sb.add_class("Person", slots=["status", "note"])
    sb.add_defaults()
    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        g = _owl_graph(sb)
    assert set(g.objects(EX.status, RDF.type)) == {OWL.DatatypeProperty}
    for union in set(g.objects(EX.status, RDFS.range)) | _all_values_from(g, "status"):
        assert (union, RDF.type, RDFS.Datatype) in g
        assert len(list(Collection(g, g.value(union, OWL.unionOf)))) == 2
    assert set(g.objects(EX.note, RDF.type)) == {OWL.ObjectProperty}
    assert not [message for message in caplog.messages if "'status'" in message]


def test_has_member_branch_without_a_range_has_the_range_of_the_entry(caplog) -> None:
    """A branch of the ``has_member`` of a class's entry for a slot that gives no range has the
    range of the entry, not that of the slot.
    """
    sb = SchemaBuilder()
    sb.add_class("Anything", class_uri="linkml:Any")
    sb.add_slot("scores", range="Anything", multivalued=True)
    has_member = {"any_of": [{"minimum_value": 90}, {"maximum_value": 10}]}
    sb.add_class("Exam", slots=["scores"], slot_usage={"scores": {"range": "integer", "has_member": has_member}})
    sb.add_defaults()
    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        _owl_graph(sb)
    assert [message for message in caplog.messages if "'scores'" in message] == [
        "In class 'Exam', slot 'scores' ranges over literals, but it is an object property, so its values there are "
        "not restricted"
    ]


@pytest.mark.parametrize(
    "narrowed,role",
    [
        (["KindEnum"], OWL.ObjectProperty),
        (["KindEnum", "UnitEnum"], OWL.ObjectProperty),
        (["integer"], OWL.DatatypeProperty),
        (["uriorcurie"], OWL.ObjectProperty),
    ],
    ids=["class_enum", "class_enum_and_enum_of_literals", "type", "type_of_nodes"],
)
def test_slot_narrowed_by_classes_has_the_kind_of_their_ranges(caplog, narrowed: list[str], role: URIRef) -> None:
    """A slot without a range has the kind of the ranges that the classes that use it narrow it
    to: a data property for a type of literals, and an object property for a type of nodes or an
    enum that is a class, also if another class narrows it to an enum of literals.

    Its kind is known, as for a class, so it is not guessed, and neither an object nor a data
    property has both literals and nodes as values (OWL 2 §5.3, §5.4).
    """
    sb = SchemaBuilder()
    sb.add_enum("KindEnum", permissible_values=["scalar", "vector"])
    sb.add_enum("UnitEnum", permissible_values=["m", "k"], implements=["rdfs:Literal"])
    sb.add_slot("unit")
    for i, enum in enumerate(narrowed):
        sb.add_class(f"Thing{i}", slots=["unit"], slot_usage={"unit": {"range": enum}})
    sb.add_defaults()
    sb.schema.default_range = None
    with caplog.at_level(logging.WARNING, logger="linkml.generators.owlgen"):
        g = _owl_graph(sb)
    assert set(g.objects(EX.unit, RDF.type)) == {role}
    assert "Guessing type for unit" not in caplog.messages


def test_union_of_a_class_enum_and_a_type_object_is_a_class_expression() -> None:
    """With ``type_objects``, a type is a class, so ``any_of`` over a type and an enum that is a
    class, and ``exactly_one_of`` over types, are class expressions (OWL 2 §8.1), not data ranges
    (§7.2, §7.3).
    """
    sb = SchemaBuilder()
    sb.add_enum("KindEnum", permissible_values=["scalar", "vector"])
    sb.add_slot("kind", any_of=[{"range": "KindEnum"}, {"range": "string"}])
    sb.add_slot("count_or_name", exactly_one_of=[{"range": "integer"}, {"range": "string"}])
    sb.add_class("Thing", slots=["kind", "count_or_name"])
    sb.add_defaults()
    g = _owl_graph(sb, type_objects=True)
    for name in ("kind", "count_or_name"):
        assert set(g.objects(EX[name], RDF.type)) == {OWL.ObjectProperty}
    unions = {union for union in g.subjects(OWL.unionOf) if isinstance(union, BNode)}
    assert len(unions) == 4
    assert not any((union, RDF.type, RDFS.Datatype) in g for union in unions)
    assert set(g.subjects(OWL.complementOf)) and not set(g.subjects(OWL.datatypeComplementOf))


def test_intersection_of_a_class_enum_and_a_constraint_is_not_a_data_range() -> None:
    """An enum that is a class is a class expression (OWL 2 §8.1), as a class is, so its
    intersection with the data range of a constraint on the slot, here ``equals_string_in``,
    is not typed ``rdfs:Datatype`` (§7.1).
    """
    sb = SchemaBuilder()
    sb.add_enum("KindEnum", permissible_values=["scalar", "vector"])
    sb.add_slot("kind", range="KindEnum", equals_string_in=["scalar"])
    sb.add_class("Thing", slots=["kind"])
    sb.add_defaults()
    g = _owl_graph(sb)
    intersections = {
        e for e in g.subjects(OWL.intersectionOf) if EX.KindEnum in Collection(g, g.value(e, OWL.intersectionOf))
    }
    assert intersections
    assert not any((e, RDF.type, RDFS.Datatype) in g for e in intersections)


@pytest.mark.parametrize("default_range", [None, "string"])
def test_exactly_one_of_and_none_of_over_data_ranges_are_data_ranges(default_range: str | None) -> None:
    """``exactly_one_of`` over data ranges is a union of intersections of each with the complement
    of the others, and ``none_of`` a complement: all data ranges (OWL 2 §7.1–§7.3), also over the
    facets of a type and as operands of another expression.
    """
    sb = SchemaBuilder()
    sb.add_slot("count_or_name", exactly_one_of=[{"range": "integer"}, {"range": "string"}])
    sb.add_slot(
        "count_or_text", exactly_one_of=[{"range": "integer"}, {"any_of": [{"range": "string"}, {"range": "date"}]}]
    )
    sb.add_slot("code", range="string", exactly_one_of=[{"pattern": "^a"}, {"pattern": "^b"}])
    sb.add_slot("size", range="integer", exactly_one_of=[{"maximum_value": 5}, {"minimum_value": 3}])
    sb.add_slot("neither", range="string", any_of=[{"none_of": [{"pattern": "^a"}]}, {"none_of": [{"pattern": "b$"}]}])
    slots = ["count_or_name", "count_or_text", "code", "size", "neither"]
    sb.add_class("Thing", slots=slots)
    sb.add_defaults()
    sb.schema.default_range = default_range
    g = _owl_graph(sb)
    expressions = {e for p in (OWL.unionOf, OWL.intersectionOf, OWL.datatypeComplementOf) for e in g.subjects(p)}
    assert set(g.subjects(OWL.unionOf))
    assert all((e, RDF.type, RDFS.Datatype) in g for e in expressions)
    assert not set(g.subjects(OWL.complementOf))
    for slot in slots:
        assert set(g.objects(EX[slot], RDF.type)) == {OWL.DatatypeProperty}, slot
