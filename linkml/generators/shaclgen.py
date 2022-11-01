import logging
import os
from copy import copy, deepcopy
from dataclasses import field
from typing import (Callable, Dict, Iterator, List, Optional, Set, TextIO,
                    Tuple, Union)

import click
from linkml_runtime.linkml_model.meta import (Annotation, ClassDefinition,
                                              SchemaDefinition, TypeDefinition)
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.collection import Collection
from rdflib.namespace import RDF, RDFS, SH, XSD

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments


class ShaclGenerator(Generator):
    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = ["ttl"]
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

    def serialize(self, **args) -> None:
        g = self.as_graph()
        data = g.serialize(
            format="turtle" if self.format in ["owl", "ttl"] else self.format
        ).decode()
        return data

    def as_graph(self) -> None:
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
            shape_pv(SH.targetClass, class_uri)  ## TODO
            shape_pv(SH.closed, Literal(True))
            if c.title is not None:
                shape_pv(SH.name, Literal(c.title))
            if c.description is not None:
                shape_pv(SH.description, Literal(c.description))
            list_node = BNode()
            coll = Collection(g, list_node, [RDF.type])
            shape_pv(SH.ignoredProperties, list_node)
            type_designator = None
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
                    pv_coll = Collection(
                        g,
                        pv_node,
                        [
                            URIRef(sv.expand_curie(pv.meaning))
                            if pv.meaning
                            else Literal(pv_name)
                            for pv_name, pv in e.permissible_values.items()
                        ],
                    )
                    prop_pv(SH["in"], pv_node)
                else:
                    None  # TODO
                if s.pattern:
                    prop_pv(SH.pattern, Literal(s.pattern))
                if s.designates_type:
                    type_designator = s

        return g


@shared_arguments(ShaclGenerator)
@click.version_option(__version__, "-V", "--version")
@click.command()
def cli(yamlfile, **args):
    """Generate SHACL turtle from a LinkML model"""
    gen = ShaclGenerator(yamlfile, **args)
    print(gen.serialize())


if __name__ == "__main__":
    cli()
