import logging
import os
from dataclasses import dataclass, field

import click
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.collection import Collection
from rdflib.namespace import RDF, SH

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments

LINK_ML_TYPES_STRING = URIRef("http://www.w3.org/2001/XMLSchema#string")
LINK_ML_TYPES_BOOL = URIRef("http://www.w3.org/2001/XMLSchema#boolean")
LINK_ML_TYPES_DECIMAL = URIRef("http://www.w3.org/2001/XMLSchema#decimal")
LINK_ML_TYPES_INTEGER = URIRef("http://www.w3.org/2001/XMLSchema#integer")
LINK_ML_TYPES_FLOAT = URIRef("http://www.w3.org/2001/XMLSchema#float")
LINK_ML_TYPES_DOUBLE = URIRef("http://www.w3.org/2001/XMLSchema#double")
LINK_ML_TYPES_DURATION = URIRef("http://www.w3.org/2001/XMLSchema#duration")
LINK_ML_TYPES_DATETIME = URIRef("http://www.w3.org/2001/XMLSchema#dateTime")
LINK_ML_TYPES_DATE = URIRef("http://www.w3.org/2001/XMLSchema#date")
LINK_ML_TYPES_TIME = URIRef("http://www.w3.org/2001/XMLSchema#time")
LINK_ML_TYPES_DATE_TIME = URIRef("http://www.w3.org/2001/XMLSchema#datetime")
LINK_ML_TYPES_URI = URIRef("http://www.w3.org/2001/XMLSchema#anyURI")
LINK_ML_TYPES_OBJECT_ID = URIRef("http://www.w3.org/ns/shex#iri")
LINK_ML_TYPES_NODE_ID = URIRef("http://www.w3.org/ns/shex#nonLiteral")


@dataclass
class ShaclGenerator(Generator):
    # ClassVars
    closed: bool = field(default_factory=lambda: True)
    """True means add 'sh:closed=true' to all shapes, except of mixin shapes and shapes, that have parents"""

    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = ["ttl"]
    file_extension = "shacl.ttl"
    visit_all_class_slots = False
    uses_schemaloader = True

    def __post_init__(self) -> None:
        self.schemaview = SchemaView(self.schema)
        super().__post_init__()
        self.generate_header()

    def generate_header(self):
        print(f"# metamodel_version: {self.schema.metamodel_version}")
        if self.schema.version:
            print(f"# version: {self.schema.version}")

    def serialize(self, **args) -> str:
        g = self.as_graph()
        data = g.serialize(format="turtle" if self.format in ["owl", "ttl"] else self.format)
        return data

    def as_graph(self) -> Graph:
        sv = self.schemaview
        g = Graph()
        g.bind("sh", SH)
        for pfx in self.schema.prefixes.values():
            g.bind(str(pfx.prefix_prefix), pfx.prefix_reference)

        for c in sv.all_classes().values():

            def shape_pv(p, v):
                if v is not None:
                    g.add((class_uri, p, v))

            class_uri = URIRef(sv.get_uri(c, expand=True))
            shape_pv(RDF.type, SH.NodeShape)
            shape_pv(SH.targetClass, class_uri)  # TODO
            if self.closed:
                if c.mixin or c.abstract:
                    shape_pv(SH.closed, Literal(False))
                else:
                    shape_pv(SH.closed, Literal(True))
            else:
                shape_pv(SH.closed, Literal(False))
            if c.title is not None:
                shape_pv(SH.name, Literal(c.title))
            if c.description is not None:
                shape_pv(SH.description, Literal(c.description))
            list_node = BNode()
            Collection(g, list_node, [RDF.type])
            shape_pv(SH.ignoredProperties, list_node)
            order = 0
            for s in sv.class_induced_slots(c.name):
                # fixed in linkml-runtime 1.1.3
                if s.name in sv.element_by_schema_map():
                    slot_uri = URIRef(sv.get_uri(s, expand=True))
                else:
                    pfx = sv.schema.default_prefix
                    slot_uri = URIRef(sv.expand_curie(f"{pfx}:{underscore(s.name)}"))
                pnode = BNode()
                shape_pv(SH.property, pnode)

                def prop_pv(p, v):
                    if v is not None:
                        g.add((pnode, p, v))

                def prop_pv_literal(p, v):
                    if v is not None:
                        g.add((pnode, p, Literal(v)))

                prop_pv(SH.path, slot_uri)
                prop_pv_literal(SH.order, order)
                order += 1
                prop_pv_literal(SH.name, s.title)
                prop_pv_literal(SH.description, s.description)
                if not s.multivalued:
                    prop_pv_literal(SH.maxCount, 1)
                if s.required:
                    prop_pv_literal(SH.minCount, 1)
                prop_pv_literal(SH.minInclusive, s.minimum_value)
                prop_pv_literal(SH.maxInclusive, s.maximum_value)
                prop_pv_literal(SH.hasValue, s.equals_number)
                r = s.range
                if r in sv.all_classes():
                    range_ref = sv.get_uri(r, expand=True)
                    prop_pv(SH["class"], URIRef(range_ref))
                    if sv.get_identifier_slot(r) is not None:
                        prop_pv(SH.nodeKind, SH.IRI)
                    else:
                        prop_pv(SH.nodeKind, SH.BlankNode)
                elif r in sv.all_types().values():
                    rt = sv.get_type(r)
                    if rt.uri:
                        prop_pv(SH.datatype, rt.uri)
                    else:
                        logging.error(f"No URI for type {rt.name}")
                elif r in sv.all_enums():
                    e = sv.get_enum(r)
                    pv_node = BNode()
                    Collection(
                        g,
                        pv_node,
                        [
                            URIRef(sv.expand_curie(pv.meaning)) if pv.meaning else Literal(pv_name)
                            for pv_name, pv in e.permissible_values.items()
                        ],
                    )
                    prop_pv(SH["in"], pv_node)
                else:
                    if r == "string":
                        prop_pv(SH.datatype, LINK_ML_TYPES_STRING)
                    elif r == "boolean":
                        prop_pv(SH.datatype, LINK_ML_TYPES_BOOL)
                    elif r == "duration":
                        prop_pv(SH.datatype, LINK_ML_TYPES_DURATION)
                    elif r == "datetime":
                        prop_pv(SH.datatype, LINK_ML_TYPES_DATETIME)
                    elif r == "date":
                        prop_pv(SH.datatype, LINK_ML_TYPES_DATE)
                    elif r == "time":
                        prop_pv(SH.datatype, LINK_ML_TYPES_TIME)
                    elif r == "datetime":
                        prop_pv(SH.datatype, LINK_ML_TYPES_DATE_TIME)
                    elif r == "decimal":
                        prop_pv(SH.datatype, LINK_ML_TYPES_DECIMAL)
                    elif r == "integer":
                        prop_pv(SH.datatype, LINK_ML_TYPES_INTEGER)
                    elif r == "float":
                        prop_pv(SH.datatype, LINK_ML_TYPES_FLOAT)
                    elif r == "double":
                        prop_pv(SH.datatype, LINK_ML_TYPES_DOUBLE)
                    elif r == "uri":
                        prop_pv(SH.datatype, LINK_ML_TYPES_URI)
                    elif r == "curi":
                        prop_pv(SH.datatype, LINK_ML_TYPES_STRING)
                    elif r == "ncname":
                        prop_pv(SH.datatype, LINK_ML_TYPES_STRING)
                    elif r == "objectidentifier":
                        prop_pv(SH.datatype, LINK_ML_TYPES_OBJECT_ID)
                    elif r == "nodeidentifier":
                        prop_pv(SH.datatype, LINK_ML_TYPES_NODE_ID)
                    elif r == "jsonpointer":
                        prop_pv(SH.datatype, LINK_ML_TYPES_STRING)
                    elif r == "jsonpath":
                        prop_pv(SH.datatype, LINK_ML_TYPES_STRING)
                    elif r == "sparqlpath":
                        prop_pv(SH.datatype, LINK_ML_TYPES_STRING)
                if s.pattern:
                    prop_pv(SH.pattern, Literal(s.pattern))
        return g


@shared_arguments(ShaclGenerator)
@click.option(
    "--closed/--non-closed",
    default=True,
    show_default=True,
    help="Use '--closed' to generate closed SHACL shapes. Use '--non-closed' to generate open SHACL shapes.",
)
@click.version_option(__version__, "-V", "--version")
@click.command()
def cli(yamlfile, **args):
    """Generate SHACL turtle from a LinkML model"""
    gen = ShaclGenerator(yamlfile, **args)
    print(gen.serialize())


if __name__ == "__main__":
    cli()
