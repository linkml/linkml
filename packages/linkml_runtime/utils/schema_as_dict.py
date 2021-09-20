from typing import Dict, Any

import yaml
from jsonasobj2 import JsonObj

from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml_runtime.dumpers import json_dumper


def _remove_names(obj: Any) -> Any:
    """
    dict-based representations may have additional names
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
    obj = json_dumper.to_dict(schema, inject_type=False)
    obj['prefixes'] = {k: v['prefix_reference'] for k, v in obj.get('prefixes', {}).items()}
    obj = _remove_names(obj)
    return obj

def schema_as_yaml_dump(schema: SchemaDefinition) -> str:
    obj = schema_as_dict(schema)
    return yaml.dump(obj, Dumper=yaml.SafeDumper, sort_keys=False)