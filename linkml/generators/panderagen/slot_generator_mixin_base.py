from abc import ABC, abstractmethod
from typing import Optional

from linkml_runtime.linkml_model.meta import ClassDefinitionName, SlotDefinition

from linkml.utils.helpers import get_range_associated_slots


class SlotGeneratorMixinBase(ABC):
    """
    An abstract base class providing a template for classes that generate
    dataframe fields from LinkML models.

    The idea here is to implement helper methods more specific to dataframes
    slot processing in this class, override things specific to individual dataframes
    and then pass the generator instance with all mixins to the jinja template
    for formatting.

    Mostly this provides common method names for each of the generators
    """

    LINKML_ANY_CURIE = "linkml:Any"

    # constants used to understand the schema (decision flags)
    FORM_INLINED_DICT = "inlined_dict"
    FORM_INLINED_LIST_DICT = "inlined_list_dict"
    FORM_INLINED_COLLECTION_DICT = "inline_collection_dict"
    FORM_INLINED_SIMPLE_DICT = "simple_dict"
    FORM_MULTIVALUED_FOREIGN_KEY = "list_foreign_key"
    FORM_FOREIGN_KEY = "foreign_key"
    FORM_ERROR = "error"

    def is_multivalued(self, slot):
        return "multivalued" in slot and slot.multivalued is True

    def is_inlined(self, slot):
        """Handles the default None case when inlined is not explicitly set in the model"""
        return slot.inlined is True

    def is_inlined_as_list(self, slot):
        """Handles the default None case when inlined_as_list is not explicitly set in the model."""
        return slot.inlined_as_list is True

    def range_id_type(self, slot):
        """Get the identifier type for the range of the given slot."""
        slot_id = self.get_identifier_or_key_slot(slot.range)

        if slot_id is None:
            return None

        slot_id_range = self.schemaview.all_types().get(slot_id.range)

        return self.map_type(slot_id_range)

    def range_has_identifier_or_key(self, slot):
        """Determine if the slot range has an identifier or key."""
        return self.get_identifier_or_key_slot(slot.range) is not None

    def range_meets_simple_dict_conditions(self, slot):
        """Determine if the slot range meets the conditions for simple dict form."""
        return self.calculate_simple_dict(slot) is not None

    def inlined_form_key(self, slot):
        """Create a tuple that can be used to look up a line in INTERNAL_INLINED_FORM"""
        return (
            self.range_meets_simple_dict_conditions(slot),
            self.range_has_identifier_or_key(slot),
            self.is_inlined(slot),
            self.is_inlined_as_list(slot),
            self.is_multivalued(slot),
        )

    # meets_simple_dict_conditions, has_identifier is True, inlined is True, inlined_as_list is True, is_multivalued
    INTERNAL_INLINED_FORM = {
        ## Simple dict conditions not met
        # Range does not have identifier
        (False, False, False, False, False): FORM_INLINED_DICT,  # 'COERCED'
        (False, False, False, False, True): FORM_INLINED_LIST_DICT,  # 'COERCED'
        (False, False, False, True, False): FORM_INLINED_LIST_DICT,
        (False, False, False, True, True): FORM_INLINED_LIST_DICT,
        (False, False, True, False, False): FORM_INLINED_DICT,
        (False, False, True, False, True): FORM_INLINED_LIST_DICT,  # 'COERCED'
        (False, False, True, True, False): FORM_INLINED_DICT,
        (False, False, True, True, True): FORM_INLINED_LIST_DICT,
        # Range has identifier
        (False, True, False, False, False): FORM_FOREIGN_KEY,
        (False, True, False, False, True): FORM_MULTIVALUED_FOREIGN_KEY,
        (False, True, False, True, False): FORM_INLINED_LIST_DICT,
        (False, True, False, True, True): FORM_INLINED_LIST_DICT,
        (False, True, True, False, False): FORM_INLINED_DICT,
        (False, True, True, False, True): FORM_INLINED_COLLECTION_DICT,
        (False, True, True, True, False): FORM_INLINED_DICT,
        (False, True, True, True, True): FORM_INLINED_LIST_DICT,
        ## Simple dict conditions met
        # Range does not have identifier
        (True, False, False, False, False): FORM_INLINED_DICT,  # 'COERCED'
        (True, False, False, False, True): FORM_INLINED_LIST_DICT,  # 'COERCED'
        (True, False, False, True, False): FORM_INLINED_LIST_DICT,
        (True, False, False, True, True): FORM_INLINED_LIST_DICT,
        (True, False, True, False, False): FORM_INLINED_DICT,
        (True, False, True, False, True): FORM_INLINED_LIST_DICT,  # 'COERCED'
        (True, False, True, True, False): FORM_INLINED_DICT,
        (True, False, True, True, True): FORM_INLINED_LIST_DICT,
        # Range has identifier
        (True, True, False, False, False): FORM_FOREIGN_KEY,
        (True, True, False, False, True): FORM_MULTIVALUED_FOREIGN_KEY,
        (True, True, False, True, False): FORM_INLINED_LIST_DICT,
        (True, True, False, True, True): FORM_INLINED_LIST_DICT,
        (True, True, True, False, False): FORM_INLINED_DICT,
        (True, True, True, False, True): FORM_INLINED_SIMPLE_DICT,
        (True, True, True, True, False): FORM_INLINED_DICT,
        (True, True, True, True, True): FORM_INLINED_LIST_DICT,
    }

    def get_identifier_or_key_slot(self, cn: ClassDefinitionName) -> Optional[SlotDefinition]:
        sv = self.schemaview
        id_slot = sv.get_identifier_slot(cn)
        if id_slot:
            return id_slot
        else:
            for s in sv.class_induced_slots(cn):
                if s.key:
                    return s
            return None

    def calculate_inlined_form(self, slot: SlotDefinition) -> str:
        return self.INTERNAL_INLINED_FORM.get(self.inlined_form_key(slot), SlotGeneratorMixinBase.FORM_ERROR)

    def calculate_simple_dict(self, slot: SlotDefinition):
        """slot is the container for the simple dict slot"""

        (_, range_simple_dict_value_slot, _) = get_range_associated_slots(self.schemaview, slot.range)

        return range_simple_dict_value_slot

    @abstractmethod
    def handle_none_slot(self, slot) -> str:
        pass

    @abstractmethod
    def handle_class_slot(self, slot, range: str) -> str:
        pass

    @abstractmethod
    def set_simple_dict_inline_details_annotation(self, slot):
        pass

    @abstractmethod
    def handle_non_inlined_class_slot(self, slot, range: str) -> str:
        pass

    @abstractmethod
    def handle_type_slot(self, slot, range: str) -> str:
        pass

    def get_enum_definition(self, range: str):
        return self.schemaview.all_enums().get(range)

    @abstractmethod
    def handle_enum_slot(self, slot, range: str) -> str:
        pass

    @abstractmethod
    def handle_multivalued_slot(self, slot, range: str) -> str:
        pass

    @abstractmethod
    def handle_slot(self, cn: str, sn: str):
        pass
