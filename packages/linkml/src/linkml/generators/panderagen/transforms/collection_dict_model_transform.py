import polars as pl

from .model_transform import ModelTransform


class CollectionDictModelTransform(ModelTransform):
    """This class assists in converting a LinkML 'collection dict' inline column
    into a form that is better for representing in a PolaRS dataframe and
    validating with a Pandera model.
    """

    def __init__(self, polars_schema, id_col):
        self.polars_schema = polars_schema
        """A polars schema representing a collection dict column"""

        self.id_col = id_col
        """The ID column in the sense of a LinkML inline collection dict"""

    def transform(self, linkml_collection_dict):
        """Converts a collection dict nested column to a list of dicts.
        { 'A': {...}, 'B': {...}, ... } -> [{'id': 'A', ...}, {'id': 'B', ...}, ...]
        """
        return self._collection_dict_to_list_of_structs(linkml_collection_dict)

    def _collection_dict_to_list_of_structs(self, linkml_collection_dict):
        """Converts a collection dict nested column to a list of dicts.
        { 'A': {...}, 'B': {...}, ... } -> [{'id': 'A', ...}, {'id': 'B', ...}, ...]

        An inefficient conversion (relative to native PolaRS operations)
        from a collection dict form to a dataframe struct column.

        linkml_collection_dict : dict
            A single row entry in a dataframe column (one cell), which itself is a dict.
            The value entries are dicts that get the key added as an id field.
        """
        arr = []
        for k, v in linkml_collection_dict.items():
            if k not in v:
                v[self.id_col] = k
            arr.append(v)
        return arr

    @classmethod
    def prepare_dataframe(cls, data, column_name, nested_cls):
        """Returns just the collection dict column transformed to an inlined list form

        note that this method uses collect and iter_rows so is very inefficient
        """
        id_column = nested_cls.get_id_column_name()
        polars_schema = nested_cls.to_schema()

        collection_dict_transformer = cls(polars_schema, id_column)

        one_column_df = data.lazyframe.select(pl.col(column_name)).collect()

        list_of_structs = [collection_dict_transformer.transform(e) for [e] in one_column_df.iter_rows()]

        return pl.DataFrame(pl.Series(list_of_structs).alias(column_name))

    def explode_unnest_dataframe(self, df, column_name):
        """Filter, explode and unnest for collection dict."""
        return df.lazy().filter(pl.col(column_name).list.len() > 0).explode(column_name).unnest(column_name).collect()
