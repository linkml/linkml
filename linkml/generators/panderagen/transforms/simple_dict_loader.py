import polars as pl


class SimpleDictLoader:
    def __init__(
        self,
        struct_schema,
        id_col="id",
        other_col="other",
        id_dtype=pl.String,
        other_dtype=pl.Int64,
        nested_tx=lambda x: x,
    ):
        self.struct_schema = struct_schema
        self.id_col: str = id_col
        self.other_col: str = other_col
        self.id_dtype = id_dtype
        self.other_dtype = other_dtype
        self.nested_tx = nested_tx
        self.polars_schema_keys = set(self.struct_schema.keys())
        self.ordered_schema_keys = list(self.struct_schema.keys())

    def tx_core(self, linkml_simple_dict):
        """core simple dict to list of dicts logic"""
        for id_value, range_value in linkml_simple_dict.items():
            base_dict = {k: None for k in self.ordered_schema_keys}
            if isinstance(range_value, dict) and (set(range_value.keys()) <= self.polars_schema_keys):
                base_dict.update(self.nested_tx(range_value))
            else:
                base_dict[self.other_col] = range_value
            base_dict[self.id_col] = id_value
            yield base_dict

    # simple dict handling
    def tx(self, sd):
        """simple dict to list of dicts"""
        return self.tx_core(sd)

    def tx_batch(self, series):
        """Process entire series of simple dicts"""
        result = []
        for simple_dict in series:
            transformed = list(self.tx(simple_dict))
            result.append(transformed)
        return pl.Series(result, dtype=pl.List(pl.Struct(self.struct_schema)))

    def load(self, source_col):
        return pl.col(source_col).map_batches(self.tx_batch, return_dtype=pl.List(pl.Struct(self.struct_schema)))

    def load_df(self, df, source_col):
        return df.with_columns(self.load(source_col))
