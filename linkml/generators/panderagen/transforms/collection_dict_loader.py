import polars as pl


class CollectionDictLoader:
    def __init__(self, struct_schema, id_col="id", nested_tx=lambda x: x):
        """
        struct_schema:
            the schema of the nested range not including the collection
        id_col: name of column in struct to hold collection key
        nested_tx: transformation to apply to nested dicts
        """
        self.struct_schema = struct_schema
        self.id_col = id_col
        self.nested_tx = nested_tx

    @staticmethod
    def tx_core(collection_dict, id_col="id", nested_tx=lambda x: x):
        """core collection to structs logic"""
        for k, v in collection_dict.items():
            yield {**nested_tx(v), id_col: k}  # Collection key overwrites nested value

    def tx(self, collection_dict):
        """collection_to_structs"""
        return self.tx_core(collection_dict, self.id_col, self.nested_tx)

    def tx_batch(self, series):
        """Process entire series of collection dicts"""
        return pl.Series(
            [list(self.tx(collection_dict)) for collection_dict in series], dtype=pl.List(self.struct_schema)
        )

    def load(self, source_col):
        return pl.col(source_col).map_batches(self.tx_batch, return_dtype=pl.List(self.struct_schema))

    def load_df(self, df, source_col):
        return df.with_columns(self.load(source_col))
