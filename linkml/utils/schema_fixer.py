import re
import logging
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Callable

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.linkml_model import SchemaDefinition, ClassDefinition, ClassDefinitionName, SlotDefinition


pattern = re.compile(r'(?<!^)(?=[A-Z])')

def uncamel(n: str) -> str:
    return pattern.sub(' ', n)


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
            title = e.name.replace('_', ' ')
            title = uncamel(title).lower()
            e.title = title
            self._add_history(f'added title {title} to {e.name}')


    def add_container(self, schema: SchemaDefinition, class_name: str = 'Container',
                      force: bool = False, **kwargs) -> ClassDefinition:
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
                logging.info(f'Forcing addition of containers')
            else:
                raise ValueError(f'Schema already has containers: {tree_roots}')
        container = ClassDefinition(class_name, tree_root=True)
        sv.add_class(container)
        self._add_history(f'added container {container.name}')
        self.add_index_slots(schema, container.name, **kwargs)
        return container


    def add_index_slots(self, schema: SchemaDefinition, container_name: ClassDefinitionName, inlined_as_list = False,
                        must_have_identifier=False, slot_name_func: Callable = None, convert_camel_case=False) -> List[SlotDefinition]:
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
                cn = cn.replace(' ', '_')
                sn = f'{cn}_index'
            index_slot = SlotDefinition(sn,
                                        range=c.name,
                                        multivalued=True,
                                        inlined_as_list=not has_identifier or inlined_as_list)
            index_slots.append(index_slot)
            schema.slots[index_slot.name] = index_slot
            container.slots.append(index_slot.name)
            self._add_history(f'Adding container slot: {index_slot.name}')
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
                raise ValueError(f'Duplicate slot {slot.name}')
            sv.add_slot(slot)
            self._add_history(f'Adding slot from attribute: {slot.name}')
        if remove_redundant_slot_usage:
            self.remove_redundant_slot_usage(schema)

    def merge_slot_usage(self, sv: SchemaView, cls: ClassDefinition, slot: SlotDefinition, overwrite=False):
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
                        raise ValueError(f'Conflict in {cls.name}.{slot.name}, attr {k} {v} != {curr_v}')
                    setattr(su, k, v)
            self._add_history(f'Merged slot usage: {slot.name}')

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
            for sn, slot in cls.slot_usage.items():
                del cls.slot_usage[sn]
                sv.set_modified()
                induced_slot = sv.induced_slot(sn, class_name)
                cls.slot_usage[sn] = slot
                sv.set_modified()
                to_delete = []
                for metaslot_name, metaslot in vars(slot).items():
                    if metaslot_name == 'name':
                        continue
                    v = getattr(slot, metaslot_name, None)
                    induced_v = getattr(induced_slot, metaslot_name, None)
                    if v is not None and v != [] and v != {} and v == induced_v:
                        logging.info(f'REDUNDANT: {class_name}.{sn}[{metaslot_name}] = {v}')
                        to_delete.append(metaslot_name)
                for metaslot_name in to_delete:
                    del slot[metaslot_name]
                    self._add_history(f'Removed redundant: {class_name}.slot_usage[{sn}].[{metaslot_name}]')
            empty_keys = []
            for sn, slot in cls.slot_usage.items():
                metaslot_keys = list(json_dumper.to_dict(slot).keys())
                if metaslot_keys == [] or metaslot_keys == ['name']:
                    empty_keys.append(sn)
            for k in empty_keys:
                del cls.slot_usage[k]


    def remove_unused_prefixes(self, schema: SchemaDefinition):
        raise NotImplementedError

    def _add_history(self, txt: str):
        if self.history is None:
            self.history = []
        self.history.append(txt)
