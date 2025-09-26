import polars as pl

from .model_transform import ModelTransform


class ListDictModelTransform(ModelTransform):
    """This class assists in converting a LinkML 'list dict' inline column
    into a form that is better for representing in a PolaRS dataframe and
    validating with a Pandera model.
    """

    def __init__(self, polars_schema):
        self.polars_schema = polars_schema
        """A polars schema representing a list dict column"""

    def transform(self, linkml_list_dict):
        """Transforms a list dict nested column.
        This is a pass-through since list dicts are already in the correct format.
        """
        return linkml_list_dict

    @classmethod
    def unnest_list_struct(cls, column_name: str, df):
        """Use this in a custom check. Pass the nested model as pandera_model."""

        # fmt: off
        unnested_column = (
            df
            .select(column_name)
            .filter(pl.col(column_name).list.len() > 0) # see: https://github.com/pola-rs/polars/issues/14381
            .explode(column_name)
            .unnest(column_name)
        )
        # fmt: on

        return unnested_column

    @classmethod
    def prepare_dataframe(cls, data, column_name, nested_cls):
        """Returns just the list dict column transformed to an inlined list form

        note that this method uses collect and iter_rows so is very inefficient
        """
        polars_schema = nested_cls.to_schema()

        list_dict_transformer = cls(polars_schema)

        one_column_df = data.lazyframe.select(pl.col(column_name)).collect()

        list_of_structs = [list_dict_transformer.transform(e) for [e] in one_column_df.iter_rows()]

        return pl.DataFrame(pl.Series(list_of_structs).alias(column_name))

    def explode_unnest_dataframe(self, df, column_name, data=None):
        """Filter, explode and unnest for list dict with struct fallback."""
        try:
            return (
                df.lazy().filter(pl.col(column_name).list.len() > 0).explode(column_name).unnest(column_name).collect()
            )
        except (pl.exceptions.PanicException, Exception):
            if data:
                from .nested_struct_model_transform import NestedStructModelTransform

                nested_transform = NestedStructModelTransform(self.polars_schema)
                return nested_transform.explode_unnest_dataframe(data.lazyframe, column_name)
            raise
