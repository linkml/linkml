import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from linkml_runtime.linkml_model.meta import ClassDefinitionName, SlotDefinition

if TYPE_CHECKING:
    from .dataframe_generator import DataframeGenerator

from linkml.utils.helpers import get_range_associated_slots

from .render_adapters.dataframe_field import DataframeField

logger = logging.getLogger(__file__)


class SlotHandlerBase(ABC):
    """
    An abstract base class providing a template for classes that generate
    dataframe fields from LinkML models.
    """

    def __init__(self, generator: "DataframeGenerator"):
        self.generator = generator

    LINKML_ANY_CURIE = "linkml:Any"

    # decision flags used to understand the schema
    FORM_INLINED_DICT = "inline_dict"
    FORM_INLINED_LIST_DICT = "inline_list_dict"
    FORM_INLINED_COLLECTION_DICT = "inline_collection_dict"
    FORM_INLINED_SIMPLE_DICT = "simple_dict"
    FORM_MULTIVALUED_FOREIGN_KEY = "list_foreign_key"
    FORM_FOREIGN_KEY = "foreign_key"
    FORM_ERROR = "error"

    def backing_inlined_form(self, inlined_form: str) -> str:
        loaded_form = {
            SlotHandlerBase.FORM_INLINED_SIMPLE_DICT: SlotHandlerBase.FORM_INLINED_LIST_DICT,
            SlotHandlerBase.FORM_INLINED_COLLECTION_DICT: SlotHandlerBase.FORM_INLINED_LIST_DICT,
        }

        if self.generator.backing_form in ["serialization", "transform"]:
            return inlined_form
        elif self.generator.backing_form in ["loaded"]:
            return loaded_form.get(inlined_form, inlined_form)

        logger.warning(f"Unknown backing form: {self.generator.backing_form}")
        return inlined_form

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

        slot_id_range = self.generator.schemaview.all_types().get(slot_id.range)

        return self.generator.map_type(slot_id_range)

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
        (False, False, False, True, False): FORM_INLINED_DICT,
        (False, False, False, True, True): FORM_INLINED_LIST_DICT,
        (False, False, True, False, False): FORM_INLINED_DICT,
        (False, False, True, False, True): FORM_INLINED_LIST_DICT,  # 'COERCED'
        (False, False, True, True, False): FORM_INLINED_DICT,
        (False, False, True, True, True): FORM_INLINED_LIST_DICT,
        # Range has identifier
        (False, True, False, False, False): FORM_FOREIGN_KEY,
        (False, True, False, False, True): FORM_MULTIVALUED_FOREIGN_KEY,
        (False, True, False, True, False): FORM_INLINED_DICT,
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
        sv = self.generator.schemaview

        if cn not in sv.all_classes():
            logger.warning(f"Name {cn} not found in schema classes.")
            return None

        id_slot = sv.get_identifier_slot(cn)
        if id_slot:
            return id_slot
        else:
            for s in sv.class_induced_slots(cn):
                if s.key:
                    return s
            return None

    def calculate_inlined_form(self, slot: SlotDefinition) -> str:
        """Based on entries in the slot definition, do a table lookup
        to determine a summarized form for association handling."""
        inline_form_key = self.inlined_form_key(slot)
        logger.info(f"Inline form key {slot.name}: {inline_form_key}")
        inline_form = self.INTERNAL_INLINED_FORM.get(inline_form_key, SlotHandlerBase.FORM_ERROR)
        logger.info(f"Inline form {slot.name}: {inline_form}")

        # to be removed
        if inline_form == "simple_dict":
            self.set_simple_dict_inline_details_annotation(slot)

        return inline_form

    def calculate_simple_dict(self, slot: SlotDefinition):
        """slot is the container for the simple dict slot"""

        (_, range_simple_dict_value_slot, _) = get_range_associated_slots(self.generator.schemaview, slot.range)

        return range_simple_dict_value_slot

    @abstractmethod
    def handle_class_slot(self, slot, field) -> None:
        pass

    def get_enum_definition(self, range: str):
        return self.generator.schemaview.all_enums().get(range)

    @abstractmethod
    def handle_enum_slot(self, slot, field) -> None:
        pass

    def handle_multivalued_slot(self, slot, range: str) -> str:
        """Use this for non-class slots only for now"""
        if (slot.inlined_as_list is True and self.is_multivalued(slot)) or (
            slot.inlined is True and slot.inlined_as_list is True and self.is_multivalued(slot)
        ):
            range = self.generator.make_multivalued(range)

        return range

    def handle_slot(self, cn: str, sn: str) -> DataframeField:
        safe_sn = self.generator.get_slot_name(sn)
        slot = self.generator.schemaview.induced_slot(sn, cn)
        logger.info(safe_sn)

        if slot.alias is not None:
            safe_sn = self.generator.get_slot_name(slot.alias)

        field = DataframeField(name=safe_sn, source_slot=slot)

        range = slot.range

        if range is None:
            self.handle_none_slot(slot, field)
        elif range in self.generator.schemaview.all_classes():
            self.handle_class_slot(slot, field)
        elif range in self.generator.schemaview.all_types():
            self.handle_type_slot(slot, field)
        elif range in self.generator.schemaview.all_enums():
            range = self.handle_enum_slot(slot, field)
        else:
            raise Exception(f"Unknown range {range}")

        return field

    def set_simple_dict_inline_details(self, slot, field) -> None:
        """Extra metadata is to help with the simple dict case"""
        (range_id_slot, range_simple_dict_value_slot, _) = get_range_associated_slots(  # range_required_slots,
            self.generator.schemaview, slot.range
        )

        field.inline_id_column_name = range_id_slot.name
        field.inline_other_column_name = range_simple_dict_value_slot.name

        other_range = range_simple_dict_value_slot.range

        if other_range in self.generator.schemaview.all_enums():
            field.inline_other_range = self.generator.get_enum_name(other_range)
        elif other_range in self.generator.schemaview.all_types():
            field.inline_other_range = self.generator.map_type(self.generator.schemaview.all_types().get(other_range))
        elif other_range in self.generator.schemaview.all_classes():
            field.inline_other_range = self.generator.get_class_name(other_range)
        else:
            raise ValueError(f"Cannot find range {other_range} for simple dict slot {slot.name}")

    def handle_non_inlined_class_slot(self, slot, field) -> None:
        """non-inlined class slots have been temporarily removed but this will be needed to support them"""
        range = slot.range
        field.range = f"ID_TYPES['{self.generator.get_class_name(range)}']"

    def handle_none_slot(self, slot, field: DataframeField) -> None:
        del slot  # unused for now
        range = self.generator.schema.default_range  # need to figure this out, set at the beginning?

        if range is None:
            range = "str"

        field.range = range

    def handle_type_slot(self, slot, field) -> None:
        t = self.generator.schemaview.all_types().get(slot.range)
        range = self.generator.map_type(t)

        if self.is_multivalued(slot):
            range = self.handle_multivalued_slot(slot, range)

        field.range = range

    def set_simple_dict_inline_details_annotation(self, slot):
        """Extra metadata is to help with the simple dict case"""
        (range_id_slot, range_simple_dict_value_slot, _) = get_range_associated_slots(  # range_required_slots,
            self.generator.schemaview, slot.range
        )

        simple_dict_id = range_id_slot.name
        other_slot = range_simple_dict_value_slot.name
        slot.annotations["inline_details"] = {"id": simple_dict_id, "other": other_slot}
