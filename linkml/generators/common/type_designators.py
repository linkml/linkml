from linkml_runtime.linkml_model.meta import SlotDefinition, ClassDefinition
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.formatutils import camelcase

def get_type_designator_value(sv: SchemaView, type_designator_slot: SlotDefinition, class_def: ClassDefinition) -> str:
    """
        retuns the correct value for a type designator field for a given class, depending on its range
        this implements the logic described in https://github.com/linkml/linkml/issues/945:
    """
    target_value = None
    if type_designator_slot.range == 'uri':
        target_value = sv.get_uri(class_def,expand=True,native=True)
    elif type_designator_slot.range == 'string':
        target_value = camelcase(class_def.name)
    else:
        target_value = sv.get_uri(class_def,expand=False)
    return target_value
