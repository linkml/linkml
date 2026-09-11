from collections import Counter
from typing import Any

import pytest
import rdflib
from rdflib import RDF, RDFS, SH, Literal, URIRef
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
    """Unrecognised rule patterns are silently skipped (no sh:sparql emitted)."""
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
    """For maximum_cardinality: 1, SPARQL uses FILTER(?other != <value>).

    The query pattern for N=1 is:
        SELECT $this WHERE {
            $this <slot> <value> .
            $this <slot> ?other .
            FILTER (?other != <value>)
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
        SELECT $this WHERE {
            $this <slot> <value> .
            {
                SELECT $this (COUNT(?val) AS ?count)
                WHERE { $this <slot> ?val . }
                GROUP BY $this
                HAVING (?count > N)
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


# ===========================================================================
# Presence-implies-value pattern tests (enum guard)
# ===========================================================================
#
# The "presence implies value" pattern generalises the boolean guard to
# enum-valued targets.  It translates a LinkML rule where:
#   - preconditions: a value slot has value_presence: PRESENT
#   - postconditions: a target slot has equals_string (single required value)
#     or equals_string_in (a set of acceptable values)
#
# Semantics: "If the value slot is present, the target slot must be present
# and hold one of the allowed values."  The motivating use case is the aiSim
# environment model, e.g. "if texture_sky_color is set, sky_model must be
# TextureSky" and "if overcast_sky_illuminance is set, sky_model must be an
# overcast model".
#
# References:
#   - W3C SHACL §5 <https://www.w3.org/TR/shacl/#sparql-constraints>
#   - W3C SHACL §5.3.1 <https://www.w3.org/TR/shacl/#sparql-constraints-prebound>
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
  SkyModelEnum:
    permissible_values:
      ClearSky:
        meaning: ex:ClearSky
      OvercastSky:
        meaning: ex:OvercastSky
      MeasuredOvercastSky:
        meaning: ex:MeasuredOvercastSky
      TextureSky:
        meaning: ex:TextureSky

  ModeEnum:
    permissible_values:
      Auto:
        description: Automatic mode (no meaning IRI).
      Manual:
        description: Manual mode (no meaning IRI).

slots:
  sky_model:
    range: SkyModelEnum
    slot_uri: ex:sky_model
  texture_sky_color:
    range: string
    slot_uri: ex:texture_sky_color
  overcast_sky_illuminance:
    range: float
    slot_uri: ex:overcast_sky_illuminance
  mode:
    range: ModeEnum
    slot_uri: ex:mode
  manual_value:
    range: decimal
    slot_uri: ex:manual_value

classes:
  Weather:
    class_uri: ex:Weather
    slots:
      - sky_model
      - texture_sky_color
      - overcast_sky_illuminance
    rules:
      - description: If texture_sky_color is provided, sky_model must be TextureSky.
        preconditions:
          slot_conditions:
            texture_sky_color:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            sky_model:
              equals_string: "TextureSky"
      - description: If overcast_sky_illuminance is provided, sky_model must be an overcast model.
        preconditions:
          slot_conditions:
            overcast_sky_illuminance:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            sky_model:
              equals_string_in:
                - OvercastSky
                - MeasuredOvercastSky

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


def test_presence_implies_value_generates_sparql():
    """Presence-implies-value rules produce sh:sparql constraints on the NodeShape."""
    g = _parse_shacl(_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML)

    shape = EX_PIV.Weather
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 2, f"Expected 2 sh:sparql constraints, got {len(sparql_nodes)}"

    for node in sparql_nodes:
        assert (node, RDF.type, SH.SPARQLConstraint) in g
        selects = list(g.objects(node, SH.select))
        assert len(selects) == 1, "Each constraint must have exactly one sh:select"
        query = str(selects[0])
        assert "$this" in query, "SPARQL must use $this pre-bound variable"
        assert "NOT IN" in query, "presence-implies-value SPARQL must use NOT IN membership test"
        assert "FILTER" in query, "SPARQL must have a FILTER clause"


def test_presence_implies_value_single_uses_enum_iri():
    """A single equals_string target resolves to the enum meaning IRI."""
    g = _parse_shacl(_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML)

    shape = EX_PIV.Weather
    sparql_nodes = list(g.objects(shape, SH.sparql))
    queries = [str(list(g.objects(n, SH.select))[0]) for n in sparql_nodes]

    texture_query = [q for q in queries if "texture_sky_color" in q]
    assert len(texture_query) == 1, "Expected exactly one texture_sky_color rule"
    query = texture_query[0]

    # value slot and target slot URIs both present
    assert str(EX_PIV.texture_sky_color) in query
    assert str(EX_PIV.sky_model) in query
    # target value resolves to the TextureSky meaning IRI in angle brackets
    assert f"<{EX_PIV.TextureSky}>" in query, f"Expected TextureSky IRI, got:\n{query}"


def test_presence_implies_value_set_uses_all_iris():
    """equals_string_in resolves every allowed value to its enum meaning IRI."""
    g = _parse_shacl(_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML)

    shape = EX_PIV.Weather
    sparql_nodes = list(g.objects(shape, SH.sparql))
    queries = [str(list(g.objects(n, SH.select))[0]) for n in sparql_nodes]

    overcast_query = [q for q in queries if "overcast_sky_illuminance" in q]
    assert len(overcast_query) == 1, "Expected exactly one overcast rule"
    query = overcast_query[0]

    assert f"<{EX_PIV.OvercastSky}>" in query, f"Expected OvercastSky IRI, got:\n{query}"
    assert f"<{EX_PIV.MeasuredOvercastSky}>" in query, f"Expected MeasuredOvercastSky IRI, got:\n{query}"


def test_presence_implies_value_no_meaning_falls_back_to_literal():
    """When the target enum value lacks a meaning IRI, it is compared as a literal."""
    g = _parse_shacl(_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML)

    shape = EX_PIV.Device
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 1

    query = str(list(g.objects(sparql_nodes[0], SH.select))[0])
    assert '"Manual"' in query, f"No-meaning enum should use literal '\"Manual\"', got:\n{query}"
    assert f"<{EX_PIV}Manual>" not in query, "Should not emit as IRI when meaning is absent"


def test_presence_implies_value_message_from_description():
    """Rule description is emitted as sh:message on the SPARQLConstraint."""
    g = _parse_shacl(_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML)

    shape = EX_PIV.Weather
    sparql_nodes = list(g.objects(shape, SH.sparql))
    messages = [str(m) for node in sparql_nodes for m in g.objects(node, SH.message)]

    assert any("sky_model must be TextureSky" in m for m in messages), (
        f"Expected message about TextureSky, got: {messages}"
    )


def test_presence_implies_value_sparql_syntax_valid():
    """Generated SPARQL for presence-implies-value rules must be syntactically valid."""
    from rdflib.plugins.sparql import prepareQuery

    g = _parse_shacl(_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML)

    for shape in (EX_PIV.Weather, EX_PIV.Device):
        sparql_nodes = list(g.objects(shape, SH.sparql))
        for node in sparql_nodes:
            query_text = str(list(g.objects(node, SH.select))[0])
            prepareQuery(query_text)


def test_presence_implies_value_pyshacl_end_to_end():
    """End-to-end: pyshacl passes conforming instances and flags violations."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_PRESENCE_IMPLIES_VALUE_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()

    # Conforming: guarded slots paired with an allowed sky_model; and an
    # unguarded instance (no texture/overcast) is unaffected by the rules.
    conforming_data = """
    @prefix ex: <https://example.org/presence-implies-value/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:wTexture a ex:Weather ;
        ex:texture_sky_color "0,0,0" ;
        ex:sky_model ex:TextureSky .

    ex:wOvercast a ex:Weather ;
        ex:overcast_sky_illuminance "5000.0"^^xsd:float ;
        ex:sky_model ex:OvercastSky .

    ex:wMeasured a ex:Weather ;
        ex:overcast_sky_illuminance "4200.0"^^xsd:float ;
        ex:sky_model ex:MeasuredOvercastSky .

    ex:wClear a ex:Weather ;
        ex:sky_model ex:ClearSky .
    """

    conforms, _, results_text = pyshacl.validate(
        data_graph=conforming_data,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert conforms, f"Conforming instances should pass SHACL validation:\n{results_text}"

    # Violating: texture_sky_color present but sky_model is ClearSky (not TextureSky).
    violating_wrong_value = """
    @prefix ex: <https://example.org/presence-implies-value/> .

    ex:wBad a ex:Weather ;
        ex:texture_sky_color "0,0,0" ;
        ex:sky_model ex:ClearSky .
    """
    conforms, _, results_text = pyshacl.validate(
        data_graph=violating_wrong_value,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert not conforms, f"Wrong-value instance should fail SHACL validation:\n{results_text}"

    # Violating: overcast_sky_illuminance present but sky_model is TextureSky
    # (not in the allowed overcast set).
    violating_not_in_set = """
    @prefix ex: <https://example.org/presence-implies-value/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:wBad2 a ex:Weather ;
        ex:overcast_sky_illuminance "5000.0"^^xsd:float ;
        ex:sky_model ex:TextureSky .
    """
    conforms, _, results_text = pyshacl.validate(
        data_graph=violating_not_in_set,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert not conforms, f"Not-in-set instance should fail SHACL validation:\n{results_text}"

    # Violating: texture_sky_color present but sky_model entirely absent.
    violating_missing_target = """
    @prefix ex: <https://example.org/presence-implies-value/> .

    ex:wBad3 a ex:Weather ;
        ex:texture_sky_color "0,0,0" .
    """
    conforms, _, results_text = pyshacl.validate(
        data_graph=violating_missing_target,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert not conforms, f"Missing-target instance should fail SHACL validation:\n{results_text}"


# ===========================================================================
# Compositional fallback: conditional-required pattern (M1)
# ===========================================================================
#
# Rule shape:
#   - preconditions:  slot X has equals_string V
#   - postconditions: slot Y has required: true
#
# Semantics: "If X = V, then Y must be present."  Emitted as an
# sh:SPARQLConstraint whose SELECT matches focus nodes where the precondition
# holds but the required slot is absent (FILTER NOT EXISTS).
# ===========================================================================

_CONDITIONAL_REQUIRED_SCHEMA_YAML = """
id: https://example.org/conditional-required
name: conditional_required_rules
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/conditional-required/
imports:
  - linkml:types
default_prefix: ex
default_range: string

enums:
  SkyModelEnum:
    permissible_values:
      ClearSky:
        meaning: ex:ClearSky
      OvercastSky:
        meaning: ex:OvercastSky
      MeasuredOvercastSky:
        meaning: ex:MeasuredOvercastSky

slots:
  sky_model:
    range: SkyModelEnum
    slot_uri: ex:sky_model
  overcast_sky_illuminance:
    range: float
    slot_uri: ex:overcast_sky_illuminance

classes:
  Weather:
    class_uri: ex:Weather
    slots:
      - sky_model
      - overcast_sky_illuminance
    rules:
      - description: The MeasuredOvercastSky model requires the sky illuminance.
        preconditions:
          slot_conditions:
            sky_model:
              equals_string: MeasuredOvercastSky
        postconditions:
          slot_conditions:
            overcast_sky_illuminance:
              required: true
"""

EX_CR = rdflib.Namespace("https://example.org/conditional-required/")


def test_conditional_required_generates_sparql():
    """equals_string precondition + required postcondition → one sh:sparql constraint."""
    g = _parse_shacl(_CONDITIONAL_REQUIRED_SCHEMA_YAML)

    shape = EX_CR.Weather
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 1, f"Expected 1 sh:sparql constraint, got {len(sparql_nodes)}"

    node = sparql_nodes[0]
    assert (node, RDF.type, SH.SPARQLConstraint) in g
    query = str(list(g.objects(node, SH.select))[0])

    assert "$this" in query, "SPARQL must use $this pre-bound variable (SHACL §5.3.1)"
    assert "FILTER NOT EXISTS" in query, "required violation must use FILTER NOT EXISTS"
    # precondition references the enum meaning IRI and the trigger slot
    assert f"<{EX_CR.MeasuredOvercastSky}>" in query, f"precondition must use the enum IRI, got:\n{query}"
    assert str(EX_CR.sky_model) in query
    assert str(EX_CR.overcast_sky_illuminance) in query


def test_conditional_required_message_from_description():
    """Rule description is emitted as sh:message."""
    g = _parse_shacl(_CONDITIONAL_REQUIRED_SCHEMA_YAML)
    messages = [str(m) for node in g.objects(EX_CR.Weather, SH.sparql) for m in g.objects(node, SH.message)]
    assert any("requires the sky illuminance" in m for m in messages), messages


def test_conditional_required_sparql_syntax_valid():
    """Generated SPARQL must be syntactically valid."""
    from rdflib.plugins.sparql import prepareQuery

    g = _parse_shacl(_CONDITIONAL_REQUIRED_SCHEMA_YAML)
    for node in g.objects(EX_CR.Weather, SH.sparql):
        prepareQuery(str(list(g.objects(node, SH.select))[0]))


def test_conditional_required_pyshacl_end_to_end():
    """End-to-end: pyshacl passes conforming instances and flags the violation."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_CONDITIONAL_REQUIRED_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()

    # Conforming: MeasuredOvercastSky WITH illuminance; ClearSky needs nothing.
    conforming = """
    @prefix ex: <https://example.org/conditional-required/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:wMeasured a ex:Weather ;
        ex:sky_model ex:MeasuredOvercastSky ;
        ex:overcast_sky_illuminance "4200.0"^^xsd:float .

    ex:wClear a ex:Weather ;
        ex:sky_model ex:ClearSky .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=conforming,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert conforms, f"Conforming instances should pass:\n{txt}"

    # Violating: MeasuredOvercastSky WITHOUT the required illuminance.
    violating = """
    @prefix ex: <https://example.org/conditional-required/> .

    ex:wBad a ex:Weather ;
        ex:sky_model ex:MeasuredOvercastSky .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=violating,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert not conforms, f"MeasuredOvercastSky without illuminance should fail:\n{txt}"


# ===========================================================================
# Compositional fallback: conditional-absent pattern (M2)
# ===========================================================================
#
# Rule shape:
#   - preconditions:  slot X has equals_string V
#   - postconditions: slot Y has value_presence: ABSENT
#
# Semantics: "If X = V, then Y must NOT be present" (inapplicable slot).
# Emitted as an sh:SPARQLConstraint whose SELECT matches focus nodes where the
# precondition holds and the forbidden slot is present.
# ===========================================================================

_CONDITIONAL_ABSENT_SCHEMA_YAML = """
id: https://example.org/conditional-absent
name: conditional_absent_rules
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/conditional-absent/
imports:
  - linkml:types
default_prefix: ex
default_range: string

enums:
  SkyModelEnum:
    permissible_values:
      ClearSky:
        meaning: ex:ClearSky
      OvercastSky:
        meaning: ex:OvercastSky

slots:
  sky_model:
    range: SkyModelEnum
    slot_uri: ex:sky_model
  overcast_sky_illuminance:
    range: float
    slot_uri: ex:overcast_sky_illuminance

classes:
  Weather:
    class_uri: ex:Weather
    slots:
      - sky_model
      - overcast_sky_illuminance
    rules:
      - description: ClearSky makes overcast_sky_illuminance inapplicable.
        preconditions:
          slot_conditions:
            sky_model:
              equals_string: ClearSky
        postconditions:
          slot_conditions:
            overcast_sky_illuminance:
              value_presence: ABSENT
"""

EX_CA = rdflib.Namespace("https://example.org/conditional-absent/")


def test_conditional_absent_generates_sparql():
    """equals_string precondition + value_presence ABSENT → one sh:sparql constraint."""
    g = _parse_shacl(_CONDITIONAL_ABSENT_SCHEMA_YAML)

    sparql_nodes = list(g.objects(EX_CA.Weather, SH.sparql))
    assert len(sparql_nodes) == 1, f"Expected 1 sh:sparql constraint, got {len(sparql_nodes)}"

    query = str(list(g.objects(sparql_nodes[0], SH.select))[0])
    assert "$this" in query
    # violation = precondition holds AND the forbidden slot is present; the
    # forbidden-slot triple must NOT be wrapped in NOT EXISTS.
    assert "FILTER NOT EXISTS" not in query, f"conditional-absent must not use NOT EXISTS, got:\n{query}"
    assert f"<{EX_CA.ClearSky}>" in query
    assert str(EX_CA.overcast_sky_illuminance) in query


def test_conditional_absent_sparql_syntax_valid():
    """Generated SPARQL must be syntactically valid."""
    from rdflib.plugins.sparql import prepareQuery

    g = _parse_shacl(_CONDITIONAL_ABSENT_SCHEMA_YAML)
    for node in g.objects(EX_CA.Weather, SH.sparql):
        prepareQuery(str(list(g.objects(node, SH.select))[0]))


def test_conditional_absent_pyshacl_end_to_end():
    """End-to-end: pyshacl passes conforming instances and flags the violation."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_CONDITIONAL_ABSENT_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()

    # Conforming: ClearSky without illuminance; OvercastSky may set illuminance.
    conforming = """
    @prefix ex: <https://example.org/conditional-absent/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:wClear a ex:Weather ;
        ex:sky_model ex:ClearSky .

    ex:wOvercast a ex:Weather ;
        ex:sky_model ex:OvercastSky ;
        ex:overcast_sky_illuminance "5000.0"^^xsd:float .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=conforming,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert conforms, f"Conforming instances should pass:\n{txt}"

    # Violating: ClearSky WITH the inapplicable illuminance.
    violating = """
    @prefix ex: <https://example.org/conditional-absent/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:wBad a ex:Weather ;
        ex:sky_model ex:ClearSky ;
        ex:overcast_sky_illuminance "5000.0"^^xsd:float .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=violating,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert not conforms, f"ClearSky with illuminance should fail:\n{txt}"


# ===========================================================================
# Compositional fallback: numeric threshold precondition (M3)
# ===========================================================================
#
# Rule shape:
#   - preconditions:  slot X has maximum_value N (or minimum_value)
#   - postconditions: slot Y has required: true
#
# Semantics: "If X <= N, then Y must be present."  The threshold becomes a
# SPARQL FILTER; combined here with the M1 required violation.
# ===========================================================================

_THRESHOLD_SCHEMA_YAML = """
id: https://example.org/threshold
name: threshold_rules
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/threshold/
imports:
  - linkml:types
default_prefix: ex
default_range: string

slots:
  meteorological_optical_range:
    range: float
    slot_uri: ex:meteorological_optical_range
  fog_note:
    range: string
    slot_uri: ex:fog_note

classes:
  Weather:
    class_uri: ex:Weather
    slots:
      - meteorological_optical_range
      - fog_note
    rules:
      - description: In fog (optical range at or below 4000) a fog note is required.
        preconditions:
          slot_conditions:
            meteorological_optical_range:
              maximum_value: 4000
        postconditions:
          slot_conditions:
            fog_note:
              required: true
"""

EX_THR = rdflib.Namespace("https://example.org/threshold/")


def test_threshold_precondition_generates_sparql():
    """maximum_value precondition emits a numeric FILTER on the trigger slot."""
    g = _parse_shacl(_THRESHOLD_SCHEMA_YAML)

    sparql_nodes = list(g.objects(EX_THR.Weather, SH.sparql))
    assert len(sparql_nodes) == 1, f"Expected 1 sh:sparql constraint, got {len(sparql_nodes)}"

    query = str(list(g.objects(sparql_nodes[0], SH.select))[0])
    assert "<= 4000" in query, f"threshold must emit '<= 4000', got:\n{query}"
    assert "FILTER NOT EXISTS" in query, "required postcondition violation must use NOT EXISTS"
    assert str(EX_THR.meteorological_optical_range) in query
    assert str(EX_THR.fog_note) in query


def test_threshold_precondition_sparql_syntax_valid():
    """Generated SPARQL must be syntactically valid."""
    from rdflib.plugins.sparql import prepareQuery

    g = _parse_shacl(_THRESHOLD_SCHEMA_YAML)
    for node in g.objects(EX_THR.Weather, SH.sparql):
        prepareQuery(str(list(g.objects(node, SH.select))[0]))


def test_threshold_precondition_pyshacl_end_to_end():
    """End-to-end: below-threshold requires the note; above-threshold does not."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_THRESHOLD_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()

    # Conforming: foggy (400) with a note; clear (5000) needs nothing.
    conforming = """
    @prefix ex: <https://example.org/threshold/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:wFog a ex:Weather ;
        ex:meteorological_optical_range "400.0"^^xsd:float ;
        ex:fog_note "reduced visibility" .

    ex:wClear a ex:Weather ;
        ex:meteorological_optical_range "5000.0"^^xsd:float .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=conforming,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert conforms, f"Conforming instances should pass:\n{txt}"

    # Violating: foggy (400) without the required note.
    violating = """
    @prefix ex: <https://example.org/threshold/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:wBad a ex:Weather ;
        ex:meteorological_optical_range "400.0"^^xsd:float .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=violating,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert not conforms, f"Fog without the required note should fail:\n{txt}"


# ===========================================================================
# Compositional fallback: nested range_expression precondition (M4)
# ===========================================================================
#
# Rule shape:
#   - preconditions:  slot X (inlined child) has range_expression on an inner
#     slot (e.g. sun_position.elevation <= 0)
#   - postconditions: slot Y has required: true
#
# Semantics: "If the child's inner value satisfies the condition, then Y must
# be present."  The SPARQL binds the child node with one extra hop.
# ===========================================================================

_NESTED_SCHEMA_YAML = """
id: https://example.org/nested
name: nested_rules
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/nested/
imports:
  - linkml:types
default_prefix: ex
default_range: string

slots:
  sun_position:
    range: SunPosition
    inlined: true
    slot_uri: ex:sun_position
  elevation:
    range: float
    slot_uri: ex:elevation
  headlight_note:
    range: string
    slot_uri: ex:headlight_note

classes:
  SunPosition:
    class_uri: ex:SunPosition
    slots:
      - elevation
  Weather:
    class_uri: ex:Weather
    slots:
      - sun_position
      - headlight_note
    rules:
      - description: When the sun is at or below the horizon a headlight note is required.
        preconditions:
          slot_conditions:
            sun_position:
              range_expression:
                slot_conditions:
                  elevation:
                    maximum_value: 0.0
        postconditions:
          slot_conditions:
            headlight_note:
              required: true
"""

EX_NEST = rdflib.Namespace("https://example.org/nested/")


def test_nested_precondition_generates_sparql():
    """A nested range_expression precondition emits a two-hop graph pattern."""
    g = _parse_shacl(_NESTED_SCHEMA_YAML)

    sparql_nodes = list(g.objects(EX_NEST.Weather, SH.sparql))
    assert len(sparql_nodes) == 1, f"Expected 1 sh:sparql constraint, got {len(sparql_nodes)}"

    query = str(list(g.objects(sparql_nodes[0], SH.select))[0])
    assert str(EX_NEST.sun_position) in query, "must traverse the container slot"
    assert str(EX_NEST.elevation) in query, "must traverse the inner slot"
    assert "<= 0.0" in query, f"inner threshold must appear, got:\n{query}"
    assert "FILTER NOT EXISTS" in query
    assert str(EX_NEST.headlight_note) in query


def test_nested_precondition_sparql_syntax_valid():
    """Generated SPARQL must be syntactically valid."""
    from rdflib.plugins.sparql import prepareQuery

    g = _parse_shacl(_NESTED_SCHEMA_YAML)
    for node in g.objects(EX_NEST.Weather, SH.sparql):
        prepareQuery(str(list(g.objects(node, SH.select))[0]))


def test_nested_precondition_pyshacl_end_to_end():
    """End-to-end: sun below horizon requires the note; above horizon does not."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_NESTED_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()

    # Conforming: night (elevation -90) with a note; day (45) needs nothing.
    conforming = """
    @prefix ex: <https://example.org/nested/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:wNight a ex:Weather ;
        ex:sun_position [ a ex:SunPosition ; ex:elevation "-90.0"^^xsd:float ] ;
        ex:headlight_note "on" .

    ex:wDay a ex:Weather ;
        ex:sun_position [ a ex:SunPosition ; ex:elevation "45.0"^^xsd:float ] .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=conforming,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert conforms, f"Conforming instances should pass:\n{txt}"

    # Violating: night (elevation -90) without the required note.
    violating = """
    @prefix ex: <https://example.org/nested/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:wBad a ex:Weather ;
        ex:sun_position [ a ex:SunPosition ; ex:elevation "-90.0"^^xsd:float ] .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=violating,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert not conforms, f"Night without a headlight note should fail:\n{txt}"


# ===========================================================================
# Compositional fallback: has_member list-membership postcondition (M5)
# ===========================================================================
#
# Rule shape:
#   - preconditions:  any supported precondition (here value_presence PRESENT)
#   - postconditions: multivalued slot has_member with a nested
#     range_expression constraining the member's inner slots
#
# Semantics: "If the precondition holds, the list must contain a member
# matching the inner conditions."  Violation = no such member (FILTER NOT
# EXISTS over the members).  Inner enum values resolve against the member
# class (LightControlGroup), which disambiguates the reused `type` slot.
# ===========================================================================

_HAS_MEMBER_SCHEMA_YAML = """
id: https://example.org/has-member
name: has_member_rules
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/has-member/
imports:
  - linkml:types
default_prefix: ex
default_range: string

enums:
  LightGroupEnum:
    permissible_values:
      Vehicle:
        meaning: ex:Vehicle
      StreetLight:
        meaning: ex:StreetLight
  LightTypeEnum:
    permissible_values:
      low_beam_headlight:
        meaning: ex:low_beam_headlight
      front_fog_light:
        meaning: ex:front_fog_light

slots:
  fog_declared:
    range: string
    slot_uri: ex:fog_declared
  enabled_light_control_groups:
    range: LightControlGroup
    multivalued: true
    inlined: true
    inlined_as_list: true
    slot_uri: ex:enabled_light_control_groups
  group:
    range: LightGroupEnum
    slot_uri: ex:group
  type:
    range: LightTypeEnum
    slot_uri: ex:type

classes:
  LightControlGroup:
    class_uri: ex:LightControlGroup
    slots:
      - group
      - type
  Weather:
    class_uri: ex:Weather
    slots:
      - fog_declared
      - enabled_light_control_groups
    rules:
      - description: When fog is declared, a front fog light group must be enabled.
        preconditions:
          slot_conditions:
            fog_declared:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            enabled_light_control_groups:
              has_member:
                range_expression:
                  slot_conditions:
                    group:
                      equals_string: Vehicle
                    type:
                      equals_string: front_fog_light
"""

EX_HM = rdflib.Namespace("https://example.org/has-member/")


def test_has_member_generates_sparql():
    """has_member postcondition emits a FILTER NOT EXISTS over list members."""
    g = _parse_shacl(_HAS_MEMBER_SCHEMA_YAML)

    sparql_nodes = list(g.objects(EX_HM.Weather, SH.sparql))
    assert len(sparql_nodes) == 1, f"Expected 1 sh:sparql constraint, got {len(sparql_nodes)}"

    query = str(list(g.objects(sparql_nodes[0], SH.select))[0])
    assert "FILTER NOT EXISTS" in query, "list-membership violation must use FILTER NOT EXISTS"
    assert str(EX_HM.enabled_light_control_groups) in query
    assert str(EX_HM.group) in query and str(EX_HM.type) in query
    # inner enum values resolve against the member class (LightControlGroup),
    # so the reused `type` slot picks LightTypeEnum, not another enum.
    assert f"<{EX_HM.Vehicle}>" in query, f"group value must be the enum IRI, got:\n{query}"
    assert f"<{EX_HM.front_fog_light}>" in query, f"type value must be the enum IRI, got:\n{query}"


def test_has_member_sparql_syntax_valid():
    """Generated SPARQL must be syntactically valid."""
    from rdflib.plugins.sparql import prepareQuery

    g = _parse_shacl(_HAS_MEMBER_SCHEMA_YAML)
    for node in g.objects(EX_HM.Weather, SH.sparql):
        prepareQuery(str(list(g.objects(node, SH.select))[0]))


def test_has_member_pyshacl_end_to_end():
    """End-to-end: fog requires a front-fog-light member; otherwise it fails."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_HAS_MEMBER_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()

    # Conforming: fog declared WITH a front-fog-light group; and no fog at all.
    conforming = """
    @prefix ex: <https://example.org/has-member/> .

    ex:wFog a ex:Weather ;
        ex:fog_declared "yes" ;
        ex:enabled_light_control_groups
            [ a ex:LightControlGroup ; ex:group ex:Vehicle ; ex:type ex:front_fog_light ] .

    ex:wNoFog a ex:Weather .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=conforming,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert conforms, f"Conforming instances should pass:\n{txt}"

    # Violating: fog declared but only a low-beam group (no front fog light).
    violating = """
    @prefix ex: <https://example.org/has-member/> .

    ex:wBad a ex:Weather ;
        ex:fog_declared "yes" ;
        ex:enabled_light_control_groups
            [ a ex:LightControlGroup ; ex:group ex:Vehicle ; ex:type ex:low_beam_headlight ] .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=violating,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert not conforms, f"Fog without a front-fog-light group should fail:\n{txt}"


# ===========================================================================
# Rule-converter robustness regressions (review hardening)
#
# These guard three defects found while reviewing the rule converters:
#   1. A single precondition combining minimum_value + maximum_value dropped
#      all but the first bound (silent under-constraint / false positives).
#   2. A slot_usage `slot_uri` (or enum `range`) override made the SPARQL body
#      query the *base* IRI while `sh:path` used the *induced* IRI, so the
#      constraint silently never fired (false negative).
#   3. An `equals_string` value containing a quote/backslash produced invalid,
#      unparsable SPARQL (broken artifact / injection).
# ===========================================================================

_COMBINED_BOUNDS_SCHEMA_YAML = """
id: https://example.org/combined-bounds
name: combined_bounds_rules
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/combined-bounds/
imports:
  - linkml:types
default_prefix: ex
default_range: string

slots:
  reading_value:
    range: integer
    slot_uri: ex:reading_value
  reading_note:
    range: string
    slot_uri: ex:reading_note

classes:
  Reading:
    class_uri: ex:Reading
    slots:
      - reading_value
      - reading_note
    rules:
      - description: A mid-range reading requires an explanatory note.
        preconditions:
          slot_conditions:
            reading_value:
              minimum_value: 10
              maximum_value: 20
        postconditions:
          slot_conditions:
            reading_note:
              required: true
"""

EX_CB = rdflib.Namespace("https://example.org/combined-bounds/")


def test_rule_precondition_combines_min_and_max_bounds():
    """A precondition with both minimum_value and maximum_value must emit both
    bounds; the pre-fix first-match dispatch kept only the maximum."""
    g = _parse_shacl(_COMBINED_BOUNDS_SCHEMA_YAML)

    nodes = list(g.objects(EX_CB.Reading, SH.sparql))
    assert len(nodes) == 1, f"Expected 1 sh:sparql constraint, got {len(nodes)}"
    query = str(list(g.objects(nodes[0], SH.select))[0])
    assert ">= 10" in query, f"lower bound must be emitted, got:\n{query}"
    assert "<= 20" in query, f"upper bound must be emitted, got:\n{query}"


def test_rule_combined_bounds_pyshacl_end_to_end():
    """End-to-end: only values inside [10, 20] trigger the required note.

    The below-threshold case is the key assertion — without the lower bound it
    would be flagged as a violation."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_COMBINED_BOUNDS_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()

    conforming = """
    @prefix ex: <https://example.org/combined-bounds/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:mid a ex:Reading ; ex:reading_value 15 ; ex:reading_note "in range" .
    ex:low a ex:Reading ; ex:reading_value 5 .
    ex:high a ex:Reading ; ex:reading_value 25 .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=conforming,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert conforms, f"Out-of-range readings must not require a note:\n{txt}"

    violating = """
    @prefix ex: <https://example.org/combined-bounds/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:bad a ex:Reading ; ex:reading_value 15 .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=violating,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert not conforms, f"A mid-range reading without a note must fail:\n{txt}"


_SLOT_URI_OVERRIDE_SCHEMA_YAML = """
id: https://example.org/slot-uri-override
name: slot_uri_override_rules
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/slot-uri-override/
imports:
  - linkml:types
default_prefix: ex
default_range: string

slots:
  trigger:
    range: string
    slot_uri: ex:GLOBAL_trigger
  dependent:
    range: string
    slot_uri: ex:GLOBAL_dependent

classes:
  Scene:
    class_uri: ex:Scene
    slots:
      - trigger
      - dependent
    slot_usage:
      trigger:
        slot_uri: ex:LOCAL_trigger
      dependent:
        slot_uri: ex:LOCAL_dependent
    rules:
      - description: If the trigger is present the dependent slot is required.
        preconditions:
          slot_conditions:
            trigger:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            dependent:
              required: true
"""

EX_OVR = rdflib.Namespace("https://example.org/slot-uri-override/")


def test_rule_slot_uri_override_matches_sh_path():
    """The SPARQL body must use the same induced (class-local) IRIs as sh:path.

    A slot_usage slot_uri override changes sh:path; if the SPARQL keeps the base
    IRI the query targets a property the data never uses and never fires."""
    g = _parse_shacl(_SLOT_URI_OVERRIDE_SCHEMA_YAML)

    paths = {str(o) for o in g.objects(None, SH.path)}
    assert str(EX_OVR.LOCAL_trigger) in paths
    assert str(EX_OVR.LOCAL_dependent) in paths

    nodes = list(g.objects(EX_OVR.Scene, SH.sparql))
    assert len(nodes) == 1
    query = str(list(g.objects(nodes[0], SH.select))[0])
    assert str(EX_OVR.LOCAL_trigger) in query, f"SPARQL must use the induced IRI, got:\n{query}"
    assert str(EX_OVR.LOCAL_dependent) in query, f"SPARQL must use the induced IRI, got:\n{query}"
    assert "GLOBAL_" not in query, f"SPARQL must not fall back to the base slot_uri, got:\n{query}"


def test_rule_slot_uri_override_pyshacl_end_to_end():
    """End-to-end: the constraint actually fires on data that uses the induced
    (LOCAL) IRIs.  Before the fix the SPARQL queried the base IRIs, so a missing
    dependent slot slipped through as conforming."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_SLOT_URI_OVERRIDE_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()

    conforming = """
    @prefix ex: <https://example.org/slot-uri-override/> .

    ex:ok a ex:Scene ; ex:LOCAL_trigger "t" ; ex:LOCAL_dependent "d" .
    ex:noTrigger a ex:Scene ; ex:LOCAL_dependent "d" .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=conforming,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert conforms, f"Trigger-with-dependent (and no-trigger) must pass:\n{txt}"

    violating = """
    @prefix ex: <https://example.org/slot-uri-override/> .

    ex:bad a ex:Scene ; ex:LOCAL_trigger "t" .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=violating,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert not conforms, f"Trigger present without the required dependent must fail:\n{txt}"


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
    g = _parse_shacl(_ENUM_NARROWING_SCHEMA_YAML)

    nodes = list(g.objects(EX_EN.Scene, SH.sparql))
    assert len(nodes) == 1
    query = str(list(g.objects(nodes[0], SH.select))[0])
    assert str(EX_EN.LOCAL_Active) in query, f"must resolve the narrowed enum meaning, got:\n{query}"
    assert "GLOBAL_Active" not in query, f"must not resolve the base enum meaning, got:\n{query}"


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

    g = _parse_shacl(_ESCAPING_SCHEMA_YAML)
    nodes = list(g.objects(EX_ESC.Item, SH.sparql))
    assert len(nodes) == 1
    query = str(list(g.objects(nodes[0], SH.select))[0])

    # Would raise ParseException on the unescaped `... = "a"b\c"` form.
    prepareQuery(query)
    assert '\\"' in query, f"double quote must be escaped, got:\n{query}"
    assert "\\\\" in query, f"backslash must be escaped, got:\n{query}"


# ===========================================================================
# Audit-fix regression tests: operator exactness, nested-slot resolution,
# numeric bound gating, elseconditions warning
# ===========================================================================

_PIV_EXTRA_PRE_SCHEMA_YAML = """
id: https://example.org/piv-extra-pre
name: piv_extra_pre
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/piv-extra-pre/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  temp:
    range: integer
    slot_uri: ex:temp
  mode:
    range: string
    slot_uri: ex:mode
classes:
  Device:
    class_uri: ex:Device
    slots: [temp, mode]
    rules:
      - description: Above 100 the mode must be High (extra precondition operator).
        preconditions:
          slot_conditions:
            temp:
              value_presence: PRESENT
              minimum_value: 100
        postconditions:
          slot_conditions:
            mode:
              equals_string: "High"
"""


def test_rule_extra_precondition_operator_skipped():
    """A precondition combining PRESENT with a threshold must not dispatch to
    presence-implies-value: dropping the threshold widens the trigger."""
    g = _parse_shacl(_PIV_EXTRA_PRE_SCHEMA_YAML)
    shape = URIRef("https://example.org/piv-extra-pre/Device")
    assert list(g.objects(shape, SH.sparql)) == [], "rule with an untranslated conjunct must be skipped"


def test_rule_extra_precondition_operator_pyshacl_end_to_end():
    """A device below the threshold satisfies the rule vacuously and must conform."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_PIV_EXTRA_PRE_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()
    data = """
    @prefix ex: <https://example.org/piv-extra-pre/> .

    ex:cool a ex:Device ; ex:temp 50 ; ex:mode "Low" .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=data,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert conforms, f"Below-threshold device must not be flagged:\n{txt}"


_POST_BOTH_EQUALS_SCHEMA_YAML = """
id: https://example.org/post-both-equals
name: post_both_equals
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/post-both-equals/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  guard:
    slot_uri: ex:guard
  target:
    slot_uri: ex:target
classes:
  Thing:
    class_uri: ex:Thing
    slots: [guard, target]
    rules:
      - preconditions:
          slot_conditions:
            guard:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            target:
              equals_string: "a"
              equals_string_in: ["b", "c"]
"""


def test_rule_post_with_both_equals_forms_skipped():
    """equals_string and equals_string_in set together is ambiguous — skip,
    do not let one form silently win."""
    g = _parse_shacl(_POST_BOTH_EQUALS_SCHEMA_YAML)
    shape = URIRef("https://example.org/post-both-equals/Thing")
    assert list(g.objects(shape, SH.sparql)) == []


_MIXED_SCALAR_SCHEMA_YAML = """
id: https://example.org/mixed-scalar
name: mixed_scalar
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/mixed-scalar/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  code:
    slot_uri: ex:code
  note:
    slot_uri: ex:note
classes:
  Obs:
    class_uri: ex:Obs
    slots: [code, note]
    rules:
      - preconditions:
          slot_conditions:
            code:
              equals_string: fog
              pattern: "^f"
        postconditions:
          slot_conditions:
            note:
              required: true
"""


def test_rule_recognized_plus_unrecognized_operator_skipped():
    """A condition mixing a supported operator (equals_string) with an
    unsupported one (pattern) must skip — translating only the supported part
    widens the trigger."""
    g = _parse_shacl(_MIXED_SCALAR_SCHEMA_YAML)
    shape = URIRef("https://example.org/mixed-scalar/Obs")
    assert list(g.objects(shape, SH.sparql)) == []


_EXPR_ANY_OF_SCHEMA_YAML = """
id: https://example.org/expr-any-of
name: expr_any_of
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/expr-any-of/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  code:
    slot_uri: ex:code
  other:
    slot_uri: ex:other
  note:
    slot_uri: ex:note
classes:
  Obs:
    class_uri: ex:Obs
    slots: [code, other, note]
    rules:
      - preconditions:
          slot_conditions:
            code:
              equals_string: fog
          any_of:
            - slot_conditions:
                other:
                  equals_string: x
            - slot_conditions:
                other:
                  equals_string: y
        postconditions:
          slot_conditions:
            note:
              required: true
"""


def test_rule_expression_level_any_of_skipped():
    """Expression-level any_of on the preconditions cannot be honoured by any
    converter; dropping the branch widens the trigger, so the rule is skipped."""
    g = _parse_shacl(_EXPR_ANY_OF_SCHEMA_YAML)
    shape = URIRef("https://example.org/expr-any-of/Obs")
    assert list(g.objects(shape, SH.sparql)) == []


def test_rule_expression_level_any_of_pyshacl_end_to_end():
    """An instance whose any_of branch is unmet satisfies the rule vacuously
    and must conform."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_EXPR_ANY_OF_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()
    data = """
    @prefix ex: <https://example.org/expr-any-of/> .

    ex:o a ex:Obs ; ex:code "fog" ; ex:other "z" .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=data,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert conforms, f"Instance with unmet any_of branch must not be flagged:\n{txt}"


_POST_MIXED_SCHEMA_YAML = """
id: https://example.org/post-mixed
name: post_mixed
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/post-mixed/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  guard:
    slot_uri: ex:guard
  target:
    slot_uri: ex:target
classes:
  Thing:
    class_uri: ex:Thing
    slots: [guard, target]
    rules:
      - preconditions:
          slot_conditions:
            guard:
              equals_string: on
        postconditions:
          slot_conditions:
            target:
              required: true
              pattern: "^x"
"""


def test_rule_post_mixed_operators_skipped():
    """A postcondition combining required with an untranslated operator must
    skip — checking only required weakens the postcondition."""
    g = _parse_shacl(_POST_MIXED_SCHEMA_YAML)
    shape = URIRef("https://example.org/post-mixed/Thing")
    assert list(g.objects(shape, SH.sparql)) == []


_ABSENT_COMBINED_SCHEMA_YAML = """
id: https://example.org/absent-combined
name: absent_combined
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/absent-combined/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  count:
    range: integer
    slot_uri: ex:count
  note:
    slot_uri: ex:note
classes:
  Obs:
    class_uri: ex:Obs
    slots: [count, note]
    rules:
      - preconditions:
          slot_conditions:
            count:
              value_presence: ABSENT
              minimum_value: 5
        postconditions:
          slot_conditions:
            note:
              required: true
"""


def test_rule_absent_combined_with_bound_skipped():
    """value_presence ABSENT combined with another operator must skip: the
    triple-binding translation would invert the declared trigger."""
    g = _parse_shacl(_ABSENT_COMBINED_SCHEMA_YAML)
    shape = URIRef("https://example.org/absent-combined/Obs")
    assert list(g.objects(shape, SH.sparql)) == []


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
    """equals_string "true" on a NON-boolean slot must dispatch to
    presence-implies-value (string comparison), not the boolean guard."""
    g = _parse_shacl(_STRING_TRUE_SCHEMA_YAML)
    shape = URIRef("https://example.org/string-true/Conf")
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 1
    query = str(list(g.objects(sparql_nodes[0], SH.select))[0])
    assert "NOT IN" in query, f"string-range 'true' must be a string comparison, got:\n{query}"
    assert '"true"' in query, "the comparison term must be the string literal"


def test_rule_equals_true_on_string_slot_pyshacl_end_to_end():
    """status "true" (string) satisfies the rule; the boolean-guard hijack used
    to flag it."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_STRING_TRUE_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()
    conforming = """
    @prefix ex: <https://example.org/string-true/> .

    ex:ok a ex:Conf ; ex:opt "x" ; ex:status "true" .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=conforming,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert conforms, f"status 'true' satisfies the rule and must conform:\n{txt}"

    violating = """
    @prefix ex: <https://example.org/string-true/> .

    ex:bad a ex:Conf ; ex:opt "x" ; ex:status "other" .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=violating,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert not conforms, f"status 'other' violates the rule:\n{txt}"


_INNER_OVERRIDE_SCHEMA_YAML = """
id: https://example.org/inner-override
name: inner_override
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/inner-override/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  sun_position:
    range: SunPosition
    inlined: true
    slot_uri: ex:sun_position
  elevation:
    range: float
    slot_uri: ex:elevation
  headlight_note:
    slot_uri: ex:headlight_note
classes:
  SunPosition:
    class_uri: ex:SunPosition
    slots: [elevation]
    slot_usage:
      elevation:
        slot_uri: ex:localElevation
  Scene:
    class_uri: ex:Scene
    slots: [sun_position, headlight_note]
    rules:
      - description: Below the horizon a headlight note is required.
        preconditions:
          slot_conditions:
            sun_position:
              range_expression:
                slot_conditions:
                  elevation:
                    maximum_value: 0
        postconditions:
          slot_conditions:
            headlight_note:
              required: true
"""


def test_rule_nested_inner_slot_uri_resolved_on_range_class():
    """The inner slot of a nested precondition lives on the container's range
    class; a slot_usage slot_uri override there must be honoured (sh:path /
    SPARQL-body parity one hop down)."""
    g = _parse_shacl(_INNER_OVERRIDE_SCHEMA_YAML)
    shape = URIRef("https://example.org/inner-override/Scene")
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 1
    query = str(list(g.objects(sparql_nodes[0], SH.select))[0])
    assert "https://example.org/inner-override/localElevation" in query, (
        f"inner slot must use the range class's induced slot_uri, got:\n{query}"
    )
    assert "https://example.org/inner-override/elevation" not in query, (
        "the base slot_uri must not leak into the member pattern"
    )


def test_rule_nested_inner_slot_uri_override_pyshacl_end_to_end():
    """A night scene without the required note must be flagged — with the
    base-URI mistranslation the constraint silently never fired."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_INNER_OVERRIDE_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()
    # The float is typed explicitly so the sh:datatype property constraint is
    # satisfied and the outcome discriminates on the rule constraint alone.
    violating = """
    @prefix ex: <https://example.org/inner-override/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:night a ex:Scene ; ex:sun_position ex:sp .
    ex:sp a ex:SunPosition ; ex:localElevation "-5.0"^^xsd:float .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=violating,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert not conforms, f"Night scene without headlight note must fail:\n{txt}"

    conforming = """
    @prefix ex: <https://example.org/inner-override/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:noon a ex:Scene ; ex:sun_position ex:sp2 .
    ex:sp2 a ex:SunPosition ; ex:localElevation "45.0"^^xsd:float .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=conforming,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert conforms, f"Daytime scene needs no headlight note:\n{txt}"


_INNER_COLLISION_SCHEMA_YAML = """
id: https://example.org/inner-collision
name: inner_collision
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/inner-collision/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  marker_flag:
    slot_uri: ex:marker_flag
  items:
    range: Item
    multivalued: true
    inlined: true
    inlined_as_list: true
    slot_uri: ex:items
  type:
    slot_uri: ex:defaultType
classes:
  Item:
    class_uri: ex:Item
    slots: [type]
    slot_usage:
      type:
        slot_uri: ex:itemType
  Box:
    class_uri: ex:Box
    slots: [marker_flag, items, type]
    slot_usage:
      type:
        slot_uri: ex:boxType
    rules:
      - description: A flagged box must contain a marker item.
        preconditions:
          slot_conditions:
            marker_flag:
              value_presence: PRESENT
        postconditions:
          slot_conditions:
            items:
              has_member:
                range_expression:
                  slot_conditions:
                    type:
                      equals_string: marker
"""


def test_rule_has_member_inner_slot_not_shadowed_by_outer_class():
    """An inner slot name that also exists on the OUTER class with a different
    slot_usage URI must still resolve against the member class."""
    g = _parse_shacl(_INNER_COLLISION_SCHEMA_YAML)
    shape = URIRef("https://example.org/inner-collision/Box")
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 1
    query = str(list(g.objects(sparql_nodes[0], SH.select))[0])
    assert "https://example.org/inner-collision/itemType" in query, (
        f"member condition must use the member class's slot URI, got:\n{query}"
    )
    assert "boxType" not in query, "the outer class's slot_usage URI must not shadow the member's"


def test_rule_has_member_inner_slot_collision_pyshacl_end_to_end():
    """A conforming box (marker item present via the member class's predicate)
    must conform — the outer-class shadowing made FILTER NOT EXISTS vacuous."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_INNER_COLLISION_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()
    conforming = """
    @prefix ex: <https://example.org/inner-collision/> .

    ex:b a ex:Box ; ex:marker_flag "y" ; ex:items ex:i1 .
    ex:i1 a ex:Item ; ex:itemType "marker" .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=conforming,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert conforms, f"Box with a marker item must conform:\n{txt}"


_CONTAINER_NARROWED_SCHEMA_YAML = """
id: https://example.org/container-narrowed
name: container_narrowed
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/container-narrowed/
imports:
  - linkml:types
default_prefix: ex
default_range: string
enums:
  BaseKindEnum:
    permissible_values:
      special:
        meaning: ex:BASE_special
  SpecialKindEnum:
    permissible_values:
      special:
        meaning: ex:SPECIAL_special
slots:
  part:
    range: BasePart
    inlined: true
    slot_uri: ex:part
  kind:
    range: BaseKindEnum
    slot_uri: ex:kind
  label_note:
    slot_uri: ex:label_note
classes:
  BasePart:
    class_uri: ex:BasePart
    slots: [kind]
  SpecialPart:
    class_uri: ex:SpecialPart
    is_a: BasePart
    slot_usage:
      kind:
        range: SpecialKindEnum
  Assembly:
    class_uri: ex:Assembly
    slots: [part, label_note]
    slot_usage:
      part:
        range: SpecialPart
    rules:
      - description: A special part requires a label note.
        preconditions:
          slot_conditions:
            part:
              range_expression:
                slot_conditions:
                  kind:
                    equals_string: special
        postconditions:
          slot_conditions:
            label_note:
              required: true
"""


def test_rule_container_range_narrowing_resolves_inner_enum():
    """A slot_usage range-narrowing of the CONTAINER slot must resolve inner
    enum values against the narrowed range class's enum."""
    g = _parse_shacl(_CONTAINER_NARROWED_SCHEMA_YAML)
    shape = URIRef("https://example.org/container-narrowed/Assembly")
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 1
    query = str(list(g.objects(sparql_nodes[0], SH.select))[0])
    assert "SPECIAL_special" in query, f"inner enum must resolve via the narrowed range, got:\n{query}"
    assert "BASE_special" not in query, "the base range's enum must not be used"


_NON_NUMERIC_BOUNDS_SCHEMA_YAML = """
id: https://example.org/non-numeric-bounds
name: non_numeric_bounds
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/non-numeric-bounds/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  v:
    range: integer
    slot_uri: ex:v
  note:
    slot_uri: ex:note
classes:
  Obs:
    class_uri: ex:Obs
    slots: [v, note]
    rules:
      - preconditions:
          slot_conditions:
            v:
              minimum_value: "abc"
        postconditions:
          slot_conditions:
            note:
              required: true
      - preconditions:
          slot_conditions:
            v:
              minimum_value: 2020-01-01
        postconditions:
          slot_conditions:
            note:
              required: true
      - preconditions:
          slot_conditions:
            v:
              maximum_value: .nan
        postconditions:
          slot_conditions:
            note:
              required: true
      - preconditions:
          slot_conditions:
            v:
              minimum_value: true
        postconditions:
          slot_conditions:
            note:
              required: true
"""


def test_rule_non_numeric_bounds_skipped():
    """Non-numeric threshold bounds (string, date, NaN, boolean) must skip the
    rule: raw interpolation produced unparsable SPARQL (poisoning the whole
    shapes graph) or silently-wrong arithmetic (2020-01-01 == 2018)."""
    g = _parse_shacl(_NON_NUMERIC_BOUNDS_SCHEMA_YAML)
    shape = URIRef("https://example.org/non-numeric-bounds/Obs")
    assert list(g.objects(shape, SH.sparql)) == []


def test_rule_non_numeric_bounds_shapes_graph_still_validates():
    """The generated shapes graph must remain usable by pyshacl — one bad bound
    used to raise a ParseException for every validation run."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_NON_NUMERIC_BOUNDS_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()
    data = """
    @prefix ex: <https://example.org/non-numeric-bounds/> .

    ex:o a ex:Obs ; ex:v 1 .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=data,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert conforms, f"Shapes graph must stay parseable and the data conform:\n{txt}"


def test_has_member_zero_members_pyshacl_end_to_end():
    """A node meeting the precondition with ZERO members violates has_member
    ('must contain a matching member'); locks the semantics in."""
    import pyshacl

    shacl_ttl = ShaclGenerator(_HAS_MEMBER_SCHEMA_YAML, mergeimports=False, emit_rules=True).serialize()
    violating = """
    @prefix ex: <https://example.org/has-member/> .

    ex:wZero a ex:Weather ; ex:fog_declared "fog" .
    """
    conforms, _, txt = pyshacl.validate(
        data_graph=violating,
        shacl_graph=shacl_ttl,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
    )
    assert not conforms, f"Zero members cannot contain the required member:\n{txt}"


_ALIAS_KEY_SCHEMA_YAML = """
id: https://example.org/alias-key
name: alias_key
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/alias-key/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  my slot:
    slot_uri: ex:customMySlot
  note:
    slot_uri: ex:note
classes:
  Obs:
    class_uri: ex:Obs
    slots: ["my slot", note]
    rules:
      - description: Underscored alias key must resolve to the declared slot.
        preconditions:
          slot_conditions:
            my_slot:
              equals_string: trigger
        postconditions:
          slot_conditions:
            note:
              required: true
"""


def test_rule_alias_form_slot_key_resolves_override():
    """A rule key written `my_slot` for a slot named `my slot` must resolve to
    that slot's URI (sh:path parity) instead of fabricating a default-prefix
    predicate that makes the constraint vacuous."""
    g = _parse_shacl(_ALIAS_KEY_SCHEMA_YAML)
    shape = URIRef("https://example.org/alias-key/Obs")
    sparql_nodes = list(g.objects(shape, SH.sparql))
    assert len(sparql_nodes) == 1
    query = str(list(g.objects(sparql_nodes[0], SH.select))[0])
    assert "https://example.org/alias-key/customMySlot" in query, (
        f"alias-form key must resolve to the declared slot_uri, got:\n{query}"
    )
    assert "https://example.org/alias-key/my_slot" not in query, (
        "the fabricated default-prefix predicate must not be emitted"
    )


_UNKNOWN_KEY_SCHEMA_YAML = """
id: https://example.org/unknown-key
name: unknown_key
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/unknown-key/
imports:
  - linkml:types
default_prefix: ex
default_range: string
slots:
  code:
    slot_uri: ex:code
  note:
    slot_uri: ex:note
classes:
  Obs:
    class_uri: ex:Obs
    slots: [code, note]
    rules:
      - description: A rule keyed on a nonexistent slot must be skipped.
        preconditions:
          slot_conditions:
            no_such_slot:
              equals_string: trigger
        postconditions:
          slot_conditions:
            note:
              required: true
"""


def test_rule_unknown_slot_key_skipped():
    """A rule whose condition keys a slot that does not exist must be skipped:
    fabricating a default-prefix predicate would emit a constraint that can
    never fire (or, for has_member, always fires)."""
    g = _parse_shacl(_UNKNOWN_KEY_SCHEMA_YAML)
    shape = URIRef("https://example.org/unknown-key/Obs")
    assert list(g.objects(shape, SH.sparql)) == []
