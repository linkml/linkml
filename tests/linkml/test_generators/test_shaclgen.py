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
