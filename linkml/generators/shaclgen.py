import os
import logging
from typing import Optional, Tuple, List, Union, TextIO, Callable, Dict, Iterator, Set
from copy import copy, deepcopy

import click
from rdflib import Graph, URIRef, BNode, Literal
from rdflib.collection import Collection
from rdflib.namespace import RDF, RDFS, SH, XSD

from linkml_runtime.utils.schemaview import SchemaView

#from linkml.generators import shacl_GEN_VERSION
from linkml_runtime.linkml_model.meta import SchemaDefinition, TypeDefinition, ClassDefinition, Annotation
from linkml_runtime.utils.formatutils import camelcase, underscore

from linkml.generators.oocodegen import OOCodeGenerator
from linkml.utils.generator import shared_arguments, Generator


def _get_pyrange(t: TypeDefinition, sv: SchemaView) -> str:
    pyrange = t.repr
    if pyrange is None:
        pyrange = t.base
    if t.base == 'XSDDateTime':
        pyrange = 'datetime '
    if t.base == 'XSDDate':
        pyrange = 'date'
    if pyrange is None and t.typeof is not None:
        pyrange = _get_pyrange(sv.get_type(t.typeof), sv)
    if pyrange is None:
        raise Exception(f'No python type for range: {s.range} // {t}')
    return pyrange

class ShaclGenerator(Generator):
    generatorname = os.path.basename(__file__)
    generatorversion = '0.0.1'
    valid_formats = ['ttl']
    visit_all_class_slots = False

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition],
                 format: str = valid_formats[0],
                 genmeta: bool=False, gen_classvars: bool=True, gen_slots: bool=True, **kwargs) -> None:
        self.sourcefile = schema
        self.schemaview = SchemaView(schema)
        self.schema = self.schemaview.schema
        self.format = format

    def serialize(self) -> None:
        g = self.as_graph()
        data = g.serialize(format='turtle' if self.format in ['owl', 'ttl'] else self.format).decode()
        return data

    def as_graph(self) -> None:
        sv = self.schemaview
        g = Graph()
        for c in sv.all_classes().values():
            def shape_pv(p, v):
                if v is not None:
                    g.add((class_uri, p, v))
            class_uri = URIRef(sv.get_uri(c, expand=True))
            shape_pv(RDF.type, SH.NodeShape)
            shape_pv(SH.targetClass, class_uri)  ## TODO
            shape_pv(SH.closed, Literal(True))
            list_node = BNode()
            coll = Collection(g, list_node, [RDF.type])
            shape_pv(SH.ignoredProperties, list_node)
            type_designator = None
            for s in sv.class_induced_slots(c.name):
                if s.name in sv.element_by_schema_map():
                    slot_uri = URIRef(sv.get_uri(s, expand=True))
                else:
                    logging.warning(f'TODO: FIX SCHEMAVIEW {s.name} not in element_by_schema_map')
                    pfx = sv.schema.default_prefix
                    slot_uri = URIRef(sv.expand_curie(f'{pfx}:{underscore(s.name)}'))
                pnode = BNode()
                shape_pv(SH.property, pnode)
                def prop_pv(p, v):
                    if v is not None:
                        g.add((pnode, p, v))
                def prop_pv_literal(p, v):
                    if v is not None:
                        g.add((pnode, p, Literal(v)))
                prop_pv(SH.path, slot_uri)
                if not s.multivalued:
                    prop_pv_literal(SH.maxCount, 1)
                if s.required:
                    prop_pv_literal(SH.minCount, 1)
                prop_pv_literal(SH.minInclusive, s.minimum_value)
                prop_pv_literal(SH.maxInclusive, s.maximum_value)
                r = s.range
                if r in sv.all_classes():
                    range_ref = sv.get_uri(r, expand=True)
                    prop_pv(SH['class'], URIRef(range_ref))
                    if sv.get_identifier_slot(r) is not None:
                        prop_pv(SH.nodeKind, SH.IRI)
                    else:
                        prop_pv(SH.nodeKind, SH.BlankNode)
                elif r in sv.all_types().values():
                    if r.uri:
                        prop_pv(SH.datatype, r.uri)
                    else:
                        logging.error(f'No URI for type {r.name}')
                elif r in sv.all_enums():
                    e = sv.get_enum(r)
                    pv_node = BNode()
                    pv_coll = Collection(g, pv_node, [URIRef(sv.expand_curie(pv.meaning)) if pv.meaning else Literal(pv_name) for pv_name, pv in e.permissible_values.items()])
                    prop_pv(SH['in'], pv_node)
                else:
                    None # TODO
                if s.pattern:
                    prop_pv(SH.pattern, Literal(s.pattern))
                if s.designates_type:
                    type_designator = s





        return g



@shared_arguments(ShaclGenerator)
@click.option("--output_directory", default="output", help="Output directory for individually generated class files")
@click.option("--package", help="Package name where relevant for generated class files")
@click.option("--template_file", help="Optional jinja2 template to use for class generation")
@click.command()
def cli(yamlfile, output_directory=None, package=None, template_file=None, head=True, emit_metadata=False, genmeta=False, classvars=True, slots=True, **args):
    """Generate shacl classes to represent a LinkML model"""
    gen = ShaclGenerator(yamlfile, package=package, template_file=template_file, emit_metadata=head, genmeta=genmeta, gen_classvars=classvars, gen_slots=slots,  **args)
    print(gen.serialize(output_directory))


if __name__ == '__main__':
    cli()
