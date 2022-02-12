import logging
from dataclasses import field, dataclass
from enum import Enum
from typing import Union, Optional, Any, Dict
from jsonasobj2 import JsonObj, items

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import SlotDefinitionName, PermissibleValue
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.eval_utils import eval_expr
from linkml_runtime.utils.walker_utils import traverse_object_tree
from linkml_runtime.utils.yamlutils import YAMLRoot


def obj_as_dict_nonrecursive(obj: YAMLRoot) -> Dict[str, Any]:
    return {k: v for k, v in items(obj)}


@dataclass
class Config:
    """
    Controls which inferences are performed
    """
    use_string_serialization: bool = field(default_factory=lambda: True)
    use_rules: bool = field(default_factory=lambda: False)
    use_expressions: bool = field(default_factory=lambda: False)


class Policy(Enum):
    """
    Policy for when inferred values differ from already set values
    """
    STRICT = "strict"
    OVERRIDE = "override"
    KEEP = "keep"


def generate_slot_value(obj: YAMLRoot, slot_name: Union[str, SlotDefinitionName], schemaview: SchemaView,
                        config: Config = Config()) -> Optional[Any]:
    """
    Infer the value of a slot for a given object

    :param obj: (not mutated)
    :param slot_name:
    :param schemaview:
    :param config:
    :return: inferred value, or None if not inference performed
    """
    cls_name = type(obj).class_name
    slot = schemaview.induced_slot(slot_name, cls_name)
    logging.debug(f'   CONF={config}')
    if config.use_string_serialization:
        if slot.string_serialization:
            if isinstance(obj, JsonObj):
                return slot.string_serialization.format(**obj_as_dict_nonrecursive(obj))
    if config.use_expressions:
        if slot.equals_expression:
            if isinstance(obj, JsonObj):
                return eval_expr(slot.equals_expression, **obj_as_dict_nonrecursive(obj))
    if config.use_rules:
        raise NotImplementedError(f'Rules not implemented for {config}')
    return None


def infer_slot_value(obj: YAMLRoot, slot_name: Union[str, SlotDefinitionName], schemaview: SchemaView,
                       policy: Policy = Policy.STRICT, config: Config = Config()):
    """
    Infer the value of a slot for an object

    :param obj: mutable object to be transformed
    :param slot_name:
    :param schemaview:
    :param policy:
    :param config:
    """
    v = getattr(obj, slot_name, None)
    if v is not None and policy == Policy.KEEP:
        return v
    new_v = generate_slot_value(obj, slot_name, schemaview, config=config)
    logging.debug(f'SETTING {slot_name} = {new_v} // current={v}, {policy}')
    if new_v:
        # check if new value is different; not str check is necessary as enums may not be converted
        if v is not None and new_v != v and str(new_v) != str(v):
            if policy == Policy.STRICT:
                raise ValueError(f'Inconsistent value {v} != {new_v} for {slot_name} for {obj}')
            elif policy == Policy.OVERRIDE:
                setattr(obj, slot_name, new_v)
                obj.__post_init__()
        else:
            setattr(obj, slot_name, new_v)
            #print(f'CALLING POST INIT ON {obj} from {slot_name} = {new_v}')
            obj.__post_init__()


def infer_all_slot_values(obj: YAMLRoot, schemaview: SchemaView,
                          policy: Policy = Policy.STRICT, config: Config = Config()):
    """
    Walks object tree inferring all slot values.

    - if a slot has a string_serialization metaslot, apply this
    - if a slot has a equals_expression metaslot, apply this. See :func:`eval_expr()`

    :param obj:
    :param schemaview:
    :param policy: default is STRICT
    :param config:
    :return:
    """
    def infer(in_obj: YAMLRoot):
        logging.debug(f'INFER={in_obj}')
        if isinstance(in_obj, YAMLRoot) and not isinstance(in_obj, EnumDefinitionImpl) and not isinstance(in_obj, PermissibleValue):
            for k, v in vars(in_obj).items():
                #print(f'  ISV={k} curr={v} policy={policy} in_obj={type(in_obj)}')
                infer_slot_value(in_obj, k, schemaview, policy=policy, config=config)
        return in_obj
    traverse_object_tree(obj, infer)


