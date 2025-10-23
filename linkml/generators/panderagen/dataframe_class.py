from linkml.generators.oocodegen import OOClass


class DataframeClass(OOClass):
    """Serves as an adapter between the template that renders the form of the
    dataframe schema and the LinkML model and schema view.

    Currently a thin wrapper around OOClass
    until the dataframe requirements are fully understood.
    """

    def identifier_key_slot(self):
        return self.annotations.get("identifier_key_slot", None)
