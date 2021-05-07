""" Generate JSONld

"""
import os
from typing import Any, Optional

import click
from jsonasobj2 import as_json

from linkml import METAMODEL_CONTEXT_URI
from linkml_model.meta import ClassDefinitionName, SlotDefinitionName, TypeDefinitionName, \
    ElementName, SlotDefinition, ClassDefinition, TypeDefinition, SubsetDefinitionName, SubsetDefinition
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.utils.yamlutils import YAMLRoot

from linkml.utils.migration_temp import is_YAMLROOT


class JSONLDGenerator(Generator):
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.2"
    valid_formats = ['jsonld']

    def _add_type(self, node: YAMLRoot) -> dict:
        typ = node.__class__.__name__
        node = node.__dict__
        node['@type'] = typ
        return node

    def _visit(self, node: Any) -> Optional[Any]:
        if isinstance(node, (YAMLRoot, dict)) or is_YAMLROOT(node):
            if isinstance(node, YAMLRoot) or is_YAMLROOT(node):
                node = self._add_type(node)
            for k, v in list(node.items()):
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
            return ClassDefinitionName(camelcase(node)) if node in self.schema.classes else \
                SlotDefinitionName(underscore(node)) if node in self.schema.slots else \
                SubsetDefinitionName(camelcase(node)) if node in self.schema.subsets else \
                TypeDefinitionName(underscore(node)) if node in self.schema.types else None
        return None

    def adjust_slot(self, slot: SlotDefinition) -> None:
        if slot.range in self.schema.classes:
            slot.range = ClassDefinitionName(camelcase(slot.range))
        elif slot.range in self.schema.slots:
            slot.range = SlotDefinitionName(underscore(slot.range))
        elif slot.range in self.schema.types:
            slot.range = TypeDefinitionName(underscore(slot.range))
        slot.slot_uri = self.namespaces.uri_for(slot.slot_uri)

    def visit_class(self, cls: ClassDefinition) -> bool:
        self._visit(cls)
        cls.class_uri = self.namespaces.uri_for(cls.class_uri)
        # Slot usage is a construction artifact
        cls.slot_usage = []
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
        json_obj = self.schema
        base_prefix = self.default_prefix()

        # JSON LD adjusts context reference using '@base'.  If context is supplied and not a URI, generate an
        # absolute URI for it
        if context is None:
            context = [METAMODEL_CONTEXT_URI]
        elif isinstance(context, str):               # Some of the older code doesn't do multiple contexts
            context = [context]
        elif isinstance(context, tuple):
            context = list(context)
        for imp in list(self.loaded.values())[1:]:
            context.append(imp[0] + ".context.jsonld")

        # Absolute file paths have to have a prefix
        for ci in range(0, len(context)):
            if context[ci].startswith('/'):           # TODO: how do we deal with absolute DOS paths?
                context[ci] = 'file://' + context[ci]

        json_obj["@context"] = [context[0] if len(context) == 1 and not base_prefix else context]
        if base_prefix:
            json_obj["@context"].append({'@base': base_prefix})
        # json_obj["@id"] = self.schema.id
        print(as_json(json_obj, indent="  "))


@shared_arguments(JSONLDGenerator)
@click.command()
@click.option("--context", default=[METAMODEL_CONTEXT_URI], multiple=True,
              help=f"JSONLD context file (default: {METAMODEL_CONTEXT_URI})")
def cli(yamlfile, **kwargs):
    """ Generate JSONLD file from biolink schema """
    print(JSONLDGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == '__main__':
    cli()
