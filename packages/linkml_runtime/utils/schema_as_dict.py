from typing import Dict, Any, Optional

import yaml

from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml_runtime.dumpers import json_dumper


def _remove_names(obj: Any, parent: Optional[str]) -> Any:
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

    Also compacts representation of prefixes

    It also takes care of the edge case:

    .. code-block:: yaml

        slots:
          name:
            ...

    :param obj: dictionary object to recursively transform
    :param parent: key for parent dict
    :return:
    """
    if isinstance(obj, dict):
        return {k: _remove_names(v, k) for k, v in obj.items() if k != 'name' or parent is None or parent == 'slots'}
    elif isinstance(obj, list):
        return [_remove_names(x, parent) for x in obj]
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
    obj = json_dumper.to_dict(schema)
    if '@type' in obj:
        del obj['@type']
    obj['prefixes'] = {k: v['prefix_reference'] for k, v in obj.get('prefixes', {}).items()}
    for k, v in obj.get('enums', {}).items():
        for pv in v.get('permissible_values', {}).values():
            del pv['text']
    obj = _remove_names(obj, None)
    return obj

def schema_as_yaml_dump(schema: SchemaDefinition) -> str:
    """
    Uses :func:`schema_as_dict` to generate a minimal YAML dump of the schema

    :param schema:
    :return: YAML string
    """
    obj = schema_as_dict(schema)
    return yaml.dump(obj, Dumper=yaml.SafeDumper, sort_keys=False)
