"""
Generate JSON-LD contexts

"""
import logging
import os
from typing import Union, TextIO, Set, Optional

import click
from jsonasobj2 import JsonObj, as_json
from rdflib import XSD

from linkml_model.meta import SchemaDefinition, ClassDefinition, SlotDefinition, Definition, Element
from linkml_runtime.utils.formatutils import camelcase, underscore, be
from linkml.utils.generator import Generator, shared_arguments
from linkml_model.types import SHEX

URI_RANGES = (XSD.anyURI, SHEX.nonliteral, SHEX.bnode, SHEX.iri)


class PrefixGenerator(Generator):
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ['json']
    visit_all_class_slots = False

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], **kwargs) -> None:
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
                self.emit_prefixes.add(self.default_ns)

    def end_schema(self, base: Optional[str] = None, output: Optional[str] = None, **_) -> None:

        context = JsonObj()
        if base:
            if '://' not in base:
                self.context_body['@base'] = os.path.relpath(base, os.path.dirname(self.schema.source_file))
            else:
                self.context_body['@base'] = base
        for prefix in sorted(self.emit_prefixes):
            context[prefix] = self.namespaces[prefix]
        for k, v in self.context_body.items():
            context[k] = v
        for k, v in self.slot_class_maps.items():
            context[k] = v
        if output:
            with open(output, 'w') as outf:
                outf.write(as_json(context))
        else:
            print(as_json(context))

    def visit_class(self, cls: ClassDefinition) -> bool:
        class_def = {}
        cn = camelcase(cls.name)
        self.add_mappings(cls)
        cls_prefix = self.namespaces.prefix_for(cls.class_uri)
        if not self.default_ns or not cls_prefix or cls_prefix != self.default_ns:
            class_def['@id'] = cls.class_uri
            if cls_prefix:
                self.add_prefix(cls_prefix)
        if class_def:
            self.slot_class_maps[cn] = class_def

        # We don't bother to visit class slots - just all slots
        return False

    def add_prefix(self, ncname: str) -> None:
        """ Add a prefix to the list of prefixes to emit

        @param ncname: name to add
        """
        if ncname not in self.namespaces:
            self.logger.warning(f"Unrecognized prefix: {ncname}")
            self.namespaces[ncname] = f"http://example.org/UNKNOWN/{ncname}/"
        self.emit_prefixes.add(ncname)

    def add_mappings(self, defn: Definition) -> None:
        """
        Process any mappings in defn, adding all of the mappings prefixes to the namespace map
        :param defn: Class or Slot Definition
        """
        self.add_id_prefixes(defn)
        for mapping in defn.mappings:
            if '://' in mapping:
                mcurie = self.namespaces.curie_for(mapping)
                self.logger.warning(f"No namespace defined for URI: {mapping}")
                if mcurie is None:
                    return        # Absolute path - no prefix/name
                else:
                    mapping = mcurie
            if ':' not in mapping or len(mapping.split(':')) != 2:
                raise ValueError(f"Definition {defn.name} - unrecognized mapping: {mapping}")
            ns = mapping.split(':')[0]
            self.add_prefix(ns)

    def add_id_prefixes(self, element: Element) -> None:
        for id_prefix in element.id_prefixes:
            self.add_prefix(id_prefix)


@shared_arguments(PrefixGenerator)
@click.command()
@click.option("--base", help="Base URI for model")
def cli(yamlfile, **args):
    """ Generate jsonld @context definition from biolink model """
    print(PrefixGenerator(yamlfile, **args).serialize(**args))
