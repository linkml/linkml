import logging
import os
from dataclasses import dataclass
from typing import Callable

import click
from linkml_runtime.linkml_model.meta import ElementName
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.collection import Collection
from rdflib.namespace import RDF, SH

from linkml._version import __version__
from linkml.generators.shacl.ifabsent_processor import IfAbsentProcessor
from linkml.generators.shacl.shacl_data_type import ShaclDataType
from linkml.utils.generator import Generator, shared_arguments


@dataclass
class ShaclGenerator(Generator):
    # ClassVars
    closed: bool = True
    """True means add 'sh:closed=true' to all shapes, except of mixin shapes and shapes, that have parents"""
    suffix: str = None
    """parameterized suffix to be appended. No suffix per default."""
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

        ifabsent_processor = IfAbsentProcessor(sv)

        for pfx in self.schema.prefixes.values():
            g.bind(str(pfx.prefix_prefix), pfx.prefix_reference)

        for c in sv.all_classes().values():

            def shape_pv(p, v):
                if v is not None:
                    g.add((class_uri_with_suffix, p, v))

            class_uri = URIRef(sv.get_uri(c, expand=True))
            class_uri_with_suffix = class_uri
            if self.suffix is not None:
                class_uri_with_suffix += self.suffix
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

                all_classes = sv.all_classes()
                if s.any_of:
                    or_node = BNode()
                    prop_pv(SH["or"], or_node)
                    range_list = []
                    for any in s.any_of:
                        r = any.range
                        if r in all_classes:
                            class_node = BNode()

                            def cl_node_pv(p, v):
                                if v is not None:
                                    g.add((class_node, p, v))

                            self._add_class(cl_node_pv, r)
                            range_list.append(class_node)
                        elif r in sv.all_types().values():
                            t_node = BNode()

                            def t_node_pv(p, v):
                                if v is not None:
                                    g.add((t_node, p, v))

                            self._add_type(t_node_pv, r)
                            range_list.append(t_node)
                        elif r in sv.all_enums():
                            en_node = BNode()

                            def en_node_pv(p, v):
                                if v is not None:
                                    g.add((en_node, p, v))

                            self._add_enum(g, en_node_pv, r)
                            range_list.append(en_node)
                        else:
                            st_node = BNode()

                            def st_node_pv(p, v):
                                if v is not None:
                                    g.add((st_node, p, v))

                            add_simple_data_type(st_node_pv, r)
                            range_list.append(st_node)
                    Collection(g, or_node, range_list)

                else:
                    prop_pv_literal(SH.hasValue, s.equals_number)
                    r = s.range
                    if r in all_classes:
                        self._add_class(prop_pv, r)
                        if sv.get_identifier_slot(r) is not None:
                            prop_pv(SH.nodeKind, SH.IRI)
                        else:
                            prop_pv(SH.nodeKind, SH.BlankNodeOrIRI)
                    elif r in sv.all_types().values():
                        self._add_type(prop_pv, r)
                    elif r in sv.all_enums():
                        self._add_enum(g, prop_pv, r)
                    else:
                        add_simple_data_type(prop_pv, r)
                    if s.pattern:
                        prop_pv(SH.pattern, Literal(s.pattern))

                ifabsent_processor.process_slot(prop_pv, s, class_uri)

        return g

    def _add_class(self, func: Callable, r: ElementName) -> None:
        sv = self.schemaview
        range_ref = sv.get_uri(r, expand=True)
        func(SH["class"], URIRef(range_ref))

    def _add_enum(self, g: Graph, func: Callable, r: ElementName) -> None:
        sv = self.schemaview
        enum = sv.get_enum(r)
        pv_node = BNode()
        Collection(
            g,
            pv_node,
            [
                URIRef(sv.expand_curie(pv.meaning)) if pv.meaning else Literal(pv_name)
                for pv_name, pv in enum.permissible_values.items()
            ],
        )
        func(SH["in"], pv_node)

    def _add_type(self, func: Callable, r: ElementName) -> None:
        sv = self.schemaview
        rt = sv.get_type(r)
        if rt.uri:
            func(SH.datatype, rt.uri)
        else:
            logging.error(f"No URI for type {rt.name}")


def add_simple_data_type(func: Callable, r: ElementName) -> None:
    for datatype in list(ShaclDataType):
        if datatype.linkml_type == r:
            func(SH.datatype, datatype.uri_ref)


@shared_arguments(ShaclGenerator)
@click.command()
@click.option(
    "--closed/--non-closed",
    default=True,
    show_default=True,
    help="Use '--closed' to generate closed SHACL shapes. Use '--non-closed' to generate open SHACL shapes.",
)
@click.option(
    "-s",
    "--suffix",
    default=None,
    show_default=True,
    help="Use --suffix to append given string to SHACL class name (e. g. --suffix Shape: Person becomes PersonShape).",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **args):
    """Generate SHACL turtle from a LinkML model"""
    gen = ShaclGenerator(yamlfile, **args)
    print(gen.serialize())


if __name__ == "__main__":
    cli()
