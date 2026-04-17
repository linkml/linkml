from collections import Counter
from typing import Any

import rdflib
from rdflib import RDF, RDFS, SH, Literal, URIRef
from rdflib.collection import Collection

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
