from linkml_runtime.linkml_model.meta import SlotDefinition, ClassDefinition
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.formatutils import camelcase
from typing import List

def get_type_designator_value(sv: SchemaView, type_designator_slot: SlotDefinition, class_def: ClassDefinition) -> str:
    """
        retuns the correct value for a type designator field for a given class, depending on its range
        this implements the logic described in https://github.com/linkml/linkml/issues/945:
    """
    target_value = None
    if type_designator_slot.range == 'uri':
        target_value = sv.get_uri(class_def,expand=True,native=False)
    elif type_designator_slot.range == 'string':
        target_value = camelcase(class_def.name)
    else:
        target_value = sv.get_uri(class_def,expand=False, native=False)
    return target_value


def get_accepted_type_designator_values(sv: SchemaView, type_designator_slot: SlotDefinition, class_def: ClassDefinition) -> List[str]:
    accepted_uri_values = [
            sv.get_uri(class_def, expand=True, native=True),
            sv.get_uri(class_def, expand=True, native=False),
            sv.get_uri(class_def, expand=False, native=True),
            sv.get_uri(class_def, expand=False, native=False),
        ]
    # unique, but with order preserved (https://stackoverflow.com/a/17016257)
    accepted_uri_values = list(dict.fromkeys(accepted_uri_values))

    slot_types = set(sv.type_ancestors(type_designator_slot.range))
    uri_types = ['uri', 'uriorcurie']

    if slot_types.intersection(uri_types):
        return accepted_uri_values
    elif type_designator_slot.range == 'string':
        return [camelcase(class_def.name)]
    else:
        return accepted_uri_values
