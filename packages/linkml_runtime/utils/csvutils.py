from json_flattener import KeyConfig, GlobalConfig, Serializer
from json_flattener.flattener import CONFIGMAP
from linkml_runtime.linkml_model.meta import SlotDefinitionName, SchemaDefinition, \
    SlotDefinition, ClassDefinition, ClassDefinitionName
from linkml_runtime.utils.schemaview import SchemaView

def get_configmap(schemaview: SchemaView, index_slot: SlotDefinitionName) -> CONFIGMAP:
    """
    Generates a configuration that specifies mapping between a CSV and a JSON structure

    :param schemaview: LinkML schema view over schema
    :param index_slot: key that indexes the top level object
    :return: mapping between top level keys and denormalization configurations
    """
    if index_slot is not None and schemaview is not None:
        slot = schemaview.get_slot(index_slot)
        if slot.range is not None and slot.range in schemaview.all_class():
            cm = {}
            for sn in schemaview.class_slots(slot.range):
                config = _get_key_config(schemaview, slot.range, sn)
                if config is not None:
                    cm[sn] = config
            return cm
        else:
            logging.warn(f'Index slot range not to class: {slot.range}')
    else:
        logging.warn(f'Index slot or schema not specified')
    return {}

def _get_key_config(schemaview: SchemaView, tgt_cls: ClassDefinitionName, sn: SlotDefinitionName, sep='_'):
    slot = schemaview.induced_slot(sn, tgt_cls)
    range = slot.range
    all_cls = schemaview.all_class()
    if range in all_cls and schemaview.is_inlined(slot):
        mappings = {}
        is_complex = False
        for inner_sn in schemaview.class_slots(range):
            denormalized_sn = f'{sn}{sep}{inner_sn}'
            mappings[inner_sn] = denormalized_sn
            inner_slot = schemaview.induced_slot(inner_sn, range)
            inner_slot_range = inner_slot.range
            if (inner_slot_range in all_cls and inner_slot.inlined) or inner_slot.multivalued:
                is_complex = True
        if is_complex:
            serializers = [Serializer.json]
        else:
            serializers = []
        return KeyConfig(is_list=slot.multivalued, delete=True, flatten=True, mappings=mappings, serializers=serializers)
    else:
        return None

# TODO: move this to schemaview
def _is_inlined(slot: SlotDefinition, schemaview: SchemaView):
    if slot.inlined:
        return True
    else:
        range = slot.range
        for sn in schemaview.class_slots(range):
            if schemaview.induced_slot(sn, range).identifier:
                # not explicitly declared inline and has an identifier: assume is ref, not inlined
                return False
        # must be inlined as has no identifier
        return True
