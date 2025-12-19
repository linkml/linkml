import logging

from ..slot_handler_base import SlotHandlerBase

logger = logging.getLogger(__file__)


class SlotHandlerPolars(SlotHandlerBase):
    """
    Prior to rendering the dataframe schema, this class provides
    and adapter between the LinkML model and schema view
    and the rendering engine.
    """

    # constants used to render the schema
    # these will be moved to a dialect-specific place
    ANY_RANGE_STRING = "pl.Object"

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
                range = self.generator.make_multivalued(f"{self.range_id_type(slot)}")
            elif inlined_form == SlotHandlerBase.FORM_FOREIGN_KEY:
                range = self.range_id_type(slot)
            elif inlined_form == SlotHandlerBase.FORM_INLINED_LIST_DICT:
                range = self.generator.get_class_name(range)
                range = self.generator.make_multivalued(f"{range}Struct")
            elif inlined_form == SlotHandlerBase.FORM_INLINED_COLLECTION_DICT:
                range = SlotHandlerPolars.ANY_RANGE_STRING
            elif inlined_form == SlotHandlerBase.FORM_INLINED_SIMPLE_DICT:
                range = SlotHandlerPolars.ANY_RANGE_STRING
                self.set_simple_dict_inline_details(slot, field)
            elif inlined_form == SlotHandlerBase.FORM_INLINED_DICT:
                range = self.generator.get_class_name(range)
                range = f"{range}Struct"
            else:
                logger.warning("No specific inlined form found")
                range = self.generator.get_class_name(range)
                range = f"{range}Struct"

        field.range = range

    def handle_enum_slot(self, slot, field) -> None:
        """Returns the name of the generated Python variable containing the enum"""
        enum_definition = self.get_enum_definition(slot.range)
        enum_name = self.generator.get_enum_name(enum_definition.name)

        if self.is_multivalued(slot):
            enum_name = self.handle_multivalued_slot(slot, enum_name)

        field.range = enum_name
