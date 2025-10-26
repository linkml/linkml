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
from linkml.generators.panderagen.dataframe_generator import DataframeGenerator  # noqa: E402
from linkml.generators.panderagen.panderagen import PANDERA_GROUP  # noqa: E402

logger = logging.getLogger(__name__)


@pytest.fixture
def test_inputs_dir():
    return Path(__file__).parent.parent / "input"


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture(scope="module")
def N():
    """Number of rows in the test dataframes, 1000 is enough to be real but not strain the build."""
    return 1000


@pytest.fixture(scope="module")
def synthetic_model_path():
    return Path(__file__).parent / "input" / "synthetic_model.yaml"


@pytest.fixture(scope="module")
def synthetic_flat_dataframe_model(synthetic_model_path):
    with open(synthetic_model_path) as f:
        return f.read()


@pytest.fixture(scope="module")
def compiled_modules(synthetic_flat_dataframe_model):
    compiled_modules = DataframeGenerator.compile_package_from_specification(
        PANDERA_GROUP, "test_package", synthetic_flat_dataframe_model
    )

    yield compiled_modules

    DataframeGenerator.cleanup_package("test_package")


@pytest.fixture(scope="module")
def compiled_synthetic_schema_module(compiled_modules):
    return compiled_modules["panderagen_polars_schema"]


@pytest.fixture(scope="module")
def compiled_synthetic_schema_loaded(compiled_modules):
    return compiled_modules["panderagen_polars_schema_loaded"]


@pytest.fixture(scope="module")
def compiled_synthetic_schema_transform(compiled_modules):
    return compiled_modules["panderagen_polars_schema_transform"]


@pytest.fixture(scope="module")
def synthetic_pandera_schema(synthetic_flat_dataframe_model):
    return PanderaDataframeGenerator(synthetic_flat_dataframe_model)


@pytest.fixture(scope="module")
def compiled_synthetic_pandera_schema_module(compiled_modules):
    """The pandera schema using the loaded backing form"""
    return compiled_modules["panderagen_schema_loaded"]


@pytest.fixture(scope="module")
def compiled_synthetic_pandera_schema_module_serialized(compiled_modules):
    return compiled_modules["panderagen_class_based"]


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
def big_synthetic_dataframe_serialized(
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
def big_synthetic_dataframe(
    big_synthetic_dataframe_serialized,
    compiled_synthetic_schema_transform,
):
    """Synthetic dataframe with inefficient inline forms converted to lists"""
    dict_to_list_transform = compiled_synthetic_schema_transform.PanderaSyntheticTable()
    return dict_to_list_transform.load(big_synthetic_dataframe_serialized)
