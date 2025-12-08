import logging

from ..slot_handler_base import SlotHandlerBase

logger = logging.getLogger(__file__)


class SlotHandlerPandera(SlotHandlerBase):
    """
    Prior to rendering the dataframe schema, this class provides
    and adapter between the LinkML model and schema view
    and the rendering engine.
    """

    # dialect-specific constants used to render the schema
    ANY_RANGE_STRING = "Object"
    CLASS_RANGE_STRING = "Struct"
    SIMPLE_DICT_RANGE_STRING = "Object"
    ENUM_RANGE_STRING = "Enum"

    # When nested inlining is done, the Pandera validator needs a specific range
    INLINED_FORM_RANGE = {
        SlotHandlerBase.FORM_INLINED_SIMPLE_DICT: SIMPLE_DICT_RANGE_STRING,
        SlotHandlerBase.FORM_INLINED_LIST_DICT: CLASS_RANGE_STRING,
        SlotHandlerBase.FORM_INLINED_COLLECTION_DICT: ANY_RANGE_STRING,
        SlotHandlerBase.FORM_INLINED_DICT: CLASS_RANGE_STRING,
        SlotHandlerBase.FORM_ERROR: None,
    }

    def handle_class_slot(self, slot, field) -> None:
        range = slot.range
        range_info = self.generator.schemaview.all_classes().get(range)
        field.reference_class = self.generator.get_class_name(range)

        if range_info and range_info["class_uri"] == SlotHandlerBase.LINKML_ANY_CURIE:
            range = self.__class__.ANY_RANGE_STRING
        else:
            inlined_form = self.backing_inlined_form(self.calculate_inlined_form(slot))
            field.inline_form = inlined_form

            if inlined_form == SlotHandlerBase.FORM_MULTIVALUED_FOREIGN_KEY:
                range = self.generator.make_multivalued(f"ID_TYPES['{self.generator.get_class_name(range)}']")
            elif inlined_form == SlotHandlerBase.FORM_FOREIGN_KEY:
                range = f"ID_TYPES['{self.generator.get_class_name(range)}']"
            elif inlined_form == SlotHandlerBase.FORM_INLINED_LIST_DICT:
                range = self.INLINED_FORM_RANGE[inlined_form]
                range = self.generator.make_multivalued(range)
            elif inlined_form == SlotHandlerBase.FORM_INLINED_COLLECTION_DICT:
                range = self.INLINED_FORM_RANGE[inlined_form]
            elif inlined_form == SlotHandlerBase.FORM_INLINED_SIMPLE_DICT:
                range = self.INLINED_FORM_RANGE[inlined_form]
                self.set_simple_dict_inline_details(slot, field)
            elif inlined_form == SlotHandlerBase.FORM_INLINED_DICT:
                range = self.INLINED_FORM_RANGE[inlined_form]
            else:
                logger.warning("No specific inlined form found")
                range = self.INLINED_FORM_RANGE[inlined_form]

        field.range = range

    def handle_enum_slot(self, slot, field) -> None:
        """Returns the name of the generated Python variable containing the enum"""
        enum_definition = self.get_enum_definition(slot.range)
        range = self.__class__.ENUM_RANGE_STRING
        field.permissible_values = self.generator.enum_handler.get_enum_permissible_values(enum_definition)

        if self.is_multivalued(slot):
            range = self.handle_multivalued_slot(slot, range)

        field.range = range
