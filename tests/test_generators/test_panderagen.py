import logging
import re

import pytest

from linkml.generators.panderagen import PanderaGenerator

logger = logging.getLogger(__name__)


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
  PanderaSyntheticTable:
    attributes:
      bool_column:
        range: boolean
        required: true
      integer_column:
        range: integer
        required: true
        minimum_value: 0
        maximum_value: 999
      float_column:
        range: float
        required: true
      string_column:
        range: string
        required: true
      date_column:
        range: date
        required: true
      datetime_column:
        range: datetime
        required: true
      enum_column:
        range: SyntheticEnum
        required: true
      ontology_enum_column:
        range: SyntheticEnumOnt
        required: true

enums:
  SyntheticEnum:
    permissible_values:
      ANIMAL:
      VEGETABLE:
      MINERAL:

  SyntheticEnumOnt:
    permissible_values:
      fiction: ex:000001
      non fiction: ex:000002
"""


MODEL_COLUMNS = [
    "bool_column",
    "integer_column",
    "float_column",
    "string_column",
    "date_column",
    "datetime_column",
    "enum_column",
    "ontology_enum_column",
]


@pytest.fixture(scope="module")
def np():
    """The numpy package is optional? so use fixtures and importorskip to only run tests when it's installed"""
    return pytest.importorskip("numpy", minversion="1.0", reason="Polars >= 1.0 not installed")


@pytest.fixture(scope="module")
def pl():
    """The PolaRS package is optional, so use fixtures and importorskip to only run tests when it's installed"""
    return pytest.importorskip("polars", minversion="1.0", reason="Polars >= 1.0 not installed")


@pytest.fixture(scope="module")
def pandera():
    """The pandera package is optional, so use fixtures and importorskip to only run tests when it's installed"""
    return pytest.importorskip("pandera", reason="Pandera not installed")


@pytest.fixture(scope="module")
def N():
    """Number of rows in the test dataframes, 1M is enough to be real but not strain most machines."""
    return 1000000


@pytest.fixture(scope="module")
def big_synthetic_dataframe(pl, np, N):
    test_enum = pl.Enum(["ANIMAL", "VEGETABLE", "MINERAL"])
    test_ont_enum = pl.Enum(["fiction", "non fiction"])

    # fmt: off
    return (
        pl.DataFrame(
            {
                "bool_column": np.random.choice([True, False], size=N),
                "integer_column": np.random.choice(range(100), size=N),
                "float_column": np.random.choice([1.0, 2.0, 3.0], size=N),
                "string_column": np.random.choice(["this", "that"], size=N),
                "date_column": np.random.choice(["2021-03-27", "2021-03-28"], size=N),
                "datetime_column": np.random.choice(["2021-03-27 03:00", "2021-03-28 03:00"], size=N),
                "enum_column": pl.Series(np.random.choice(["ANIMAL", "VEGETABLE", "MINERAL"], size=N), dtype=test_enum),
                "ontology_enum_column": pl.Series(
                    np.random.choice(["fiction", "non fiction"], size=N), dtype=test_ont_enum
                )
            }
        )
        .with_columns(
            pl.col("date_column").str.to_date(),
            pl.col("datetime_column").str.to_datetime()
        )
    )
    # fmt: on


@pytest.fixture(scope="module")
def synthetic_schema(synthetic_flat_dataframe_model):
    return PanderaGenerator(synthetic_flat_dataframe_model)


@pytest.fixture(scope="module")
def compiled_synthetic_schema_module(synthetic_schema):
    return synthetic_schema.compile_pandera(compile_python_dataclasses=False)


def test_pandera_basic_class_based(synthetic_schema):
    """
    Test generation of Pandera for classed-based mode

    This test will check the generated python, but does not include a compilation step
    """
    code = synthetic_schema.generate_pandera()  # default is class-based

    logger.info(f"\nGenerated Pandera model:\n{code}")

    classes = []

    class_declaration_re = re.compile(r"class (\S+)\(")

    for item in code.splitlines():
        match = class_declaration_re.search(item)
        if match:
            classes.append(match.group(1))

    expected_classes = ["PanderaSyntheticTable"]

    assert sorted(expected_classes) == sorted(classes)


#
# TODO: note that this is using series
#       and this page doesn't? https://pandera.readthedocs.io/en/v0.20.1/polars.html
#
def test_dump_schema_code(synthetic_schema):
    code = synthetic_schema.generate_pandera()

    assert all(column in code for column in MODEL_COLUMNS)


#
# so cool
#
def test_dump_synthetic_df(big_synthetic_dataframe):
    print(big_synthetic_dataframe)


def test_pandera_compile_basic_class_based(compiled_synthetic_schema_module, big_synthetic_dataframe):
    """
    tests compilation and validation of correct class-based schema
    """
    # raises pandera.errors.SchemaErrors, so no assert needed
    compiled_synthetic_schema_module.PanderaSyntheticTable.validate(big_synthetic_dataframe, lazy=True)


def test_pandera_validation_error_ge(pl, pandera, compiled_synthetic_schema_module, big_synthetic_dataframe):
    """
    tests ge range validation error
    """
    # fmt: off
    high_int_dataframe = (
        big_synthetic_dataframe
        .with_columns(
            pl.lit(1000, pl.Int64).alias("integer_column")
        )
    )
    # fmt: on

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_synthetic_schema_module.PanderaSyntheticTable.validate(high_int_dataframe, lazy=True)

    assert "DATAFRAME_CHECK" in str(e.value)
    assert "less_than_or_equal_to(999)" in str(e.value)
    assert "'column': 'integer_column'" in str(e)


@pytest.mark.parametrize("bad_column", MODEL_COLUMNS)
def test_synthetic_dataframe_wrong_datatype(
    pl, pandera, compiled_synthetic_schema_module, big_synthetic_dataframe, bad_column
):
    if bad_column == "bool_column":
        bad_value = None
    else:
        bad_value = False

    # fmt: off
    error_dataframe = (
        big_synthetic_dataframe
        .with_columns(
            pl.lit(bad_value).alias(bad_column)
        )
    )
    # fmt: on

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_synthetic_schema_module.PanderaSyntheticTable.validate(error_dataframe, lazy=True)

    assert "WRONG_DATATYPE" in str(e.value)
    assert f"expected column '{bad_column}' to have type" in str(e.value)


@pytest.mark.parametrize("drop_column", MODEL_COLUMNS)
def test_synthetic_dataframe_boolean_error(
    pl, pandera, compiled_synthetic_schema_module, big_synthetic_dataframe, drop_column
):

    # fmt: off
    error_dataframe = (
        big_synthetic_dataframe
        .drop(
            pl.col(drop_column)
        )
    )
    # fmt: on

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_synthetic_schema_module.PanderaSyntheticTable.validate(error_dataframe, lazy=True)

    assert "COLUMN_NOT_IN_DATAFRAME" in str(e.value)
    assert f"column '{drop_column}' not in dataframe" in str(e.value)
