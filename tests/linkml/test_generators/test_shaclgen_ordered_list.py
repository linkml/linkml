"""SHACL generation for ordered multivalued slots (``list_elements_ordered``).

Such slots are serialized by the RDF dumper as an ``rdf:List`` (issue #3531), so the
generated property shape must constrain each *list member* rather than the list head.
This is done with a SHACL sequence path that walks the list:

    sh:path ( <slot> [ sh:zeroOrMorePath rdf:rest ] rdf:first )

These tests assert both the generated shape structure and, end to end, that the
``rdf:List`` output of the dumper actually validates against the generated shapes.
"""

import rdflib
from pyshacl import validate
from rdflib import RDF, SH, Graph, Literal, URIRef
from rdflib.collection import Collection

from linkml.generators.pythongen import PythonGenerator
from linkml.generators.shaclgen import ShaclGenerator
from linkml_runtime.dumpers.rdflib_dumper import RDFLibDumper
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.schemaview import SchemaView

EX = "https://w3id.org/linkml/examples/ordered_list/"
COLUMN_DESC = URIRef(EX + "ColumnDesc")
SCOPE = URIRef(EX + "scope")
SCOPE_VALUES = ["latitude", "longitude", "easting", "northing"]


def _shapes_graph(schema: str) -> Graph:
    g = Graph()
    g.parse(data=ShaclGenerator(schema, mergeimports=True, closed=False).serialize())
    return g


def _property_shape(g: Graph, cls: URIRef, slot_uri: URIRef):
    """Return the property-shape node whose path traverses ``slot_uri``."""
    for pnode in g.objects(cls, SH.property):
        path = next(g.objects(pnode, SH.path), None)
        if path == slot_uri or (path is not None and slot_uri in Collection(g, path)):
            return pnode
    return None


def test_ordered_slot_emits_list_traversal_path(input_path):
    """An ordered slot's ``sh:path`` is the ``( slot rest* first )`` sequence path."""
    g = _shapes_graph(input_path("shaclgen/list_elements_ordered.yaml"))
    pnode = _property_shape(g, COLUMN_DESC, SCOPE)
    assert pnode is not None
    path = next(g.objects(pnode, SH.path))
    members = list(Collection(g, path))
    assert members[0] == SCOPE
    assert members[-1] == RDF.first
    # middle element is a [ sh:zeroOrMorePath rdf:rest ] blank node
    assert (members[1], SH.zeroOrMorePath, RDF.rest) in g
    # the datatype constraint still rides on the same property shape
    assert (pnode, SH.datatype, rdflib.XSD.string) in g


def test_unordered_slot_keeps_plain_path(input_path):
    """A plain multivalued slot is unaffected: ``sh:path`` is the slot URI directly."""
    g = _shapes_graph(input_path("shaclgen/list_elements_ordered.yaml"))
    pnode = _property_shape(g, COLUMN_DESC, URIRef(EX + "tags"))
    assert pnode is not None
    assert next(g.objects(pnode, SH.path)) == URIRef(EX + "tags")


def test_generated_shapes_validate_rdf_list_output(input_path):
    """End to end: the dumper's ``rdf:List`` output conforms to the generated shapes."""
    schema = input_path("shaclgen/list_elements_ordered.yaml")
    sv = SchemaView(schema)
    module = compile_python(PythonGenerator(schema).serialize())

    obj = module.ColumnDesc(
        atom="ex:sampled_data",
        scope=SCOPE_VALUES,
        items=[module.Item("ex:z"), module.Item("ex:m")],
        tags=["a", "b"],
    )
    data = Graph()
    data.parse(data=RDFLibDumper().dumps(obj, schemaview=sv), format="turtle")
    shapes = _shapes_graph(schema)

    conforms, _, report = validate(data, shacl_graph=shapes, inference="none")
    assert conforms, report

    # a non-string member injected into the list must be flagged
    head = next(data.objects(None, SCOPE))
    data.set((head, RDF.first, Literal(42)))
    conforms_bad, _, _ = validate(data, shacl_graph=shapes, inference="none")
    assert not conforms_bad
