from copy import copy
from typing import Union, Any, List, Optional, Type, Callable

import yaml
from jsonasobj import JsonObj, as_json
from rdflib import Graph
from yaml.constructor import ConstructorError

from linkml.utils.context_utils import CONTEXTS_PARAM_TYPE, merge_contexts


class YAMLMark(yaml.error.Mark):
    def __str__(self):
        snippet = self.get_snippet()
        where = "\nFile \"%s\", line %d, column %d"   \
                % (self.name, self.line+1, self.column+1)
        if snippet is not None:
            where += ":\n"+snippet
        return where


class YAMLRoot(JsonObj):

    """
    The root object for all python YAML representations
    """
    def __post_init__(self, **kwargs):
        if kwargs:
            messages: List[str] = []
            for k in kwargs.keys():
                v = repr(kwargs[k])[:40].replace('\n', '\\n')
                messages.append(f"{TypedNode.yaml_loc(k)} Unknown argument: {k} = {v}")
            raise ValueError('\n'.join(messages))

    def _default(self, obj, filtr: Callable[[dict], dict] = None):
        """ JSON serializer callback.
        1) Filter out empty values (None, {}, [] and False) and mangle the names
        2) Add ID entries for dictionary entries

        :param obj: YAMLRoot object to serialize
        :param filtr: Filter to remove elements
        :return: Serialized version of obj
        """

        if isinstance(obj, JsonObj):
            rval = dict()
            for k, v in (filtr(obj.__dict__) if filtr else obj.__dict__).items():
                is_classvar = k.startswith("type_") and hasattr(type(obj), k)
                if is_classvar:
                    print(f"***** {k} is classvar ")
                if not is_classvar and not k.startswith('_') and v is not None and\
                        (not isinstance(v, (dict, list, bool)) or v):

                    from linkml.utils.enumerations import EnumDefinitionImpl
                    if isinstance(v, dict):
                        itemslist = []
                        for vk, vv in v.items():
                            # if isinstance(vv, ClassDefinition):
                            #     vv['@id'] = camelcase(vk)
                            # elif isinstance(vv, (SlotDefinition, TypeDefinition)):
                            #     if k != 'slot_usage':
                            #         vv['@id'] = underscore(vk)
                            itemslist.append(vv)
                        rval[k] = itemslist
                    # TODO: Figure out how to make EnumDefinitionImpl a subclass of EnumDefinition
                    # elif isinstance(v, EnumDefinition):
                    elif isinstance(v, EnumDefinitionImpl):
                        rval[k] = v.code
                    else:
                        rval[k] = v
            return rval
        else:
            return super()._default(obj)

    def _normalize_inlined_slot(self, slot_name: str, slot_type: Type, key_name: Optional[str],
                                inlined_as_list: Optional[bool], keyed: bool) -> None:
        """
         __post_init__ function for a list of inlined keyed or identified classes.
        The input to this is either a list or dictionary of dictionaries.  In the list case, every key entry
        in the list must be unique.  In the dictionary case, the key may or may not be repeated in the dictionary
        element. The internal storage structure is a dictionary of dictionaries.
        @param slot_name: Name of the slot being normalized
        @param slot_type: Slot range type
        @param key_name: Name of the key or identifier in the range
        @param inlined_as_list: True means represent as a list, false or None as a dictionary
        @param keyed: True means each identifier must be unique
        """
        raw_slot: Union[list, dict] = self[slot_name]
        cooked_slot = list() if inlined_as_list else dict()
        key_list = list()

        def cook_a_slot(entry) -> None:
            if keyed:
                if key in key_list:
                    raise ValueError(f"{TypedNode.yaml_loc(key)}: duplicate key")
                key_list.append(key)
            if inlined_as_list:
                cooked_slot.append(entry)
            else:
                cooked_slot[entry[key_name]] = entry

        if isinstance(raw_slot, list):
            # A list of dictionaries
            #   [ {key_name: v11, slot_2: v12, ..., slot_n:v1n}, {key_name: v21, slot_2: v22, ..., slot_n:v2n}, ...]
            for raw_slot_entry in raw_slot:
                if not isinstance(raw_slot_entry, (dict, YAMLRoot)):
                    raise ValueError(f"Slot: {slot_name} - unrecognized element: {raw_slot_entry}")
                if keyed and key_name in raw_slot_entry:
                    value = raw_slot_entry if isinstance(raw_slot_entry, slot_type) else \
                            slot_type(**raw_slot_entry) if isinstance(raw_slot_entry, dict) else\
                            slot_type(**raw_slot_entry.__dict__)
                    key = getattr(value, key_name)
                    cook_a_slot(value)
                else:
                    for k, v in raw_slot_entry.items():
                        key = k
                        cook_a_slot(slot_type(k, v))
        elif isinstance(raw_slot, dict):
            # A dictionary
            # One of:
            #    {key_1: {[key_name: v11], slot_2: v12, ... slot_n: v1n}, key_2: {...}}   or
            #    {v11: v12, v21: v22, ...}
            for key, value in raw_slot.items():
                if not isinstance(value, (dict, YAMLRoot)):
                    cook_a_slot(slot_type(key, value))
                elif isinstance(value, YAMLRoot):
                    vk = getattr(value, key_name, None)
                    if vk is None or vk == key:
                        setattr(value, key_name, key)
                        cook_a_slot(value)
                    else:
                        raise ValueError(f"Slot: {slot_name} - value ({vk}) does not match key ({key})")
                else:
                    # Inject a key if not there otherwise make sure it matches
                    vk = value.get(key_name, None)
                    if vk is None:
                        value_copy = value.copy()
                        value_copy[key_name] = key
                        cook_a_slot(slot_type(**value_copy))
                    elif vk != key:
                        raise ValueError(f"Slot: {slot_name} - value ({vk}) does not match key ({key})")
                    else:
                        cook_a_slot(slot_type(**value))
        else:
            raise ValueError(f"Slot: {slot_name} must be a dictionary or a list")
        self[slot_name] = cooked_slot


def root_representer(dumper: yaml.Dumper, data: YAMLRoot):
    """ YAML callback -- used to filter out empty values (None, {}, [] and false)

    @param dumper: data dumper
    @param data: data to be dumped
    @return:
    """
    # TODO: Figure out how to import EnumDefinition here
    # elif isinstance(v, EnumDefinition):
    from linkml.utils.enumerations import EnumDefinitionImpl
    if isinstance(data, EnumDefinitionImpl):
        data = data.code
    rval = dict()
    for k, v in data.__dict__.items():
        if not k.startswith('_') and v is not None and (not isinstance(v, (dict, list)) or v):
            rval[k] = v
    return dumper.represent_data(rval)


def from_yaml(data: str, cls: Type[YAMLRoot]) -> YAMLRoot:
    return cls(**yaml.load(data, DupCheckYamlLoader))


def as_yaml(element: YAMLRoot) -> str:
    """
    Return element in a YAML representation

    :param element: YAML object
    :return: Stringified representation
    """
    return yaml.dump(element, Dumper=yaml.SafeDumper, sort_keys=False)


def as_json_object(element: YAMLRoot, contexts: CONTEXTS_PARAM_TYPE = None) -> JsonObj:
    """
    Return the representation of element as a JsonObj object
    :param element: element to return
    :param contexts: context(s) to include in the output
    :return: JsonObj representation of element
    """
    rval = copy(element)
    rval['@type'] = element.__class__.__name__
    context_element = merge_contexts(contexts)
    if context_element:
        inner_context = context_element['@context']
        rval['@context'] = inner_context if isinstance(inner_context, JsonObj) else JsonObj(inner_context)
    return rval


class TypedNode:
    def __init__(self, v: Union[Any, "TypedNode"]):
        self._s = v._s if isinstance(v, TypedNode) else None
        self._len = v._len if isinstance(v, TypedNode) else None
        super().__init__()

    def add_node(self, node):
        self._s = node.start_mark
        self._len = node.end_mark.index - node.start_mark.index
        return self

    def loc(self) -> str:
        return f'File "{self._s.name}", line {self._s.line + 1}, col {self._s.column + 1}' if self._s else ''

    @staticmethod
    def yaml_loc(loc_str: Optional[Union["TypedNode", str]] = None) -> str:
        """ Return the yaml file and location of loc_str if it exists """
        return '' if loc_str is None or not hasattr(loc_str, "loc" or not callable(loc_str.loc)) else\
            (loc_str.loc() + ": ")


class extended_str(str, TypedNode):
    def concat(self, *items) -> "extended_str":
        rval = extended_str(str(self) + ''.join([str(item) for item in items]))
        for item in items[::-1]:
            if isinstance(item, TypedNode):
                rval._s = item._s
                rval._len = item._len
                break
        return rval


class extended_int(int, TypedNode):
    pass


class extended_float(float, TypedNode):
    pass


class DupCheckYamlLoader(yaml.loader.SafeLoader):
    """
    A YAML loader that throws an error when the same key appears twice
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, DupCheckYamlLoader.map_constructor)
        self.add_constructor(yaml.resolver.BaseResolver.DEFAULT_SEQUENCE_TAG, DupCheckYamlLoader.seq_constructor)
        self.add_constructor('tag:yaml.org,2002:str', DupCheckYamlLoader.construct_yaml_str)
        self.add_constructor('tag:yaml.org,2002:int', DupCheckYamlLoader.construct_yaml_int)
        self.add_constructor('tag:yaml.org,2002:float', DupCheckYamlLoader.construct_yaml_float)

    def get_mark(self):
        if self.stream is None:
            return YAMLMark(self.name, self.index, self.line, self.column, self.buffer, self.pointer)
        else:
            return YAMLMark(self.name, self.index, self.line, self.column, None, None)

    def construct_yaml_int(self, node):
        """ Scalar constructor that returns the node information as the value """
        return extended_int(super().construct_yaml_int(node)).add_node(node)

    def construct_yaml_str(self, node):
        """ Scalar constructor that returns the node information as the value """
        return extended_str(super().construct_yaml_str(node)).add_node(node)

    def construct_yaml_float(self, node):
        """ Scalar constructor that returns the node information as the value """
        return extended_float(super().construct_yaml_float(node)).add_node(node)

    @staticmethod
    def map_constructor(loader,  node, deep=False):
        """ Duplicate of constructor.construct_mapping w/ exception that we check for dups

        """
        if not isinstance(node, yaml.MappingNode):
            raise ConstructorError(None, None, "expected a mapping node, but found %s" % node.id, node.start_mark)
        mapping = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            value = loader.construct_object(value_node, deep=deep)
            if key in mapping:
                raise ValueError(f"Duplicate key: \"{key}\"")
            mapping[key] = value
        return mapping

    @staticmethod
    def seq_constructor(loader, node, deep=False):
        if not isinstance(node, yaml.SequenceNode):
            raise ConstructorError(None, None,
                                   "expected a sequence node, but found %s" % node.id,
                                   node.start_mark)
        for child in node.value:
            if not child.value:
                raise ConstructorError(None, None, "Empty list elements are not allowed", node.start_mark)
        return [loader.construct_object(child, deep=deep)
                for child in node.value]


yaml.SafeDumper.add_multi_representer(YAMLRoot, root_representer)
yaml.SafeDumper.add_multi_representer(extended_str, yaml.SafeDumper.represent_str)
yaml.SafeDumper.add_multi_representer(extended_int, yaml.SafeDumper.represent_int)
yaml.SafeDumper.add_multi_representer(extended_float, yaml.SafeDumper.represent_float)
yaml.SafeDumper.add_multi_representer(str, yaml.SafeDumper.represent_str)
yaml.SafeDumper.add_multi_representer(int, yaml.SafeDumper.represent_int)
yaml.SafeDumper.add_multi_representer(float, yaml.SafeDumper.represent_float)


def as_rdf(element: YAMLRoot, contexts: CONTEXTS_PARAM_TYPE = None) -> Graph:
    """
    Convert element into an RDF graph guided by the context(s) in contexts
    :param element: element to represent in RDF
    :param contexts: JSON-LD context(s) in the form of a file or URL name, a json string or a json obj
    :return: rdflib Graph containing element
    """

    jsonld = as_json_object(element, contexts)
    graph = Graph()
    graph.parse(data=as_json(jsonld), format="json-ld", prefix=True)
    return graph
