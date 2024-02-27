import logging
import re
from collections import defaultdict
from copy import copy
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union

import click
import yaml
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.linkml_model import (
    ClassDefinition,
    ClassDefinitionName,
    EnumDefinition,
    SchemaDefinition,
    SlotDefinition,
    TypeDefinition,
)
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.yamlutils import YAMLRoot

logger = logging.getLogger(__name__)

pattern = re.compile(r"(?<!^)(?=[A-Z])")


def yaml_rewrite(obj: Any, replacements: Dict[str, Any], include_keys=True) -> Any:
    if isinstance(obj, YAMLRoot):
        obj2 = copy(obj)
        for k, v in vars(obj).items():
            setattr(obj2, k, yaml_rewrite(v, replacements, include_keys))
        return obj2
    if isinstance(obj, dict):
        if include_keys and set(obj.keys()).intersection(replacements):
            obj = {replacements.get(k, k): v for k, v in obj.items()}
        return {k: yaml_rewrite(v, replacements, include_keys) for k, v in obj.items()}
    if isinstance(obj, list):
        return [yaml_rewrite(v, replacements, include_keys) for v in obj]
    if isinstance(obj, str) and obj in replacements:
        return replacements.get(obj)
    return obj


def uncamel(n: str) -> str:
    return pattern.sub(" ", n)


@dataclass
class SchemaFixer:
    """
    Multiple methods for adding additional information to schemas
    """

    history: List[str] = None

    def add_titles(self, schema: SchemaDefinition):
        """
        Add titles to all elements if not present.

        Title will be generated from the name, expanding CamelCase => Camel Case,
        and replacing underscores with spaces.

        :param schema: input schema, will be modified in place
        :return:
        """
        sv = SchemaView(schema)
        for e in sv.all_elements().values():
            if e.title is not None:
                continue
            title = e.name.replace("_", " ")
            title = uncamel(title).lower()
            e.title = title
            self._add_history(f"added title {title} to {e.name}")

    def add_container(
        self,
        schema: SchemaDefinition,
        class_name: str = "Container",
        force: bool = False,
        **kwargs,
    ) -> ClassDefinition:
        """
        Adds a container class

        Also wraps :ref:`add_index_slots`

        :param schema: input schema, will be modified in place
        :param class_name: name for container
        :param force: if true, force adding a container, even if present
        :return: container class
        """
        sv = SchemaView(schema)
        tree_roots = [c for c in sv.all_classes().values() if c.tree_root]
        if len(tree_roots) > 0:
            if force:
                logging.info("Forcing addition of containers")
            else:
                raise ValueError(f"Schema already has containers: {tree_roots}")
        container = ClassDefinition(class_name, tree_root=True)
        sv.add_class(container)
        self._add_history(f"added container {container.name}")
        self.add_index_slots(schema, container.name, **kwargs)
        return container

    def add_index_slots(
        self,
        schema: SchemaDefinition,
        container_name: ClassDefinitionName,
        inlined_as_list=False,
        must_have_identifier=False,
        slot_name_func: Callable = None,
        convert_camel_case=False,
    ) -> List[SlotDefinition]:
        """
        Adds index slots to a container pointing at all top-level classes

        :param schema: input schema, will be modified in place
        :param container_name:
        :param inlined_as_list:
        :param must_have_identifier:
        :param slot_name_func: function to determine the name of the slot from the class
        :return: new slots
        """
        sv = SchemaView(schema)
        container = sv.get_class(container_name)
        ranges = set()
        for cn in sv.all_classes():
            for s in sv.class_induced_slots(cn):
                ranges.add(s.range)
        top_level_classes = [c for c in sv.all_classes().values() if not c.tree_root and c.name not in ranges]
        if must_have_identifier:
            top_level_classes = [c for c in top_level_classes if sv.get_identifier_slot(c.name) is not None]
        index_slots = []
        for c in top_level_classes:
            has_identifier = sv.get_identifier_slot(c.name)
            if slot_name_func:
                sn = slot_name_func(c)
            else:
                cn = c.name
                if convert_camel_case:
                    cn = uncamel(cn).lower()
                cn = cn.replace(" ", "_")
                sn = f"{cn}_index"
            index_slot = SlotDefinition(
                sn,
                range=c.name,
                multivalued=True,
                inlined_as_list=not has_identifier or inlined_as_list,
            )
            index_slots.append(index_slot)
            schema.slots[index_slot.name] = index_slot
            container.slots.append(index_slot.name)
            self._add_history(f"Adding container slot: {index_slot.name}")
        return index_slots

    def attributes_to_slots(self, schema: SchemaDefinition, remove_redundant_slot_usage=True) -> None:
        """
        Convert all attributes to slots

        :param schema:
        :param remove_redundant_slot_usage:
        :return:
        """
        sv = SchemaView(schema)
        new_slots = []
        for c in sv.all_classes().values():
            for a in c.attributes:
                new_slots.append(a)
                self.merge_slot_usage(sv, c, a)
                del c.attributes[a.name]
        for slot in new_slots:
            if slot.name in sv.all_slots():
                raise ValueError(f"Duplicate slot {slot.name}")
            sv.add_slot(slot)
            self._add_history(f"Adding slot from attribute: {slot.name}")
        if remove_redundant_slot_usage:
            self.remove_redundant_slot_usage(schema)

    def merge_slot_usage(
        self,
        sv: SchemaView,
        cls: ClassDefinition,
        slot: SlotDefinition,
        overwrite=False,
    ):
        """
        Merge a SlotDefinition into the class_usage for a class

        If the class has no slot usage defined for that slot, then the class usage
        will be set to the input slot

        otherwise, each metaslot will be individually merged

        :param sv:
        :param cls:
        :param slot:
        :param overwrite: if True then overwrite conflicting values rather than raising error
        :return:
        """
        if slot.name not in cls.slot_usage:
            cls.slot_usage[slot.name] = slot
        else:
            su = cls.slot_usage[slot.name]
            for k, v in vars(slot).items():
                if v is not None and v != [] and v != {}:
                    curr_v = getattr(su, k, None)
                    if not overwrite and curr_v and curr_v != v:
                        raise ValueError(f"Conflict in {cls.name}.{slot.name}, attr {k} {v} != {curr_v}")
                    setattr(su, k, v)
            self._add_history(f"Merged slot usage: {slot.name}")

    def remove_redundant_slot_usage(self, schema: SchemaDefinition, class_name: ClassDefinitionName = None):
        """
        Remove parts of slot_usage that can be inferred

        :param schema:
        :param class_name:
        :return:
        """
        sv = SchemaView(schema)
        if class_name is None:
            for class_name in sv.all_classes():
                self.remove_redundant_slot_usage(schema, class_name)
        else:
            cls = sv.get_class(class_name)
            # test every key-value pair in the slot usage to determine which
            # slots within that are redundant
            slot_usage_keys = list(cls.slot_usage.keys())
            for slot_usage_key in slot_usage_keys:
                logging.debug(f"TESTING: {class_name}.{slot_usage_key}")
                slot_usage_value = cls.slot_usage[slot_usage_key]
                # perform a deletion test: what can be retrieved by inference
                del cls.slot_usage[slot_usage_key]
                sv.set_modified()
                try:
                    induced_slot = sv.induced_slot(slot_usage_key, class_name)
                except ValueError:
                    logging.warning(f"slot_usage with no slot: {slot_usage_key}")
                    continue
                # restore value
                cls.slot_usage[slot_usage_key] = slot_usage_value
                sv.set_modified()
                to_delete = []
                for metaslot_name, metaslot in vars(slot_usage_value).items():
                    if metaslot_name == "name":
                        # redundant with key
                        to_delete.append(metaslot_name)
                        continue
                    if metaslot_name in ["from_schema", "owner", "domain_of", "definition_uri"]:
                        # metamodel readonly slots are redundant by definition
                        to_delete.append(metaslot_name)
                        continue
                    v = getattr(slot_usage_value, metaslot_name, None)
                    if isinstance(v, bool) and not v:
                        # booleans with value False are inherently redundant
                        to_delete.append(metaslot_name)
                        continue
                    induced_v = getattr(induced_slot, metaslot_name, None)
                    if v is not None and v != [] and v != {} and v == induced_v:
                        logging.info(f"REDUNDANT: {class_name}.{slot_usage_key}[{metaslot_name}] = {v}")
                        to_delete.append(metaslot_name)
                for metaslot_name in to_delete:
                    del slot_usage_value[metaslot_name]
                    self._add_history(f"Removed redundant: {class_name}.slot_usage[{slot_usage_key}].[{metaslot_name}]")
            empty_keys = []
            for slot_usage_key, slot_usage_value in cls.slot_usage.items():
                metaslot_keys = list(json_dumper.to_dict(slot_usage_value).keys())
                if metaslot_keys == [] or metaslot_keys == ["name"]:
                    empty_keys.append(slot_usage_key)
            for k in empty_keys:
                del cls.slot_usage[k]

    @staticmethod
    def implicit_slots(schema: SchemaDefinition) -> Dict[str, Dict]:
        """
        Find slots that are implicit in the schema from slot_usage

        :param schema:
        :return:
        """
        sv = SchemaView(schema)
        implicit_slots1 = defaultdict(list)
        for cls in sv.all_classes().values():
            for slot in cls.slot_usage.values():
                slot_name = slot.name
                if slot_name not in sv.all_slots():
                    implicit_slots1[slot_name].append(json_dumper.to_dict(slot))
        new_slots = {}
        for slot_name, slot_list in implicit_slots1.items():
            all_keys = set()
            for slot in slot_list:
                all_keys.update(slot.keys())
            harmonized_slot = {}
            for k in all_keys:
                vals = []
                vals_strs = set()
                for slot in slot_list:
                    val = slot.get(k, None)
                    vals_strs.add(str(val))
                    vals.append(val)
                if len(vals_strs) == 1:
                    harmonized_slot[k] = vals.pop()
                elif len(vals_strs) > 1:
                    logging.info(f"Variable values in {slot_name}.{k}: {vals_strs}")
            new_slots[str(slot_name)] = harmonized_slot
        return new_slots

    def remove_unused_prefixes(self, schema: SchemaDefinition):
        raise NotImplementedError

    def _add_history(self, txt: str):
        if self.history is None:
            self.history = []
        self.history.append(txt)

    @staticmethod
    def fix_element_names(
        schema: SchemaDefinition,
        schema_dict: Dict[str, Any] = None,
        rules: Dict[str, Callable] = None,
        imports=False,
        preserve_original_using: Optional[str] = None,
    ) -> Union[YAMLRoot, Dict]:
        """
        Changes element names to conform to naming conventions.

        :param schema: input schema
        :param schema_dict: if specified, the transformation will happen on this dictionary object
        :param rules: mappings between index slots and functions that normalize names
        :param imports: if True, all that imported modules are also fixed
        :param preserve_original_using: if specified, the original name will be preserved in this slot
        :return:
        """
        if rules is None:
            rules = {
                ClassDefinition.__name__: camelcase,
                TypeDefinition.__name__: camelcase,
                SlotDefinition.__name__: underscore,
                EnumDefinition.__name__: camelcase,
            }
        fixes = {}
        sv = SchemaView(schema)
        preserved = []
        for n, e in sv.all_elements(imports=imports).items():
            if e.from_schema == "https://w3id.org/linkml/types":
                continue
            typ = type(e).__name__
            if typ in rules:
                func = rules[typ]
                normalized = func(n)
                if normalized != n:
                    fixes[n] = normalized
                if preserve_original_using is not None:
                    preserved.append((typ, normalized, n))
                # if preserve_original_using is not None:
                #    setattr(e, preserve_original_using, n)
                #    print(f"SETTING {typ} {e.name}.{preserve_original_using} = {n}")
        if schema_dict is not None:
            schema = schema_dict
        schema = yaml_rewrite(schema, fixes)
        for typ, normalized, original in preserved:
            pathmap = {
                ClassDefinition.__name__: "classes",
                TypeDefinition.__name__: "types",
                SlotDefinition.__name__: "slots",
                EnumDefinition.__name__: "enums",
            }
            if isinstance(schema, dict):
                path = schema[pathmap[typ]]
                if normalized not in path:
                    logger.warning(f"Cannot find {typ} {normalized} in {pathmap[typ]}")
                    continue
                e = path[normalized]
                if preserve_original_using not in e:
                    path[normalized][preserve_original_using] = original
            else:
                path = getattr(schema, pathmap[typ])
                e = path[normalized]
                if not getattr(e, preserve_original_using, None):
                    setattr(e, preserve_original_using, original)
        return schema


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
def main(verbose: int, quiet: bool):
    """Apply schema-fixer commands."""
    if verbose >= 2:
        logger.setLevel(level=logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)
    if quiet:
        logger.setLevel(level=logging.ERROR)


@main.command()
@click.argument("input_schema")
@click.option(
    "--imports/--no-imports",
    default=False,
    show_default=True,
    help="Apply fix to referenced elements from modules",
)
@click.option(
    "--preserve-original-using",
    "-P",
    default=None,
    show_default=True,
    help="If specified, original name will be preserved in this slot (e.g. title)",
)
def fix_names(input_schema, **kwargs):
    """Fix element names to conform to naming conventions"""
    with open(input_schema) as f:
        schema_dict = yaml.safe_load(f)
    sv = SchemaView(input_schema)
    fixer = SchemaFixer()
    schema = fixer.fix_element_names(sv.schema, schema_dict, **kwargs)
    print(yaml.dump(schema, sort_keys=False))


@main.command()
@click.argument("input_schema")
@click.option(
    "--imports/--no-imports",
    default=False,
    show_default=True,
    help="Apply fix to referenced elements from modules",
)
def implicit_slots(input_schema, **kwargs):
    """Find implicit slots in schema"""
    with open(input_schema) as f:
        yaml.safe_load(f)
    sv = SchemaView(input_schema)
    fixer = SchemaFixer()
    slots = fixer.implicit_slots(sv.schema)
    for slot in slots.values():
        del slot["name"]
    print(yaml.dump({"slots": slots}, sort_keys=False))


if __name__ == "__main__":
    main()
