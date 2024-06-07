import logging
import os
from dataclasses import dataclass
from typing import Callable, List

import click
from jsonasobj2 import JsonObj, as_dict
from linkml_runtime.linkml_model.meta import ElementName
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import TypedNode, extended_float, extended_int, extended_str
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.collection import Collection
from rdflib.namespace import RDF, SH, XSD

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
    include_annotations: bool = False
    """True means include all class / slot / type annotations in generated Node or Property shapes"""
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

    def generate_header(self) -> str:
        out = f"\n# metamodel_version: {self.schema.metamodel_version}"
        if self.schema.version:
            out += f"\n# version: {self.schema.version}"
        return out

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
            if c.annotations and self.include_annotations:
                self._add_annotations(shape_pv, c)
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
                    # It is not allowed to use any of and equals_string or equals_string_in in one
                    # slot definition, as both are mapped to sh:in in SHACL
                    if s.equals_string or s.equals_string_in:
                        error = "'equals_string'/'equals_string_in' and 'any_of' are mutually exclusive"
                        raise ValueError(f'{TypedNode.yaml_loc(s, suffix="")} {error}')

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
                        elif r in sv.all_types():
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
                    if s.equals_string or s.equals_string_in:
                        # Check if range is "string" as this is mandatory for "equals_string" and "equals_string_in"
                        if r != "string":
                            raise ValueError(
                                f"slot: \"{slot_uri}\" - 'equals_string' and 'equals_string_in'"
                                f" require range 'string' and not '{r}'"
                            )

                    if r in all_classes:
                        self._add_class(prop_pv, r)
                        if sv.get_identifier_slot(r) is not None:
                            prop_pv(SH.nodeKind, SH.IRI)
                        else:
                            prop_pv(SH.nodeKind, SH.BlankNodeOrIRI)
                    elif r in sv.all_types():
                        self._add_type(prop_pv, r)
                    elif r in sv.all_enums():
                        self._add_enum(g, prop_pv, r)
                    else:
                        add_simple_data_type(prop_pv, r)
                    if s.pattern:
                        prop_pv(SH.pattern, Literal(s.pattern))
                    if s.annotations and self.include_annotations:
                        self._add_annotations(prop_pv, s)
                    if s.equals_string:
                        # Map equal_string and equal_string_in to sh:in
                        self._and_equals_string(g, prop_pv, [s.equals_string])
                    if s.equals_string_in:
                        # Map equal_string and equal_string_in to sh:in
                        self._and_equals_string(g, prop_pv, s.equals_string_in)

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
        func(SH.nodeKind, SH.Literal)
        sv = self.schemaview
        rt = sv.get_type(r)
        if rt.uri:
            func(SH.datatype, URIRef(sv.get_uri(rt, expand=True)))
            if rt.pattern:
                func(SH.pattern, Literal(rt.pattern))
            if rt.annotations and self.include_annotations:
                self._add_annotations(func, rt)
        else:
            logging.error(f"No URI for type {rt.name}")

    def _and_equals_string(self, g: Graph, func: Callable, values: List) -> None:
        pv_node = BNode()
        Collection(
            g,
            pv_node,
            [Literal(v) for v in values],
        )
        func(SH["in"], pv_node)

    def _add_annotations(self, func: Callable, item) -> None:
        # TODO: migrate some of this logic to SchemaView
        sv = self.schemaview
        annotations = item.annotations
        # item could be a class, slot or type
        # annotation type could be dict (on types) or JsonObj (on slots)
        if type(annotations) == JsonObj:
            annotations = as_dict(annotations)
        for a in annotations.values():
            # If ':' is in the tag, treat it as a CURIE, otherwise string Literal
            if ":" in a["tag"]:
                N_predicate = URIRef(sv.expand_curie(a["tag"]))
            else:
                N_predicate = Literal(a["tag"], datatype=XSD.string)
            # If the value is a string and ':' is in the value, treat it as a CURIE,
            # otherwise treat as Literal with derived XSD datatype
            if type(a["value"]) == extended_str and ":" in a["value"]:
                N_object = URIRef(sv.expand_curie(a["value"]))
            else:
                N_object = Literal(a["value"], datatype=self._getXSDtype(a["value"]))

            func(N_predicate, N_object)

    def _getXSDtype(self, value):
        value_type = type(value)
        if value_type == bool:
            return XSD.boolean
        elif value_type == extended_str:
            return XSD.string
        elif value_type == extended_int:
            return XSD.integer
        elif value_type == extended_float:
            # TODO: distinguish between xsd:decimal and xsd:double?
            return XSD.decimal
        else:
            return None

    def _and_equals_string(self, g: Graph, func: Callable, values: List) -> None:
        pv_node = BNode()
        Collection(
            g,
            pv_node,
            [Literal(v) for v in values],
        )
        func(SH["in"], pv_node)


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
@click.option(
    "--include-annotations/--exclude-annotations",
    default=False,
    show_default=True,
    help="Use --include-annotations to include annotations of slots, types, and classes in the generated SHACL shapes.",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **args):
    """Generate SHACL turtle from a LinkML model"""
    gen = ShaclGenerator(yamlfile, **args)
    print(gen.serialize())


if __name__ == "__main__":
    cli()
