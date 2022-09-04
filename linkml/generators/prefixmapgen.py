"""
Generate JSON-LD contexts

"""
import csv
import logging
import os
from dataclasses import dataclass, field
from typing import Dict, Mapping, Optional, Set, TextIO, Union

import click
from jsonasobj2 import JsonObj, as_json
from linkml_runtime.linkml_model.meta import (ClassDefinition, Definition,
                                              Element, SchemaDefinition,
                                              SlotDefinition)
from linkml_runtime.linkml_model.types import SHEX
from linkml_runtime.utils.formatutils import be, camelcase, underscore
from rdflib import XSD

from linkml.utils.generator import Generator, shared_arguments

URI_RANGES = (XSD.anyURI, SHEX.nonliteral, SHEX.bnode, SHEX.iri)


@dataclass
class PrefixGenerator(Generator):

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ["json", "tsv"]
    visit_all_class_slots = False
    uses_schemaloader = True

    # ObjectVars
    emit_prefixes: Set[str] = field(default_factory=lambda: set())
    default_ns: str = None
    context_body: Dict = field(default_factory=lambda: dict())
    slot_class_maps: Dict = field(default_factory=lambda: dict())
    base: str = None

    def __post_init__(self):
        super().__post_init__()
        if self.namespaces is None:
            raise TypeError(
                "Schema text must be supplied to context generater.  Preparsed schema will not work"
            )

    def visit_schema(
        self, base: Optional[str] = None, output: Optional[str] = None, **_
    ):
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

    def end_schema(
        self, base: Optional[str] = None, output: Optional[str] = None, **_
    ) -> None:
        context = JsonObj()
        if base:
            if "://" not in base:
                self.context_body["@base"] = os.path.relpath(
                    base, os.path.dirname(self.schema.source_file)
                )
            else:
                self.context_body["@base"] = base
        for prefix in sorted(self.emit_prefixes):
            context[prefix] = self.namespaces[prefix]
        for k, v in self.context_body.items():
            context[k] = v
        for k, v in self.slot_class_maps.items():
            context[k] = v

        if output:
            output_ext = output.split(".")[-1]

            if output_ext == "tsv":
                mapping: Dict = {}
                for prefix in sorted(self.emit_prefixes):
                    mapping[prefix] = self.namespaces[prefix]

                with open(output, "w", encoding="UTF-8") as outf:
                    writer = csv.writer(outf, delimiter="\t")
                    for key, value in mapping.items():
                        writer.writerow([key, value])
            else:
                with open(output, "w", encoding="UTF-8") as outf:
                    outf.write(as_json(context))
        else:
            if self.format == "tsv":
                mapping: Dict = {}  # prefix to IRI mapping
                for prefix in sorted(self.emit_prefixes):
                    mapping[prefix] = self.namespaces[prefix]

                for key, value in mapping.items():
                    print(key, value, sep="\t")
            else:
                print(as_json(context))

    def visit_class(self, cls: ClassDefinition) -> bool:
        class_def = {}
        cn = camelcase(cls.name)
        self.add_mappings(cls)
        cls_prefix = self.namespaces.prefix_for(cls.class_uri)
        if not self.default_ns or not cls_prefix or cls_prefix != self.default_ns:
            class_def["@id"] = cls.class_uri
            if cls_prefix:
                self.add_prefix(cls_prefix)
        if class_def:
            self.slot_class_maps[cn] = class_def

        # We don't bother to visit class slots - just all slots
        return False

    def visit_slot(self, aliased_slot_name: str, slot: SlotDefinition) -> None:
        self.add_mappings(slot)


@shared_arguments(PrefixGenerator)
@click.command()
@click.option("--base", help="Base URI for model")
@click.option("--output", "-o", help="Output file path")
def cli(yamlfile, **args):
    """Generate jsonld @context definition from LinkML model"""
    print(PrefixGenerator(yamlfile, **args).serialize(**args))
