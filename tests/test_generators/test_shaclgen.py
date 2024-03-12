from collections import Counter
from typing import List, Tuple

import rdflib

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


def test_shacl(kitchen_sink_path):
    """tests shacl generation"""
    shaclstr = ShaclGenerator(kitchen_sink_path, mergeimports=True).serialize()
    do_test(shaclstr, EXPECTED)


def test_shacl_closed(kitchen_sink_path):
    """tests shacl generation"""
    shaclstr = ShaclGenerator(kitchen_sink_path, mergeimports=True, closed=False).serialize()
    do_test(shaclstr, EXPECTED_closed)


def do_test(shaclstr, expected):
    g = rdflib.Graph()
    g.parse(data=shaclstr)
    triples = list(g.triples((None, None, None)))
    for et in expected:
        assert et in triples
    # TODO: test shacl validation; pyshacl requires rdflib6

    assert_any_of(EXPECTED_any_of, triples)


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
