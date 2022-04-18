import json
import os
from io import TextIOWrapper
from typing import Optional, Union, List, Any, Dict, Callable

import yaml
from jsonasobj2 import JsonObj, loads

CONTEXT_TYPE = Union[str, dict, JsonObj]
CONTEXTS_PARAM_TYPE = Optional[Union[CONTEXT_TYPE, List[CONTEXT_TYPE]]]


def merge_contexts(contexts: CONTEXTS_PARAM_TYPE = None, base: Optional[Any] = None) -> JsonObj:
    """ Take a list of JSON-LD contexts, which can be one of:
        * the name of a JSON-LD file
        * the URI of a JSON-lD file
        * JSON-LD text
        * A JsonObj object that contains JSON-LD
        * A dictionary that contains JSON-LD

    And turn it into an object that can be tacked onto the end of any JSON object for conversion into RDF

    The base is added back in because @base is ignored in imported and nested contexts -- it must be at the
    root in the object itself.

    :param contexts: Ordered list of contexts to add
    :param base: base to add in (optional)
    :return: aggregated context
    """
    def prune_context_node(ctxt: Union[str, JsonObj]) -> Union[str, JsonObj]:
        return ctxt['@context'] if isinstance(ctxt, JsonObj) and '@context' in ctxt else ctxt

    def to_file_uri(fname: str) -> str:
        return 'file://' + fname

    context_list = []
    for context in [] if contexts is None else [contexts] if not isinstance(contexts, (list, tuple, set)) else contexts:
        if isinstance(context, str):
            # One of filename, URL or json text
            if context.strip().startswith("{"):
                context = loads(context)
            elif '://' not in context:
                context = to_file_uri(context)
        elif not isinstance(context, (JsonObj, str)):
            context = JsonObj(**context)    # dict
        context_list.append(prune_context_node(context))
    if base:
        context_list.append(JsonObj(**{'@base': str(base)}))
    return None if not context_list else \
        JsonObj(**{"@context": context_list[0] if len(context_list) == 1 else context_list})


def map_import(importmap: Dict[str, str], namespaces: Callable[[None], "Namespaces"], imp: Any) -> str:
    sname = str(imp)
    if ':' in sname:
        prefix, lname = sname.split(':', 1)
        prefix += ':'
        sname = importmap.get(prefix, prefix) + lname
    sname = importmap.get(sname, sname)  # Import map may use CURIE
    sname = str(namespaces().uri_for(sname)) if ':' in sname else sname
    return importmap.get(sname, sname)  # It may also use URI or other forms


def parse_import_map(map_: Optional[Union[str, Dict[str, str], TextIOWrapper]],
                     base: Optional[str] = None) -> Dict[str, str]:
    """
    Process the import map
    :param map_: A map location, the JSON for a map, YAML for a map or an existing dictionary
    :param base: Base location to turn relative locations into absolute
    :return: Import map
    """
    if map_ is None:
        rval = dict()
    elif isinstance(map_, TextIOWrapper):
        map_.seek(0)
        return parse_import_map(map_.read(), base)
    elif isinstance(map_, dict):
        rval = map_
    elif map_.strip().startswith('{'):
        rval = json.loads(map_)
    elif '\n' in map_ or '\r' in map_ or ' ' in map_:
        rval = yaml.safe_load(map_)
    else:
        with open(map_) as ml:
            return parse_import_map(ml.read(), os.path.dirname(map_))

    if base:
        outmap = dict()
        for k, v in rval.items():
            if ':' not in v:
                v = os.path.join(os.path.abspath(base), v)
            outmap[k] = v
        rval = outmap
    return rval
