from typing import Dict, Any

import yaml
from jsonasobj2 import JsonObj

from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml_runtime.dumpers import json_dumper


def _remove_names(obj: Any) -> Any:
    """
    Remove `name` keys from dictionary objects, where that dictionary is already keyed by name

    E.g. in the following:

    .. code-block:: yaml

      classes:
        Person:
          name: Person
          description: ...

    translated to:

    .. code-block:: yaml

      classes:
        Person:
          description: ...

    :param obj:
    :return:
    """
    if isinstance(obj, dict):
        return {k: _remove_names(v) for k, v in obj.items() if k != 'name'}
    elif isinstance(obj, list):
        return [_remove_names(x) for x in obj]
    else:
        return obj


def schema_as_dict(schema: SchemaDefinition) -> Dict:
    """
    Translates a SchemaDefinition object into a python dictionary, removing redundant elements

    This is a wrapper to standard runtime dumper methods, but will produce a more compact schema, in particular:

    * prefix maps are normalized to simple key-value pairs
    * for schema elements inlined_as_dict, remove name key from value object using :func:`_remove_names`
    :param schema:
    :return: minimal canonical dictionary object
    """
    obj = json_dumper.to_dict(schema, inject_type=False)
    obj['prefixes'] = {k: v['prefix_reference'] for k, v in obj.get('prefixes', {}).items()}
    obj = _remove_names(obj)
    return obj

def schema_as_yaml_dump(schema: SchemaDefinition) -> str:
    """
    Uses :func:`schema_as_dict` to generate a minimal YAML dump of the schema

    :param schema:
    :return: YAML string
    """
    obj = schema_as_dict(schema)
    return yaml.dump(obj, Dumper=yaml.SafeDumper, sort_keys=False)