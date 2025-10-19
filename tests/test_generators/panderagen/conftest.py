import logging
from pathlib import Path

import pytest
from click.testing import CliRunner

# The following packages are required for these tests but optional for linkml
# avoid pytest collection errors if not installed
# see: https://docs.pytest.org/en/latest/how-to/skipping.html#skipping-on-a-missing-import-dependency
np = pytest.importorskip("numpy", minversion="1.0", reason="NumPy >= 1.0 not installed")
pl = pytest.importorskip("polars", minversion="1.0", reason="PolaRS >= 1.0 not installed")
pandera = pytest.importorskip("pandera.polars", reason="Pandera not installed")

# These depend on PolaRS and Numpy so need to be after importerskip
from linkml.generators.panderagen import PanderaDataframeGenerator  # noqa: E402

logger = logging.getLogger(__name__)


@pytest.fixture
def test_inputs_dir():
    return Path(__file__).parent.parent / "input"


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture(scope="module")
def N():
    """Number of rows in the test dataframes, 1M is enough to be real but not strain most machines."""
    return 1000


@pytest.fixture(scope="module")
def synthetic_flat_dataframe_model():
    return """\
id: https://w3id.org/linkml/examples/pandera_constraints
name: test_pandera_constraints
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://w3id.org/linkml/examples/pandera_constraints/
imports:
  - linkml:types
default_range: string
default_prefix: ex

classes:

  AnyType:
    description: the magic class_uri makes this map to linkml Any or polars Object
    class_uri: linkml:Any

  ColumnType:
    description: Nested in a column
    attributes:
      id:
        identifier: true
        range: string
      x:
        range: integer
        required: true
      y:
        range: integer
        required: true

  SimpleDictType:
    description: Nested as a simple dict
    attributes:
      id:
        identifier: True
        range: string
      x:
        range: integer
        required: true

  PanderaSyntheticTable:
    description: A flat table with a reasonably complete assortment of datatypes.
    attributes:
      identifier_column:
        description: identifier
        identifier: true
        range: integer
        required: true
      bool_column:
        description: test boolean column
        range: boolean
        required: true
        #ifabsent: true
      integer_column:
        description: test integer column with min/max values
        range: integer
        required: true
        minimum_value: 0
        maximum_value: 999
        #ifabsent: int(5)
      float_column:
        description: test float column
        range: float
        required: true
        #ifabsent: float(2.3)
      string_column:
        description: test string column
        range: string
        required: true
        pattern: "^(this)|(that)|(whatever)$"
        #ifabsent: string("whatever")
      date_column:
        description: test date column
        range: date
        required: true
        #ifabsent: date("2020-01-31")
      datetime_column:
        description: test datetime column
        range: datetime
        required: true
        #ifabsent: datetime("2020-01-31 03:23:57")
      enum_column:
        description: test enum column
        range: SyntheticEnum
        required: true
      ontology_enum_column:
        description: test enum column with ontology values
        range: SyntheticEnumOnt
        required: true
        #ifabsent: SyntheticEnumOnt(ANIMAL)
      multivalued_column:
        description: one-to-many form
        range: integer
        required: true
        multivalued: true
        inlined_as_list: true
      any_type_column:
        description: needs to have type object
        range: AnyType
        required: true

enums:
  SyntheticEnum:
    description: simple enum for tests
    permissible_values:
      ANIMAL:
      VEGETABLE:
      MINERAL:

  SyntheticEnumOnt:
    description: ontology enum for tests
    permissible_values:
      fiction: ex:000001
      non fiction: ex:000002
"""


@pytest.fixture(scope="module")
def column_type_instances():
    """valid ColumnType instances that can be used in tests"""
    return [
        pl.struct(
            pl.lit("thing_one").alias("id"),
            pl.lit(1111, dtype=pl.Int64).alias("x"),
            pl.lit(2222, dtype=pl.Int64).alias("y"),
        ),
        pl.struct(
            pl.lit("thing_two").alias("id"),
            pl.lit(3333, dtype=pl.Int64).alias("x"),
            pl.lit(4444, dtype=pl.Int64).alias("y"),
        ),
    ]


@pytest.fixture(scope="module")
def invalid_column_type_instances():
    """invalid (float values) ColumnType instances that can trigger failures."""
    return [
        pl.struct(
            pl.lit("thing_one").alias("id"),
            pl.lit(1111.0).alias("x"),
            pl.lit(2222.0).alias("y"),
        ),
        pl.struct(
            pl.lit("thing_two").alias("id"),
            pl.lit(3333.0).alias("x"),
            pl.lit(4444.0).alias("y"),
        ),
    ]


@pytest.fixture(scope="module")
def valid_inlined_dict_column_expression(column_type_instances):
    """synthetic data that conforms to the inlined_class_column schema
    using polars expression API.
    """
    # fmt: off
    return pl.struct(
        column_type_instances[0].alias("thing_one"),
        column_type_instances[1].alias("thing_two")
    )
    # fmt: on


@pytest.fixture(scope="module")
def invalid_inlined_dict_column_expression(invalid_column_type_instances):
    """synthetic data that conforms to the inlined_class_column schema
    using polars expression API.
    """
    # fmt: off
    return pl.struct(
        invalid_column_type_instances[0].alias("thing_one"),
        invalid_column_type_instances[1].alias("thing_two")
    )
    # fmt: on


@pytest.fixture(scope="module")
def valid_simple_dict_column_expression():
    """synthetic data that conforms to the inlined_simple_dict_column schema
    using polars expression API.
    """
    # fmt: off
    return pl.struct(
      pl.lit(1).alias("A"),
      pl.lit(2).alias("B"),
      pl.lit(3).alias("C")
    )
    # fmt: on


@pytest.fixture(scope="module")
def invalid_simple_dict_column_expression():
    """synthetic data with float values that does not conform to the inlined_simple_dict_column schema
    using polars expression API.
    """
    # fmt: off
    return pl.struct(
      pl.lit(1.0).alias("A"),
      pl.lit(2.0).alias("B"),
      pl.lit(3.0).alias("C")
    )
    # fmt: on


@pytest.fixture(scope="module")
def valid_inlined_as_list_column_expression(N):
    """synthetic data that conforms to the inlined_as_list_column schema
    using polars expression API.
    """
    # fmt: off
    return pl.concat_list([
      pl.struct(
          pl.Series(values=np.arange(0, N), dtype=pl.Int64).cast(pl.Utf8).alias("id"),
          pl.Series(values=np.random.choice([0, 1], size=N), dtype=pl.Int64).alias("x"),
          pl.Series(values=np.random.choice([0, 1], size=N), dtype=pl.Int64).alias("y")
      )
    ])
    # fmt: on


@pytest.fixture(scope="module")
def invalid_inlined_as_list_column_expression(N):
    """synthetic data that does not conforms to the inlined_as_list_column schema
    using polars expression API.
    """
    # fmt: off
    return pl.concat_list([
      pl.struct(
          pl.Series(values=np.arange(0, N), dtype=pl.Int64).cast(pl.Utf8).alias("id"),
          pl.Series(values=np.random.choice([0.0, 1.0], size=N), dtype=pl.Float64).alias("x"),
          pl.Series(values=np.random.choice([0.1, 1.0], size=N), dtype=pl.Float64).alias("y")
      )
    ])
    # fmt: on


@pytest.fixture(scope="module")
def big_synthetic_dataframe(
    N,
):
    """Construct a reasonably sized dataframe that complies with the PanderaSyntheticTable model"""
    test_enum = pl.Enum(["ANIMAL", "VEGETABLE", "MINERAL"])
    test_ont_enum = pl.Enum(["fiction", "non fiction"])

    # fmt: off
    df = (
        pl.DataFrame(
            {
                "identifier_column": pl.Series(np.arange(0, N), dtype=pl.Int64),
                "bool_column": pl.Series(np.random.choice([True, False], size=N), dtype=pl.Boolean),
                "integer_column": pl.Series(np.random.choice(range(100), size=N), dtype=pl.Int64),
                "float_column": pl.Series(np.random.choice([1.0, 2.0, 3.0], size=N), dtype=pl.Float64),
                "string_column": np.random.choice(["this", "that"], size=N),
                "date_column": pl.Series(
                    np.random.choice(["2021-03-27", "2021-03-28"], size=N),
                    dtype=pl.Date,
                    strict=False
                ),
                "datetime_column": pl.Series(
                    np.random.choice(["2021-03-27T03:00:00", "2021-03-28T03:00:00"], size=N),
                    dtype=pl.Datetime,
                    strict=False
                ),
                "enum_column": pl.Series(
                    np.random.choice(["ANIMAL", "VEGETABLE", "MINERAL"], size=N),
                    dtype=test_enum,
                    strict=False
                ),
                "ontology_enum_column": pl.Series(
                    np.random.choice(["fiction", "non fiction"], size=N),
                    dtype=test_ont_enum,
                    strict=False
                ),
                "multivalued_column": [[1, 2, 3],] * N,
                "any_type_column": pl.Series([1,] * N, dtype=pl.Object),
            }
        )
    )
    # fmt: on

    return df


@pytest.fixture(scope="module")
def synthetic_schema(synthetic_flat_dataframe_model):
    return PanderaDataframeGenerator(synthetic_flat_dataframe_model)


@pytest.fixture(scope="module")
def compiled_synthetic_schema_module(synthetic_schema):
    return synthetic_schema.compile_dataframe_model()
