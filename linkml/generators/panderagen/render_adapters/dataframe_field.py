from linkml.generators.oocodegen import OOField


class DataframeField(OOField):
    """Serves as an adapter between the template that renders the form of the
    dataframe schema fields and the LinkML model and schema view.

    Currently a thin wrapper around OOField
    until the dataframe requirements are fully understood.
    """

    def __init__(
        self,
        name,
        range=None,
        default_value=None,
        annotations=None,
        source_slot=None,
        inline_id_column_name: str = None,
        inline_id_other_name: str = None,
        inline_other_range: str = None,
        reference_class: str = None,
        inline_form: str = None,
        permissible_values: list[str] = None,
    ):
        """information about schema fields for rendering in jinja2 template.

        name: str
            as rendered in target convention
        range:
        default_value: string
            target form of default
        annotations:
            deprecated
        source_slot:
            additional information
        inline_id_column_name:
            for inlined as simple dict form
        inline_id_other_name:
            for inlined as simple dict form
        inline_other_range:
            for inlined as simple dict form
        permissible values:
            for enums as rendered
        inline_form: str
            which style of inlining is used for a slot
        permissible_values: list[str]
            rendered form of enum values
        """
        super().__init__(name, range, default_value, annotations, source_slot)
        self.inline_id_column_name = inline_id_column_name
        self.inline_id_other_name = inline_id_other_name
        self.inline_other_range = inline_other_range
        self.reference_class = reference_class
        self.inline_form = inline_form
        self._permissible_values = permissible_values

    @property
    def permissible_values(self):
        return self._permissible_values or []

    @permissible_values.setter
    def permissible_values(self, value):
        self._permissible_values = value

    #
    # convenience methods
    #
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

    def inline_details(self):
        return self.source_slot.annotations._get("inline_details", None)

    def required(self):
        return self.source_slot.required

    def identifier(self):
        return self.source_slot.identifier

    def description(self):
        return self.source_slot.description
