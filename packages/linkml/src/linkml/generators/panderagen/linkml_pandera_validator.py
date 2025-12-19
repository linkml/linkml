import logging

import polars as pl
from pandera.api.polars.types import PolarsData
from pandera.errors import SchemaError

from .transforms import CollectionDictLoader, SimpleDictLoader

logger = logging.getLogger(__name__)


class LinkmlPanderaValidator:
    """Recursively calls Pandera validate on nested classes"""

    @classmethod
    def get_id_column_name(cls):
        """
        _id_name is present in the implementing class
        """
        return cls._id_name

    @classmethod
    def _check_simple_dict(
        cls,
        data: PolarsData,
        nested_cls: type,
        id_col: str,
        other_col: str,
        polars_schema: pl.Schema,
        polars_schema_dict,
    ):
        """The 'simple dict' inlined form is not efficient for dataframe storage.
        Ideally the dataframe is converted at load time to a schema with
        only lists of structs. If not, this method transforms at validation time.
        """
        column_name = data.key

        tx = SimpleDictLoader(
            polars_schema,
            id_col,
            other_col,
            polars_schema_dict[id_col],
            polars_schema_dict[other_col],
        )

        one_column_lf = data.lazyframe.select(tx.load(column_name)).filter(pl.col(column_name).list.len() > 0)

        # may be expensive, consider making it optional
        actual = one_column_lf.collect_schema()[column_name]
        expected = pl.List(pl.Struct(polars_schema))

        if actual != expected:
            raise SchemaError(
                polars_schema_dict, one_column_lf, f"Schema mismatch for {column_name}: {actual} != {expected}"
            )

        nested_lf = one_column_lf.explode(column_name).unnest(column_name)

        if isinstance(data.lazyframe, pl.LazyFrame):
            nested_cls.validate(nested_lf)
        else:
            nested_cls.validate(nested_lf.collect(engine="streaming"))

        return data.lazyframe.select(pl.lit(True))

    @classmethod
    def _check_collection_struct(cls, data: PolarsData, nested_cls: type, polars_schema_struct: pl.Struct):
        """The 'collection dict' inline form is not efficient for dataframe.
        Ideally the dataframe is converted at load time to a schema with
        only lists of structs. If not, this method transforms at validation time."""
        column_name = data.key

        tx = CollectionDictLoader(struct_schema=polars_schema_struct, id_col="id")

        one_column_lf = data.lazyframe.select(tx.load(column_name))

        # may be expensive, consider making it optional
        actual = one_column_lf.collect_schema()[column_name]
        expected = pl.List(polars_schema_struct)

        if actual != expected:
            raise SchemaError(
                polars_schema_struct, one_column_lf, f"Schema mismatch for {column_name}: {actual} != {expected}"
            )

        nested_lf = one_column_lf.explode(column_name).unnest(column_name)

        if isinstance(data.lazyframe, pl.LazyFrame):
            nested_cls.validate(nested_lf)
        else:
            nested_cls.validate(nested_lf.collect(engine="streaming"))

        return data.lazyframe.select(pl.lit(True))

    @classmethod
    def _check_nested_list_struct(cls, data: PolarsData, nested_cls: type, polars_schema):
        """Use explode and unnest operations to pass nested lists to pandera validate"""
        column_name = data.key

        one_column_lf = data.lazyframe.select(column_name)

        # may be expensive, consider making it optional
        actual = one_column_lf.collect_schema()[column_name]
        expected = pl.List(pl.Struct(polars_schema))

        # TODO: form of polars_schema needs to be more regular wrt container
        if actual != expected:
            raise SchemaError(
                polars_schema, one_column_lf, f"Schema mismatch for {column_name}: {actual} != {expected}"
            )

        # fmt: off
        nested_lf = (
            one_column_lf
            .filter(pl.col(column_name).list.len() > 0)
            .explode(column_name)
            .unnest(column_name)
        )
        # fmt: on
        if isinstance(data.lazyframe, pl.LazyFrame):
            nested_cls.validate(nested_lf)
        else:
            nested_cls.validate(nested_lf.collect(engine="streaming"))

        return data.lazyframe.select(pl.lit(True))

    @classmethod
    def _check_nested_struct(cls, data: PolarsData, nested_cls: type, polars_schema: pl.Schema):
        """Use this in a custom check. Pass the nested model as pandera_model."""
        column_name = data.key

        lf = data.lazyframe

        # may be expensive, consider making it optional
        actual = lf.collect_schema()[column_name]
        expected = pl.Struct(polars_schema)

        if actual != expected:
            raise SchemaError(polars_schema, lf, f"Schema mismatch for {column_name}: {actual} != {expected}")

        nested_lf = lf.select(column_name).unnest(column_name)
        if isinstance(data.lazyframe, pl.LazyFrame):
            nested_cls.validate(nested_lf)
        else:
            nested_cls.validate(nested_lf.collect(engine="streaming"))

        return data.lazyframe.select(pl.lit(True))
