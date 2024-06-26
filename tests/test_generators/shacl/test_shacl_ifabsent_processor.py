import pytest
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import ClassDefinitionName, SlotDefinitionName
from rdflib import SH, BNode, Graph, URIRef
from rdflib.term import Identifier, Literal

from linkml.generators.shacl.shacl_data_type import ShaclDataType
from linkml.generators.shacl.shacl_ifabsent_processor import ShaclIfAbsentProcessor

schema = """
id: ifabsent_tests
name: ifabsent_tests

prefixes:
  ex: https://example.org/
default_prefix: ex

classes:
  Student:
    attributes:
      - name: studentName
        range: string
        ifabsent: string(N/A)
      - name: presence
        range: PresenceEnum
        ifabsent: PresenceEnum(Missing)
      - name: thisURI
        range: uriorcurie
        ifabsent: class_curie
      - name: missing
        range: string
        ifabsent:
      - name: empty
        range: string
        ifabsent: string('')
      - name: incompatible
        range: decimal
        ifabsent: not a decimal
      - name: impossibleRange
        range: ImpossibleEnum
        ifabsent: ImpossibleEnum(DivideByZero)

enums:
  PresenceEnum:
    permissible_values:
      Present:
        description: It's there.
      Missing:
        description: It's not there.
"""


def test_process_ifabsent_literal():
    add_prop, attribute_node, graph, schema_view = initialize_graph()

    add_prop(SH.path, URIRef("ex:studentName"))
    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("studentName")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("N/A", datatype=ShaclDataType.STRING.uri_ref)


def test_process_class_curie():
    add_prop, attribute_node, graph, schema_view = initialize_graph()

    add_prop(SH.path, URIRef("ex:thisURI"))
    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("thisURI")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == URIRef("https://example.org/Student")


def test_process_ifabsent_enum():
    add_prop, attribute_node, graph, schema_view = initialize_graph()

    add_prop(SH.path, URIRef("ex:presence"))
    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("presence")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("Missing")


def test_process_missing_ifabsent_attribute():
    add_prop, attribute_node, graph, schema_view = initialize_graph()

    add_prop(SH.path, URIRef("ex:missing"))
    processor = ShaclIfAbsentProcessor(schema_view)

    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("missing")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        is None
    )


def test_process_empty_ifabsent_attribute():
    add_prop, attribute_node, graph, schema_view = initialize_graph()

    add_prop(SH.path, URIRef("ex:empty"))
    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("empty")], schema_view.all_classes()[ClassDefinitionName("Student")]
    ) == Literal("", datatype=ShaclDataType.STRING.uri_ref)


def test_process_incompatible_ifabsent_attribute():
    add_prop, attribute_node, graph, schema_view = initialize_graph()

    add_prop(SH.path, URIRef("ex:incompatible"))
    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("incompatible")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("not a decimal", datatype=ShaclDataType.DECIMAL.uri_ref)


def test_process_impossible_range_ifabsent_attribute():
    add_prop, attribute_node, graph, schema_view = initialize_graph()

    add_prop(SH.path, URIRef("ex:impossibleRange"))
    processor = ShaclIfAbsentProcessor(schema_view)

    with pytest.raises(ValueError) as e:
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("impossibleRange")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )

    assert str(e.value) == (
        "The ifabsent value `ImpossibleEnum(DivideByZero)` of the `impossibleRange` slot could not " "be processed"
    )


def initialize_graph():
    schema_view = SchemaView(schema)

    graph = Graph()
    class_node = BNode()
    graph.add((class_node, SH.targetClass, Literal("Student")))

    attribute_node = BNode()
    graph.add((class_node, SH.property, attribute_node))

    def add_prop(uri_ref: URIRef, object: Identifier):
        graph.add((attribute_node, uri_ref, object))

    return add_prop, attribute_node, graph, schema_view
