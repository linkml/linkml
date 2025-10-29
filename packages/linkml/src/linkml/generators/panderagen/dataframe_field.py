from contextlib import suppress

from linkml.generators.oocodegen import OOField


class DataframeField(OOField):
    """Serves as an adapter between the template that renders the form of the
    dataframe schema fields and the LinkML model and schema view.

    Currently a thin wrapper around OOField
    until the dataframe requirements are fully understood.
    """

    def inline_form(self):
        return self.source_slot.annotations._get("inline_form", None)

    def reference_class(self):
        with suppress(AttributeError, KeyError):
            return self.source_slot.annotations._get("reference_class", None)
        return None

    def maximum_value(self):
        return self.source_slot.maximum_value

    def minimum_value(self):
        return self.source_slot.minimum_value

    def pattern(self):
        return self.source_slot.pattern

    def minimum_cardinality(self):
        return self.source_slot.minimum_cardinality

    def maximum_cardinality(self):
        return self.source_slot.maximum_cardinality

    def permissible_values(self):
        return self.source_slot.annotations._get("permissible_values", [])

    def inline_details(self):
        return self.source_slot.annotations._get("inline_details", None)

    def required(self):
        return self.source_slot.required

    def identifier(self):
        return self.source_slot.identifier

    def description(self):
        return self.source_slot.description
