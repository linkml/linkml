"""
Generate JSON-LD contexts

"""
import os
import re
from typing import Union, TextIO, Set, Optional

import click
from jsonasobj2 import JsonObj, as_json
from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition, SlotDefinition, Definition, Element
from linkml_runtime.linkml_model.types import SHEX
from linkml_runtime.utils.formatutils import camelcase, underscore, be
from rdflib import XSD, SKOS

from linkml.utils.generator import Generator, shared_arguments

URI_RANGES = (XSD.anyURI, SHEX.nonliteral, SHEX.bnode, SHEX.iri)


ENUM_CONTEXT = {
    "@vocab": "@null",
    "text": "skos:notation",
    "description": "skos:prefLabel",
    "meaning": "@id"
}


class ContextGenerator(Generator):
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ['context', 'json']
    visit_all_class_slots = False

    def __init__(self,
                 schema: Union[str, TextIO, SchemaDefinition],
                 **kwargs) -> None:
        super().__init__(schema, **kwargs)
        if self.namespaces is None:
            raise TypeError("Schema text must be supplied to context generater.  Preparsed schema will not work")
        self.emit_prefixes: Set[str] = set()
        self.default_ns = None
        self.context_body = dict()
        self.slot_class_maps = dict()

    def visit_schema(self, base: Optional[str]=None, output: Optional[str]=None, **_):
        # Add any explicitly declared prefixes
        for prefix in self.schema.prefixes.values():
            self.emit_prefixes.add(prefix.prefix_prefix)

        # Add any prefixes explicitly declared
        for pfx in self.schema.emit_prefixes:
            self.add_prefix(pfx)

        # Add the default prefix
        if self.schema.default_prefix:
            dflt = self.namespaces.prefix_for(self.schema.default_prefix)
            if dflt:
                self.default_ns = dflt
            if self.default_ns:
                default_uri = self.namespaces[self.default_ns]
                self.emit_prefixes.add(self.default_ns)
            else:
                default_uri=self.schema.default_prefix
                if self.schema.name:
                    self.namespaces[self.schema.name] = default_uri
                    self.emit_prefixes.add(self.schema.name)
            self.context_body['@vocab'] = default_uri
            # self.context_body['@base'] = self.base_dir

    def end_schema(self,
                   base: Optional[str] = None,
                   output: Optional[str] = None,
                   prefixes: Optional[bool] = True,
                   flatprefixes: Optional[bool] = False,
                   model: Optional[bool] = True, **_) -> None:
        context = JsonObj()
        if self.emit_metadata:
            comments = f'''Auto generated from {self.schema.source_file} by {self.generatorname} version: {self.generatorversion}'''
            if self.schema.generation_date:
                comments += f'''
    Generation date: {self.schema.generation_date}
    Schema: {self.schema.name}
    '''
            comments += f'''
    id: {self.schema.id}
    description: {be(self.schema.description)}
    license: {be(self.schema.license)}
    '''
            context["_comments"] = comments
        context_content = {}
        if base:
            if '://' not in base:
                self.context_body['@base'] = os.path.relpath(base, os.path.dirname(self.schema.source_file))
            else:
                self.context_body['@base'] = base
        if prefixes:
            for prefix in sorted(self.emit_prefixes):
                url = str(self.namespaces[prefix])
                # Derived from line # ~5223 in pyld/lib/jsonld.py
                if bool(re.match(r'.*[:/\?#\[\]@]$', url)) or flatprefixes:
                    context_content[prefix] = url
                else:
                    prefix_obj = JsonObj()
                    prefix_obj["@id"] = url
                    prefix_obj["@prefix"] = True
                    context_content[prefix] = prefix_obj
        if model:
            for k, v in self.context_body.items():
                context_content[k] = v
            for k, v in self.slot_class_maps.items():
                context_content[k] = v
        context['@context'] = context_content
        if output:
            with open(output, 'w') as outf:
                outf.write(as_json(context))
        else:
            print(as_json(context))

    def visit_class(self, cls: ClassDefinition) -> bool:
        class_def = {}
        cn = camelcase(cls.name)
        self.add_mappings(cls)
        cls_uri_prefix, cls_uri_suffix = self.namespaces.prefix_suffix(cls.class_uri)
        if not self.default_ns or not cls_uri_prefix or cls_uri_prefix != self.default_ns:
            class_def['@id'] = (cls_uri_prefix + ':' + cls_uri_suffix) if cls_uri_prefix else cls.class_uri
            if cls_uri_prefix:
                self.add_prefix(cls_uri_prefix)
        if class_def:
            self.slot_class_maps[cn] = class_def

        # We don't bother to visit class slots - just all slots
        return False

    def visit_slot(self, aliased_slot_name: str, slot: SlotDefinition) -> None:
        if slot.identifier:
            slot_def = '@id'
        else:
            slot_def = {}
            if not slot.usage_slot_name:
                if slot.range in self.schema.classes:
                    slot_def['@type'] = '@id'
                elif slot.range in self.schema.enums:
                    slot_def['@context'] = ENUM_CONTEXT
                    # Add the necessary prefixes to the namespace
                    skos = self.namespaces.prefix_for(SKOS)
                    if not skos:
                        self.namespaces['skos'] = SKOS
                        skos = 'skos'
                    self.emit_prefixes.add(skos)
                else:
                    range_type = self.schema.types[slot.range]
                    if self.namespaces.uri_for(range_type.uri) == XSD.string:
                        pass
                    elif self.namespaces.uri_for(range_type.uri) in URI_RANGES:
                        slot_def['@type'] = '@id'
                    else:
                        slot_def['@type'] = range_type.uri
                slot_prefix = self.namespaces.prefix_for(slot.slot_uri)
                if not self.default_ns or not slot_prefix or slot_prefix != self.default_ns:
                    slot_def['@id'] = slot.slot_uri
                    if slot_prefix:
                        self.add_prefix(slot_prefix)
                self.add_mappings(slot)
        if slot_def:
            self.context_body[underscore(aliased_slot_name)] = slot_def

@shared_arguments(ContextGenerator)
@click.command()
@click.option("--base", help="Base URI for model")
@click.option("--prefixes/--no-prefixes",  default=True, help="Emit context for prefixes (default=--prefixes)")
@click.option("--model/--no-model",  default=True, help="Emit context for model elements (default=--model)")
@click.option("--flatprefixes/--no-flatprefixes", default=False, help="Emit non-parsable prefixes as an object")
def cli(yamlfile, **args):
    """ Generate jsonld @context definition from LinkML model """
    print(ContextGenerator(yamlfile, **args).serialize(**args))


if __name__ == '__main__':
    cli()
