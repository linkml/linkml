import json
from typing import TextIO, Type, Union

import jsonschema
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.utils.yamlutils import YAMLRoot

from linkml.generators.jsonschemagen import JsonSchemaGenerator


def _as_dict(inst):
    # TODO: replace this with linkml_runtime.dictutils when 1.0.14 is released
    inst_dict = json.loads(json_dumper.dumps(element=inst))
    del inst_dict["@type"]
    return inst_dict


# Deprecated: use validators module
def validate_object(
    data: YAMLRoot,
    schema: Union[str, TextIO, SchemaDefinition],
    target_class: Type[YAMLRoot] = None,
    closed: bool = True,
):
    """
    validates instance data against a schema

    :param data: LinkML instance to be validates
    :param schema: LinkML schema
    :param target_class: class in schema to validate against
    :param closed:
    :return:
    """
    if target_class is None:
        target_class = type(data)
    inst_dict = _as_dict(data)
    not_closed = not closed
    jsonschemastr = JsonSchemaGenerator(
        schema,
        mergeimports=True,
        top_class=target_class.class_name,
        not_closed=not_closed,
    ).serialize(not_closed=not_closed)
    jsonschema_obj = json.loads(jsonschemastr)
    return jsonschema.validate(
        inst_dict, schema=jsonschema_obj, format_checker=jsonschema.Draft7Validator.FORMAT_CHECKER
    )
