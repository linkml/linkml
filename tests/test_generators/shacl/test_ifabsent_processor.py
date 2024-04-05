import pytest
from linkml_runtime import SchemaView
from rdflib import SH, BNode, Graph, URIRef
from rdflib.term import Identifier, Literal

from linkml.generators.shacl.ifabsent_processor import IfAbsentProcessor
from linkml.generators.shacl.shacl_data_type import ShaclDataType

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
    processor = IfAbsentProcessor(schema_view)
    processor.process_slot(add_prop, schema_view.all_slots()["studentName"])

    assert (attribute_node, SH.defaultValue, Literal("N/A", datatype=ShaclDataType.STRING.uri_ref)) in graph


def test_process_class_curie():
    add_prop, attribute_node, graph, schema_view = initialize_graph()

    cls_uri = URIRef("https://example.org/Student")
    add_prop(SH.path, URIRef("ex:thisURI"))
    processor = IfAbsentProcessor(schema_view)
    processor.process_slot(add_prop, schema_view.all_slots()["thisURI"], cls_uri)

    assert (attribute_node, SH.defaultValue, URIRef(cls_uri)) in graph


def test_process_ifabsent_enum():
    add_prop, attribute_node, graph, schema_view = initialize_graph()

    add_prop(SH.path, URIRef("ex:presence"))
    processor = IfAbsentProcessor(schema_view)
    processor.process_slot(add_prop, schema_view.all_slots()["presence"])

    assert (attribute_node, SH.defaultValue, Literal("Missing")) in graph


def test_process_missing_ifabsent_attribute():
    add_prop, attribute_node, graph, schema_view = initialize_graph()

    add_prop(SH.path, URIRef("ex:missing"))
    processor = IfAbsentProcessor(schema_view)
    processor.process_slot(add_prop, schema_view.all_slots()["missing"])

    assert (attribute_node, SH.defaultValue, None) not in graph


def test_process_empty_ifabsent_attribute():
    add_prop, attribute_node, graph, schema_view = initialize_graph()

    add_prop(SH.path, URIRef("ex:empty"))
    processor = IfAbsentProcessor(schema_view)
    processor.process_slot(add_prop, schema_view.all_slots()["empty"])

    assert (attribute_node, SH.defaultValue, Literal("", datatype=ShaclDataType.STRING.uri_ref)) in graph


def test_process_incompatible_ifabsent_attribute():
    add_prop, attribute_node, graph, schema_view = initialize_graph()

    add_prop(SH.path, URIRef("ex:incompatible"))
    processor = IfAbsentProcessor(schema_view)
    processor.process_slot(add_prop, schema_view.all_slots()["incompatible"])

    assert (attribute_node, SH.defaultValue, Literal("not a decimal", datatype=ShaclDataType.DECIMAL.uri_ref)) in graph


def test_process_impossible_range_ifabsent_attribute():
    add_prop, attribute_node, graph, schema_view = initialize_graph()

    add_prop(SH.path, URIRef("ex:impossibleRange"))
    processor = IfAbsentProcessor(schema_view)

    with pytest.raises(ValueError) as e:
        processor.process_slot(add_prop, schema_view.all_slots()["impossibleRange"])

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
