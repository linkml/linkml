""" Generate JSONld

"""
import logging
import os
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Optional

import click
from jsonasobj2 import as_json, items, loads
from linkml_runtime.linkml_model.meta import (ClassDefinition,
                                              ClassDefinitionName, ElementName,
                                              SchemaDefinition, SlotDefinition,
                                              SlotDefinitionName,
                                              SubsetDefinition,
                                              SubsetDefinitionName,
                                              TypeDefinition,
                                              TypeDefinitionName)
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.yamlutils import YAMLRoot

from linkml import METAMODEL_CONTEXT_URI
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.utils.generator import Generator, shared_arguments


@dataclass
class JSONLDGenerator(Generator):
    """
    Generates JSON-LD from a Schema

    Status: incompletely implemented

    Note: this is distinct from :ref:`ContextGenerator`, which generates a JSON-LD context
    """
    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.2"
    valid_formats = [
        "jsonld",
        "json",
    ]  # jsonld includes @type and @context.  json is pure JSON
    uses_schemaloader = True
    requires_metamodel = True

    # ObjectVars
    original_schema: SchemaDefinition = None
    """See https://github.com/linkml/linkml/issues/871"""

    context: str = None
    """Path to a JSONLD context file"""

    def __post_init__(self) -> None:
        super().__post_init__()
        self.original_schema = deepcopy(self.schema)

    def _add_type(self, node: YAMLRoot) -> dict:
        if self.format == "jsonld":
            typ = node.__class__.__name__
            node = node.__dict__
            node["@type"] = typ
        return node

    def _visit(self, node: Any) -> Optional[Any]:
        if isinstance(node, (YAMLRoot, dict)):
            if isinstance(node, YAMLRoot):
                node = self._add_type(node)
            for k, v in list(items(node)):
                if v:
                    new_v = self._visit(v)
                    if new_v is not None:
                        node[k] = new_v
        elif isinstance(node, list):
            for i in range(0, len(node)):
                new_v = self._visit(node[i])
                if new_v is not None:
                    node[i] = new_v
        elif isinstance(node, set):
            for v in list(node):
                new_v = self._visit(v)
                if new_v is not None:
                    node.remove(v)
                    node.add(new_v)
        elif isinstance(node, ClassDefinitionName):
            return ClassDefinitionName(camelcase(node))
        elif isinstance(node, SlotDefinitionName):
            return SlotDefinitionName(underscore(node))
        elif isinstance(node, TypeDefinitionName):
            return TypeDefinitionName(underscore(node))
        elif isinstance(node, SubsetDefinitionName):
            return SubsetDefinitionName(underscore(node))
        elif isinstance(node, ElementName):
            return (
                ClassDefinitionName(camelcase(node))
                if node in self.schema.classes
                else SlotDefinitionName(underscore(node))
                if node in self.schema.slots
                else SubsetDefinitionName(camelcase(node))
                if node in self.schema.subsets
                else TypeDefinitionName(underscore(node))
                if node in self.schema.types
                else None
            )
        return None

    def adjust_slot(self, slot: SlotDefinition) -> None:
        if slot.range in self.schema.classes:
            slot.range = ClassDefinitionName(camelcase(slot.range))
        elif slot.range in self.schema.slots:
            slot.range = SlotDefinitionName(underscore(slot.range))
        elif slot.range in self.schema.types:
            slot.range = TypeDefinitionName(underscore(slot.range))
        slot.slot_uri = self.namespaces.uri_for(slot.slot_uri)
        for f in [
            "mappings",
            "exact_mappings",
            "broad_mappings",
            "close_mappings",
            "narrow_mappings",
            "related_mappings",
        ]:
            setattr(slot, f, [self.namespaces.uri_for(v) for v in getattr(slot, f)])

    def visit_class(self, cls: ClassDefinition) -> bool:
        self._visit(cls)
        cls.class_uri = self.namespaces.uri_for(cls.class_uri)
        # Slot usage is a construction artifact
        # TODO: Figure out why this is here.  It isn't good form to alter a schema that may be used by other things
        cls.slot_usage = {}
        return False

    def visit_slot(self, aliased_slot_name: str, slot: SlotDefinition) -> None:
        self._visit(slot)
        self.adjust_slot(slot)

    def visit_type(self, typ: TypeDefinition) -> None:
        self._visit(typ)
        typ.uri = self.namespaces.uri_for(typ.uri)

    def visit_subset(self, ss: SubsetDefinition) -> None:
        self._visit(ss)

    def end_schema(self, context: str = None, **_) -> None:
        self._add_type(self.schema)
        base_prefix = self.default_prefix()

        # TODO: fix this, see https://github.com/linkml/linkml/issues/871
        # JSON LD adjusts context reference using '@base'.  If context is supplied and not a URI, generate an
        # absolute URI for it
        if context is None and self.format == "jsonld":
            # TODO: Once we get pyld running w/ relative contexts, we need to figure out how to generate and add
            #       the relative (?) context reference below
            # model_context = self.schema.source_file.replace('.yaml', '.prefixes.context.jsonld')
            # context = [METAMODEL_CONTEXT_URI, f'file://./{model_context}']
            # TODO: The _visit function above alters the schema in situ
            add_prefixes = ContextGenerator(
                self.original_schema, model=False, metadata=False
            ).serialize()
            add_prefixes_json = loads(add_prefixes)
            context = [METAMODEL_CONTEXT_URI, add_prefixes_json["@context"]]
        elif isinstance(
            context, str
        ):  # Some of the older code doesn't do multiple contexts
            context = [context]
        elif isinstance(context, tuple):
            context = list(context)
        for imp in list(self.loaded.values())[1:]:
            context.append(imp[0] + ".context.jsonld")

        # Absolute file paths have to have a prefix
        for ci in range(0, len(context)):
            if isinstance(context[ci], str) and context[ci].startswith(
                "/"
            ):  # TODO: how do we deal with absolute DOS paths?
                context[ci] = "file://" + context[ci]

        if self.format == "jsonld":
            self.schema["@context"] = (
                context[0] if len(context) == 1 and not base_prefix else context
            )
            if base_prefix:
                self.schema["@context"].append({"@base": base_prefix})
        # json_obj["@id"] = self.schema.id
        print(as_json(self.schema, indent="  "))
        self.schema = self.original_schema


@shared_arguments(JSONLDGenerator)
@click.command()
@click.option(
    "--context",
    multiple=True,
    help=f"JSONLD context file (default: {METAMODEL_CONTEXT_URI} and <model>.prefixes.context.jsonld)",
)
def cli(yamlfile, **kwargs):
    """Generate JSONLD file from LinkML schema.

    Status: incomplete
    """
    print(JSONLDGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
