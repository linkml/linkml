import json
import logging
import re
from collections import Counter
from typing import Any

import pytest
import rdflib
from rdflib import RDF, RDFS, SH, XSD, Literal, URIRef
from rdflib.collection import Collection

from linkml.generators.shacl.shacl_data_type import ShaclDataType
from linkml.generators.shaclgen import ShaclGenerator
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.utils.schema_builder import SchemaBuilder

EXPECTED = [
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/Person"),
        rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
        rdflib.term.URIRef("http://www.w3.org/ns/shacl#NodeShape"),
    ),
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/Person"),
        rdflib.term.URIRef("http://www.w3.org/ns/shacl#closed"),
        rdflib.term.Literal("true", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#boolean")),
    ),
]

EXPECTED_closed = [
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/Person"),
        rdflib.term.URIRef("http://www.w3.org/ns/shacl#closed"),
        rdflib.term.Literal("false", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#boolean")),
    ),
]

EXPECTED_suffix = [
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/PersonShape"),
        rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
        rdflib.term.URIRef("http://www.w3.org/ns/shacl#NodeShape"),
    ),
]


def test_as_graph_materializes_structured_patterns(input_path) -> None:
    """Resolve structured patterns without modifying the source schema."""
    generator = ShaclGenerator(input_path("pattern-example.yaml"))
    height_slot = generator.schemaview.get_slot("height")
    email_type = generator.schemaview.get_type("EmailString")

    assert height_slot.pattern is None
    assert email_type.pattern is None

    graph = generator.as_graph()

    assert Literal(r"^(?:\d+[\.\d+] (centimeter|meter|inch))$") in graph.objects(None, SH.pattern)
    assert Literal(r"^(?:\S+@\S+{\.\w}+)$") in graph.objects(None, SH.pattern)
    assert height_slot.pattern is None
    assert email_type.pattern is None


EXPECTED_any_of = [
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/AnyOfSimpleType"),
        [
            (
                rdflib.term.URIRef("http://www.w3.org/ns/shacl#datatype"),
                rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#integer"),
            ),
            (
                rdflib.term.URIRef("http://www.w3.org/ns/shacl#datatype"),
                rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#string"),
            ),
        ],
    ),
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/AnyOfClasses"),
        [
            (
                rdflib.term.URIRef("http://www.w3.org/ns/shacl#class"),
                rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/Person"),
            ),
            (
                rdflib.term.URIRef("http://www.w3.org/ns/shacl#class"),
                rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/Organization"),
            ),
        ],
    ),
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/AnyOfEnums"),
        [
            (
                rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
                rdflib.term.URIRef("https://example.org/bizcodes/001"),
            ),
            (
                rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
                rdflib.term.URIRef("https://example.org/bizcodes/002"),
            ),
            (
                rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
                rdflib.term.URIRef("https://example.org/bizcodes/003"),
            ),
            (
                rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
                rdflib.term.URIRef("https://example.org/bizcodes/004"),
            ),
            (rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"), rdflib.term.Literal("TODO")),
        ],
    ),
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/AnyOfMix"),
        [
            (
                rdflib.term.URIRef("http://www.w3.org/ns/shacl#datatype"),
                rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#integer"),
            ),
            (
                rdflib.term.URIRef("http://www.w3.org/ns/shacl#class"),
                rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/Person"),
            ),
            (
                rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
                rdflib.term.URIRef("https://example.org/bizcodes/001"),
            ),
            (
                rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
                rdflib.term.URIRef("https://example.org/bizcodes/002"),
            ),
            (
                rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
                rdflib.term.URIRef("https://example.org/bizcodes/003"),
            ),
            (
                rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
                rdflib.term.URIRef("https://example.org/bizcodes/004"),
            ),
        ],
    ),
]

EXPECTED_any_of_with_suffix = [
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/AnyOfSimpleTypeShape"),
        [
            (
                rdflib.term.URIRef("http://www.w3.org/ns/shacl#datatype"),
                rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#integer"),
            ),
            (
                rdflib.term.URIRef("http://www.w3.org/ns/shacl#datatype"),
                rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#string"),
            ),
        ],
    ),
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/AnyOfClassesShape"),
        [
            (
                rdflib.term.URIRef("http://www.w3.org/ns/shacl#class"),
                rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/Person"),
            ),
            (
                rdflib.term.URIRef("http://www.w3.org/ns/shacl#class"),
                rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/Organization"),
            ),
        ],
    ),
]

EXPECTED_with_annotations = [
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/Person"),
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/viewer"),
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/PersonViewer"),
    ),
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/Person"),
        rdflib.term.Literal("resting", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#string")),
        rdflib.term.Literal("supine", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#string")),
    ),
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/Person"),
        rdflib.term.Literal("opinions", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#string")),
        rdflib.term.Literal("1000", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#integer")),
    ),
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/Person"),
        rdflib.term.Literal("fallible", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#string")),
        rdflib.term.Literal("true", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#boolean")),
    ),
]

EXPECTED_equals_string = [
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/EqualsString"),
        [
            (
                rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
                rdflib.term.Literal("foo"),
            ),
        ],
    ),
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/EqualsStringIn"),
        [
            (
                rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
                rdflib.term.Literal("bar"),
            ),
            (
                rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
                rdflib.term.Literal("foo"),
            ),
        ],
    ),
]

EXPECTED_equals_string_with_suffix = [
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/EqualsStringShape"),
        [
            (
                rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
                rdflib.term.Literal("foo"),
            ),
        ],
    ),
    (
        rdflib.term.URIRef("https://w3id.org/linkml/tests/kitchen_sink/EqualsStringInShape"),
        [
            (
                rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
                rdflib.term.Literal("bar"),
            ),
            (
                rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
                rdflib.term.Literal("foo"),
            ),
        ],
    ),
]


def test_shacl(kitchen_sink_path):
    """tests shacl generation"""
    shaclstr = ShaclGenerator(kitchen_sink_path, mergeimports=True).serialize()
    do_test(shaclstr, EXPECTED, EXPECTED_any_of, EXPECTED_equals_string)


def test_shacl_closed(kitchen_sink_path):
    """tests shacl generation"""
    shaclstr = ShaclGenerator(kitchen_sink_path, mergeimports=True, closed=False).serialize()
    do_test(shaclstr, EXPECTED_closed, EXPECTED_any_of, EXPECTED_equals_string)


def test_shacl_suffix(kitchen_sink_path):
    """tests shacl generation with suffix option"""
    shaclstr = ShaclGenerator(kitchen_sink_path, mergeimports=True, closed=True, suffix="Shape").serialize()
    do_test(shaclstr, EXPECTED_suffix, EXPECTED_any_of_with_suffix, EXPECTED_equals_string_with_suffix)


def test_shacl_annotations(kitchen_sink_path):
    """tests shacl generation with annotation option"""
    shaclstr = ShaclGenerator(kitchen_sink_path, mergeimports=True, include_annotations=True).serialize()
    do_test(shaclstr, EXPECTED_with_annotations, EXPECTED_any_of, EXPECTED_equals_string)


def do_test(shaclstr, expected, expected_any_of, expected_equals_string):
    g = rdflib.Graph()
    g.parse(data=shaclstr)
    triples = list(g.triples((None, None, None)))
    for et in expected:
        assert et in triples
    # TODO: test shacl validation; pyshacl requires rdflib6

    assert_any_of(expected_any_of, triples)
    assert_equals_string(expected_equals_string, triples)


def assert_equals_string(
    expected: list[tuple[rdflib.term.URIRef, list[tuple[rdflib.term.URIRef, rdflib.term.URIRef]]]], triples: list
) -> None:
    for ex in expected:
        found = False
        # look for "property" triplet
        for property_triple in triples:
            if property_triple[0] == ex[0] and property_triple[1] == rdflib.term.URIRef(
                "http://www.w3.org/ns/shacl#property"
            ):
                # look for "or" triplet
                for path_triplet in triples:
                    if path_triplet[0] == property_triple[2] and path_triplet[1] == rdflib.term.URIRef(
                        "http://www.w3.org/ns/shacl#in"
                    ):
                        found = True
                        for tuple in ex[1]:
                            assert tuple in _get_data_type(path_triplet[2], triples)
        if not found:
            print(str(ex) + "not found")
            assert False


def assert_any_of(
    expected: list[tuple[rdflib.term.URIRef, list[tuple[rdflib.term.URIRef, rdflib.term.URIRef]]]], triples: list
) -> None:
    for ex in expected:
        found = False
        for property_triple in triples:
            # look for "property" triplet
            if property_triple[0] == ex[0] and property_triple[1] == rdflib.term.URIRef(
                "http://www.w3.org/ns/shacl#property"
            ):
                # look for "or" triplet
                for or_triplet in triples:
                    if or_triplet[0] == property_triple[2] and or_triplet[1] == rdflib.term.URIRef(
                        "http://www.w3.org/ns/shacl#or"
                    ):
                        found = True
                        assert Counter(_get_data_type(or_triplet[2], triples)) == Counter(ex[1])
        if not found:
            print(str(ex) + "not found")
            assert False


def assert_equals(
    expected: list[tuple[rdflib.term.URIRef, list[tuple[rdflib.term.URIRef, rdflib.term.URIRef]]]], triples: list
) -> None:
    for ex in expected:
        found = False
        for property_triple in triples:
            # look for "property" triplet
            if property_triple[0] == ex[0] and property_triple[1] == rdflib.term.URIRef(
                "http://www.w3.org/ns/shacl#property"
            ):
                # look for "or" triplet
                for or_triplet in triples:
                    if or_triplet[0] == property_triple[2] and or_triplet[1] == rdflib.term.URIRef(
                        "http://www.w3.org/ns/shacl#or"
                    ):
                        found = True
                        assert Counter(_get_data_type(or_triplet[2], triples)) == Counter(ex[1])
        if not found:
            print(str(ex) + "not found")
            assert False


def _get_data_type(blank_node: rdflib.term.BNode, triples: list) -> list[rdflib.term.URIRef]:
    """
    Any of refers a list of nodes, which are either
     - rdflib.term.URIRef('http://www.w3.org/ns/shacl#in') for enumerations
     - rdflib.term.URIRef('http://www.w3.org/ns/shacl#datatype') for simple datatypes
     - rdflib.term.URIRef('http://www.w3.org/ns/shacl#class') for classes

    Go through list of rdf triples and return all nodes referred be GIVEN any of node.
    """
    datatypes = []
    for node_triplet in triples:
        if node_triplet[0] == blank_node:
            # look for first node
            if node_triplet[1] == rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"):
                # parsing first rdf triples of list
                if isinstance(node_triplet[2], rdflib.Literal):
                    # we found a leaf as first node
                    datatypes.append(
                        (rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"), node_triplet[2])
                    )
                elif isinstance(node_triplet[2], rdflib.BNode):
                    # we found a blank node and have to retrieve all triples, which have blank node as origin
                    datatypes.extend(_get_data_type(node_triplet[2], triples))
                elif isinstance(node_triplet[2], rdflib.term.URIRef):
                    # we found a URI as first node
                    if node_triplet[1] == rdflib.term.URIRef("http://www.w3.org/ns/shacl#in"):
                        # we found an enumeration
                        datatypes.extend(_get_data_type(node_triplet[2], triples))
                    else:
                        datatypes.append((node_triplet[1], node_triplet[2]))
            elif node_triplet[1] == rdflib.term.URIRef("http://www.w3.org/ns/shacl#in"):
                # we found an enumeration
                datatypes.extend(_get_data_type(node_triplet[2], triples))
            elif node_triplet[1] == rdflib.term.URIRef("http://www.w3.org/ns/shacl#datatype"):
                # we found a data type
                datatypes.append((node_triplet[1], node_triplet[2]))
            elif node_triplet[1] == rdflib.term.URIRef("http://www.w3.org/ns/shacl#class"):
                # we found a data type
                datatypes.append((node_triplet[1], node_triplet[2]))
            # look for remaining rdf triples in list
            elif node_triplet[1] == rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#rest"):
                datatypes.extend(_get_data_type(node_triplet[2], triples))
    return datatypes


def test_ifabsent(input_path):
    """Test that the LinkML ifabsent attribute is supported by ShaclGenerator"""
    shacl = ShaclGenerator(input_path("kitchen_sink_ifabsent.yaml"), mergeimports=True).serialize()
    g = rdflib.Graph()
    g.parse(data=shacl)

    def check_slot_default_value(slot: URIRef, default_value: Any, datatype: str = None) -> None:
        for subject, predicate, object in g.triples((None, SH.path, slot)):
            # pyoxigraph's RDFC-1.0 serialization drops explicit ^^xsd:string
            # per RDF 1.1 (plain literals and xsd:string are equivalent).
            # Accept either form for xsd:string typed values.
            expected = Literal(default_value, datatype=datatype)
            if (subject, SH.defaultValue, expected) in g:
                return
            if datatype and str(datatype) == "http://www.w3.org/2001/XMLSchema#string":
                if (subject, SH.defaultValue, Literal(default_value)) in g:
                    return
            raise AssertionError(f"Expected ({subject}, sh:defaultValue, {expected!r}) not found in graph")

    check_slot_default_value(
        URIRef("https://w3id.org/linkml/tests/kitchen_sink/ifabsent_string"),
        "This works",
        datatype=ShaclDataType.STRING.uri_ref,
    )
    check_slot_default_value(
        URIRef("https://w3id.org/linkml/tests/kitchen_sink/ifabsent_boolean"),
        True,
        datatype=ShaclDataType.BOOLEAN.uri_ref,
    )
    check_slot_default_value(
        URIRef("https://w3id.org/linkml/tests/kitchen_sink/ifabsent_int"), 123, datatype=ShaclDataType.INTEGER.uri_ref
    )
    check_slot_default_value(
        URIRef("https://w3id.org/linkml/tests/kitchen_sink/ifabsent_decimal"),
        1.23,
        datatype=ShaclDataType.DECIMAL.uri_ref,
    )
    check_slot_default_value(
        URIRef("https://w3id.org/linkml/tests/kitchen_sink/ifabsent_float"),
        1.23456,
        datatype=ShaclDataType.FLOAT.uri_ref,
    )
    check_slot_default_value(
        URIRef("https://w3id.org/linkml/tests/kitchen_sink/ifabsent_double"),
        1.234567,
        datatype=ShaclDataType.DOUBLE.uri_ref,
    )
    check_slot_default_value(
        URIRef("https://w3id.org/linkml/tests/kitchen_sink/ifabsent_date"),
        "2024-02-08",
        datatype=ShaclDataType.DATE.uri_ref,
    )
    check_slot_default_value(
        URIRef("https://w3id.org/linkml/tests/kitchen_sink/ifabsent_datetime"),
        "2024-02-08T09:39:25",
        datatype=ShaclDataType.DATETIME.uri_ref,
    )
    check_slot_default_value(
        URIRef("https://w3id.org/linkml/tests/kitchen_sink/ifabsent_uri"),
        "https://w3id.org/linkml/tests/kitchen_sink/ifabsent_boolean",
        datatype=ShaclDataType.URI.uri_ref,
    )
    check_slot_default_value(URIRef("https://w3id.org/linkml/tests/kitchen_sink/ifabsent_not_literal"), "heartfelt")


def test_custom_class_range_is_blank_node_or_iri(input_path):
    shacl = ShaclGenerator(input_path("shaclgen/custom_class_range.yaml"), mergeimports=True).serialize()

    g = rdflib.Graph()
    g.parse(data=shacl)

    container_properties = g.objects(URIRef("https://w3id.org/linkml/examples/personinfo/Container"), SH.property)
    persons_node = next(container_properties, None)
    assert persons_node

    assert (persons_node, SH.nodeKind, SH.BlankNodeOrIRI) in g


def test_slot_with_annotations_and_any_of(input_path):
    shacl = ShaclGenerator(
        input_path("shaclgen/boolean_constraints.yaml"), mergeimports=True, include_annotations=True
    ).serialize()

    g = rdflib.Graph()
    g.parse(data=shacl)

    class_properties = g.objects(
        URIRef("https://w3id.org/linkml/examples/boolean_constraints/AnyOfSimpleType"), SH.property
    )
    attribute_node = next(class_properties, None)
    assert attribute_node

    assert (
        attribute_node,
        rdflib.term.Literal("resting", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#string")),
        rdflib.term.Literal("supine", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#string")),
    ) in g


def test_ignore_subclass_properties(input_path):
    shacl = ShaclGenerator(input_path("shaclgen/subclass_ignored_properties.yaml"), mergeimports=True).serialize()

    g = rdflib.Graph()
    g.parse(data=shacl)

    count = 0
    ignored_properties = {}
    for triple in g.triples((None, SH.ignoredProperties, None)):
        count += 1
        (subject, predicate, object) = triple
        ignored_properties[subject] = list(Collection(g, object))

    assert count == 7
    assert frozenset(ignored_properties[URIRef("https://w3id.org/linkml/examples/animals/Animal")]) == frozenset(
        [
            URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
            URIRef("https://w3id.org/linkml/examples/animals/maxAltitude"),
            URIRef("https://w3id.org/linkml/examples/animals/maxDepth"),
            URIRef("https://w3id.org/linkml/examples/animals/mammaryGlandCount"),
            URIRef("https://w3id.org/linkml/examples/animals/ocean"),
            URIRef("https://w3id.org/linkml/examples/animals/name"),
        ]
    )
    assert frozenset(ignored_properties[URIRef("https://w3id.org/linkml/examples/animals/CanFly")]) == frozenset(
        [URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")]
    )
    assert frozenset(ignored_properties[URIRef("https://w3id.org/linkml/examples/animals/CanSwim")]) == frozenset(
        [URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")]
    )
    assert frozenset(ignored_properties[URIRef("https://w3id.org/linkml/examples/animals/Mammal")]) == frozenset(
        [
            URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
            URIRef("https://w3id.org/linkml/examples/animals/maxAltitude"),
            URIRef("https://w3id.org/linkml/examples/animals/maxDepth"),
            URIRef("https://w3id.org/linkml/examples/animals/ocean"),
            URIRef("https://w3id.org/linkml/examples/animals/name"),
        ]
    )
    assert frozenset(ignored_properties[URIRef("https://w3id.org/linkml/examples/animals/Whale")]) == frozenset(
        [URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")]
    )
    assert frozenset(ignored_properties[URIRef("https://w3id.org/linkml/examples/animals/Dog")]) == frozenset(
        [URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")]
    )
    assert frozenset(ignored_properties[URIRef("https://w3id.org/linkml/examples/animals/Bat")]) == frozenset(
        [URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")]
    )


def test_ignored_properties_list_is_sorted(input_path):
    """sh:ignoredProperties RDF list elements must be in deterministic order.

    Regression test for https://github.com/linkml/linkml/issues/3516: the
    set holding ignored properties was iterated in PYTHONHASHSEED-dependent
    order, producing non-isomorphic graphs across processes that
    RDFC-1.0 canonicalization could not normalize.
    """
    shacl = ShaclGenerator(input_path("shaclgen/subclass_ignored_properties.yaml"), mergeimports=True).serialize()
    g = rdflib.Graph()
    g.parse(data=shacl)

    lists_checked = 0
    for _, _, list_node in g.triples((None, SH.ignoredProperties, None)):
        elements = [str(e) for e in Collection(g, list_node)]
        assert elements == sorted(elements), f"sh:ignoredProperties list not sorted: {elements}"
        lists_checked += 1
    assert lists_checked == 7


def test_multivalued_slot_min_cardinality(input_path):
    shacl = ShaclGenerator(input_path("shaclgen/cardinality.yaml"), mergeimports=True).serialize()

    g = rdflib.Graph()
    g.parse(data=shacl)

    variable_class_properties = g.objects(
        URIRef("https://w3id.org/linkml/examples/cardinality/VariableClass"), SH.property
    )
    variable_size_list_node = next(variable_class_properties, None)
    assert variable_size_list_node

    assert (
        variable_size_list_node,
        SH.minCount,
        rdflib.term.Literal("2", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#integer")),
    ) in g


def test_multivalued_slot_max_cardinality(input_path):
    shacl = ShaclGenerator(input_path("shaclgen/cardinality.yaml"), mergeimports=True).serialize()

    g = rdflib.Graph()
    g.parse(data=shacl)

    variable_class_properties = g.objects(
        URIRef("https://w3id.org/linkml/examples/cardinality/VariableClass"), SH.property
    )
    variable_size_list_node = next(variable_class_properties, None)
    assert variable_size_list_node

    assert (
        variable_size_list_node,
        SH.maxCount,
        rdflib.term.Literal("5", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#integer")),
    ) in g


def test_multivalued_slot_exact_cardinality(input_path):
    shacl = ShaclGenerator(input_path("shaclgen/cardinality.yaml"), mergeimports=True).serialize()

    g = rdflib.Graph()
    g.parse(data=shacl)

    exact_class_properties = g.objects(URIRef("https://w3id.org/linkml/examples/cardinality/ExactClass"), SH.property)
    exact_size_list_node = next(exact_class_properties, None)
    assert exact_size_list_node

    assert (
        exact_size_list_node,
        SH.minCount,
        rdflib.term.Literal("3", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#integer")),
    ) in g
    assert (
        exact_size_list_node,
        SH.maxCount,
        rdflib.term.Literal("3", datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#integer")),
    ) in g


def test_zero_maximum_cardinality_emits_maxcount(input_path):
    """Test that maximum_cardinality: 0 correctly emits sh:maxCount 0.

    Regression test for the bug where Python truthiness check
    `if s.maximum_cardinality:` would skip the value 0 (falsy),
    failing to emit sh:maxCount 0 in the generated SHACL shape.
    The fix uses `if s.maximum_cardinality is not None:` instead.

    This is the primary mechanism for suppressing inherited slots on
    subclasses via slot_usage (e.g., OWL maxCardinality 0 pattern).
    """
    shacl = ShaclGenerator(input_path("shaclgen/cardinality.yaml"), mergeimports=True).serialize()

    g = rdflib.Graph()
    g.parse(data=shacl)

    # Find the ChildWithZeroMaxCard shape
    child_uri = URIRef("https://w3id.org/linkml/examples/cardinality/ChildWithZeroMaxCard")
    restricted_slot_uri = URIRef("https://w3id.org/linkml/examples/cardinality/restricted_slot")

    # Get all property shapes for the child class
    prop_nodes = list(g.objects(child_uri, SH.property))
    assert prop_nodes, "ChildWithZeroMaxCard should have property shapes"

    # Find the property shape for restricted_slot
    restricted_prop_node = None
    for pn in prop_nodes:
        if (pn, SH.path, restricted_slot_uri) in g:
            restricted_prop_node = pn
            break
    assert restricted_prop_node is not None, "Should have a property shape for restricted_slot"

    # The critical assertion: sh:maxCount 0 must be emitted
    max_count_values = list(g.objects(restricted_prop_node, SH.maxCount))
    assert len(max_count_values) == 1, f"Expected exactly one sh:maxCount, got {max_count_values}"
    assert max_count_values[0] == rdflib.term.Literal(
        0, datatype=rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#integer")
    ), f"sh:maxCount should be 0, got {max_count_values[0]}"


def test_zero_exact_cardinality_emits_both_counts(input_path):
    """Test that exact_cardinality: 0 emits both sh:minCount 0 and sh:maxCount 0.

    Same truthiness bug as maximum_cardinality: `if s.exact_cardinality:`
    skips value 0 (falsy). The fix uses `is not None` instead.
    """
    shacl = ShaclGenerator(input_path("shaclgen/cardinality.yaml"), mergeimports=True).serialize()

    g = rdflib.Graph()
    g.parse(data=shacl)

    child_uri = URIRef("https://w3id.org/linkml/examples/cardinality/ChildWithZeroExactCard")
    restricted_slot_uri = URIRef("https://w3id.org/linkml/examples/cardinality/restricted_slot")

    prop_nodes = list(g.objects(child_uri, SH.property))
    assert prop_nodes, "ChildWithZeroExactCard should have property shapes"

    restricted_prop_node = None
    for pn in prop_nodes:
        if (pn, SH.path, restricted_slot_uri) in g:
            restricted_prop_node = pn
            break
    assert restricted_prop_node is not None, "Should have a property shape for restricted_slot"

    XSD_INT = rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#integer")

    min_count_values = list(g.objects(restricted_prop_node, SH.minCount))
    assert len(min_count_values) == 1, f"Expected exactly one sh:minCount, got {min_count_values}"
    assert min_count_values[0] == rdflib.term.Literal(0, datatype=XSD_INT)

    max_count_values = list(g.objects(restricted_prop_node, SH.maxCount))
    assert len(max_count_values) == 1, f"Expected exactly one sh:maxCount, got {max_count_values}"
    assert max_count_values[0] == rdflib.term.Literal(0, datatype=XSD_INT)


def test_zero_minimum_cardinality_emits_mincount(input_path):
    """Test that minimum_cardinality: 0 emits sh:minCount 0.

    Same truthiness bug as maximum_cardinality: `if s.minimum_cardinality:`
    skips value 0 (falsy). The fix uses `is not None` instead. sh:minCount 0
    is vacuously satisfied (W3C SHACL 4.2.2) but is emitted for consistency
    with owlgen (owl:minCardinality 0) and to faithfully reflect the schema.
    """
    shacl = ShaclGenerator(input_path("shaclgen/cardinality.yaml"), mergeimports=True).serialize()

    g = rdflib.Graph()
    g.parse(data=shacl)

    child_uri = URIRef("https://w3id.org/linkml/examples/cardinality/ChildWithZeroMinCard")
    restricted_slot_uri = URIRef("https://w3id.org/linkml/examples/cardinality/restricted_slot")

    prop_nodes = list(g.objects(child_uri, SH.property))
    assert prop_nodes, "ChildWithZeroMinCard should have property shapes"

    restricted_prop_node = None
    for pn in prop_nodes:
        if (pn, SH.path, restricted_slot_uri) in g:
            restricted_prop_node = pn
            break
    assert restricted_prop_node is not None, "Should have a property shape for restricted_slot"

    XSD_INT = rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#integer")

    min_count_values = list(g.objects(restricted_prop_node, SH.minCount))
    assert len(min_count_values) == 1, f"Expected exactly one sh:minCount, got {min_count_values}"
    assert min_count_values[0] == rdflib.term.Literal(0, datatype=XSD_INT)


def test_explicit_minimum_cardinality_overrides_required(input_path):
    """An explicit minimum_cardinality: 0 takes precedence over required: true.

    The generator resolves min-count with an ``elif`` cascade in which an
    explicit ``minimum_cardinality`` wins and ``required`` is only the fallback.
    This mirrors owlgen.py (``if slot.minimum_cardinality is not None ... elif
    slot.required``), so ``required: true`` + ``minimum_cardinality: 0`` yields
    ``sh:minCount 0`` (not 1). The combination is a schema contradiction; the
    explicit, more specific constraint is emitted.
    """
    shacl = ShaclGenerator(input_path("shaclgen/cardinality.yaml"), mergeimports=True).serialize()

    g = rdflib.Graph()
    g.parse(data=shacl)

    child_uri = URIRef("https://w3id.org/linkml/examples/cardinality/ChildWithRequiredAndZeroMinCard")
    restricted_slot_uri = URIRef("https://w3id.org/linkml/examples/cardinality/restricted_slot")

    prop_nodes = list(g.objects(child_uri, SH.property))
    assert prop_nodes, "ChildWithRequiredAndZeroMinCard should have property shapes"

    restricted_prop_node = None
    for pn in prop_nodes:
        if (pn, SH.path, restricted_slot_uri) in g:
            restricted_prop_node = pn
            break
    assert restricted_prop_node is not None, "Should have a property shape for restricted_slot"

    XSD_INT = rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#integer")

    min_count_values = list(g.objects(restricted_prop_node, SH.minCount))
    assert len(min_count_values) == 1, f"Expected exactly one sh:minCount, got {min_count_values}"
    assert min_count_values[0] == rdflib.term.Literal(0, datatype=XSD_INT), (
        f"explicit minimum_cardinality: 0 should override required: true (minCount 0, not 1), got {min_count_values[0]}"
    )


def test_exclude_imports(input_path):
    shacl = ShaclGenerator(
        input_path("shaclgen/exclude_imports.yaml"), mergeimports=True, exclude_imports=True
    ).serialize()
    print(shacl)

    g = rdflib.Graph()
    g.parse(data=shacl)

    # Check there is a single class from the source LinkML file, not the extended classes
    classes = list(g.subjects(RDF.type, SH.NodeShape))

    assert classes == [URIRef("https://example.org/ExtendedClass")]

    # Check that the single extending class has its slots and inherited slots too from the extended class
    property_paths = []
    for subject_node, property_node in g.subject_objects(URIRef("http://www.w3.org/ns/shacl#property")):
        property_paths.append(str(next(g.objects(property_node, SH.path, True))))

    assert len(property_paths) == 2
    assert "https://example.org/extendedProperty" in property_paths
    assert "https://example.org/baseProperty" in property_paths


def test_nodeshape_uses_rdfs_predicates(kitchen_sink_path):
    """Test that NodeShapes use rdfs:label and rdfs:comment, not sh:name and sh:description.

    Per the SHACL spec, sh:name and sh:description both have rdfs:domain of sh:PropertyShape,
    so using them on NodeShapes causes RDFS-aware validators to incorrectly infer the
    NodeShape is also a PropertyShape. See issue #3059.
    """
    shacl = ShaclGenerator(kitchen_sink_path, mergeimports=True).serialize()
    g = rdflib.Graph()
    g.parse(data=shacl)

    person_uri = URIRef("https://w3id.org/linkml/tests/kitchen_sink/Person")

    # Verify Person is a NodeShape
    assert (person_uri, RDF.type, SH.NodeShape) in g

    # Verify NodeShape uses rdfs:comment for its description (not sh:description)
    nodeshape_comments = list(g.objects(person_uri, RDFS.comment))
    assert len(nodeshape_comments) == 1
    assert "person" in str(nodeshape_comments[0]).lower()

    # Verify NodeShape does NOT have sh:description (this was the bug)
    nodeshape_sh_descriptions = list(g.objects(person_uri, SH.description))
    assert len(nodeshape_sh_descriptions) == 0, "NodeShapes should not use sh:description; use rdfs:comment instead"

    # Verify no NodeShape has sh:name (sh:name also has rdfs:domain sh:PropertyShape)
    for node_shape in g.subjects(RDF.type, SH.NodeShape):
        sh_names = list(g.objects(node_shape, SH.name))
        assert len(sh_names) == 0, f"NodeShape {node_shape} should not use sh:name; use rdfs:label instead"

    # Verify PropertyShapes still use sh:description (this is correct per spec)
    # Check that at least one property shape (BNode) uses sh:description
    found_property_description = False
    for prop_shape in g.subjects(SH.description, None):
        # Property shapes are blank nodes, NodeShapes are URIs
        if isinstance(prop_shape, rdflib.BNode):
            found_property_description = True
            break
    assert found_property_description, "PropertyShapes should use sh:description"


def test_subproperty_of_generates_sh_in():
    """Test that subproperty_of generates sh:in constraint with slot descendants."""
    schema_yaml = """
id: https://example.org/test
name: test

prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

default_prefix: ex

slots:
  related_to:
    description: Root predicate
    slot_uri: ex:related_to
  causes:
    is_a: related_to
    slot_uri: ex:causes
  treats:
    is_a: related_to
    slot_uri: ex:treats

  predicate:
    range: uriorcurie
    subproperty_of: related_to

classes:
  Association:
    slots:
      - predicate
"""
    gen = ShaclGenerator(schema_yaml)
    shacl = gen.serialize()
    g = rdflib.Graph()
    g.parse(data=shacl)

    # Find the property shape for predicate
    association_uri = URIRef("https://example.org/Association")
    predicate_property = None
    for prop_node in g.objects(association_uri, SH.property):
        path = list(g.objects(prop_node, SH.path))
        if path and str(path[0]) == "https://example.org/predicate":
            predicate_property = prop_node
            break

    assert predicate_property is not None, "Should find predicate property shape"

    # Check that sh:in constraint exists
    sh_in_nodes = list(g.objects(predicate_property, SH["in"]))
    assert len(sh_in_nodes) == 1, "Should have sh:in constraint"

    # Get the list values
    in_values = list(Collection(g, sh_in_nodes[0]))
    expected_uris = [
        URIRef("https://example.org/causes"),
        URIRef("https://example.org/related_to"),
        URIRef("https://example.org/treats"),
    ]
    assert sorted(in_values, key=str) == expected_uris


def test_subproperty_of_with_deeper_hierarchy():
    """Test that subproperty_of includes all descendants, not just direct children."""
    schema_yaml = """
id: https://example.org/test
name: test

prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

default_prefix: ex

slots:
  related_to:
    slot_uri: ex:related_to
  causes:
    is_a: related_to
    slot_uri: ex:causes
  directly_causes:
    is_a: causes
    slot_uri: ex:directly_causes
  treats:
    is_a: related_to
    slot_uri: ex:treats

  predicate:
    range: uriorcurie
    subproperty_of: related_to

classes:
  Association:
    slots:
      - predicate
"""
    gen = ShaclGenerator(schema_yaml)
    shacl = gen.serialize()
    g = rdflib.Graph()
    g.parse(data=shacl)

    # Find the property shape for predicate
    association_uri = URIRef("https://example.org/Association")
    predicate_property = None
    for prop_node in g.objects(association_uri, SH.property):
        path = list(g.objects(prop_node, SH.path))
        if path and str(path[0]) == "https://example.org/predicate":
            predicate_property = prop_node
            break

    assert predicate_property is not None

    # Get the sh:in values
    sh_in_nodes = list(g.objects(predicate_property, SH["in"]))
    in_values = list(Collection(g, sh_in_nodes[0]))

    # Should include grandchild (directly_causes)
    expected_uris = [
        URIRef("https://example.org/causes"),
        URIRef("https://example.org/directly_causes"),
        URIRef("https://example.org/related_to"),
        URIRef("https://example.org/treats"),
    ]
    assert sorted(in_values, key=str) == expected_uris


def test_subproperty_of_with_string_range():
    """Test that subproperty_of with string range uses Literal values."""
    schema_yaml = """
id: https://example.org/test
name: test

prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

default_prefix: ex

slots:
  related_to:
    slot_uri: ex:related_to
  causes:
    is_a: related_to
    slot_uri: ex:causes
  treats:
    is_a: related_to
    slot_uri: ex:treats

  predicate:
    range: string
    subproperty_of: related_to

classes:
  Association:
    slots:
      - predicate
"""
    gen = ShaclGenerator(schema_yaml)
    shacl = gen.serialize()
    g = rdflib.Graph()
    g.parse(data=shacl)

    # Find the property shape for predicate
    association_uri = URIRef("https://example.org/Association")
    predicate_property = None
    for prop_node in g.objects(association_uri, SH.property):
        path = list(g.objects(prop_node, SH.path))
        if path and str(path[0]) == "https://example.org/predicate":
            predicate_property = prop_node
            break

    assert predicate_property is not None

    # Get the sh:in values
    sh_in_nodes = list(g.objects(predicate_property, SH["in"]))
    in_values = list(Collection(g, sh_in_nodes[0]))

    # Should be Literal values with slot names (snake_case)
    expected_literals = [
        Literal("causes"),
        Literal("related_to"),
        Literal("treats"),
    ]
    assert sorted(in_values, key=str) == expected_literals


def test_subproperty_of_can_be_disabled():
    """Test that expand_subproperty_of=False disables sh:in generation."""
    schema_yaml = """
id: https://example.org/test
name: test

prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

default_prefix: ex

slots:
  related_to:
    slot_uri: ex:related_to
  causes:
    is_a: related_to
    slot_uri: ex:causes

  predicate:
    range: uriorcurie
    subproperty_of: related_to

classes:
  Association:
    slots:
      - predicate
"""
    gen = ShaclGenerator(schema_yaml, expand_subproperty_of=False)
    shacl = gen.serialize()
    g = rdflib.Graph()
    g.parse(data=shacl)

    # Find the property shape for predicate
    association_uri = URIRef("https://example.org/Association")
    predicate_property = None
    for prop_node in g.objects(association_uri, SH.property):
        path = list(g.objects(prop_node, SH.path))
        if path and str(path[0]) == "https://example.org/predicate":
            predicate_property = prop_node
            break

    assert predicate_property is not None

    # Should NOT have sh:in constraint when disabled
    sh_in_nodes = list(g.objects(predicate_property, SH["in"]))
    assert len(sh_in_nodes) == 0, "Should not have sh:in when expand_subproperty_of=False"


def test_subproperty_of_with_slot_usage():
    """Test that slot_usage subproperty_of narrows the constraint."""
    schema_yaml = """
id: https://example.org/test
name: test

prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

default_prefix: ex

slots:
  related_to:
    slot_uri: ex:related_to
  causes:
    is_a: related_to
    slot_uri: ex:causes
  directly_causes:
    is_a: causes
    slot_uri: ex:directly_causes
  treats:
    is_a: related_to
    slot_uri: ex:treats

  predicate:
    range: uriorcurie

classes:
  Association:
    slots:
      - predicate
  CausalAssociation:
    is_a: Association
    slot_usage:
      predicate:
        subproperty_of: causes
"""
    gen = ShaclGenerator(schema_yaml)
    shacl = gen.serialize()
    g = rdflib.Graph()
    g.parse(data=shacl)

    # Find the property shape for predicate in CausalAssociation
    causal_uri = URIRef("https://example.org/CausalAssociation")
    predicate_property = None
    for prop_node in g.objects(causal_uri, SH.property):
        path = list(g.objects(prop_node, SH.path))
        if path and str(path[0]) == "https://example.org/predicate":
            predicate_property = prop_node
            break

    assert predicate_property is not None

    # Get the sh:in values - should only include causes and its descendants
    sh_in_nodes = list(g.objects(predicate_property, SH["in"]))
    assert len(sh_in_nodes) == 1

    in_values = list(Collection(g, sh_in_nodes[0]))
    expected_uris = [
        URIRef("https://example.org/causes"),
        URIRef("https://example.org/directly_causes"),
    ]
    assert sorted(in_values, key=str) == expected_uris


def test_subproperty_of_with_uri_range():
    """Test that subproperty_of with uri range generates URIRef values."""
    schema_yaml = """
id: https://example.org/test
name: test

prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

default_prefix: ex

slots:
  related_to:
    slot_uri: ex:related_to
  causes:
    is_a: related_to
    slot_uri: ex:causes

  predicate:
    range: uri
    subproperty_of: related_to

classes:
  Association:
    slots:
      - predicate
"""
    gen = ShaclGenerator(schema_yaml)
    shacl = gen.serialize()
    g = rdflib.Graph()
    g.parse(data=shacl)

    # Find the property shape for predicate
    association_uri = URIRef("https://example.org/Association")
    predicate_property = None
    for prop_node in g.objects(association_uri, SH.property):
        path = list(g.objects(prop_node, SH.path))
        if path and str(path[0]) == "https://example.org/predicate":
            predicate_property = prop_node
            break

    assert predicate_property is not None

    # Get the sh:in values - should be full URIs
    sh_in_nodes = list(g.objects(predicate_property, SH["in"]))
    in_values = list(Collection(g, sh_in_nodes[0]))

    expected_uris = [
        URIRef("https://example.org/causes"),
        URIRef("https://example.org/related_to"),
    ]
    assert sorted(in_values, key=str) == expected_uris


def test_cross_directory_import_with_importmap(input_path):
    """Test that ShaclGenerator resolves cross-directory imports via importmap.

    Regression test for https://github.com/linkml/linkml/issues/2913.
    When a schema imports another schema from a subdirectory, the SHACL
    generator must honour the ``importmap`` and ``base_dir`` parameters
    to resolve the import correctly.
    """
    from pathlib import Path

    schema_path = input_path("shaclgen/cross_dir_import/main_schema.yaml")
    base_dir = str(Path(schema_path).parent)
    importmap = {
        "imported_types": str(Path(base_dir) / "subdir" / "imported_types"),
    }

    shacl = ShaclGenerator(
        schema_path,
        importmap=importmap,
        base_dir=base_dir,
        mergeimports=True,
    ).serialize()

    g = rdflib.Graph()
    g.parse(data=shacl)

    # Both the imported and local shapes should be present
    shapes = {str(s) for s in g.subjects(RDF.type, SH.NodeShape)}
    assert "https://example.org/imported/BaseEntity" in shapes
    assert "https://example.org/main/DerivedEntity" in shapes

    # DerivedEntity should inherit BaseEntity's "name" property
    derived_uri = URIRef("https://example.org/main/DerivedEntity")
    prop_paths = set()
    for prop_node in g.objects(derived_uri, SH.property):
        for path in g.objects(prop_node, SH.path):
            prop_paths.add(str(path))
    assert "https://example.org/imported/name" in prop_paths
    assert "https://example.org/main/value" in prop_paths


def test_shacl_omits_linkml_any_class_constraint():
    """sh:class linkml:Any must not appear in SHACL output.

    linkml:Any is an internal meta-type representing an unconstrained
    range. When a class has class_uri=linkml:Any (e.g. AnyObject in the
    kitchen_sink schema), the SHACL generator must not emit an
    sh:class constraint pointing to it. Such a constraint would cause
    every instance to fail validation because no real data instantiates
    the linkml:Any class.
    """
    LINKML_ANY = URIRef("https://w3id.org/linkml/Any")

    schema_yaml = """
id: https://example.org/test-any
name: test_any
default_prefix: test
prefixes:
  linkml: https://w3id.org/linkml/
  test: https://example.org/test-any/
imports:
  - linkml:types
classes:
  AnyThing:
    class_uri: linkml:Any
    description: unconstrained class
  Container:
    attributes:
      payload:
        range: AnyThing
        description: slot with unconstrained range
      name:
        range: string
"""
    gen = ShaclGenerator(schema_yaml)
    shacl = gen.serialize()
    g = rdflib.Graph()
    g.parse(data=shacl)

    # Verify linkml:Any never appears as an sh:class value
    any_class_triples = list(g.triples((None, SH["class"], LINKML_ANY)))
    assert any_class_triples == [], f"sh:class linkml:Any must not be emitted in SHACL, but found: {any_class_triples}"

    # Also verify linkml:Any never appears as sh:nodeKind target
    # (no BlankNodeOrIRI should be set for an Any-ranged slot)
    container_shape = URIRef("https://example.org/test-any/Container")
    for prop_node in g.objects(container_shape, SH.property):
        path = list(g.objects(prop_node, SH.path))
        if path and "payload" in str(path[0]):
            nodekind = list(g.objects(prop_node, SH.nodeKind))
            assert nodekind == [], f"sh:nodeKind should not be set for linkml:Any-ranged slot, got: {nodekind}"


def test_nodeidentifier_range_produces_blank_node_or_iri():
    """Test that range: nodeidentifier produces sh:nodeKind sh:BlankNodeOrIRI, not sh:Literal.

    The ``nodeidentifier`` built-in type (type_uri ``shex:nonLiteral``) represents
    an IRI or blank-node reference. The SHACL generator must emit
    ``sh:nodeKind sh:BlankNodeOrIRI`` (not ``sh:Literal`` with ``sh:datatype``).
    """
    schema_yaml = """
id: https://example.org/test-nodeident
name: test_nodeident

prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

default_prefix: ex
default_range: string

slots:
  node_ref:
    range: nodeidentifier
    slot_uri: ex:nodeRef
  uri_ref:
    range: uri
    slot_uri: ex:uriRef

classes:
  Container:
    slots:
      - node_ref
      - uri_ref
"""
    gen = ShaclGenerator(schema_yaml)
    shacl = gen.serialize()
    g = rdflib.Graph()
    g.parse(data=shacl)

    container_uri = URIRef("https://example.org/Container")

    # Collect property shapes keyed by sh:path
    props = {}
    for prop_node in g.objects(container_uri, SH.property):
        path = list(g.objects(prop_node, SH.path))
        if path:
            props[str(path[0])] = prop_node

    # nodeidentifier → sh:nodeKind sh:BlankNodeOrIRI, no sh:datatype
    node_ref = props["https://example.org/nodeRef"]
    node_kinds = list(g.objects(node_ref, SH.nodeKind))
    assert SH.BlankNodeOrIRI in node_kinds, f"Expected sh:BlankNodeOrIRI for nodeidentifier, got {node_kinds}"
    assert SH.Literal not in node_kinds
    assert list(g.objects(node_ref, SH.datatype)) == []

    # uri → sh:nodeKind sh:IRI (unchanged existing behaviour)
    uri_ref = props["https://example.org/uriRef"]
    uri_kinds = list(g.objects(uri_ref, SH.nodeKind))
    assert SH.IRI in uri_kinds, f"Expected sh:IRI for uri, got {uri_kinds}"


# ---------------------------------------------------------------------------
# --default-language tests
# ---------------------------------------------------------------------------

EX = rdflib.Namespace("http://example.org/test-schema/")


def _build_shacl_lang_schema():
    """Build a schema with title/description for language-tag testing."""
    sb = SchemaBuilder()
    sb.add_slot(
        SlotDefinition(
            "vehicle_name",
            range="string",
            description="The vehicle name.",
            title="Name",
        )
    )
    sb.add_class(
        "Vehicle",
        slots=["vehicle_name"],
        description="A road vehicle.",
        title="Vehicle",
    )
    sb.add_defaults()
    return sb.schema


def _build_message_test_schema():
    """Build a schema for sh:message testing (includes a second slot without title)."""
    sb = SchemaBuilder()
    sb.add_slot(
        SlotDefinition(
            "vehicle_name",
            range="string",
            description="The vehicle name.",
            title="Name",
            required=True,
        )
    )
    sb.add_slot(
        SlotDefinition(
            "speed",
            range="integer",
            description="Speed in km/h.",
        )
    )
    sb.add_class(
        "Vehicle",
        slots=["vehicle_name", "speed"],
        description="A road vehicle.",
    )
    sb.add_defaults()
    return sb.schema


# Helper functions
# ---------------------------------------------------------------------------


def _parse_shacl(schema, **kwargs):
    shacl = ShaclGenerator(schema, mergeimports=False, **kwargs).serialize()
    g = rdflib.Graph()
    g.parse(data=shacl)
    return g


def _get_prop_objects(g, shape_uri, prop_path_uri, predicate):
    """Get predicate values for the property shape with the given sh:path."""
    for prop_node in g.objects(shape_uri, SH.property):
        paths = list(g.objects(prop_node, SH.path))
        if paths and paths[0] == prop_path_uri:
            return list(g.objects(prop_node, predicate))
    return []


def test_shacl_default_language_node_shape():
    """NodeShape rdfs:label and rdfs:comment get @en with --default-language."""
    schema = _build_shacl_lang_schema()
    g = _parse_shacl(schema, default_language="en")

    vehicle_shape = EX.Vehicle

    labels = list(g.objects(vehicle_shape, RDFS.label))
    assert Literal("Vehicle", lang="en") in labels

    comments = list(g.objects(vehicle_shape, RDFS.comment))
    assert Literal("A road vehicle.", lang="en") in comments


def test_shacl_default_language_property_shape():
    """PropertyShape sh:name and sh:description get @en with --default-language."""
    schema = _build_shacl_lang_schema()
    g = _parse_shacl(schema, default_language="en")

    vehicle_shape = EX.Vehicle
    slot_uri = EX.vehicle_name

    sh_names = _get_prop_objects(g, vehicle_shape, slot_uri, SH["name"])
    assert Literal("Name", lang="en") in sh_names

    sh_descs = _get_prop_objects(g, vehicle_shape, slot_uri, SH.description)
    assert Literal("The vehicle name.", lang="en") in sh_descs


def test_shacl_no_default_language_plain_literals():
    """Without --default-language, literals have no language tag (backward-compat)."""
    schema = _build_shacl_lang_schema()
    g = _parse_shacl(schema)

    vehicle_shape = EX.Vehicle

    labels = list(g.objects(vehicle_shape, RDFS.label))
    assert Literal("Vehicle") in labels
    for lit in labels:
        assert lit.language is None, f"Expected no lang tag, got {lit.language!r}"

    slot_uri = EX.vehicle_name
    sh_names = _get_prop_objects(g, vehicle_shape, slot_uri, SH["name"])
    assert Literal("Name") in sh_names
    for lit in sh_names:
        assert lit.language is None, f"Expected no lang tag, got {lit.language!r}"


def test_shacl_default_language_numeric_literals_untagged():
    """Numeric literals (sh:order, sh:minCount, etc.) must never get language tags."""
    schema = _build_shacl_lang_schema()
    schema.slots["vehicle_name"].required = True
    g = _parse_shacl(schema, default_language="fr")

    vehicle_shape = EX.Vehicle
    slot_uri = EX.vehicle_name

    orders = _get_prop_objects(g, vehicle_shape, slot_uri, SH.order)
    for lit in orders:
        assert lit.language is None, f"sh:order must not be language-tagged: {lit!r}"

    min_counts = _get_prop_objects(g, vehicle_shape, slot_uri, SH.minCount)
    for lit in min_counts:
        assert lit.language is None, f"sh:minCount must not be language-tagged: {lit!r}"


def test_shacl_default_language_annotations_tagged():
    """SHACL string annotations are language-tagged with --default-language."""
    from linkml_runtime.linkml_model.meta import Annotation, Prefix

    schema = _build_shacl_lang_schema()
    schema.prefixes["skos"] = Prefix(
        prefix_prefix="skos",
        prefix_reference="http://www.w3.org/2004/02/skos/core#",
    )
    schema.classes["Vehicle"].annotations["skos:altLabel"] = Annotation(tag="skos:altLabel", value="Car")
    g = _parse_shacl(schema, default_language="en", include_annotations=True)

    vehicle_shape = EX.Vehicle
    SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
    alt_labels = list(g.objects(vehicle_shape, SKOS.altLabel))
    assert Literal("Car", lang="en") in alt_labels


def test_shacl_default_language_empty_string_treated_as_none():
    """An empty string default_language is normalised to None (no tags)."""
    schema = _build_shacl_lang_schema()
    g = _parse_shacl(schema, default_language="")

    vehicle_shape = EX.Vehicle

    labels = list(g.objects(vehicle_shape, RDFS.label))
    assert Literal("Vehicle") in labels
    for lit in labels:
        assert lit.language is None, f"Expected no lang tag, got {lit.language!r}"


def test_shacl_default_language_whitespace_only_treated_as_none():
    """A whitespace-only default_language is normalised to None (no tags)."""
    schema = _build_shacl_lang_schema()
    g = _parse_shacl(schema, default_language="   ")

    vehicle_shape = EX.Vehicle

    labels = list(g.objects(vehicle_shape, RDFS.label))
    assert Literal("Vehicle") in labels
    for lit in labels:
        assert lit.language is None, f"Expected no lang tag, got {lit.language!r}"


def test_shacl_default_language_in_language_override():
    """Element-level in_language overrides the generator default_language in SHACL."""
    schema = _build_shacl_lang_schema()
    schema.classes["Vehicle"].in_language = "de"
    g = _parse_shacl(schema, default_language="en")

    vehicle_shape = EX.Vehicle

    # Vehicle class should use element-level "de", not default "en"
    labels = list(g.objects(vehicle_shape, RDFS.label))
    assert Literal("Vehicle", lang="de") in labels
    assert Literal("Vehicle", lang="en") not in labels

    comments = list(g.objects(vehicle_shape, RDFS.comment))
    assert Literal("A road vehicle.", lang="de") in comments
    assert Literal("A road vehicle.", lang="en") not in comments


def test_shacl_default_language_bcp47_warning(caplog):
    """A malformed BCP 47 tag logs a warning but still produces output."""
    import logging

    schema = _build_shacl_lang_schema()
    # "toolongtag" passes rdflib's lax regex but fails strict BCP 47.
    with caplog.at_level(logging.WARNING):
        shacl = ShaclGenerator(schema, mergeimports=False, default_language="toolongtag").serialize()
    g = rdflib.Graph()
    g.parse(data=shacl)

    # Tag is still applied (warning, not error)
    labels = list(g.objects(EX.Vehicle, RDFS.label))
    assert any(lit.language == "toolongtag" for lit in labels)
    # Warning was emitted
    assert any("not a well-formed BCP 47 tag" in rec.message for rec in caplog.records)


def test_shacl_default_language_bcp47_valid_no_warning(caplog):
    """A well-formed BCP 47 tag does not log any warning."""
    import logging

    schema = _build_shacl_lang_schema()
    with caplog.at_level(logging.WARNING):
        ShaclGenerator(schema, mergeimports=False, default_language="en").serialize()
    assert not any("BCP 47" in rec.message for rec in caplog.records)


def test_shacl_default_language_in_language_bcp47_warning(caplog):
    """A malformed in_language value logs a warning in SHACL generator."""
    import logging

    schema = _build_shacl_lang_schema()
    # "toolongtag" passes rdflib but fails strict BCP 47.
    schema.classes["Vehicle"].in_language = "toolongtag"
    with caplog.at_level(logging.WARNING):
        shacl = ShaclGenerator(schema, mergeimports=False, default_language="en").serialize()
    g = rdflib.Graph()
    g.parse(data=shacl)

    # Vehicle uses the (malformed) in_language, not the default
    labels = list(g.objects(EX.Vehicle, RDFS.label))
    assert any(lit.language == "toolongtag" for lit in labels)
    assert any("in_language" in rec.message and "toolongtag" in rec.message for rec in caplog.records)


def test_shacl_default_language_bcp47_warning_is_deduplicated(caplog):
    """Each distinct malformed tag warns at most once across the whole SHACL run.

    Mirrors the owlgen regression test (see PR #3449 review comment): the
    original implementation emitted one warning per element. The shared
    :class:`linkml.utils.language_tags.LanguageTagResolver` collapses these
    to one warning per distinct malformed tag.
    """
    import logging

    schema = _build_shacl_lang_schema()
    schema.classes["Vehicle"].in_language = "toolongtag"
    schema.slots["vehicle_name"].in_language = "toolongtag"

    with caplog.at_level(logging.WARNING, logger="linkml.utils.language_tags"):
        ShaclGenerator(
            schema,
            mergeimports=False,
            default_language="anothertoolongone",
        ).serialize()

    in_language_warnings = [
        rec for rec in caplog.records if "in_language" in rec.message and "toolongtag" in rec.message
    ]
    default_warnings = [
        rec for rec in caplog.records if "default language" in rec.message and "anothertoolongone" in rec.message
    ]
    assert len(in_language_warnings) == 1, (
        f"expected exactly 1 in_language warning for 'toolongtag', got {len(in_language_warnings)}"
    )
    assert len(default_warnings) == 1, f"expected exactly 1 default-language warning, got {len(default_warnings)}"


# ---------------------------------------------------------------------------
# --message-template tests
# ---------------------------------------------------------------------------


def test_message_template_basic():
    """--message-template emits sh:message on every property shape."""
    schema = _build_message_test_schema()
    g = _parse_shacl(schema, message_template="Validation of {name} failed!")

    vehicle_shape = EX.Vehicle

    msgs = _get_prop_objects(g, vehicle_shape, EX.vehicle_name, SH.message)
    assert Literal("Validation of vehicle_name failed!") in msgs

    msgs = _get_prop_objects(g, vehicle_shape, EX.speed, SH.message)
    assert Literal("Validation of speed failed!") in msgs


def test_message_template_title_placeholder():
    """{title} expands to slot title, falling back to slot name."""
    schema = _build_message_test_schema()
    g = _parse_shacl(schema, message_template="{title} is invalid")

    vehicle_shape = EX.Vehicle

    # vehicle_name has title="Name"
    msgs = _get_prop_objects(g, vehicle_shape, EX.vehicle_name, SH.message)
    assert Literal("Name is invalid") in msgs

    # speed has no title → falls back to slot name
    msgs = _get_prop_objects(g, vehicle_shape, EX.speed, SH.message)
    assert Literal("speed is invalid") in msgs


def test_message_template_class_placeholder():
    """{class} expands to the enclosing class name."""
    schema = _build_message_test_schema()
    g = _parse_shacl(schema, message_template="{class}.{name} constraint violated")

    vehicle_shape = EX.Vehicle

    msgs = _get_prop_objects(g, vehicle_shape, EX.vehicle_name, SH.message)
    assert Literal("Vehicle.vehicle_name constraint violated") in msgs


def test_message_template_description_placeholder():
    """{description} expands to the slot description, empty string when absent."""
    schema = _build_message_test_schema()
    g = _parse_shacl(schema, message_template="{name} ({class}): {description}")

    vehicle_shape = EX.Vehicle

    # vehicle_name has description="The vehicle name."
    msgs = _get_prop_objects(g, vehicle_shape, EX.vehicle_name, SH.message)
    assert Literal("vehicle_name (Vehicle): The vehicle name.") in msgs

    # speed has description="Speed in km/h."
    msgs = _get_prop_objects(g, vehicle_shape, EX.speed, SH.message)
    assert Literal("speed (Vehicle): Speed in km/h.") in msgs


def test_message_template_description_fallback_empty():
    """{description} falls back to empty string when slot has no description."""
    sb = SchemaBuilder()
    sb.add_slot(SlotDefinition("bare_slot", range="string"))
    sb.add_class("Thing", slots=["bare_slot"])
    sb.add_defaults()
    g = _parse_shacl(sb.schema, message_template="{name}: {description}")

    msgs = _get_prop_objects(g, EX.Thing, EX.bare_slot, SH.message)
    assert Literal("bare_slot:") in msgs


def test_message_template_comments_placeholder():
    """{comments} expands to slot comments joined with '; '."""
    sb = SchemaBuilder()
    sb.add_slot(
        SlotDefinition(
            "wind_speed",
            range="float",
            description="Wind speed in metres per second.",
            comments=["ISO 34503:2023, Section 10.2.3"],
        )
    )
    sb.add_class("Weather", slots=["wind_speed"])
    sb.add_defaults()
    g = _parse_shacl(sb.schema, message_template="{name} ({class}): {description} [{comments}]")

    msgs = _get_prop_objects(g, EX.Weather, EX.wind_speed, SH.message)
    assert Literal("wind_speed (Weather): Wind speed in metres per second. [ISO 34503:2023, Section 10.2.3]") in msgs


def test_message_template_comments_multiple():
    """{comments} joins multiple comments with '; '."""
    sb = SchemaBuilder()
    sb.add_slot(
        SlotDefinition(
            "temperature",
            range="float",
            comments=["ISO 34503:2023, Section 10.2", "Unit: Celsius"],
        )
    )
    sb.add_class("Weather", slots=["temperature"])
    sb.add_defaults()
    g = _parse_shacl(sb.schema, message_template="{comments}")

    msgs = _get_prop_objects(g, EX.Weather, EX.temperature, SH.message)
    assert Literal("ISO 34503:2023, Section 10.2; Unit: Celsius") in msgs


def test_message_template_comments_fallback_empty():
    """{comments} falls back to empty string when slot has no comments."""
    sb = SchemaBuilder()
    sb.add_slot(SlotDefinition("bare_slot", range="string"))
    sb.add_class("Thing", slots=["bare_slot"])
    sb.add_defaults()
    g = _parse_shacl(sb.schema, message_template="{name}: {comments}")

    msgs = _get_prop_objects(g, EX.Thing, EX.bare_slot, SH.message)
    assert Literal("bare_slot:") in msgs


def test_no_message_template_no_sh_message():
    """Without --message-template, no sh:message is emitted (backward-compat)."""
    schema = _build_message_test_schema()
    g = _parse_shacl(schema)

    vehicle_shape = EX.Vehicle

    msgs = _get_prop_objects(g, vehicle_shape, EX.vehicle_name, SH.message)
    assert msgs == []

    msgs = _get_prop_objects(g, vehicle_shape, EX.speed, SH.message)
    assert msgs == []


def test_message_template_invalid_placeholder_raises():
    """An invalid placeholder in --message-template raises ValueError."""
    schema = _build_message_test_schema()
    with pytest.raises(ValueError, match="Invalid placeholder"):
        _parse_shacl(schema, message_template="Error: {invalid}")


def test_message_template_positional_placeholder_raises():
    """Positional placeholders like {0} raise ValueError."""
    schema = _build_message_test_schema()
    with pytest.raises(ValueError, match="Invalid placeholder"):
        _parse_shacl(schema, message_template="Error: {0}")


def test_message_template_format_spec_raises():
    """Format specs like {name:d} raise ValueError."""
    schema = _build_message_test_schema()
    with pytest.raises(ValueError, match="Invalid placeholder"):
        _parse_shacl(schema, message_template="Error: {name:d}")


def test_message_template_empty_string_treated_as_none():
    """An empty message_template is normalised to None (no sh:message)."""
    schema = _build_message_test_schema()
    g = _parse_shacl(schema, message_template="")

    vehicle_shape = EX.Vehicle
    msgs = _get_prop_objects(g, vehicle_shape, EX.vehicle_name, SH.message)
    assert msgs == []


def test_message_template_whitespace_only_treated_as_none():
    """A whitespace-only message_template is normalised to None (no sh:message)."""
    schema = _build_message_test_schema()
    g = _parse_shacl(schema, message_template="   ")

    vehicle_shape = EX.Vehicle
    msgs = _get_prop_objects(g, vehicle_shape, EX.vehicle_name, SH.message)
    assert msgs == []


def test_message_template_with_default_language():
    """sh:message is language-tagged when both --message-template and --default-language are set."""
    schema = _build_message_test_schema()
    g = _parse_shacl(
        schema,
        message_template="Validation of {name} failed!",
        default_language="en",
    )

    vehicle_shape = EX.Vehicle
    msgs = _get_prop_objects(g, vehicle_shape, EX.vehicle_name, SH.message)
    assert Literal("Validation of vehicle_name failed!", lang="en") in msgs

    # Verify the message is NOT a plain literal
    assert Literal("Validation of vehicle_name failed!") not in msgs


def test_message_template_path_placeholder():
    """{path} expands to the fully-expanded property IRI."""
    schema = _build_message_test_schema()
    g = _parse_shacl(schema, message_template="{path}")

    vehicle_shape = EX.Vehicle
    msgs = _get_prop_objects(g, vehicle_shape, EX.vehicle_name, SH.message)
    assert Literal(str(EX.vehicle_name)) in msgs


def test_message_template_expands_to_empty_no_message():
    """A template that expands to an empty string emits no sh:message."""
    sb = SchemaBuilder()
    sb.add_slot(SlotDefinition("bare_slot", range="string"))
    sb.add_class("Thing", slots=["bare_slot"])
    sb.add_defaults()
    # bare_slot has no description, so "{description}" -> "" -> no sh:message.
    g = _parse_shacl(sb.schema, message_template="{description}")

    msgs = _get_prop_objects(g, EX.Thing, EX.bare_slot, SH.message)
    assert msgs == []


def test_message_template_attribute_access_raises():
    """Attribute access in a placeholder (e.g. {name.upper}) raises a friendly ValueError."""
    schema = _build_message_test_schema()
    with pytest.raises(ValueError, match="Invalid placeholder"):
        _parse_shacl(schema, message_template="{name.upper}")


def test_message_template_index_access_raises():
    """Index access in a placeholder (e.g. {name[0]}) raises a friendly ValueError."""
    schema = _build_message_test_schema()
    with pytest.raises(ValueError, match="Invalid placeholder"):
        _parse_shacl(schema, message_template="{name[0]}")


def test_message_template_unbalanced_brace_raises():
    """A malformed template (unbalanced brace) raises a friendly ValueError."""
    schema = _build_message_test_schema()
    with pytest.raises(ValueError, match="Invalid placeholder"):
        _parse_shacl(schema, message_template="Broken {name")


def test_message_template_validated_up_front_on_slotless_schema():
    """An invalid template is rejected up-front, even when no slots are iterated."""
    sb = SchemaBuilder()
    sb.add_class("Empty")  # no slots -> the per-slot loop never runs
    sb.add_defaults()
    with pytest.raises(ValueError, match="Invalid placeholder"):
        ShaclGenerator(sb.schema, mergeimports=False, message_template="{bogus}")


def test_message_template_ignores_per_slot_in_language():
    """sh:message follows default_language only, ignoring a slot's in_language.

    The message text is a single global template (one language), so unlike
    sh:name / sh:description it must not be tagged with the slot's in_language.
    """
    schema = _build_message_test_schema()
    schema.slots["vehicle_name"].in_language = "de"
    g = _parse_shacl(
        schema,
        message_template="Validation of {name} failed!",
        default_language="en",
    )

    vehicle_shape = EX.Vehicle
    msgs = _get_prop_objects(g, vehicle_shape, EX.vehicle_name, SH.message)
    # Message uses the generator default ("en"), NOT the slot's in_language ("de").
    assert Literal("Validation of vehicle_name failed!", lang="en") in msgs
    assert Literal("Validation of vehicle_name failed!", lang="de") not in msgs

    # Contrast: sh:name DOES follow the slot's in_language ("de").
    names = _get_prop_objects(g, vehicle_shape, EX.vehicle_name, SH.name)
    assert Literal("Name", lang="de") in names


# ---------------------------------------------------------------------------
# --emit-rules / sh:sparql tests
# ---------------------------------------------------------------------------

_RULES_SCHEMA_YAML = """
id: https://example.org/boolean-guards
name: boolean_guard_rules
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/boolean-guards/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  WeatherWind:
    range: boolean
    slot_uri: ex:WeatherWind
  weatherWindValue:
    description: Wind speed value.
    range: decimal
    slot_uri: ex:weatherWindValue
  WeatherRain:
    range: boolean
    slot_uri: ex:WeatherRain
  weatherRainValue:
    description: Rain intensity value.
    range: decimal
    slot_uri: ex:weatherRainValue
  Temperature:
    range: decimal
    slot_uri: ex:Temperature
classes:
  Environment:
    class_uri: ex:Environment
    slots:
      - WeatherWind
      - weatherWindValue
      - WeatherRain
      - weatherRainValue
      - Temperature
    rules:
      - description: If weatherWindValue is provided, WeatherWind must be true.
        preconditions:
          slot_conditions:
            weatherWindValue:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            WeatherWind:
              equals_string: "true"
      - description: If weatherRainValue is provided, WeatherRain must be true.
        preconditions:
          slot_conditions:
            weatherRainValue:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            WeatherRain:
              equals_string: "true"
"""

EX_RULES = rdflib.Namespace("https://example.org/boolean-guards/")


def test_rule_boolean_guard_generates_sparql():
    """Boolean-guard rules produce sh:sparql constraints on the NodeShape."""
    g = _parse_shacl(_RULES_SCHEMA_YAML)

    shape = EX_RULES.Environment
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 2, f"Expected 2 sh:sparql constraints, got {len(sparql_nodes)}"

    for node in sparql_nodes:
        assert (node, RDF.type, SH.SPARQLConstraint) in g
        selects = list(g.objects(node, SH.select))
        assert len(selects) == 1, "Each constraint must have exactly one sh:select"
        query = str(selects[0])
        assert "$this" in query, "SPARQL must use $this pre-bound variable"
        assert "OPTIONAL" in query, "SPARQL must use OPTIONAL for flag/value"
        assert "FILTER" in query, "SPARQL must have a FILTER clause"
        assert "BOUND" in query, "SPARQL must use BOUND()"


def test_rule_with_description_generates_message():
    """Rule description is emitted as sh:message on the SPARQLConstraint."""
    g = _parse_shacl(_RULES_SCHEMA_YAML)

    shape = EX_RULES.Environment
    sparql_nodes = list(g.objects(shape, SH.sparql))

    messages = set()
    for node in sparql_nodes:
        for msg in g.objects(node, SH.message):
            messages.add(str(msg))

    assert "If weatherWindValue is provided, WeatherWind must be true." in messages
    assert "If weatherRainValue is provided, WeatherRain must be true." in messages


def test_rule_sparql_contains_correct_uris():
    """SPARQL queries reference the correct slot URIs."""
    g = _parse_shacl(_RULES_SCHEMA_YAML)

    shape = EX_RULES.Environment
    sparql_nodes = list(g.objects(shape, SH.sparql))

    queries = [str(list(g.objects(n, SH.select))[0]) for n in sparql_nodes]
    all_sparql = "\n".join(queries)

    assert str(EX_RULES.WeatherWind) in all_sparql
    assert str(EX_RULES.weatherWindValue) in all_sparql
    assert str(EX_RULES.WeatherRain) in all_sparql
    assert str(EX_RULES.weatherRainValue) in all_sparql


_DEACTIVATED_RULE_SCHEMA_YAML = """
id: https://example.org/deactivated-test
name: deactivated_rule_test
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/deactivated-test/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  Flag:
    range: boolean
    slot_uri: ex:Flag
  flagValue:
    range: decimal
    slot_uri: ex:flagValue
classes:
  TestClass:
    class_uri: ex:TestClass
    slots:
      - Flag
      - flagValue
    rules:
      - description: This rule is deactivated.
        deactivated: true
        preconditions:
          slot_conditions:
            flagValue:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            Flag:
              equals_string: "true"
"""


def test_rule_deactivated_skipped():
    """Deactivated rules do not produce sh:sparql constraints."""
    g = _parse_shacl(_DEACTIVATED_RULE_SCHEMA_YAML)

    shape = URIRef("https://example.org/deactivated-test/TestClass")
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 0, f"Deactivated rule should not emit sh:sparql, got {len(sparql_nodes)}"


_UNSUPPORTED_RULE_SCHEMA_YAML = """
id: https://example.org/unsupported-test
name: unsupported_rule_test
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/unsupported-test/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  slotA:
    range: string
    slot_uri: ex:slotA
  slotB:
    range: string
    slot_uri: ex:slotB
classes:
  TestClass:
    class_uri: ex:TestClass
    slots:
      - slotA
      - slotB
    rules:
      - description: Rule with no postconditions.
        preconditions:
          slot_conditions:
            slotA:
              value_presence: PRESENT
"""


def test_rule_unsupported_pattern_skipped():
    """Unrecognised rule patterns are skipped (no sh:sparql emitted)."""
    g = _parse_shacl(_UNSUPPORTED_RULE_SCHEMA_YAML)

    shape = URIRef("https://example.org/unsupported-test/TestClass")
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 0


def test_rule_no_emit_rules_flag():
    """--no-emit-rules suppresses sh:sparql constraint generation."""
    g = _parse_shacl(_RULES_SCHEMA_YAML, emit_rules=False)

    shape = EX_RULES.Environment
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 0, f"emit_rules=False should suppress rules, got {len(sparql_nodes)}"


_NO_RULES_SCHEMA_YAML = """
id: https://example.org/no-rules
name: no_rules_test
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/no-rules/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  name:
    range: string
    slot_uri: ex:name
classes:
  SimpleClass:
    class_uri: ex:SimpleClass
    slots:
      - name
"""


def test_rule_no_rules_no_sparql():
    """Classes without rules: blocks produce no sh:sparql constraints."""
    g = _parse_shacl(_NO_RULES_SCHEMA_YAML)

    shape = URIRef("https://example.org/no-rules/SimpleClass")
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 0


def test_rule_multiple_rules_per_class():
    """Multiple boolean-guard rules on one class produce multiple sh:sparql constraints."""
    g = _parse_shacl(_RULES_SCHEMA_YAML)

    shape = EX_RULES.Environment
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 2

    # Each constraint should reference different slot pairs
    queries = [str(list(g.objects(n, SH.select))[0]) for n in sparql_nodes]
    wind_query = [q for q in queries if "weatherWindValue" in q]
    rain_query = [q for q in queries if "weatherRainValue" in q]
    assert len(wind_query) == 1, "Expected exactly one wind query"
    assert len(rain_query) == 1, "Expected exactly one rain query"


# ---------------------------------------------------------------------------
# Tests for URI resolution without explicit slot_uri
# ---------------------------------------------------------------------------

_NO_SLOT_URI_SCHEMA_YAML = """
id: https://example.org/no-slot-uri
name: no_slot_uri_test
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/no-slot-uri/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  is_active:
    range: boolean
  measured_value:
    range: decimal
classes:
  Reading:
    class_uri: ex:Reading
    slots:
      - is_active
      - measured_value
    rules:
      - description: If measured_value is provided, is_active must be true.
        preconditions:
          slot_conditions:
            measured_value:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            is_active:
              equals_string: "true"
"""


def test_rule_no_explicit_slot_uri():
    """Slots without explicit slot_uri resolve via default_prefix + underscore(name)."""
    g = _parse_shacl(_NO_SLOT_URI_SCHEMA_YAML)

    shape = URIRef("https://example.org/no-slot-uri/Reading")
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 1

    query = str(list(g.objects(sparql_nodes[0], SH.select))[0])
    # URIs should be default_prefix:underscore(name)
    assert "https://example.org/no-slot-uri/is_active" in query
    assert "https://example.org/no-slot-uri/measured_value" in query


# ---------------------------------------------------------------------------
# Tests for elseconditions rejection
# ---------------------------------------------------------------------------

_ELSE_COND_SCHEMA_YAML = """
id: https://example.org/else-test
name: else_cond_test
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/else-test/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  Flag:
    range: boolean
    slot_uri: ex:Flag
  flagValue:
    range: decimal
    slot_uri: ex:flagValue
  fallbackValue:
    range: string
    slot_uri: ex:fallbackValue
classes:
  TestClass:
    class_uri: ex:TestClass
    slots:
      - Flag
      - flagValue
      - fallbackValue
    rules:
      - description: Rule with elseconditions should be skipped.
        preconditions:
          slot_conditions:
            flagValue:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            Flag:
              equals_string: "true"
        elseconditions:
          slot_conditions:
            fallbackValue:
              value_presence: PRESENT
"""


def test_rule_with_elseconditions_emitted():
    """Rules with elseconditions emit the forward (if/then) branch and warn."""

    g = _parse_shacl(_ELSE_COND_SCHEMA_YAML)

    shape = URIRef("https://example.org/else-test/TestClass")
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) >= 1, "Rule with elseconditions should emit sh:sparql for the forward branch"


def test_rule_with_elseconditions_warns(caplog):
    """Rules with elseconditions emit a warning about the dropped else branch."""
    import logging

    with caplog.at_level(logging.WARNING):
        _parse_shacl(_ELSE_COND_SCHEMA_YAML)

    assert any("elseconditions" in rec.message for rec in caplog.records), (
        "Expected a warning about elseconditions being dropped"
    )


_BIDIRECTIONAL_RULE_SCHEMA_YAML = """
id: https://example.org/bidir-test
name: bidir_rule_test
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/bidir-test/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  Flag:
    range: boolean
    slot_uri: ex:Flag
  flagValue:
    range: decimal
    slot_uri: ex:flagValue
classes:
  TestClass:
    class_uri: ex:TestClass
    slots:
      - Flag
      - flagValue
    rules:
      - description: Bidirectional rule should be skipped.
        bidirectional: true
        preconditions:
          slot_conditions:
            flagValue:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            Flag:
              equals_string: "true"
"""


def test_rule_bidirectional_skipped(caplog):
    """Rules with bidirectional=true are skipped entirely with a warning."""
    import logging

    with caplog.at_level(logging.WARNING):
        g = _parse_shacl(_BIDIRECTIONAL_RULE_SCHEMA_YAML)

    shape = URIRef("https://example.org/bidir-test/TestClass")
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 0, "Bidirectional rules should NOT emit sh:sparql"
    assert any("bidirectional" in rec.message for rec in caplog.records), (
        "Expected a warning about bidirectional rules being skipped"
    )


# ---------------------------------------------------------------------------
# End-to-end pyshacl validation test
# ---------------------------------------------------------------------------


def test_rule_boolean_guard_pyshacl_end_to_end():
    """End-to-end: pyshacl flags a violation and passes a conforming instance."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_RULES_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()

    # Build a conforming RDF instance: weatherWindValue present AND WeatherWind = true
    conforming_data = """
    @prefix ex: <https://example.org/boolean-guards/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:env1 a ex:Environment ;
        ex:WeatherWind "true"^^xsd:boolean ;
        ex:weatherWindValue "12.5"^^xsd:decimal .
    """

    # Build a violating RDF instance: weatherWindValue present but WeatherWind missing
    violating_data = """
    @prefix ex: <https://example.org/boolean-guards/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:env2 a ex:Environment ;
        ex:weatherWindValue "8.0"^^xsd:decimal .
    """

    # Conforming instance should pass
    conforms, _, _ = pyshacl.validate(
        data_graph=conforming_data,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert conforms, "Conforming instance should pass SHACL validation"

    # Violating instance should fail
    conforms, results_graph, results_text = pyshacl.validate(
        data_graph=violating_data,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert not conforms, f"Violating instance should fail SHACL validation:\n{results_text}"


# ---------------------------------------------------------------------------
# SPARQL syntax validation
# ---------------------------------------------------------------------------


def test_rule_sparql_syntax_valid():
    """Generated SPARQL queries must be syntactically valid."""
    from rdflib.plugins.sparql import prepareQuery

    g = _parse_shacl(_RULES_SCHEMA_YAML)

    shape = EX_RULES.Environment
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) >= 1

    for node in sparql_nodes:
        query_text = str(list(g.objects(node, SH.select))[0])
        # prepareQuery validates SPARQL syntax; $this is a valid variable name
        prepareQuery(query_text)


# ===========================================================================
# Exclusive-value pattern tests (SHACL §5 SPARQL constraints)
# ===========================================================================
#
# The "exclusive value" pattern translates a LinkML rule where:
#   - preconditions: slot X has equals_string (a specific enum value name)
#   - postconditions: same slot X has maximum_cardinality N
#
# Semantics: "If value V is present in multivalued slot X, then X has at most
# N values total."  For N=1 this means V must be the sole value (mutual
# exclusion with other enum members).
#
# Generated SHACL: sh:SPARQLConstraint per W3C SHACL §5.3.1, using $this
# pre-bound to each focus node.
#
# References:
#   - W3C SHACL §5 <https://www.w3.org/TR/shacl/#sparql-constraints>
#   - W3C SHACL §5.3.1 <https://www.w3.org/TR/shacl/#sparql-constraints-prebound>
#   - ISO 34503:2023, 9.3.6 (motivating use case: EdgeNone exclusivity)
# ===========================================================================

_EXCLUSIVE_VALUE_SCHEMA_YAML = """
id: https://example.org/exclusive-value
name: exclusive_value_rules
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/exclusive-value/
imports:
  - linkml:types
default_prefix: ex
default_range: string

enums:
  EdgeTypeEnum:
    permissible_values:
      EdgeNone:
        meaning: ex:EdgeNone
      EdgeBarriers:
        meaning: ex:EdgeBarriers
      EdgeMarkers:
        meaning: ex:EdgeMarkers

  PriorityEnum:
    permissible_values:
      High:
        description: High priority (no meaning IRI).
      Medium:
        description: Medium priority (no meaning IRI).
      Low:
        description: Low priority (no meaning IRI).

slots:
  edgeType:
    range: EdgeTypeEnum
    multivalued: true
    slot_uri: ex:edgeType
  priority:
    range: PriorityEnum
    multivalued: true
    slot_uri: ex:priority
  otherSlot:
    range: string
    slot_uri: ex:otherSlot

classes:
  Road:
    class_uri: ex:Road
    slots:
      - edgeType
      - otherSlot
    rules:
      - description: >-
          EdgeNone is mutually exclusive with other edge types.
        preconditions:
          slot_conditions:
            edgeType:
              equals_string: "EdgeNone"
        postconditions:
          slot_conditions:
            edgeType:
              maximum_cardinality: 1

  Intersection:
    class_uri: ex:Intersection
    slots:
      - edgeType
    rules:
      - description: >-
          EdgeNone allows at most 2 total edge values.
        preconditions:
          slot_conditions:
            edgeType:
              equals_string: "EdgeNone"
        postconditions:
          slot_conditions:
            edgeType:
              maximum_cardinality: 2

  Task:
    class_uri: ex:Task
    slots:
      - priority
    rules:
      - description: >-
          High priority is exclusive (literal fallback test).
        preconditions:
          slot_conditions:
            priority:
              equals_string: "High"
        postconditions:
          slot_conditions:
            priority:
              maximum_cardinality: 1

  MismatchedSlots:
    class_uri: ex:MismatchedSlots
    slots:
      - edgeType
      - otherSlot
    rules:
      - description: >-
          Different slots in pre/post — not an exclusive-value pattern.
        preconditions:
          slot_conditions:
            edgeType:
              equals_string: "EdgeNone"
        postconditions:
          slot_conditions:
            otherSlot:
              maximum_cardinality: 1
"""

EX_EXCL = rdflib.Namespace("https://example.org/exclusive-value/")


def test_exclusive_value_generates_sparql():
    """Exclusive-value rules produce sh:sparql constraints on the NodeShape."""
    g = _parse_shacl(_EXCLUSIVE_VALUE_SCHEMA_YAML)

    shape = EX_EXCL.Road
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 1, f"Expected 1 sh:sparql constraint, got {len(sparql_nodes)}"

    node = sparql_nodes[0]
    assert (node, RDF.type, SH.SPARQLConstraint) in g
    selects = list(g.objects(node, SH.select))
    assert len(selects) == 1, "Constraint must have exactly one sh:select"


def test_exclusive_value_sparql_uses_enum_iri():
    """SPARQL references the enum value's meaning IRI, not a string literal.

    Per the enum definition, EdgeNone has meaning: ex:EdgeNone which expands
    to <https://example.org/exclusive-value/EdgeNone>.  The generated SPARQL
    must use this full IRI in angle brackets.
    """
    g = _parse_shacl(_EXCLUSIVE_VALUE_SCHEMA_YAML)

    shape = EX_EXCL.Road
    sparql_nodes = list(g.objects(shape, SH.sparql))
    query = str(list(g.objects(sparql_nodes[0], SH.select))[0])

    edge_none_iri = str(EX_EXCL.EdgeNone)
    assert f"<{edge_none_iri}>" in query, f"SPARQL must reference EdgeNone as full IRI <{edge_none_iri}>, got:\n{query}"


def test_exclusive_value_max_card_1_sparql_structure():
    """For maximum_cardinality: 1, SPARQL reports each ?other value coexisting with <value>.

    The query pattern for N=1 is:
        SELECT DISTINCT $this (<slot> AS ?path) (?other AS ?value) WHERE {
            $this <slot> ?exclusive .
            $this <slot> ?other .
            FILTER ( COALESCE( ?exclusive = <value>, false ) &&
                     !COALESCE( ?other = <value>, false ) )
        }

    This is more efficient than the COUNT-based approach for the common
    singleton exclusion case.
    """
    g = _parse_shacl(_EXCLUSIVE_VALUE_SCHEMA_YAML)

    shape = EX_EXCL.Road
    sparql_nodes = list(g.objects(shape, SH.sparql))
    query = str(list(g.objects(sparql_nodes[0], SH.select))[0])

    assert "$this" in query, "SPARQL must use $this pre-bound variable (SHACL §5.3.1)"
    assert "FILTER" in query, "N=1 pattern must use FILTER for exclusion check"
    assert "?other" in query, "N=1 pattern must bind ?other for comparison"
    # Must NOT use COUNT for the N=1 case (simpler pattern)
    assert "COUNT" not in query, "N=1 pattern should use FILTER, not COUNT"
    # The slot URI must appear (property path)
    assert str(EX_EXCL.edgeType) in query, "SPARQL must reference the slot URI"


def test_exclusive_value_max_card_gt1_sparql_structure():
    """For maximum_cardinality > 1, SPARQL uses COUNT-based subquery.

    The query pattern for N>1 is:
        SELECT DISTINCT $this (<slot> AS ?path) WHERE {
            $this <slot> ?exclusive .
            FILTER ( COALESCE( ?exclusive = <value>, false ) )
            {
                SELECT $this
                WHERE { $this <slot> ?item . }
                GROUP BY $this
                HAVING ( COUNT(?item) > N )
            }
        }
    """
    g = _parse_shacl(_EXCLUSIVE_VALUE_SCHEMA_YAML)

    shape = EX_EXCL.Intersection
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 1, f"Expected 1 sh:sparql constraint, got {len(sparql_nodes)}"

    query = str(list(g.objects(sparql_nodes[0], SH.select))[0])

    assert "$this" in query, "SPARQL must use $this pre-bound variable"
    assert "COUNT" in query, "N>1 pattern must use COUNT"
    assert "GROUP BY" in query, "N>1 pattern must GROUP BY $this"
    assert "HAVING" in query, "N>1 pattern must use HAVING for count check"
    assert "> 2" in query, "HAVING must check count > maximum_cardinality (2)"


def test_exclusive_value_no_meaning_falls_back_to_literal():
    """When enum values lack a meaning IRI, the value is compared as a literal.

    PriorityEnum values have no meaning field, so 'High' is used as a
    quoted string in the SPARQL rather than an IRI in angle brackets.
    """
    g = _parse_shacl(_EXCLUSIVE_VALUE_SCHEMA_YAML)

    shape = EX_EXCL.Task
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 1, f"Expected 1 sh:sparql constraint, got {len(sparql_nodes)}"

    query = str(list(g.objects(sparql_nodes[0], SH.select))[0])

    # Should use quoted literal, not angle-bracket IRI
    assert '"High"' in query, f"No-meaning enum should use literal '\"High\"', got:\n{query}"
    assert "<High>" not in query, "Should not emit as IRI when meaning is absent"


def test_exclusive_value_different_slots_not_recognised():
    """Rules where pre/post reference different slots are NOT exclusive-value.

    The pattern requires the SAME slot in both preconditions and
    postconditions.  When they differ, the rule is unrecognised and
    silently skipped (no sh:sparql emitted).
    """
    g = _parse_shacl(_EXCLUSIVE_VALUE_SCHEMA_YAML)

    shape = EX_EXCL.MismatchedSlots
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 0, (
        f"Mismatched slots should not trigger exclusive-value pattern, got {len(sparql_nodes)}"
    )


def test_exclusive_value_message_from_description():
    """Rule description is emitted as sh:message on the SPARQLConstraint."""
    g = _parse_shacl(_EXCLUSIVE_VALUE_SCHEMA_YAML)

    shape = EX_EXCL.Road
    sparql_nodes = list(g.objects(shape, SH.sparql))
    messages = [str(m) for node in sparql_nodes for m in g.objects(node, SH.message)]

    assert any("EdgeNone is mutually exclusive" in m for m in messages), (
        f"Expected message about EdgeNone exclusivity, got: {messages}"
    )


def test_exclusive_value_sparql_syntax_valid():
    """Generated SPARQL for exclusive-value rules must be syntactically valid.

    Uses rdflib's prepareQuery() which validates SPARQL syntax.
    $this is a valid SPARQL variable name per the grammar.
    """
    from rdflib.plugins.sparql import prepareQuery

    g = _parse_shacl(_EXCLUSIVE_VALUE_SCHEMA_YAML)

    for shape in (EX_EXCL.Road, EX_EXCL.Intersection, EX_EXCL.Task):
        sparql_nodes = list(g.objects(shape, SH.sparql))
        for node in sparql_nodes:
            query_text = str(list(g.objects(node, SH.select))[0])
            # prepareQuery validates SPARQL syntax
            prepareQuery(query_text)


def test_exclusive_value_coexists_with_boolean_guard():
    """Exclusive-value and boolean-guard rules can coexist on the same class.

    When a class has both pattern types, both produce sh:sparql constraints.
    """
    schema = """
id: https://example.org/mixed-rules
name: mixed_rules
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/mixed-rules/
imports:
  - linkml:types
default_prefix: ex
default_range: string

enums:
  StatusEnum:
    permissible_values:
      None:
        meaning: ex:None
      Active:
        meaning: ex:Active

slots:
  status:
    range: StatusEnum
    multivalued: true
    slot_uri: ex:status
  Flag:
    range: boolean
    slot_uri: ex:Flag
  flagValue:
    range: decimal
    slot_uri: ex:flagValue

classes:
  Widget:
    class_uri: ex:Widget
    slots:
      - status
      - Flag
      - flagValue
    rules:
      - description: None is exclusive.
        preconditions:
          slot_conditions:
            status:
              equals_string: "None"
        postconditions:
          slot_conditions:
            status:
              maximum_cardinality: 1
      - description: If flagValue present, Flag must be true.
        preconditions:
          slot_conditions:
            flagValue:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            Flag:
              equals_string: "true"
"""
    g = _parse_shacl(schema)

    shape = URIRef("https://example.org/mixed-rules/Widget")
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 2, (
        f"Expected 2 sh:sparql constraints (1 exclusive + 1 boolean guard), got {len(sparql_nodes)}"
    )

    queries = [str(list(g.objects(n, SH.select))[0]) for n in sparql_nodes]
    # One should have FILTER(?other != ...) pattern, the other BOUND pattern
    has_exclusive = any("?other" in q for q in queries)
    has_boolean = any("BOUND" in q for q in queries)
    assert has_exclusive, "Expected one exclusive-value SPARQL constraint"
    assert has_boolean, "Expected one boolean-guard SPARQL constraint"


def test_shacl_modular_schema_with_reused_attribute_name(tmp_path) -> None:
    """A modular schema imported by relative path generates SHACL (#3878).

    Two classes reuse an attribute name with distinct slot_uris, and the schema declaring
    them is imported as ``../nucleo/core``, so its closure key differs from its name.
    """
    nucleo = tmp_path / "nucleo"
    dominios = tmp_path / "dominios"
    nucleo.mkdir()
    dominios.mkdir()
    (nucleo / "core.yaml").write_text(
        "id: https://example.org/core\n"
        "name: core\n"
        "prefixes: {linkml: 'https://w3id.org/linkml/', core: 'https://example.org/core/'}\n"
        "default_prefix: core\n"
        "default_range: string\n"
        "imports: [linkml:types]\n"
        "classes:\n"
        "  Transaccion:\n"
        "    attributes:\n"
        "      id_transaccion: {identifier: true}\n"
        "      estado: {slot_uri: core:transaccion_estado}\n"
        "  Compromiso:\n"
        "    attributes:\n"
        "      id_compromiso: {identifier: true}\n"
        "      estado: {slot_uri: core:compromiso_estado}\n"
    )
    domain = dominios / "domain.yaml"
    domain.write_text(
        "id: https://example.org/domain\n"
        "name: domain\n"
        "prefixes: {linkml: 'https://w3id.org/linkml/', core: 'https://example.org/core/', "
        "dom: 'https://example.org/domain/'}\n"
        "default_prefix: dom\n"
        "default_range: string\n"
        "imports: [linkml:types, ../nucleo/core]\n"
        "classes:\n"
        "  Pedido:\n"
        "    is_a: Transaccion\n"
        "    attributes:\n"
        "      importe: {range: float}\n"
    )

    graph = rdflib.Graph()
    graph.parse(data=ShaclGenerator(str(domain)).serialize(), format="turtle")
    shapes = set(graph.subjects(RDF.type, SH.NodeShape))
    assert URIRef("https://example.org/domain/Pedido") in shapes


# ===========================================================================
# Presence-implies-value pattern tests (enum guard)
# ===========================================================================
#
# The "presence implies value" pattern generalises the boolean guard to
# enum-valued targets.  It translates a LinkML rule where:
#   - preconditions: a guard slot has value_presence: PRESENT
#   - postconditions: a target slot has equals_string (single required value)
#     or equals_string_in (a set of acceptable values)
#
# Semantics: "If the guard slot is present, the target slot must be present
# and hold one of the allowed values", e.g. "if a document has a signature,
# its status must be Published".
#
# References:
#   - W3C SHACL §5 <https://www.w3.org/TR/shacl/#sparql-constraints>
#   - W3C SHACL §5.3.1 <https://www.w3.org/TR/shacl/#sparql-constraints-prebound>
#   - W3C SHACL §5.3.2 <https://www.w3.org/TR/shacl/#sparql-constraints-variables>
# ===========================================================================

_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML = """
id: https://example.org/presence-implies-value
name: presence_implies_value_rules
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/presence-implies-value/
imports:
  - linkml:types
default_prefix: ex
default_range: string

enums:
  StatusEnum:
    permissible_values:
      Draft:
        meaning: ex:Draft
      Reviewed:
        meaning: ex:Reviewed
      Approved:
        meaning: ex:Approved
      Published:
        meaning: ex:Published

  ModeEnum:
    permissible_values:
      Auto:
        description: Automatic mode (no meaning IRI).
      Manual:
        description: Manual mode (no meaning IRI).

slots:
  status:
    range: StatusEnum
    slot_uri: ex:status
  signature:
    range: string
    slot_uri: ex:signature
  review_score:
    range: float
    slot_uri: ex:review_score
  mode:
    range: ModeEnum
    slot_uri: ex:mode
  manual_value:
    range: decimal
    slot_uri: ex:manual_value

classes:
  Document:
    class_uri: ex:Document
    slots:
      - status
      - signature
      - review_score
    rules:
      - description: If a document has a signature, its status must be Published.
        preconditions:
          slot_conditions:
            signature:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            status:
              equals_string: "Published"
      - description: If a document has a review score, its status must be Reviewed or Approved.
        preconditions:
          slot_conditions:
            review_score:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            status:
              equals_string_in:
                - Reviewed
                - Approved

  Device:
    class_uri: ex:Device
    slots:
      - mode
      - manual_value
    rules:
      - description: If manual_value is provided, mode must be Manual (literal fallback).
        preconditions:
          slot_conditions:
            manual_value:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            mode:
              equals_string: "Manual"
"""

EX_PIV = rdflib.Namespace("https://example.org/presence-implies-value/")


def _rule_results(schema: str, data: str | rdflib.Graph) -> tuple[bool, list[tuple]]:
    """Validate *data* against the shapes generated for *schema*.

    *data* is Turtle or a graph.  Returns whether the data conforms overall,
    and the ``(focus node, result path, value)`` of each result that a rule
    constraint (``sh:sparql``) reports, so that a property-shape result
    (datatype, cardinality, ...) can neither mask nor stand in for what a rule
    decides.
    """
    import pyshacl

    shapes = rdflib.Graph().parse(data=ShaclGenerator(schema, mergeimports=False).serialize(), format="turtle")
    data_graph = data if isinstance(data, rdflib.Graph) else rdflib.Graph().parse(data=data, format="turtle")
    conforms, report, _ = pyshacl.validate(data_graph, shacl_graph=shapes, advanced=True)
    results = [
        (report.value(result, SH.focusNode), report.value(result, SH.resultPath), report.value(result, SH.value))
        for result in report.subjects(SH.sourceConstraintComponent, SH.SPARQLConstraintComponent)
    ]
    return conforms, results


def _validate_rules(schema: str, data: str | rdflib.Graph) -> tuple[bool, set]:
    """Whether *data* conforms to the shapes of *schema*, and the focus nodes its rule constraints report."""
    conforms, results = _rule_results(schema, data)
    return conforms, {focus_node for focus_node, _, _ in results}


def _sparql_queries(g: rdflib.Graph, shape: URIRef) -> list[str]:
    """The ``sh:select`` query of every ``sh:sparql`` constraint on *shape*."""
    return [str(query) for node in g.objects(shape, SH.sparql) for query in g.objects(node, SH.select)]


def test_presence_implies_value_generates_sparql():
    """Presence-implies-value rules produce sh:sparql constraints on the NodeShape."""
    g = _parse_shacl(_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML)

    shape = EX_PIV.Document
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 2, f"Expected 2 sh:sparql constraints, got {len(sparql_nodes)}"

    for node in sparql_nodes:
        assert (node, RDF.type, SH.SPARQLConstraint) in g
        selects = list(g.objects(node, SH.select))
        assert len(selects) == 1, "Each constraint must have exactly one sh:select"
        query = str(selects[0])
        assert "$this" in query, "SPARQL must use $this pre-bound variable"
        assert "?value = " in query, "presence-implies-value SPARQL must compare the target by value"
        assert "FILTER" in query, "SPARQL must have a FILTER clause"


def test_presence_implies_value_single_uses_enum_iri():
    """A single equals_string target resolves to the enum meaning IRI."""
    g = _parse_shacl(_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML)

    signature_query = [q for q in _sparql_queries(g, EX_PIV.Document) if str(EX_PIV.signature) in q]
    assert len(signature_query) == 1, "Expected exactly one signature rule"
    query = signature_query[0]

    assert str(EX_PIV.status) in query
    assert f"<{EX_PIV.Published}>" in query, f"Expected Published IRI, got:\n{query}"


def test_presence_implies_value_set_uses_all_iris():
    """equals_string_in resolves every allowed value to its enum meaning IRI."""
    g = _parse_shacl(_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML)

    review_query = [q for q in _sparql_queries(g, EX_PIV.Document) if str(EX_PIV.review_score) in q]
    assert len(review_query) == 1, "Expected exactly one review_score rule"
    query = review_query[0]

    assert f"<{EX_PIV.Reviewed}>" in query, f"Expected Reviewed IRI, got:\n{query}"
    assert f"<{EX_PIV.Approved}>" in query, f"Expected Approved IRI, got:\n{query}"


def test_presence_implies_value_no_meaning_falls_back_to_literal():
    """When the target enum value lacks a meaning IRI, it is compared as a literal."""
    g = _parse_shacl(_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML)

    queries = _sparql_queries(g, EX_PIV.Device)
    assert len(queries) == 1
    query = queries[0]
    assert '"Manual"' in query, f"No-meaning enum should use literal '\"Manual\"', got:\n{query}"
    assert f"<{EX_PIV}Manual>" not in query, "Should not emit as IRI when meaning is absent"


def test_presence_implies_value_message_from_description():
    """Rule description is emitted as sh:message on the SPARQLConstraint."""
    g = _parse_shacl(_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML)

    sparql_nodes = list(g.objects(EX_PIV.Document, SH.sparql))
    messages = [str(m) for node in sparql_nodes for m in g.objects(node, SH.message)]

    assert any("status must be Published" in m for m in messages), f"Expected message about Published, got: {messages}"


def test_presence_implies_value_sparql_syntax_valid():
    """Generated SPARQL for presence-implies-value rules must be syntactically valid."""
    from rdflib.plugins.sparql import prepareQuery

    g = _parse_shacl(_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML)

    for shape in (EX_PIV.Document, EX_PIV.Device):
        for query in _sparql_queries(g, shape):
            prepareQuery(query)


@pytest.mark.parametrize(
    "instance,violates",
    [
        pytest.param('ex:x a ex:Document ; ex:signature "s" ; ex:status ex:Published .', False, id="single-ok"),
        pytest.param(
            'ex:x a ex:Document ; ex:review_score "4.5"^^xsd:float ; ex:status ex:Reviewed .', False, id="set-ok"
        ),
        pytest.param(
            'ex:x a ex:Document ; ex:review_score "3.0"^^xsd:float ; ex:status ex:Approved .',
            False,
            id="set-other-member-ok",
        ),
        pytest.param("ex:x a ex:Document ; ex:status ex:Draft .", False, id="unguarded"),
        pytest.param('ex:x a ex:Document ; ex:signature "s" ; ex:status ex:Draft .', True, id="wrong-value"),
        pytest.param(
            'ex:x a ex:Document ; ex:review_score "4.5"^^xsd:float ; ex:status ex:Published .',
            True,
            id="not-in-set",
        ),
        pytest.param('ex:x a ex:Document ; ex:signature "s" .', True, id="target-absent"),
        pytest.param('ex:x a ex:Device ; ex:manual_value 1.5 ; ex:mode "Manual" .', False, id="literal-ok"),
        pytest.param('ex:x a ex:Device ; ex:manual_value 1.5 ; ex:mode "Auto" .', True, id="literal-wrong"),
    ],
)
def test_presence_implies_value_pyshacl_end_to_end(instance: str, violates: bool):
    """End-to-end: pyshacl passes conforming instances and flags violations."""
    data = (
        "@prefix ex: <https://example.org/presence-implies-value/> .\n"
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n" + instance
    )
    conforms, focus_nodes = _validate_rules(_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML, data)
    assert focus_nodes == ({EX_PIV.x} if violates else set())
    assert conforms is not violates


@pytest.mark.parametrize(
    "instance,value",
    [
        pytest.param('ex:signature "s" ; ex:status ex:Draft', EX_PIV.Draft, id="wrong-value"),
        pytest.param('ex:signature "s"', EX_PIV.x, id="target-absent"),
    ],
)
def test_presence_implies_value_result_names_path_and_value(instance, value):
    """A result names the target property (``sh:resultPath``) and the
    offending value (``sh:value``); when the target is absent, SHACL §5.3.2
    falls back to the focus node as the value."""
    data = f"@prefix ex: <https://example.org/presence-implies-value/> .\nex:x a ex:Document ; {instance} ."
    _, results = _rule_results(_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML, data)
    assert results == [(EX_PIV.x, EX_PIV.status, value)]


# ===========================================================================
# equals_string / equals_string_in compare strings
# ===========================================================================
#
# The metamodel defines both operators for slots of range string: "the slot
# must have range string and the value of the slot must equal the specified
# value".  Enums, whose values are strings in instance data, and types with
# datatype xsd:string are treated alike.  A rule applying them to a slot of
# any other range is skipped with a warning: its RDF values are typed literals
# ("3"^^xsd:integer, false) or IRIs that equal no string, so a translated
# constraint would report conforming data or never fire.  On a string-valued
# slot the value is compared with the SPARQL "=" operator, which matches the
# RDF 1.1-identical plain and xsd:string literal forms alike, and an
# incomparable value counts as unequal rather than as an error.
#
# References:
#   - SPARQL 1.1 §17.4.1.3 <https://www.w3.org/TR/sparql11-query/#func-coalesce>
#   - SPARQL 1.1 §17.4.1.9 <https://www.w3.org/TR/sparql11-query/#func-in>
#   - RDF 1.1 Concepts §3.3 <https://www.w3.org/TR/rdf11-concepts/#section-Graph-Literal>
# ===========================================================================

_RULE_TARGET_RANGE_SCHEMA_YAML = """
id: https://example.org/rule-target-range
name: rule_target_range
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/rule-target-range/
  xsd: http://www.w3.org/2001/XMLSchema#
imports:
  - linkml:types
default_prefix: ex
default_range: string
types:
  label_string:
    typeof: string
  token_string:
    typeof: string
    uri: xsd:token
  flag_boolean:
    typeof: boolean
enums:
  Code:
    permissible_values:
      alpha:
      beta:
  Color:
    permissible_values:
      Red:
        meaning: ex:Red
      Blue:
        meaning: ex:Blue
  Answer:
    permissible_values:
      "true":
        meaning: ex:Yes
      "false":
        meaning: ex:No
  Mixed:
    permissible_values:
      A:
        meaning: ex:A
      B:
classes:
  Item:
    class_uri: ex:Item
    attributes:
      id:
        identifier: true
        range: uriorcurie
  Thing:
    class_uri: ex:Thing
    attributes:
      guard:
        multivalued: {guard_multivalued}
      target:
        range: {range}
        multivalued: {multivalued}
    rules:
      - open_world: {open_world}
        preconditions:
          slot_conditions:
            guard: {guard_condition}
        postconditions:
          slot_conditions:
            target: {target_condition}
  Sub:
    is_a: Thing
    class_uri: ex:Sub
"""

EX_RTR = rdflib.Namespace("https://example.org/rule-target-range/")

_RTR_PREFIXES = (
    "@prefix ex: <https://example.org/rule-target-range/> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
)


def _rule_target_schema(
    target_range: str,
    value: str | list[str],
    multivalued: bool = False,
    *,
    operator: str = "equals_string",
    open_world: bool = False,
    guard_multivalued: bool = False,
    guard_extra: dict | None = None,
    target_extra: dict | None = None,
) -> str:
    """The rule-target schema: if ``guard`` is present, ``target`` (of *target_range*) must satisfy *operator*.

    *value* is the operand of *operator* (a list for ``equals_string_in``);
    *guard_extra* and *target_extra* add operators to the two conditions.
    ``Sub`` inherits the rule from ``Thing``.
    """
    return _RULE_TARGET_RANGE_SCHEMA_YAML.format(
        range=target_range,
        multivalued=str(multivalued).lower(),
        guard_multivalued=str(guard_multivalued).lower(),
        open_world=str(open_world).lower(),
        guard_condition=json.dumps({"value_presence": "PRESENT", **(guard_extra or {})}),
        target_condition=json.dumps({operator: value, **(target_extra or {})}),
    )


@pytest.mark.parametrize(
    "target_range,operator,value,conforming_term",
    [
        pytest.param("integer", "equals_string", "3", "3", id="integer"),
        pytest.param("integer", "equals_string_in", ["3", "4"], "3", id="integer-equals-string-in"),
        pytest.param("float", "equals_string", "1.5", '"1.5"^^xsd:float', id="float"),
        pytest.param("decimal", "equals_string", "1.5", "1.5", id="decimal"),
        pytest.param("date", "equals_string", "2024-01-01", '"2024-01-01"^^xsd:date', id="date"),
        pytest.param("uriorcurie", "equals_string", "ex:a", "ex:a", id="uriorcurie"),
        pytest.param("token_string", "equals_string", "a", '"a"^^xsd:token', id="string-derived-xsd-token"),
        pytest.param("Item", "equals_string", "ex:i1", "ex:i1 . ex:i1 a ex:Item", id="class"),
    ],
)
def test_rule_equals_string_on_non_string_range_skipped(caplog, target_range, operator, value, conforming_term):
    """equals_string on a slot that does not hold strings is skipped with a warning.

    The data holds a typed literal or an IRI, which equals no string: comparing
    it with one would report every conforming instance.  The conforming instance
    must therefore pass, and the skip must be reported.
    """
    schema = _rule_target_schema(target_range, value, operator=operator)
    with caplog.at_level(logging.WARNING):
        g = _parse_shacl(schema)

    assert _sparql_queries(g, EX_RTR.Thing) == []
    assert _sparql_queries(g, EX_RTR.Sub) == []
    assert any(
        f"slot 'target', whose range '{target_range}' is neither an enum nor a type with datatype xsd:string or "
        "xsd:boolean" in rec.message
        for rec in caplog.records
    ), caplog.text
    conforms, focus_nodes = _validate_rules(
        schema, f'{_RTR_PREFIXES}ex:x a ex:Thing ; ex:guard "g" ; ex:target {conforming_term} .'
    )
    assert conforms and focus_nodes == set()


_STRING_TARGETS = [
    pytest.param("string", "x", '"x"', '"y"', id="string"),
    pytest.param("label_string", "x", '"x"', '"y"', id="string-derived"),
    pytest.param("curie", "ex:a", '"ex:a"', '"ex:b"', id="curie"),
    pytest.param("Code", "alpha", '"alpha"', '"beta"', id="enum-literal"),
    pytest.param("Color", "Red", "ex:Red", "ex:Blue", id="enum-meaning"),
    pytest.param("Answer", "true", "ex:Yes", "ex:No", id="enum-meaning-named-true"),
]


@pytest.mark.parametrize("target_range,value,allowed,other", _STRING_TARGETS)
@pytest.mark.parametrize(
    "body,violates",
    [
        pytest.param('ex:guard "g" ; ex:target {allowed}', False, id="allowed"),
        pytest.param('ex:guard "g" ; ex:target {allowed_xsd_string}', False, id="allowed-xsd-string"),
        pytest.param('ex:guard "g" ; ex:target {other}', True, id="other"),
        pytest.param('ex:guard "g" ; ex:target {allowed}, {other}', True, id="allowed-and-other"),
        pytest.param('ex:guard "g"', True, id="target-absent"),
        pytest.param("ex:target {other}", False, id="guard-absent"),
    ],
)
@pytest.mark.parametrize("multivalued", [False, True])
def test_rule_equals_string_on_string_range_compares_values(
    target_range, value, allowed, other, body, violates, multivalued
):
    """On a string-valued target, equals_string compares the value the range holds.

    A string type holds plain literals, an enum its meaning IRI or a plain
    literal; the ``xsd:string``-typed form of a plain literal is the same RDF
    1.1 term and must also satisfy the rule.  An enum value named ``true``
    with a meaning is an IRI like any other, not a boolean.
    """
    allowed_xsd_string = f"{allowed}^^xsd:string" if allowed.startswith('"') else allowed
    schema = _rule_target_schema(target_range, value, multivalued)
    data = body.format(allowed=allowed, allowed_xsd_string=allowed_xsd_string, other=other)

    assert len(_sparql_queries(_parse_shacl(schema), EX_RTR.Thing)) == 1
    _, focus_nodes = _validate_rules(schema, f"{_RTR_PREFIXES}ex:x a ex:Thing ; {data} .")
    assert focus_nodes == ({EX_RTR.x} if violates else set())


_RULE_INSTANCES = [
    pytest.param({"guard": "g", "target": "{value}"}, True, True, id="allowed"),
    pytest.param({"guard": "g", "target": "{other}"}, False, False, id="other"),
    pytest.param({"guard": "g"}, False, True, id="target-absent"),
    pytest.param({"target": "{other}"}, True, True, id="guard-absent"),
]
"""JSON instances of the rule-target schema, with their validity under closed- and open-world rules."""


def _json_schema_and_shacl_verdicts(
    schema: str, target_class: str, obj: dict, coerce_xsd_string: bool = False
) -> tuple[bool, bool]:
    """Whether the JSON Schema and the SHACL rules generated for *schema* accept *obj*.

    *obj* is validated as is by the generated JSON Schema, and as RDF loaded
    through the generated JSON-LD context by the generated SHACL shapes (rule
    constraints only).  With *coerce_xsd_string* the context types the
    ``target`` slot ``xsd:string``, as JSON-LD 1.1 type coercion permits,
    which yields the RDF 1.1-identical typed form of a plain literal.
    """
    import jsonschema

    from linkml.generators.jsonldcontextgen import ContextGenerator
    from linkml.generators.jsonschemagen import JsonSchemaGenerator

    json_schema = json.loads(JsonSchemaGenerator(schema, top_class=target_class).serialize())
    json_schema_valid = jsonschema.Draft7Validator(json_schema).is_valid(obj)

    context = json.loads(ContextGenerator(schema).serialize())["@context"]
    if coerce_xsd_string and context["target"].get("@type") is None:
        context["target"]["@type"] = "xsd:string"
    document = {"@context": context, "@type": target_class, **obj}
    _, focus_nodes = _validate_rules(schema, rdflib.Graph().parse(data=json.dumps(document), format="json-ld"))
    return json_schema_valid, focus_nodes == set()


@pytest.mark.parametrize(
    "target_range,value,other",
    [
        pytest.param("string", "x", "y", id="string"),
        pytest.param("curie", "ex:a", "ex:b", id="curie"),
        pytest.param("Code", "alpha", "beta", id="enum-literal"),
        pytest.param("Color", "Red", "Blue", id="enum-meaning"),
    ],
)
@pytest.mark.parametrize("instance,valid,_valid_open_world", _RULE_INSTANCES)
@pytest.mark.parametrize("coerce_xsd_string", [False, True])
def test_rule_equals_string_agrees_with_json_schema(
    target_range, value, other, instance, valid, _valid_open_world, coerce_xsd_string
):
    """The SHACL rule and the JSON Schema rule decide the same instance alike.

    One JSON object is checked by both generated artifacts (see
    :func:`_json_schema_and_shacl_verdicts`), with and without ``xsd:string``
    coercion of the target, which the test adds to the generated context.  An
    enum whose values all have a meaning in one namespace is mapped to those
    IRIs by the context and stays untyped.
    """
    obj = {key: text.format(value=value, other=other) for key, text in instance.items()}
    verdicts = _json_schema_and_shacl_verdicts(
        _rule_target_schema(target_range, value), "Thing", obj, coerce_xsd_string
    )
    assert verdicts == (valid, valid)


@pytest.mark.parametrize(
    "target_range,value,other",
    [
        pytest.param("string", "x", "y", id="string"),
        pytest.param("Color", "Red", "Blue", id="enum-meaning"),
    ],
)
@pytest.mark.parametrize("instance,valid_closed_world,valid_open_world", _RULE_INSTANCES)
@pytest.mark.parametrize("target_class", ["Thing", "Sub"])
@pytest.mark.parametrize("open_world", [False, True])
def test_rule_inheritance_and_open_world_agree_with_json_schema(
    target_range, value, other, instance, valid_closed_world, valid_open_world, target_class, open_world
):
    """A rule binds the instances of subclasses of its class, and ``open_world``
    lets the postcondition be omitted, in SHACL as in JSON Schema.

    The metamodel defines ``open_world`` as "the postconditions may be omitted
    in instance data", so an absent target satisfies an open-world rule.
    """
    obj = {key: text.format(value=value, other=other) for key, text in instance.items()}
    schema = _rule_target_schema(target_range, value, open_world=open_world)
    valid = valid_open_world if open_world else valid_closed_world
    assert _json_schema_and_shacl_verdicts(schema, target_class, obj) == (valid, valid)


@pytest.mark.parametrize("flag_range", ["boolean", "flag_boolean"])
@pytest.mark.parametrize("open_world", [False, True])
@pytest.mark.parametrize("required", ["true", "1", "false", "0"])
@pytest.mark.parametrize(
    "flag,datatype",
    [
        pytest.param("true", XSD.boolean, id="true"),
        pytest.param("1", XSD.boolean, id="lexical-1"),
        pytest.param("false", XSD.boolean, id="false"),
        pytest.param("0", XSD.boolean, id="lexical-0"),
        pytest.param("true", None, id="string-true"),
        pytest.param(None, None, id="absent"),
    ],
)
def test_rule_boolean_target_compared_by_value(flag_range, open_world, required, flag, datatype):
    """equals_string on an xsd:boolean-typed slot (the boolean guard, for
    "true") requires the boolean its value denotes in the lexical space of
    xsd:boolean (XML Schema 1.1 Part 2 §3.3.2.2), whichever type the slot's
    range derives it from.  The flag is compared by value, so every lexical
    form of a boolean satisfies the rule and a string "true" does not; an
    open-world rule lets the flag be omitted.

    The data is built with unnormalised literals: rdflib would otherwise
    rewrite ``"1"^^xsd:boolean`` to ``true`` while parsing, and a lexical
    comparison would pass as well.
    """
    schema = _rule_target_schema(flag_range, required, open_world=open_world)
    required_value = required in ("true", "1")
    queries = _sparql_queries(_parse_shacl(schema), EX_RTR.Thing)
    assert len(queries) == 1
    assert f"?value = {str(required_value).lower()}" in queries[0], queries[0]

    data = rdflib.Graph()
    data.add((EX_RTR.x, RDF.type, EX_RTR.Thing))
    data.add((EX_RTR.x, EX_RTR.guard, Literal("g")))
    if flag is not None:
        data.add((EX_RTR.x, EX_RTR.target, Literal(flag, datatype=datatype, normalize=False)))
    if flag is None:
        violates = not open_world
    else:
        violates = datatype is None or (flag in ("true", "1")) != required_value
    _, focus_nodes = _validate_rules(schema, data)
    assert focus_nodes == ({EX_RTR.x} if violates else set())


@pytest.mark.parametrize("value", ["yes", "True", "TRUE", " true", ""])
def test_rule_boolean_target_non_lexical_value_skipped(caplog, value):
    """A value outside the lexical space of xsd:boolean on a boolean slot equals
    no boolean, so the rule is skipped with a warning.  The lexical space is
    exactly {true, false, 1, 0}: it is case-sensitive and has no whitespace."""
    with caplog.at_level(logging.WARNING):
        g = _parse_shacl(_rule_target_schema("boolean", value))
    assert _sparql_queries(g, EX_RTR.Thing) == []
    assert any("not all xsd:boolean lexical forms" in rec.message for rec in caplog.records), caplog.text


@pytest.mark.parametrize(
    "target,violates",
    [
        pytest.param("ex:A", False, id="meaning-iri"),
        pytest.param('"B"', False, id="literal"),
        pytest.param('"B"^^xsd:string', False, id="literal-xsd-string"),
        pytest.param('"A"', True, id="literal-of-value-with-meaning"),
        pytest.param("ex:B", True, id="iri-of-value-without-meaning"),
        pytest.param('"C"', True, id="other"),
    ],
)
def test_rule_equals_string_in_mixes_meaning_iris_and_literals(target, violates):
    """``equals_string_in`` over permissible values with and without a meaning
    compares each as the term it is rendered as: its meaning IRI, or a literal."""
    schema = _rule_target_schema("Mixed", ["A", "B"], operator="equals_string_in")
    _, focus_nodes = _validate_rules(schema, f'{_RTR_PREFIXES}ex:x a ex:Thing ; ex:guard "g" ; ex:target {target} .')
    assert focus_nodes == ({EX_RTR.x} if violates else set())


@pytest.mark.parametrize(
    "target,violates",
    [pytest.param('"x"', False, id="allowed"), pytest.param('"y"', True, id="other")],
)
def test_rule_multivalued_guard(target, violates):
    """Several guard values trigger the rule once per focus node, like one."""
    schema = _rule_target_schema("string", "x", guard_multivalued=True)
    data = f'{_RTR_PREFIXES}ex:x a ex:Thing ; ex:guard "g1", "g2", "g3" ; ex:target {target} .'
    _, results = _rule_results(schema, data)
    assert results == ([(EX_RTR.x, EX_RTR.target, rdflib.Literal("y"))] if violates else [])


def test_rule_query_yields_one_solution_per_focus_node():
    """Each solution of a SPARQL-based constraint is a validation result
    (SHACL §5.3.2), so several guard values must not multiply the solutions.
    pyshacl merges identical results; the query itself must not rely on it."""
    schema = _rule_target_schema("string", "x", guard_multivalued=True)
    (query,) = _sparql_queries(_parse_shacl(schema), EX_RTR.Thing)
    data = rdflib.Graph().parse(
        data=f'{_RTR_PREFIXES}ex:x a ex:Thing ; ex:guard "g1", "g2", "g3" ; ex:target "y" .', format="turtle"
    )
    assert len(list(data.query(query, initBindings={"this": EX_RTR.x}))) == 1


@pytest.mark.parametrize("dawg_literal_collation", [False, True])
def test_rule_incomparable_value_is_a_violation(monkeypatch, dawg_literal_collation):
    """A value no allowed value can be compared with equals none of them.

    SPARQL ``=`` raises a type error for literals it cannot compare
    (RDFterm-equal, SPARQL 1.1 §17.4.1.7), and a FILTER error drops the row, so
    a spec-conformant engine would miss the violation unless the comparison
    turns the error into false.  ``rdflib.DAWG_LITERAL_COLLATION`` switches
    rdflib from its lenient comparison to that spec-conformant one.
    """
    monkeypatch.setattr(rdflib, "DAWG_LITERAL_COLLATION", dawg_literal_collation)
    schema = _rule_target_schema("string", "x")
    data = f'{_RTR_PREFIXES}ex:x a ex:Thing ; ex:guard "g" ; ex:target "x"^^ex:custom .'
    _, focus_nodes = _validate_rules(schema, data)
    assert focus_nodes == {EX_RTR.x}

    exclusive = _exclusive_schema("Tag", "alpha", 1)
    data = (
        '@prefix ex: <https://example.org/exclusive-range/> .\nex:x a ex:Thing ; ex:tags "alpha", "beta"^^ex:custom .'
    )
    _, focus_nodes = _validate_rules(exclusive, data)
    assert focus_nodes == {EX_EXR.x}


def test_rule_value_not_a_permissible_value_warns(caplog):
    """An equals_string value that is not a permissible value of the enum is
    reported: no valid value of the slot can equal it, so the rule rejects
    every instance it applies to."""
    schema = _rule_target_schema("Color", "Purple")
    with caplog.at_level(logging.WARNING):
        queries = _sparql_queries(_parse_shacl(schema), EX_RTR.Thing)

    assert len(queries) == 1
    assert any("'Purple', which is not a permissible value of enum 'Color'" in rec.message for rec in caplog.records)
    _, focus_nodes = _validate_rules(schema, f'{_RTR_PREFIXES}ex:x a ex:Thing ; ex:guard "g" ; ex:target ex:Red .')
    assert focus_nodes == {EX_RTR.x}


@pytest.mark.parametrize(
    "value",
    [
        pytest.param('a"b', id="quote"),
        pytest.param("a\\b", id="backslash"),
        pytest.param("line\nbreak", id="newline"),
        pytest.param("carriage\rreturn", id="carriage-return"),
        pytest.param("tab\there", id="tab"),
        pytest.param("a\\u0022b", id="backslash-u"),
        pytest.param("a\\U00000022b", id="backslash-capital-u"),
        pytest.param("check ✓", id="non-ascii"),
        pytest.param("", id="empty"),
    ],
)
def test_rule_string_value_round_trips(value):
    """An equals_string value of any content is matched exactly: the query
    parses, the value itself satisfies the rule, and any other value does not.

    Codepoint escapes are replaced before a SPARQL query is parsed (SPARQL 1.1
    §19.2), so a backslash followed by ``u`` in the value must not reach the
    query as an escape sequence.
    """
    from rdflib.plugins.sparql import prepareQuery

    schema = _rule_target_schema("string", value)
    queries = _sparql_queries(_parse_shacl(schema), EX_RTR.Thing)
    assert len(queries) == 1
    prepareQuery(queries[0])

    for target, violates in ((value, False), (value + "!", True)):
        data = rdflib.Graph()
        data.add((EX_RTR.x, RDF.type, EX_RTR.Thing))
        data.add((EX_RTR.x, EX_RTR.guard, Literal("g")))
        data.add((EX_RTR.x, EX_RTR.target, Literal(target)))
        _, focus_nodes = _validate_rules(schema, data)
        assert focus_nodes == ({EX_RTR.x} if violates else set()), repr(target)


_EXCLUSIVE_RANGE_SCHEMA_YAML = """
id: https://example.org/exclusive-range
name: exclusive_range
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/exclusive-range/
imports:
  - linkml:types
default_prefix: ex
default_range: string
enums:
  Tag:
    permissible_values:
      alpha:
      beta:
      gamma:
classes:
  Thing:
    class_uri: ex:Thing
    attributes:
      tags:
        range: {range}
        multivalued: true
    rules:
      - preconditions:
          slot_conditions:
            tags: {precondition}
        postconditions:
          slot_conditions:
            tags:
              maximum_cardinality: {max_card}
"""

EX_EXR = rdflib.Namespace("https://example.org/exclusive-range/")


def _exclusive_schema(tag_range: str, value: str, max_card: int, *, has_member: bool = True) -> str:
    """The exclusive-value schema: if *value* is one of the ``tags``, there are at most *max_card* of them.

    The precondition is ``has_member: {equals_string: value}``, or with
    ``has_member=False`` the bare ``equals_string: value``.
    """
    precondition = {"has_member": {"equals_string": value}} if has_member else {"equals_string": value}
    return _EXCLUSIVE_RANGE_SCHEMA_YAML.format(
        range=tag_range, precondition=json.dumps(precondition), max_card=max_card
    )


@pytest.mark.parametrize("has_member", [True, False])
@pytest.mark.parametrize(
    "max_card,values,violates",
    [
        pytest.param(1, '"alpha", "beta"', True, id="max1-plain"),
        pytest.param(1, '"alpha"^^xsd:string, "beta"^^xsd:string', True, id="max1-xsd-string"),
        pytest.param(1, '"alpha"', False, id="max1-alone"),
        pytest.param(1, '"beta", "gamma"', False, id="max1-absent"),
        pytest.param(2, '"alpha", "beta", "gamma"', True, id="max2-plain"),
        pytest.param(2, '"alpha"^^xsd:string, "beta", "gamma"', True, id="max2-xsd-string"),
        pytest.param(2, '"alpha", "beta"', False, id="max2-within"),
    ],
)
def test_exclusive_value_matches_value_not_term(has_member, max_card, values, violates):
    """The exclusive value is matched by value, so its RDF 1.1-identical
    ``xsd:string``-typed form triggers the rule as the plain literal does, and
    a ``maximum_cardinality`` above 1 is enforced.  The precondition
    ``has_member: {equals_string: V}`` and the bare ``equals_string: V`` are
    translated alike."""
    schema = _exclusive_schema("Tag", "alpha", max_card, has_member=has_member)
    data = (
        "@prefix ex: <https://example.org/exclusive-range/> .\n"
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
        f"ex:x a ex:Thing ; ex:tags {values} ."
    )
    _, focus_nodes = _validate_rules(schema, data)
    assert focus_nodes == ({EX_EXR.x} if violates else set())


@pytest.mark.parametrize("max_card", [1, 2])
def test_exclusive_value_result_names_path_and_value(max_card):
    """A result names the slot.  For ``maximum_cardinality: 1`` its value is
    each value coexisting with the exclusive one; otherwise no value is
    projected and SHACL §5.3.2 falls back to the focus node."""
    data = '@prefix ex: <https://example.org/exclusive-range/> .\nex:x a ex:Thing ; ex:tags "alpha", "beta", "gamma" .'
    _, results = _rule_results(_exclusive_schema("Tag", "alpha", max_card), data)
    if max_card == 1:
        assert sorted(results) == sorted(
            [(EX_EXR.x, EX_EXR.tags, Literal("beta")), (EX_EXR.x, EX_EXR.tags, Literal("gamma"))]
        )
    else:
        assert results == [(EX_EXR.x, EX_EXR.tags, EX_EXR.x)]


@pytest.mark.parametrize("max_card", [1, 2])
def test_exclusive_value_query_yields_distinct_solutions(max_card):
    """The exclusive value in both RDF 1.1-identical forms binds twice; each
    solution is a validation result (SHACL §5.3.2), so the query must not
    multiply them."""
    (query,) = _sparql_queries(_parse_shacl(_exclusive_schema("Tag", "alpha", max_card)), EX_EXR.Thing)
    data = rdflib.Graph().parse(
        data="@prefix ex: <https://example.org/exclusive-range/> .\n"
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
        'ex:x a ex:Thing ; ex:tags "alpha", "alpha"^^xsd:string, "beta" .',
        format="turtle",
    )
    assert len(list(data.query(query, initBindings={"this": EX_EXR.x}))) == 1


def test_exclusive_value_bare_equals_string_warns(caplog):
    """A bare equals_string precondition on a multivalued slot is translated as
    "one of the values equals", with a warning: the specification applies a
    slot constraint to all members of a collection, and has_member states the
    intended reading explicitly."""
    with caplog.at_level(logging.WARNING):
        assert _sparql_queries(_parse_shacl(_exclusive_schema("Tag", "alpha", 1, has_member=False)), EX_EXR.Thing)
    assert any("has_member" in rec.message and "all members" in rec.message for rec in caplog.records), caplog.text
    caplog.clear()
    with caplog.at_level(logging.WARNING):
        _parse_shacl(_exclusive_schema("Tag", "alpha", 1))
    assert not any("has_member" in rec.message for rec in caplog.records), caplog.text


@pytest.mark.parametrize(
    "precondition",
    [
        pytest.param({"has_member": {"equals_string": "alpha", "pattern": "^a"}}, id="inside-has_member"),
        pytest.param({"has_member": {"equals_string": "alpha"}, "minimum_cardinality": 2}, id="beside-has_member"),
    ],
)
def test_exclusive_value_has_member_extra_operator_skipped(caplog, precondition):
    """has_member is exact too: an operator next to its equals_string, or next
    to has_member itself, makes the rule untranslatable."""
    precondition = json.dumps(precondition)
    schema = _EXCLUSIVE_RANGE_SCHEMA_YAML.format(range="Tag", precondition=precondition, max_card=1)
    with caplog.at_level(logging.WARNING):
        assert _sparql_queries(_parse_shacl(schema), EX_EXR.Thing) == []
    assert any("match none of the translated patterns" in rec.message for rec in caplog.records), caplog.text


def test_exclusive_value_on_non_string_range_skipped(caplog):
    """equals_string on a slot that does not hold strings is skipped with a
    warning in the exclusive-value pattern too: the integer ``3`` never equals
    the string "3", so the constraint would never fire."""
    schema = _exclusive_schema("integer", "3", 1)
    with caplog.at_level(logging.WARNING):
        g = _parse_shacl(schema)

    assert _sparql_queries(g, EX_EXR.Thing) == []
    assert any("whose range 'integer' is neither an enum" in rec.message for rec in caplog.records), caplog.text


def test_rule_non_operator_fields_are_the_metamodel_element_metadata():
    """The fields the operator accounting ignores are exactly the metamodel's
    ``element`` slots that are not ``slot_expression`` slots."""
    from linkml_runtime.utils.formatutils import underscore
    from linkml_runtime.utils.introspection import package_schemaview

    metamodel = package_schemaview("linkml_runtime.linkml_model.meta")
    element_slots = {underscore(s) for s in metamodel.class_slots("element")}
    operator_slots = {underscore(s) for s in metamodel.class_slots("slot_expression")}

    assert ShaclGenerator._NON_OPERATOR_FIELDS == element_slots - operator_slots
    assert {"description", "annotations", "title"} <= ShaclGenerator._NON_OPERATOR_FIELDS


def test_rule_condition_metadata_does_not_block_translation():
    """Metadata on a condition does not change which instances satisfy it,
    so it does not make an otherwise recognised rule untranslatable."""
    schema = _rule_target_schema(
        "string",
        "x",
        guard_extra={"title": "Guard set"},
        target_extra={"description": "The target must then be x.", "comments": ["Metadata only."]},
    )
    assert len(_sparql_queries(_parse_shacl(schema), EX_RTR.Thing)) == 1


# ===========================================================================
# Rule inheritance
#
# A rule applies to "all members of this class" (metamodel `rules`), so a
# class shape carries the rules of its ancestors and mixins, each translated
# in the class's own context.
# ===========================================================================

_RULE_INHERITANCE_SCHEMA_YAML = """
id: https://example.org/rule-inheritance
name: rule_inheritance
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/rule-inheritance/
imports:
  - linkml:types
default_prefix: ex
default_range: string
enums:
  Color:
    permissible_values:
      Red:
        meaning: ex:Red
      Blue:
        meaning: ex:Blue
  Shade:
    permissible_values:
      Red:
        meaning: ex:ShadeRed
slots:
  guard: {}
  target:
    range: Color
  code: {}
  label: {}
classes:
  Base:
    class_uri: ex:Base
    slots: [guard, target]
    rules:
      - preconditions:
          slot_conditions:
            guard:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            target:
              equals_string: Red
  Child:
    is_a: Base
    class_uri: ex:Child
  GrandChild:
    is_a: Child
    class_uri: ex:GrandChild
  Shaded:
    is_a: Base
    class_uri: ex:Shaded
    slot_usage:
      target:
        range: Shade
  Counted:
    is_a: Base
    class_uri: ex:Counted
    slot_usage:
      target:
        range: integer
  Labelled:
    mixin: true
    class_uri: ex:Labelled
    slots: [code, label]
    rules:
      - preconditions:
          slot_conditions:
            code:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            label:
              equals_string: x
  Mixed:
    class_uri: ex:Mixed
    mixins: [Labelled]
  SameUri:
    is_a: Base
    class_uri: ex:Base
"""

EX_RI = rdflib.Namespace("https://example.org/rule-inheritance/")


def test_rule_inherited_by_descendant_shapes(caplog):
    """The shape of a class carries the rules of its ancestors and mixins, each
    translated in the class's own context: a ``slot_usage`` that narrows the
    target to another enum resolves the value there, and one that narrows it to
    a non-string range skips the rule for that class only.  A class sharing its
    ancestor's ``class_uri`` shares its shape, which carries the rule once."""
    with caplog.at_level(logging.WARNING):
        g = _parse_shacl(_RULE_INHERITANCE_SCHEMA_YAML)

    for cls in ("Base", "Child", "GrandChild", "Shaded", "Labelled", "Mixed"):
        assert len(_sparql_queries(g, EX_RI[cls])) == 1, cls
    assert f"<{EX_RI.ShadeRed}>" in _sparql_queries(g, EX_RI.Shaded)[0]
    assert _sparql_queries(g, EX_RI.Counted) == []
    assert any("'Counted'" in rec.message and "is neither an enum" in rec.message for rec in caplog.records)


@pytest.mark.parametrize(
    "instance,violates",
    [
        pytest.param('ex:x a ex:Child ; ex:guard "g" ; ex:target ex:Red .', False, id="child-ok"),
        pytest.param('ex:x a ex:Child ; ex:guard "g" ; ex:target ex:Blue .', True, id="child-violates"),
        pytest.param('ex:x a ex:GrandChild ; ex:guard "g" ; ex:target ex:Blue .', True, id="grandchild-violates"),
        pytest.param('ex:x a ex:Shaded ; ex:guard "g" ; ex:target ex:ShadeRed .', False, id="narrowed-ok"),
        pytest.param('ex:x a ex:Shaded ; ex:guard "g" ; ex:target ex:Red .', True, id="narrowed-violates"),
        pytest.param('ex:x a ex:Mixed ; ex:code "c" ; ex:label "x" .', False, id="mixin-ok"),
        pytest.param('ex:x a ex:Mixed ; ex:code "c" ; ex:label "y" .', True, id="mixin-violates"),
    ],
)
def test_rule_inherited_rule_enforced_on_descendant_instances(instance, violates):
    """An instance typed only with a descendant class is held to the inherited rule."""
    data = f"@prefix ex: <https://example.org/rule-inheritance/> .\n{instance}"
    _, focus_nodes = _validate_rules(_RULE_INHERITANCE_SCHEMA_YAML, data)
    assert focus_nodes == ({EX_RI.x} if violates else set())


def test_rule_shared_shape_reports_once():
    """Two classes sharing a ``class_uri`` share one shape, so an instance
    violating the rule both inherit gets one result, not one per class."""
    data = '@prefix ex: <https://example.org/rule-inheritance/> .\nex:x a ex:Base ; ex:guard "g" ; ex:target ex:Blue .'
    _, results = _rule_results(_RULE_INHERITANCE_SCHEMA_YAML, data)
    assert results == [(EX_RI.x, EX_RI.target, EX_RI.Blue)]


# ===========================================================================
# Slot resolution and value rendering
#
# A rule's SPARQL body must query the same IRI that ``sh:path`` emits for the
# slot, and resolve the slot's range in the class:
#   1. a slot_usage `slot_uri` (or enum `range`) override applies to the rule;
#   2. an alias-form key (``my_slot`` for slot ``my slot``) names the slot;
#   3. a slot without a range takes the schema's `default_range`;
#   4. built-in type names resolve without importing linkml:types;
#   5. a condition on an unknown or identifier slot makes the rule untranslatable.
# ===========================================================================


_ENUM_NARROWING_SCHEMA_YAML = """
id: https://example.org/enum-narrowing
name: enum_narrowing_rules
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/enum-narrowing/
imports:
  - linkml:types
default_prefix: ex
default_range: string

enums:
  BaseMode:
    permissible_values:
      Active:
        meaning: ex:GLOBAL_Active
  SceneMode:
    permissible_values:
      Active:
        meaning: ex:LOCAL_Active

slots:
  activator:
    range: string
    slot_uri: ex:activator
  mode:
    range: BaseMode
    slot_uri: ex:mode

classes:
  Scene:
    class_uri: ex:Scene
    slots:
      - activator
      - mode
    slot_usage:
      mode:
        range: SceneMode
    rules:
      - description: If an activator is present the mode must be Active.
        preconditions:
          slot_conditions:
            activator:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            mode:
              equals_string: Active
"""

EX_EN = rdflib.Namespace("https://example.org/enum-narrowing/")


def test_rule_enum_range_narrowed_by_slot_usage():
    """A slot_usage range override to a class-specific enum must resolve the
    value's meaning against the induced (narrowed) enum, not the base range."""
    queries = _sparql_queries(_parse_shacl(_ENUM_NARROWING_SCHEMA_YAML), EX_EN.Scene)
    assert len(queries) == 1
    query = queries[0]
    assert str(EX_EN.LOCAL_Active) in query, f"must resolve the narrowed enum meaning, got:\n{query}"
    assert "GLOBAL_Active" not in query, f"must not resolve the base enum meaning, got:\n{query}"


_SLOT_RESOLUTION_SCHEMA_YAML = """
id: https://example.org/slot-resolution
name: slot_resolution
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/slot-resolution/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  guard: {}
  my slot: {}
  target: {}
classes:
  Thing:
    class_uri: ex:Thing
    slots: [guard, my slot, target]
    slot_usage:
      target:
        slot_uri: ex:narrowed_target
    rules:
      - preconditions:
          slot_conditions:
            guard:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            target:
              equals_string: x
      - preconditions:
          slot_conditions:
            my_slot:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            target:
              equals_string: x
"""

EX_SR = rdflib.Namespace("https://example.org/slot-resolution/")


def test_rule_slot_iris_match_sh_path():
    """Every predicate a rule queries is one that ``sh:path`` emits: a
    slot_usage ``slot_uri`` override and an alias-form key resolve to the
    slot's own IRI rather than a fabricated one the data never uses."""
    g = _parse_shacl(_SLOT_RESOLUTION_SCHEMA_YAML)

    paths = {str(path) for path in g.objects(None, SH.path)}
    queries = _sparql_queries(g, EX_SR.Thing)
    assert len(queries) == 2
    for query in queries:
        assert set(re.findall(r"<([^>]+)>", query)) <= paths, query
        assert f"<{EX_SR.narrowed_target}>" in query, query
    assert any(f"<{EX_SR.my_slot}>" in query for query in queries)

    _, focus_nodes = _validate_rules(
        _SLOT_RESOLUTION_SCHEMA_YAML,
        "@prefix ex: <https://example.org/slot-resolution/> .\n"
        'ex:x a ex:Thing ; ex:my_slot "s" ; ex:narrowed_target "y" .',
    )
    assert focus_nodes == {EX_SR.x}


_RANGE_RESOLUTION_SCHEMA_YAML = """
id: https://example.org/range-resolution
name: range_resolution
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/range-resolution/
imports:
  - linkml:types
default_prefix: ex
default_range: {default_range}
slots:
  guard:
    range: string
  target: {target_slot}
classes:
  Thing:
    class_uri: ex:Thing
    slots: {class_slots}
    slot_usage: {slot_usage}
    rules:
      - preconditions:
          slot_conditions:
            guard:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            target:
              equals_string: "3"
"""

EX_RR = rdflib.Namespace("https://example.org/range-resolution/")


@pytest.mark.parametrize(
    "default_range,target_slot,class_slots,slot_usage,translated",
    [
        pytest.param("string", "{}", "[guard, target]", "{}", True, id="default-range-string"),
        pytest.param("integer", "{}", "[guard, target]", "{}", False, id="default-range-integer"),
        pytest.param(
            "string",
            "{range: integer}",
            "[guard, target]",
            "{target: {range: string}}",
            True,
            id="slot-usage-to-string",
        ),
        pytest.param(
            "string", "{}", "[guard, target]", "{target: {range: integer}}", False, id="slot-usage-to-integer"
        ),
        pytest.param("string", "{}", "[guard]", "{}", True, id="slot-not-on-class-default-string"),
        pytest.param("integer", "{}", "[guard]", "{}", False, id="slot-not-on-class-default-integer"),
    ],
)
def test_rule_target_range_resolved_in_class_context(default_range, target_slot, class_slots, slot_usage, translated):
    """Whether the target holds strings is decided by its range in the class:
    the schema's ``default_range`` for a slot without one, as refined by
    ``slot_usage``, also for a slot the class does not declare."""
    schema = _RANGE_RESOLUTION_SCHEMA_YAML.format(
        default_range=default_range, target_slot=target_slot, class_slots=class_slots, slot_usage=slot_usage
    )
    assert len(_sparql_queries(_parse_shacl(schema), EX_RR.Thing)) == (1 if translated else 0)
    if translated:
        prefix = "@prefix ex: <https://example.org/range-resolution/> .\n"
        assert _validate_rules(schema, f'{prefix}ex:x a ex:Thing ; ex:guard "g" ; ex:target "3" .')[1] == set()
        assert _validate_rules(schema, f'{prefix}ex:x a ex:Thing ; ex:guard "g" ; ex:target "4" .')[1] == {EX_RR.x}


EX_SINGLE = rdflib.Namespace("https://example.org/single-rule/")


def _single_rule_schema(rule: dict, attributes: dict | None = None, *, imports: bool = True) -> str:
    """A schema whose class ``Thing`` has *attributes* and the one *rule* (JSON, which is YAML).

    By default the attributes are the string slots ``guard``, ``target`` and
    ``other``, the boolean ``flag`` and the multivalued ``tags``.  Without
    *imports* the schema does not import ``linkml:types`` and has no
    ``default_range``.
    """
    schema = {
        "id": "https://example.org/single-rule",
        "name": "single_rule",
        "prefixes": {"linkml": "https://w3id.org/linkml/", "ex": str(EX_SINGLE)},
        "default_prefix": "ex",
        "classes": {
            "Thing": {
                "class_uri": "ex:Thing",
                "attributes": attributes
                or {
                    "guard": {"range": "string"},
                    "target": {"range": "string"},
                    "other": {"range": "string"},
                    "flag": {"range": "boolean"},
                    "tags": {"range": "string", "multivalued": True},
                },
                "rules": [rule],
            }
        },
    }
    if imports:
        schema["imports"] = ["linkml:types"]
        schema["default_range"] = "string"
    return json.dumps(schema)


def _rule(pre: dict, post: dict, **rule_fields) -> dict:
    """A rule with the slot conditions *pre* and *post*."""
    return {"preconditions": {"slot_conditions": pre}, "postconditions": {"slot_conditions": post}, **rule_fields}


_GUARD_PRESENT = {"guard": {"value_presence": "PRESENT"}}


def _assert_skipped(caplog, schema: str, reason: str) -> None:
    """Generating *schema* emits no rule constraint and warns that the rule was skipped for *reason*."""
    with caplog.at_level(logging.WARNING):
        g = _parse_shacl(schema)
    assert _sparql_queries(g, EX_SINGLE.Thing) == []
    assert any("skipped, because" in rec.message and reason in rec.message for rec in caplog.records), caplog.text


@pytest.mark.parametrize(
    "target_range,value,allowed,other",
    [
        pytest.param("boolean", "true", "true", "false", id="boolean-guard"),
        pytest.param("string", "x", '"x"', '"y"', id="string"),
        pytest.param("curie", "ex:a", '"ex:a"', '"ex:b"', id="curie"),
        pytest.param(None, "x", '"x"', '"y"', id="no-range"),
    ],
)
def test_rule_builtin_types_without_imports(target_range, value, allowed, other):
    """In a schema that does not import ``linkml:types``, a built-in range name
    resolves as the main slot loop resolves it, so the boolean guard and the
    string comparison are both translated.  A slot with no range at all (and
    no ``default_range``) holds untyped values, compared as strings as the
    JSON Schema generator compares them."""
    target = {} if target_range is None else {"range": target_range}
    schema = _single_rule_schema(
        _rule(_GUARD_PRESENT, {"target": {"equals_string": value}}),
        {"guard": {"range": "string"}, "target": target},
        imports=False,
    )
    assert len(_sparql_queries(_parse_shacl(schema), EX_SINGLE.Thing)) == 1
    prefix = "@prefix ex: <https://example.org/single-rule/> .\n"
    for term, violates in ((allowed, False), (other, True)):
        data = f'{prefix}ex:x a ex:Thing ; ex:guard "g" ; ex:target {term} .'
        assert _validate_rules(schema, data)[1] == ({EX_SINGLE.x} if violates else set())


def test_rule_builtin_non_string_type_without_imports_skipped(caplog):
    """A built-in non-string range without the ``linkml:types`` import is skipped like an imported one."""
    schema = _single_rule_schema(
        _rule(_GUARD_PRESENT, {"target": {"equals_string": "3"}}),
        {"guard": {"range": "string"}, "target": {"range": "integer"}},
        imports=False,
    )
    _assert_skipped(caplog, schema, "is neither an enum nor a type with datatype xsd:string or xsd:boolean")


def test_curie_slot_without_imports_has_xsd_string_datatype():
    """A ``curie`` slot in a schema without the ``linkml:types`` import gets
    ``sh:datatype xsd:string``, as with the import."""
    schema = _single_rule_schema(
        _rule(_GUARD_PRESENT, {"target": {"equals_string": "ex:a"}}),
        {"guard": {"range": "string"}, "target": {"range": "curie"}},
        imports=False,
    )
    g = _parse_shacl(schema)
    datatypes = {
        o
        for p in g.objects(EX_SINGLE.Thing, SH.property)
        if (p, SH.path, EX_SINGLE.target) in g
        for o in g.objects(p, SH.datatype)
    }
    assert datatypes == {XSD.string}


def test_rule_dynamic_enum_value_not_reported(caplog):
    """An enum without static permissible values (a dynamic enum) can hold
    values the schema does not list, so its equals_string value is not
    reported as unknown."""

    schema = json.loads(_single_rule_schema(_rule(_GUARD_PRESENT, {"target": {"equals_string": "GO:0008150"}})))
    schema["enums"] = {"Process": {"reachable_from": {"source_ontology": "obo:go", "source_nodes": ["GO:0008150"]}}}
    schema["classes"]["Thing"]["attributes"]["target"] = {"range": "Process"}
    with caplog.at_level(logging.WARNING):
        queries = _sparql_queries(_parse_shacl(json.dumps(schema)), EX_SINGLE.Thing)
    assert len(queries) == 1 and '"GO:0008150"' in queries[0]
    assert not any("permissible value" in rec.message for rec in caplog.records), caplog.text


def test_rule_message_follows_default_language():
    """The rule description becomes ``sh:message``, tagged with the default
    language like every other human-readable literal the generator emits."""
    rule = _rule(_GUARD_PRESENT, {"target": {"equals_string": "x"}}, description="The target must be x.")
    g = _parse_shacl(_single_rule_schema(rule), default_language="en")
    (node,) = g.objects(EX_SINGLE.Thing, SH.sparql)
    assert set(g.objects(node, SH.message)) == {Literal("The target must be x.", lang="en")}


@pytest.mark.parametrize(
    "descriptions,constraints",
    [
        pytest.param(["Same.", "Same."], 1, id="identical-rules"),
        pytest.param(["First.", "Second."], 2, id="different-messages"),
    ],
)
def test_rule_identical_constraints_emitted_once(descriptions, constraints):
    """A shape carries an identical constraint (query and message) once; rules
    that differ in their message are kept apart."""
    schema = json.loads(_single_rule_schema(_rule(_GUARD_PRESENT, {"target": {"equals_string": "x"}})))
    rule = schema["classes"]["Thing"]["rules"][0]
    schema["classes"]["Thing"]["rules"] = [{**rule, "description": text} for text in descriptions]
    assert len(list(_parse_shacl(json.dumps(schema)).objects(EX_SINGLE.Thing, SH.sparql))) == constraints


def test_rule_problem_reported_once_for_inheriting_classes(caplog):
    """A problem with a rule is reported once, naming the declaring class and
    the rule's position, however many classes inherit it; and a skipped rule
    with elseconditions is not also reported as partially emitted."""

    schema = json.loads(
        _single_rule_schema(
            _rule(_GUARD_PRESENT, {"target": {"pattern": "^x"}}, elseconditions={"slot_conditions": {}})
        )
    )
    for name in ("C1", "C2", "C3"):
        schema["classes"][name] = {"is_a": "Thing", "class_uri": f"ex:{name}"}
    with caplog.at_level(logging.WARNING):
        _parse_shacl(json.dumps(schema))
    messages = [rec.message for rec in caplog.records if "Rule 1 of class 'Thing'" in rec.message]
    assert len(messages) == 1, messages
    assert "skipped, because" in messages[0] and "(in the shapes of 'Thing', 'C1', 'C2', 'C3')" in messages[0]
    assert not any("elseconditions" in rec.message for rec in caplog.records), caplog.text


def test_rule_problem_names_every_affected_shape_whatever_the_class_order(caplog):
    """A problem with an inherited rule names every class shape it affects, so
    the report does not depend on the order in which classes are declared."""
    schema = json.loads(_single_rule_schema(_rule(_GUARD_PRESENT, {"target": {"pattern": "^x"}})))
    schema["classes"] = {"Sub": {"is_a": "Thing", "class_uri": "ex:Sub"}, **schema["classes"]}
    with caplog.at_level(logging.WARNING):
        _parse_shacl(json.dumps(schema))
    messages = [rec.message for rec in caplog.records if "Rule 1 of class 'Thing'" in rec.message]
    assert len(messages) == 1, messages
    assert "'Sub'" in messages[0] and "'Thing'" in messages[0], messages[0]


def test_rule_problems_reported_per_rule_and_per_problem(caplog):
    """Problems are kept apart by rule and by kind: two rules with the same
    problem, and one rule with two problems, each produce their own warning.
    Each warning names the rule by its position and description."""
    schema = json.loads(_single_rule_schema(_rule(_GUARD_PRESENT, {"target": {"pattern": "^x"}})))
    schema["enums"] = {"Color": {"permissible_values": {"Red": {}, "Blue": {}}}}
    schema["classes"]["Thing"]["attributes"]["color"] = {"range": "Color"}
    schema["classes"]["Thing"]["rules"] = [
        _rule(_GUARD_PRESENT, {"target": {"pattern": "^x"}}, description="First"),
        _rule(_GUARD_PRESENT, {"target": {"pattern": "^y"}}, description="Second"),
        _rule(
            _GUARD_PRESENT,
            {"color": {"equals_string": "Purple"}},
            description="Third",
            elseconditions={"slot_conditions": {"color": {"equals_string": "Red"}}},
        ),
    ]
    with caplog.at_level(logging.WARNING):
        _parse_shacl(json.dumps(schema))
    messages = [rec.message for rec in caplog.records if "of class 'Thing'" in rec.message]
    assert len([m for m in messages if m.startswith("Rule 1 of class 'Thing' (First): skipped")]) == 1, messages
    assert len([m for m in messages if m.startswith("Rule 2 of class 'Thing' (Second): skipped")]) == 1, messages
    third = [m for m in messages if m.startswith("Rule 3 of class 'Thing' (Third)")]
    assert len(third) == 2 and any("elseconditions" in m for m in third), messages
    assert any("'Purple', which is not a permissible value" in m for m in third), messages


def test_rule_first_unknown_slot_is_the_reported_problem(caplog):
    """A rule is skipped at its first untranslatable condition: with an
    unknown guard and an unknown target, only the guard is reported."""
    schema = _single_rule_schema(
        _rule({"no_such_guard": {"value_presence": "PRESENT"}}, {"no_such_target": {"equals_string": "x"}})
    )
    with caplog.at_level(logging.WARNING):
        _parse_shacl(schema)
    messages = [rec.message for rec in caplog.records if "Rule 1 of class 'Thing'" in rec.message]
    assert len(messages) == 1 and "no_such_guard" in messages[0], messages


def test_exclusive_value_bare_equals_string_on_single_valued_slot_does_not_warn(caplog):
    """On a single-valued slot, "the value equals V" and "one of the values
    equals V" coincide, so the bare form is translated without a warning."""
    schema = _single_rule_schema(_rule({"target": {"equals_string": "x"}}, {"target": {"maximum_cardinality": 1}}))
    with caplog.at_level(logging.WARNING):
        assert len(_sparql_queries(_parse_shacl(schema), EX_SINGLE.Thing)) == 1
    assert not any("has_member" in rec.message for rec in caplog.records), caplog.text


def test_rule_message_follows_rule_language():
    """A rule's own ``in_language`` takes precedence over the default language."""
    rule = _rule(_GUARD_PRESENT, {"target": {"equals_string": "x"}}, description="Das Ziel muss x sein.")
    rule["in_language"] = "de"
    g = _parse_shacl(_single_rule_schema(rule), default_language="en")
    (node,) = g.objects(EX_SINGLE.Thing, SH.sparql)
    assert set(g.objects(node, SH.message)) == {Literal("Das Ziel muss x sein.", lang="de")}


@pytest.mark.parametrize(
    "rule",
    [
        pytest.param(
            _rule({"no_such_slot": {"value_presence": "PRESENT"}}, {"flag": {"equals_string": "true"}}),
            id="boolean-guard-unknown-guard",
        ),
        pytest.param(
            _rule({"no_such_slot": {"value_presence": "PRESENT"}}, {"target": {"equals_string": "x"}}),
            id="presence-implies-value-unknown-guard",
        ),
        pytest.param(
            _rule(_GUARD_PRESENT, {"no_such_slot": {"equals_string": "x"}}),
            id="presence-implies-value-unknown-target",
        ),
        pytest.param(
            _rule({"no_such_slot": {"equals_string": "x"}}, {"no_such_slot": {"maximum_cardinality": 1}}),
            id="exclusive-value-unknown-slot",
        ),
    ],
)
def test_rule_unknown_slot_key_skipped(caplog, rule):
    """A rule whose condition names a slot that does not exist is skipped:
    a fabricated predicate would make a constraint that never fires (unknown
    guard) or always fires (unknown target)."""
    _assert_skipped(caplog, _single_rule_schema(rule), "'no_such_slot', which is not a slot")


@pytest.mark.parametrize(
    "rule",
    [
        pytest.param(_rule({"id": {"value_presence": "PRESENT"}}, {"target": {"equals_string": "x"}}), id="guard"),
        pytest.param(_rule(_GUARD_PRESENT, {"id": {"equals_string": "x"}}), id="target"),
    ],
)
def test_rule_identifier_slot_skipped(caplog, rule):
    """The identifier is the node's IRI, not a property arc, so a condition on
    it can never match a triple and the rule is skipped."""
    attributes = {"id": {"identifier": True, "range": "uriorcurie"}, "guard": {}, "target": {}}
    _assert_skipped(caplog, _single_rule_schema(rule, attributes), "identifier slot 'id'")


_ESCAPING_SCHEMA_YAML = """
id: https://example.org/escaping
name: escaping_rules
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/escaping/
imports:
  - linkml:types
default_prefix: ex
default_range: string

slots:
  trigger:
    range: string
    slot_uri: ex:trigger
  label:
    range: string
    slot_uri: ex:label

classes:
  Item:
    class_uri: ex:Item
    slots:
      - trigger
      - label
    rules:
      - description: If a trigger is present the label must equal the quoted marker.
        preconditions:
          slot_conditions:
            trigger:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            label:
              equals_string: 'a"b\\\\c'
"""

EX_ESC = rdflib.Namespace("https://example.org/escaping/")


def test_rule_equals_string_special_chars_escaped():
    """An equals_string value with a quote and backslash must be escaped so the
    generated SPARQL stays syntactically valid (no injection / broken query)."""
    from rdflib.plugins.sparql import prepareQuery

    queries = _sparql_queries(_parse_shacl(_ESCAPING_SCHEMA_YAML), EX_ESC.Item)
    assert len(queries) == 1
    query = queries[0]

    # Would raise ParseException on the unescaped `... = "a"b\c"` form.
    prepareQuery(query)
    assert '\\"' in query, f"double quote must be escaped, got:\n{query}"
    assert "\\\\" in query, f"backslash must be escaped, got:\n{query}"


# ===========================================================================
# Operator exactness
#
# A rule is translated only when its conditions set exactly the operators a
# pattern translates.  Each rule below would match a pattern if the converter
# dropped the extra operator, which would widen the precondition (false
# positives) or weaken the postcondition (false negatives).
# ===========================================================================


@pytest.mark.parametrize(
    "extra",
    [
        pytest.param({"pattern": "^x"}, id="pattern"),
        pytest.param({"minimum_value": 0}, id="minimum_value"),
        pytest.param({"maximum_value": 5}, id="maximum_value"),
        pytest.param({"required": True}, id="required"),
        pytest.param({"recommended": True}, id="recommended"),
        pytest.param({"minimum_cardinality": 1}, id="minimum_cardinality"),
        pytest.param({"exact_cardinality": 1}, id="exact_cardinality"),
        pytest.param({"equals_number": 3}, id="equals_number"),
        pytest.param({"has_member": {"equals_string": "x"}}, id="has_member"),
        pytest.param({"any_of": [{"equals_string": "x"}]}, id="slot-any_of"),
    ],
)
@pytest.mark.parametrize("condition", ["guard", "target"])
def test_rule_extra_condition_operator_skipped(caplog, condition, extra):
    """A guard or target condition that adds any operator to the ones a pattern
    translates makes the rule untranslatable."""
    guard = {"value_presence": "PRESENT", **(extra if condition == "guard" else {})}
    target = {"equals_string": "x", **(extra if condition == "target" else {})}
    schema = _single_rule_schema(_rule({"guard": guard}, {"target": target}))
    _assert_skipped(caplog, schema, "match none of the translated patterns")


@pytest.mark.parametrize("presence", ["ABSENT", "UNCOMMITTED"])
def test_rule_guard_presence_other_than_present_skipped(caplog, presence):
    """Only ``value_presence: PRESENT`` is a guard: reading ``ABSENT`` as a
    guard would invert the trigger."""
    schema = _single_rule_schema(_rule({"guard": {"value_presence": presence}}, {"target": {"equals_string": "x"}}))
    _assert_skipped(caplog, schema, "match none of the translated patterns")


@pytest.mark.parametrize("operator", ["any_of", "all_of", "exactly_one_of", "none_of"])
@pytest.mark.parametrize("side", ["preconditions", "postconditions"])
def test_rule_expression_level_operator_skipped(caplog, side, operator):
    """An expression-level boolean operator on either side cannot be honoured
    by any pattern; dropping it would widen or weaken the rule."""
    rule = _rule(_GUARD_PRESENT, {"target": {"equals_string": "x"}})
    rule[side][operator] = [{"slot_conditions": {"other": {"equals_string": "y"}}}]
    _assert_skipped(caplog, _single_rule_schema(rule), f"its {side} use {operator}")


def test_rule_post_with_both_equals_forms_skipped(caplog):
    """equals_string and equals_string_in set together is ambiguous — skip,
    do not let one form silently win."""
    schema = _single_rule_schema(_rule(_GUARD_PRESENT, {"target": {"equals_string": "a", "equals_string_in": ["b"]}}))
    _assert_skipped(caplog, schema, "match none of the translated patterns")


def test_rule_exclusive_value_extra_operator_skipped(caplog):
    """The exclusive-value pattern is exact too: a precondition mixing
    equals_string with an unsupported operator is skipped."""
    schema = _single_rule_schema(
        _rule({"tags": {"equals_string": "x", "pattern": "^x"}}, {"tags": {"maximum_cardinality": 1}})
    )
    _assert_skipped(caplog, schema, "match none of the translated patterns")


_STRING_TRUE_SCHEMA_YAML = """
id: https://example.org/string-true
name: string_true
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/string-true/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  opt:
    slot_uri: ex:opt
  status:
    range: string
    slot_uri: ex:status
classes:
  Conf:
    class_uri: ex:Conf
    slots: [opt, status]
    rules:
      - description: If opt is present, status must be the string "true".
        preconditions:
          slot_conditions:
            opt:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            status:
              equals_string: "true"
"""


def test_rule_equals_true_on_string_slot_uses_piv():
    """equals_string "true" on a NON-boolean slot is compared as the string
    "true", not as the boolean of the boolean guard."""
    queries = _sparql_queries(_parse_shacl(_STRING_TRUE_SCHEMA_YAML), URIRef("https://example.org/string-true/Conf"))
    assert len(queries) == 1
    assert '?value = "true"' in queries[0], f"string-range 'true' must be a string comparison, got:\n{queries[0]}"
    assert "?value = true" not in queries[0], "the boolean guard must not apply to a string slot"


@pytest.mark.parametrize(
    "status,violates",
    [
        pytest.param('"true"', False, id="plain"),
        pytest.param('"true"^^xsd:string', False, id="xsd-string"),
        pytest.param('"other"', True, id="other"),
    ],
)
def test_rule_equals_true_on_string_slot_pyshacl_end_to_end(status, violates):
    """status "true" (string) satisfies the rule in either RDF 1.1-identical form."""
    data = (
        "@prefix ex: <https://example.org/string-true/> .\n"
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
        f'ex:x a ex:Conf ; ex:opt "x" ; ex:status {status} .'
    )
    _, focus_nodes = _validate_rules(_STRING_TRUE_SCHEMA_YAML, data)
    assert focus_nodes == ({URIRef("https://example.org/string-true/x")} if violates else set())
