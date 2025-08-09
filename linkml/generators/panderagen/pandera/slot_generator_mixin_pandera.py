import logging

from linkml.utils.helpers import get_range_associated_slots

from ..render_adapters.dataframe_field import DataframeField
from ..slot_generator_mixin_base import SlotGeneratorMixinBase

logger = logging.getLogger(__file__)


class SlotGeneratorMixinPandera(SlotGeneratorMixinBase):
    """
    Prior to rendering the dataframe schema, this class provides
    and adapter between the LinkML model and schema view
    and the rendering engine.
    """

    # constants used to render the schema
    # these will be moved to a dialect-specific place
    ANY_RANGE_STRING = "Object"
    CLASS_RANGE_STRING = "Struct"
    SIMPLE_DICT_RANGE_STRING = "Struct"
    ENUM_RANGE_STRING = "Enum"

    # When nested inlining is done, the Pandera validator needs a specific range
    INLINED_FORM_RANGE_PANDERA = {
        SlotGeneratorMixinBase.FORM_INLINED_SIMPLE_DICT: SIMPLE_DICT_RANGE_STRING,
        SlotGeneratorMixinBase.FORM_INLINED_LIST_DICT: CLASS_RANGE_STRING,
        SlotGeneratorMixinBase.FORM_INLINED_COLLECTION_DICT: CLASS_RANGE_STRING,
        SlotGeneratorMixinBase.FORM_INLINED_DICT: CLASS_RANGE_STRING,
        SlotGeneratorMixinBase.FORM_ERROR: None,
    }

    def handle_none_slot(self, slot) -> str:
        range = self.schema.default_range  # need to figure this out, set at the beginning?
        if range is None:
            range = "str"

        return range

    def handle_class_slot(self, slot, range: str) -> str:
        range_info = self.schemaview.all_classes().get(range)

        if range_info["class_uri"] == SlotGeneratorMixinBase.LINKML_ANY_CURIE:
            range = self.__class__.ANY_RANGE_STRING
        else:
            inlined_form = self.calculate_inlined_form(slot)

            if inlined_form == SlotGeneratorMixinBase.FORM_INLINED_COLLECTION_DICT:
                logger.warning(
                    f"Slot {slot.name} uses inlined dictionary form,"
                    "which may be less efficient than inlined as list form with the current implementation."
                )
            elif inlined_form == SlotGeneratorMixinBase.FORM_INLINED_SIMPLE_DICT:
                logger.warning(
                    f"Slot {slot.name} uses inlined simple dictionary form. Support is incomplete "
                    "and performance is less efficient than inlined as list form with the current implementation."
                )

            if inlined_form in (
                SlotGeneratorMixinBase.FORM_MULTIVALUED_FOREIGN_KEY,
                SlotGeneratorMixinBase.FORM_FOREIGN_KEY,
            ):
                logger.warning(f"Foreign key not implemented for slot {slot.name}")
                range = f"ID_TYPES['{self.get_class_name(range)}']"
            else:
                # TODO: make these setters
                slot.annotations["reference_class"] = self.get_class_name(range)
                slot.annotations["inline_form"] = inlined_form

                range = SlotGeneratorMixinPandera.INLINED_FORM_RANGE_PANDERA[inlined_form]

                if inlined_form == SlotGeneratorMixinBase.FORM_INLINED_SIMPLE_DICT:
                    self.set_simple_dict_inline_details_annotation(slot)
                elif inlined_form in [SlotGeneratorMixinBase.FORM_INLINED_LIST_DICT]:
                    range = self.make_multivalued(range)

        return range

    def set_simple_dict_inline_details_annotation(self, slot):
        """Extra metadata is to help with the simple dict case"""
        (range_id_slot, range_simple_dict_value_slot, _) = get_range_associated_slots(  # range_required_slots,
            self.schemaview, slot.range
        )

        simple_dict_id = range_id_slot.name
        other_slot = range_simple_dict_value_slot.name
        slot.annotations["inline_details"] = {"id": simple_dict_id, "other": other_slot}

    def handle_non_inlined_class_slot(self, slot, range: str) -> str:
        """non-inlined class slots have been temporarily removed but this will be needed to support them"""
        return f"ID_TYPES['{self.get_class_name(range)}']"

    def handle_type_slot(self, slot, range: str) -> str:
        del slot  # unused for now

        t = self.schemaview.all_types().get(range)
        range = self.map_type(t)

        return range

    def handle_enum_slot(self, slot, range: str) -> str:
        """Returns the name of the generated Python variable containing the enum"""
        enum_definition = self.get_enum_definition(range)
        range = self.__class__.ENUM_RANGE_STRING
        slot.annotations["permissible_values"] = self.get_enum_permissible_values(enum_definition)

        return range

    def handle_multivalued_slot(self, slot, range: str) -> str:
        if (slot.inlined_as_list is True and self.is_multivalued(slot)) or (
            slot.inlined is True and slot.inlined_as_list is True and self.is_multivalued(slot)
        ):
            range = self.make_multivalued(range)

        return range

    def handle_slot(self, cn: str, sn: str):
        safe_sn = self.get_slot_name(sn)
        slot = self.schemaview.induced_slot(sn, cn)
        range = slot.range

        if slot.alias is not None:
            safe_sn = self.get_slot_name(slot.alias)

        if range is None:
            range = self.handle_none_slot(slot)
        elif range in self.schemaview.all_classes():
            range = self.handle_class_slot(slot, range)
        elif range in self.schemaview.all_types():
            range = self.handle_type_slot(slot, range)
            if self.is_multivalued(slot):
                range = self.make_multivalued(range)
        elif range in self.schemaview.all_enums():
            range = self.handle_enum_slot(slot, range)
            range = self.handle_multivalued_slot(slot, range)
        else:
            raise Exception(f"Unknown range {range}")

        return DataframeField(
            name=safe_sn,
            source_slot=slot,
            range=range,
        )
