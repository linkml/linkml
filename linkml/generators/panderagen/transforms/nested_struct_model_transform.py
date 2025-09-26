from .model_transform import ModelTransform


class NestedStructModelTransform(ModelTransform):
    """This class assists in converting a LinkML 'nested struct' inline column
    into a form that is better for representing in a PolaRS dataframe and
    validating with a Pandera model.
    """

    def __init__(self, polars_schema):
        self.polars_schema = polars_schema
        """A polars schema representing a nested struct column"""

    def transform(self, linkml_nested_struct):
        """Transforms a nested struct column.
        This is a pass-through since nested structs are already in the correct format.
        """
        return linkml_nested_struct

    def explode_unnest_dataframe(self, df, column_name):
        """Unnest for nested struct."""
        return df.lazy().select(column_name).unnest(column_name).collect()

    @classmethod
    def prepare_dataframe(cls, data, column_name, nested_cls):
        """Returns the nested struct column as-is since no transformation needed"""
        return data.lazyframe.collect()
