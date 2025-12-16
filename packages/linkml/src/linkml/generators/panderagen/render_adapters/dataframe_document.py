from linkml.generators.oocodegen import OODocument


class DataframeDocument(OODocument):
    """Serves as an adapter between the template that renders the form of the
    dataframe schema and the LinkML model and schema view.

    Currently a thin wrapper around OODocument
    until the dataframe requirements are fully understood.
    """
