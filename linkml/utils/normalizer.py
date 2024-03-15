from copy import copy
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, List

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import SlotDefinitionName, ClassDefinitionName
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.yamlutils import YAMLRoot




@lru_cache()
def class_slots_ordered(sv: SchemaView, class_name: str) -> List[SlotDefinitionName]:
    seed = [class_name]
    slot_names = []
    visited = []
    print(f'ANC: {class_name}')
    while len(seed) > 0:
        ix = 0
        while ix < len(seed):
            if sv.get_class(seed[ix]).mixin:
                break
            ix += 1
        if ix == len(seed):
            # no mixin: process next class
            ix = 0
        cn = seed[ix]
        del seed[ix]
        print(f'  NEXT: {cn}')
        if cn in visited:
            continue
        c = sv.get_class(cn)
        this_slot_names = c.slots + list(c.attributes.keys())
        print(f'    THIS SNs: {this_slot_names}')
        slot_names = this_slot_names + slot_names
        seed = c.mixins + seed
        if c.is_a:
            seed.append(c.is_a)
        visited.append(cn)
    print(f'FINAL1: {slot_names}')
    slot_names = list(dict.fromkeys(slot_names))
    print(f'FINAL: {slot_names}')
    return slot_names




@dataclass
class DataNormalizer:
    schemaview: SchemaView
    _alias_map: Dict[str, str] = None

    def as_normalized_obj(self, obj: Any):
        """
        TODO: this method doesn't currently work as ordering is determined by __post_init__

        :param obj:
        :return:
        """
        typ = type(obj)
        return typ(**self.as_normalized_dict(obj))

    def alias_map(self):
        if self._alias_map is not None:
            return self._alias_map
        sv = self.schemaview
        snm = sv.slot_name_mappings()
        snm_inv = {}
        for k, v in snm.items():
            alias = v.alias if v.alias else v.name
            alias = underscore(alias)
            snm_inv[alias] = k
        self._alias_map = snm_inv
        return snm_inv

    def as_normalized_dict(self, obj: Any) -> Any:
        """
        TODO: for this to work we need to be able to specify
        traversal order for class_induced_slots
        :param obj:
        :return:
        """
        sv = self.schemaview
        cnm = sv.class_name_mappings()
        snm = sv.slot_name_mappings()
        snm_inv = self.alias_map()
        typ = type(obj)
        if isinstance(obj, YAMLRoot):
            cn = typ.class_name
            cls = sv.get_class(cn)
            nu_dict = {}
            for slot_name in class_slots_ordered(sv, cls.name):
                slot = sv.induced_slot(slot_name, cls.name)
                att_name = snm_inv[slot.alias]
                v = getattr(obj, att_name, None)
                if v is not None:
                    v2 = self.as_normalized_dict(v)
                    nu_dict[att_name] = v2
            return nu_dict
        elif isinstance(obj, list):
            return [self.as_normalized_dict(x) for x in obj]
        elif isinstance(obj, dict):
            return {k: self.as_normalized_dict(v) for k, v in obj.items()}
        else:
            return obj

