import re
from decimal import Decimal
from numbers import Number
from typing import List, Any, Union

from jsonasobj2 import JsonObj, as_dict, is_list, is_dict, items, as_json_obj

ws_pattern = re.compile(r'\s+')
us_pattern = re.compile(r'_+')


def uncamelcase(txt: str) -> str:
    split_txt = re.split('(?=[A-Z])', txt)
    new_text = ""
    for word in split_txt:
        if new_text == "":
            new_text = word.lower()
        else:
            new_text = new_text + " " + word.lower()
    return new_text


def camelcase(txt: str) -> str:
    def _up(s: str):
        return s[0].upper() + (s[1:] if len(s) > 1 else '')

    return ''.join([_up(word) for word in us_pattern.sub(' ', txt.strip().replace(',', '')).split()])


def underscore(txt: str) -> str:
    return ws_pattern.sub('_', txt.strip()).replace(',', '').replace('-', '_')


def lcamelcase(txt: str) -> str:
    s = camelcase(txt)
    return s[0].lower() + s[1:]


def be(entry: object) -> str:
    """ Return a stringified version of object replacing Nones with empty strings """
    return str(entry).strip() if entry else ''


def mangled_attribute_name(clsname: str, attributename: str) -> str:
    """ Return the mangling we use for attributes definitions """
    return lcamelcase(clsname) + '__' + underscore(attributename)


split_col = 115


def sfx(uri: str) -> str:
    """
    Add a separator to a uri if none exists.

    Note: This should only be used with module id's -- it is not uncommon to use partial prefixes,
    e.g. PREFIX bfo: http://purl.obolibrary.org/obo/BFO_
    :param uri: uri to be suffixed
    :return: URI with suffix
    """
    return str(uri) + ('' if uri.endswith(('/', '#', '_', ':')) else '/')


def uri_for(prefix: str, suffix: str) -> str:
    """ Generator for predicate and identifier URI's """
    if ':' in prefix:
        return sfx(prefix) + suffix
    else:
        return prefix + ':' + suffix


def split_line(txt: str, split_len: int = split_col) -> List[str]:
    # TODO: consider replacing by textwrap.fill function, but note that its behavior is a bit different
    out_lines = []
    words = txt.split()
    cur_line = ""
    for word in words:
        word += ' '
        if len(cur_line) + len(word) > split_len:
            out_lines.append(cur_line if cur_line else word)
            if not cur_line:
                word = ""
            else:
                cur_line = ""
        cur_line += word
    if cur_line:
        out_lines.append(cur_line)
    return out_lines


def wrapped_annotation(txt: str) -> str:
    rval = []
    for line in [line.strip() for line in txt.split('\n')]:
        if len(line) > split_col:
            rval += split_line(line)
        else:
            rval.append(line)
    return '\n\t'.join(rval)

def shex_results_as_string(rslts) -> str:
    """ Pretty print ShEx Evaluation result """
    # TODO: Add this method to ShEx itself
    rval = [f"Evalutating: {str(rslts.focus)} against {str(rslts.start)}"]
    if rslts.result:
        rval.append("Result: CONFORMS")
    else:
        rval.append("Result: NonConforming")
    rval += rslts.reason.split('\n')
    return '\n'.join(rval)


def is_empty(v: Any) -> bool:
    """
    Determine whether v is considered "empty" in the LinkML context.
    An element is "empty" if:
    1) it is None
    2) It is an empty dictionary
    3) It is an empty list
    4) It is an empty JsonObj
    """
    return v is None or (isinstance(v, (dict, list)) and not v) or (isinstance(v, JsonObj) and not as_dict(v))


def remove_empty_items(obj: Any, hide_protected_keys: bool = False, inside: bool = False) -> Any:
    """
    Recursively iterate over obj removing any empty internal entries.  Note:  this returns a _copy_ of obj of we are
    dealing with a list or a dictionary.

    If hide_protected_keys is true, any key that begins with an underscore is removed from the structure, meaning that
       {
          '_k1': {
             'x': ...
          }
       }
       becomes
       {
          'x': ...
       }

    The above situation ONLY applies when there is ONE k,v pair and v is a dictionary

    Note that this will also convert Decimals to floats or ints; this is necessary
    as both json dumpers and yaml dumpers will encode Decimal types by default.
    See https://github.com/linkml/linkml/issues
    
    This is easier than fixing the individual serializers, described here:
    
    - JSON: https://bugs.python.org/issue16535, https://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object
    - YAML: https://stackoverflow.com/questions/21695705/dump-an-python-object-as-yaml-file/51261042, https://github.com/yaml/pyyaml/pull/372

    :param obj: Object to be tweaked
    :param hide_protected_keys: True means remove keys that begin with an underscore
    :param inside: Keep from removing the outermost container
    :return: copy of obj with empty items removed or None if obj itself is "empty"
    """
    if is_list(obj):
        # for discussion of logic, see: https://github.com/linkml/linkml-runtime/issues/42
        obj_list = [e for e in [remove_empty_items(l, hide_protected_keys=hide_protected_keys, inside=True)
                                for l in obj if l != '_root'] if not is_empty(e)]
        return obj_list if not inside or not is_empty(obj_list) else None
    elif is_dict(obj):
        obj_dict = {k: v for k, v in [(k2, remove_empty_items(v2, hide_protected_keys=hide_protected_keys, inside=True))
                                      for k2, v2 in items(obj)] if not is_empty(v)}

        # https://github.com/linkml/linkml/issues/119
        # Remove the additional level of nesting with enums
        if len(obj_dict) == 1 and list(obj_dict.keys())[0] == '_code':
            enum_text = list(obj_dict.values())[0].get('text', None)
            if enum_text is not None:
                return enum_text
        if hide_protected_keys and len(obj_dict) == 1 and str(list(obj_dict.keys())[0]).startswith('_'):
            inner_element = list(obj_dict.values())[0]
            if isinstance(inner_element, dict):
                obj_dict = inner_element
        return obj_dict if not inside or not is_empty(obj_dict) else None
    elif is_empty(obj):
        return None
    elif isinstance(obj, Decimal):
        # note that attempting to implement https://bugs.python.org/issue16535
        # will not work for yaml serializations
        v = str(obj)
        if '.' in v and not v.endswith('.0'):
            return float(obj)
        else:
            return int(obj)
    else:
        return obj
