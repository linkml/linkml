from copy import copy
from json import JSONDecoder
from typing import Union, Any, List, Optional, Type, Callable, Dict

import yaml
from deprecated.classic import deprecated
from jsonasobj2 import JsonObj, as_json, as_dict, JsonObjTypes, items
import jsonasobj2
from rdflib import Graph
from yaml.constructor import ConstructorError

from linkml_runtime.utils.context_utils import CONTEXTS_PARAM_TYPE, merge_contexts
from linkml_runtime.utils.formatutils import is_empty

YAMLObjTypes = Union[JsonObjTypes, "YAMLRoot"]


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
    def __init__(self, *args, **kwargs):
        """
        Override dataclass initializer
        @param args:
        @param kwargs:
        """
        super().__init__(*args, **kwargs)

    def __post_init__(self, *args: List[str],  **kwargs):
        if args or kwargs:
            messages: List[str] = []
            for v in args:
                v = repr(v)[:40].replace('\n', '\\n')
                messages.append(f"Unknown positional argument: {v}")
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

        if isinstance(obj, YAMLRoot):
            rval = dict()
            for k, v in (filtr(obj.__dict__) if filtr else obj.__dict__).items():
                is_classvar = k.startswith("type_") and hasattr(type(obj), k)
                if is_classvar:
                    print(f"***** {k} is classvar ")
                if not is_classvar and not k.startswith('_') and v is not None and\
                        (not isinstance(v, (dict, list, bool)) or v):

                    from linkml_runtime.utils.enumerations import EnumDefinitionImpl
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
            return obj._default(obj) if hasattr(obj, '_default') and callable(obj._default) else\
                JSONDecoder().decode(obj)

    @staticmethod
    def _is_empty(v: Any) -> bool:
        # TODO: Deprecate this function and migrate the python generator over to the stand alone is_empty
        return is_empty(v)

    def _normalize_inlined_as_list(self, slot_name: str, slot_type: Type, key_name: str, keyed: bool) -> None:
        self._normalize_inlined(slot_name, slot_type, key_name, keyed, True)

    def _normalize_inlined_as_dict(self, slot_name: str, slot_type: Type, key_name: str, keyed: bool) -> None:
        self._normalize_inlined(slot_name, slot_type, key_name, keyed, False)

    def _normalize_inlined(self, slot_name: str, slot_type: Type, key_name: str, keyed: bool, is_list: bool) \
            -> None:
        """
         __post_init__ function for a list of inlined keyed or identified classes.

        The input to this is either a list or dictionary of dictionaries.  In the list case, every key entry
        in the list must be unique.  In the dictionary case, the key may or may not be repeated in the dictionary
        element. The internal storage structure is a dictionary of dictionaries.
        @param slot_name: Name of the slot being normalized
        @param slot_type: Slot range type
        @param key_name: Name of the key or identifier in the range
        @param keyed: True means each identifier must be unique
        @param is_list: True means inlined as list
        """
        raw_slot: Union[list, dict, JsonObj] = self[slot_name]
        if raw_slot is None:
            raw_slot = []
        elif not isinstance(raw_slot, (dict, list, JsonObj)):
            raw_slot = [raw_slot]
        cooked_slot = list() if is_list else dict()
        cooked_keys = set()

        def order_up(key: Any, cooked_entry: YAMLRoot) -> None:
            """ A cooked entry is ready to be added to the return slot """
            if cooked_entry[key_name] != key:
                raise ValueError(
                    f"Slot: {loc(slot_name)} - attribute {loc(key_name)} " \
                    f"value ({loc(cooked_entry[key_name])}) does not match key ({loc(key)})")
            if keyed and key in cooked_keys:
                raise ValueError(f"{loc(key)}: duplicate key")
            cooked_keys.add(key)
            if is_list:
                cooked_slot.append(cooked_entry)
            else:
                cooked_slot[key] = cooked_entry

        def loc(s):
            loc_str = TypedNode.yaml_loc(s) if isinstance(s, TypedNode) else ''
            if loc_str == ': ':
                loc_str = ''
            return loc_str + str(s)

        def form_1(entries: Dict[Any, Optional[Union[dict, JsonObj]]]) -> None:
            """ A dictionary of key:dict entries where key is the identifier and dict is an instance of slot_type """
            for key, raw_obj in items(entries):
                if raw_obj is None:
                    raw_obj = {}
                if key_name not in raw_obj:
                    raw_obj = copy(raw_obj)
                    raw_obj[key_name] = key
                if not issubclass(type(raw_obj), slot_type):
                    order_up(key, slot_type(**as_dict(raw_obj)))
                else:
                    order_up(key, raw_obj)

        # TODO: Make an external function extract a root JSON list
        if isinstance(raw_slot, JsonObj):
            raw_slot = raw_slot._hide_list()

        if isinstance(raw_slot, list):
            # We have a list of entries
            for list_entry in raw_slot:
                if isinstance(list_entry, (dict, JsonObj)):
                    # list_entry is either a key:dict, key_name:value or **kwargs
                    if len(list_entry) == 1:
                        # key:dict or key_name:key
                        for lek, lev in items(list_entry):
                            if lek == key_name and not isinstance(lev, (list, dict, JsonObj)):
                                # key_name:value
                                order_up(list_entry[lek], slot_type(list_entry))
                                break   # Not strictly necessary, but
                            elif not isinstance(lev, (list, dict, JsonObj)):
                                # key: value --> slot_type(key, value)
                                order_up(lek, slot_type(lek, lev))
                            else:
                                form_1(list_entry)
                    else:
                        # **kwargs
                        cooked_obj = slot_type(**as_dict(list_entry))
                        order_up(cooked_obj[key_name], cooked_obj)
                elif isinstance(list_entry, list):
                    # *args
                    cooked_obj = slot_type(*list_entry)
                    order_up(cooked_obj[key_name], cooked_obj)
                else:
                    # lone key [key1: , key2: ... }
                    order_up(list_entry, slot_type(**{key_name: list_entry}))
        else:
            # We have a dictionary
            if key_name in raw_slot and not isinstance(raw_slot[key_name], (list, dict, JsonObj)):
                # Vanilla dictionary - {key: v11, s12: v12, ...}
                order_up(raw_slot[key_name], slot_type(**as_dict(raw_slot)))
            else:
                # We have either {key1: {obj1}, key2: {obj2}...} or {key1:, key2:, ...}
                for k, v in items(raw_slot):
                    if v is None:
                        v = dict()
                    if isinstance(v, (dict, JsonObj)):
                        form_1({k: v})
                    elif not isinstance(v, list):
                        order_up(k, slot_type(*[k, v]))
                    else:
                        raise ValueError(f"Unrecognized entry: {loc(k)}: {str(v)}")
        self[slot_name] = cooked_slot

    def _normalize_inlined_slot(self, slot_name: str, slot_type: Type, key_name: Optional[str],
                                inlined_as_list: Optional[bool], keyed: bool) -> None:
        """
        A deprecated entry point to slot normalization. Used for models generated prior to the linkml-runtime split.

        This code is invoked via one of the following patterns:
            if self.<slot> is None:
                self.<slot> = []
            if not isinstance(self.<slot>, list):
                self.extensions = [self.<slot>]
            self._normalize_inlined_slot(slot_name="<slot>", slot_type=<type>, key_name="<key>", inlined_as_list=True, keyed=...)
        or
            if self.<slot> is None:
                self.<slot> = []
            if not isinstance(self.<slot>, (list, dict)):
                self.local_names = [self.<slot>]
            self._normalize_inlined_slot(slot_name="<slot>", slot_type=<type>, key_name="<key>", inlined_as_list=None, keyed=...)

        The above pattern broke when the new jsonasobj was introduced, which is why we have the normalization above.  The code
        below reverse engineers the above and invokes the new form

        """
        if inlined_as_list:
            list_slot = self[slot_name]
            if len(list_slot) == 1 and not isinstance(list_slot[0], list):
                self[slot_name] = list_slot[0]
            self._normalize_inlined_as_list(slot_name, slot_type, key_name, keyed)
        else:
            dict_slot = self[slot_name]
            if isinstance(dict_slot, list):
                if len(dict_slot) == 1 and not isinstance(dict_slot[0], (list, dict)):
                    self[slot_name] = dict_slot[0]
            self._normalize_inlined_as_dict(slot_name, slot_type, key_name, keyed)

    # ==================
    # Error intercepts
    # ==================
    def MissingRequiredField(self, field_name: str) -> None:
        """ Generic loader error handler """
        raise ValueError(f"{field_name} must be supplied")


def root_representer(dumper: yaml.Dumper, data: YAMLRoot):
    """ YAML callback -- used to filter out empty values (None, {}, [] and false)

    @param dumper: data dumper
    @param data: data to be dumped
    @return:
    """
    # TODO: Figure out how to import EnumDefinition here
    # elif isinstance(v, EnumDefinition):
    from linkml_runtime.utils.enumerations import EnumDefinitionImpl
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

    Uses SafeDumper, key-vals are omitted if val is None

    :param element: YAML object
    :return: Stringified representation
    """
    return yaml.dump(element, Dumper=yaml.SafeDumper, sort_keys=False)


def as_json_object(element: YAMLRoot, contexts: CONTEXTS_PARAM_TYPE = None, inject_type = True) -> JsonObj:
    """
    Return the representation of element as a JsonObj object
    :param element: element to return
    :param contexts: context(s) to include in the output
    :param inject_type: if True (default), add a @type at the top level
    :return: JsonObj representation of element
    """
    rval = copy(element)
    if inject_type:
        rval['@type'] = element.__class__.__name__
    context_element = merge_contexts(contexts)
    if context_element:
        rval['@context'] = context_element['@context']
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

    @deprecated(reason="Use yaml_loc instead")
    def loc(self) -> str:
        return self._loc()

    def _loc(self) -> str:
        return f'File "{self._s.name}", line {self._s.line + 1}, col {self._s.column + 1}' if self._s else ''

    @staticmethod
    def yaml_loc(loc_str: Optional[Union["TypedNode", str]] = None, suffix: Optional[str] = ": ") -> str:
        """ Return the yaml file and location of loc_str if it exists """
        return '' if loc_str is None or not hasattr(loc_str, "_loc" or not callable(loc_str._loc)) else\
            (loc_str._loc() + suffix)


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
