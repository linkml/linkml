from collections import Counter
from typing import Any, List, Tuple

import rdflib
from rdflib import RDFS, SH, Literal, URIRef

from linkml.generators.shacl.shacl_data_type import ShaclDataType
from linkml.generators.shaclgen import ShaclGenerator

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
    expected: List[Tuple[rdflib.term.URIRef, List[Tuple[rdflib.term.URIRef, rdflib.term.URIRef]]]], triples: List
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
    expected: List[Tuple[rdflib.term.URIRef, List[Tuple[rdflib.term.URIRef, rdflib.term.URIRef]]]], triples: List
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
    expected: List[Tuple[rdflib.term.URIRef, List[Tuple[rdflib.term.URIRef, rdflib.term.URIRef]]]], triples: List
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


def _get_data_type(blank_node: rdflib.term.BNode, triples: List) -> List[rdflib.term.URIRef]:
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
            assert (subject, SH.defaultValue, Literal(default_value, datatype=datatype)) in g

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
    shacl = ShaclGenerator(input_path("shaclgen_custom_class_range.yaml"), mergeimports=True).serialize()

    g = rdflib.Graph()
    g.parse(data=shacl)

    container_properties = g.objects(URIRef("https://w3id.org/linkml/examples/personinfo/Container"), SH.property)
    persons_node = next(container_properties, None)
    assert persons_node

    assert (persons_node, SH.nodeKind, SH.BlankNodeOrIRI) in g


def test_is_a_becomes_a_rdfs_subclass_of(input_path):
    shacl = ShaclGenerator(input_path("shaclgen_subclass_of.yaml"), mergeimports=True).serialize()

    g = rdflib.Graph()
    g.parse(data=shacl)

    assert (
        URIRef("https://w3id.org/linkml/examples/personinfo/Citizen"),
        RDFS.subClassOf,
        URIRef("https://w3id.org/linkml/examples/personinfo/Person"),
    ) in g
