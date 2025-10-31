import json
import logging
import re
from pathlib import Path

import pytest
from click.testing import CliRunner

from linkml.cli.main import linkml as linkml_cli
from linkml.generators.panderagen import PanderaGenerator, cli

# The following packages are required for these tests but optional for linkml
# avoid pytest collection errors if not installed
# see: https://docs.pytest.org/en/latest/how-to/skipping.html#skipping-on-a-missing-import-dependency
np = pytest.importorskip("numpy", minversion="1.0", reason="NumPy >= 1.0 not installed")
pl = pytest.importorskip("polars", minversion="1.0", reason="PolaRS >= 1.0 not installed")
pandera = pytest.importorskip("pandera.polars", reason="Pandera not installed")

logger = logging.getLogger(__name__)


@pytest.fixture
def test_inputs_dir():
    return Path(__file__).parent / "input"


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
      inlined_as_object_column:
        description: test column that is a directly nested single object
        range: ColumnType
        required: true
        inlined: true
        multivalued: false
      inlined_class_column:
        description: test column with another class inlined as a struct
        range: ColumnType
        required: true
        inlined: true
        inlined_as_list: false
        multivalued: true
      inlined_as_list_column:
        description: test column with another class inlined as a list
        range: ColumnType
        required: true
        inlined: true
        inlined_as_list: true
        multivalued: true
      inlined_simple_dict_column:
        description: test column inlined using simple dict form
        range: SimpleDictType
        multivalued: true
        inlined: true
        inlined_as_list: false
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


MODEL_COLUMNS = [
    "identifier_column",
    "bool_column",
    "integer_column",
    "float_column",
    "string_column",
    "date_column",
    "datetime_column",
    "enum_column",
    "ontology_enum_column",
    "multivalued_column",
    "any_type_column",
    "inlined_as_object_column",
    "inlined_class_column",
    "inlined_as_list_column",
    "inlined_simple_dict_column",
]


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
    valid_inlined_dict_column_expression,
    valid_simple_dict_column_expression,
    valid_inlined_as_list_column_expression,
    column_type_instances,
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
        .with_columns(
            column_type_instances[0].alias("inlined_as_object_column"),
            valid_simple_dict_column_expression.alias("inlined_simple_dict_column"),
            valid_inlined_as_list_column_expression.alias("inlined_as_list_column"),
            valid_inlined_dict_column_expression.alias("inlined_class_column")
        )
    )
    # fmt: on

    return df


@pytest.fixture(scope="module")
def synthetic_schema(synthetic_flat_dataframe_model):
    return PanderaGenerator(synthetic_flat_dataframe_model)


@pytest.fixture(scope="module")
def compiled_synthetic_schema_module(synthetic_schema):
    return synthetic_schema.compile_pandera()


def test_pandera_basic_class_based(synthetic_schema):
    """
    Test generation of Pandera for classed-based mode

    This test will check the generated python, but does not include a compilation step
    """
    code = synthetic_schema.serialize()

    classes = []

    class_declaration_re = re.compile(r"class (\S+)\(")

    for item in code.splitlines():
        match = class_declaration_re.search(item)
        if match:
            classes.append(match.group(1))

    expected_classes = ["AnyType", "ColumnType", "SimpleDictType", "PanderaSyntheticTable"]

    assert sorted(expected_classes) == sorted(classes)


def test_dump_schema_code(synthetic_schema):
    code = synthetic_schema.serialize()

    logger.info(f"\nGenerated Pandera model:\n{code}")

    assert all(column in code for column in MODEL_COLUMNS)


def test_get_metadata(compiled_synthetic_schema_module):
    logger.info(compiled_synthetic_schema_module.PanderaSyntheticTable.get_metadata())


def test_dump_synthetic_df(big_synthetic_dataframe):
    logger.info(big_synthetic_dataframe)


def test_pandera_compile_basic_class_based(compiled_synthetic_schema_module, big_synthetic_dataframe):
    """
    tests compilation and validation of correct class-based schema
    """
    # raises pandera.errors.SchemaErrors, so no assert needed
    compiled_synthetic_schema_module.PanderaSyntheticTable.validate(big_synthetic_dataframe, lazy=True)


def test_pandera_validation_error_ge(compiled_synthetic_schema_module, big_synthetic_dataframe):
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
def test_synthetic_dataframe_wrong_datatype(compiled_synthetic_schema_module, big_synthetic_dataframe, bad_column):
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

    with pytest.raises((pandera.errors.SchemaError, pandera.errors.SchemaErrors)) as e:
        compiled_synthetic_schema_module.PanderaSyntheticTable.validate(error_dataframe, lazy=True)

    assert "WRONG_DATATYPE" in str(e.value)
    assert f"expected column '{bad_column}' to have type" in str(e.value)


@pytest.mark.parametrize("drop_column", MODEL_COLUMNS)
def test_synthetic_dataframe_boolean_error(compiled_synthetic_schema_module, big_synthetic_dataframe, drop_column):
    """Note that this test accepts SchemaError as well as SchemaErrors
    even though lazy validation is performed, because nested checks
    may be run non-lazy.
    """
    # fmt: off
    error_dataframe = (
        big_synthetic_dataframe
        .drop(
            pl.col(drop_column)
        )
    )
    # fmt: on

    with pytest.raises((pandera.errors.SchemaErrors, pandera.errors.SchemaError)) as e:
        compiled_synthetic_schema_module.PanderaSyntheticTable.validate(error_dataframe, lazy=True)

    assert "COLUMN_NOT_IN_DATAFRAME" in str(e.value)
    assert f"column '{drop_column}' not in dataframe" in str(e.value)

    if len(e.value.message["SCHEMA"].keys()) > 1 or "DATA" in e.value.message:
        logger.info(json.dumps(e.value.message, indent=2))
        assert False


def test_inlined_object_nested_range_type_error(
    compiled_synthetic_schema_module, big_synthetic_dataframe, invalid_column_type_instances
):
    """Change the object column values from Int64 to Float64"""
    df_with_nested_object_type_error = big_synthetic_dataframe.with_columns(
        invalid_column_type_instances[0].alias("inlined_as_object_column")
    )

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_synthetic_schema_module.PanderaSyntheticTable.validate(df_with_nested_object_type_error, lazy=True)

    error_details = e.value.message["DATA"]["CHECK_ERROR"][0]
    logger.info(f"Details for expected error: {error_details}")

    assert error_details["column"] == "inlined_as_object_column"
    assert error_details["check"] == "check_nested_struct_inlined_as_object_column"
    assert error_details["error"] == "SchemaError(\"expected column 'x' to have type Int64, got Float64\")"


def test_inlined_simple_dict_nested_range_type_error(
    compiled_synthetic_schema_module, big_synthetic_dataframe, invalid_simple_dict_column_expression
):
    """Change the simple dict column values from Int64 to Float64"""
    df_with_nested_simple_dict_type_error = big_synthetic_dataframe.with_columns(
        invalid_simple_dict_column_expression.alias("inlined_simple_dict_column")
    )

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_synthetic_schema_module.PanderaSyntheticTable.validate(
            df_with_nested_simple_dict_type_error, lazy=True
        )

    error_details = e.value.message["DATA"]["CHECK_ERROR"][0]
    logger.info(f"Details for expected error: {error_details}")

    assert error_details["column"] == "inlined_simple_dict_column"
    assert error_details["check"] == "check_nested_struct_inlined_simple_dict_column"
    assert error_details["error"] == "SchemaError(\"expected column 'x' to have type Int64, got Float64\")"


def test_inlined_dict_nested_range_type_error(
    compiled_synthetic_schema_module, big_synthetic_dataframe, invalid_inlined_dict_column_expression
):
    """Change the inlined dict column values from Int64 to Float64"""
    df_with_nested_dict_type_error = big_synthetic_dataframe.with_columns(
        invalid_inlined_dict_column_expression.alias("inlined_class_column")
    )

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_synthetic_schema_module.PanderaSyntheticTable.validate(df_with_nested_dict_type_error, lazy=True)

    error_details = e.value.message["DATA"]["CHECK_ERROR"][0]
    logger.info(f"Details for expected error: {error_details}")

    assert error_details["column"] == "inlined_class_column"
    assert error_details["check"] == "check_nested_struct_inlined_class_column"
    assert error_details["error"] == "SchemaError(\"expected column 'x' to have type Int64, got Float64\")"


def test_inlined_list_nested_range_type_error(
    compiled_synthetic_schema_module, big_synthetic_dataframe, invalid_inlined_as_list_column_expression
):
    """Change the simple dict column values from Int64 to Float64"""
    df_with_nested_dict_type_error = big_synthetic_dataframe.with_columns(
        invalid_inlined_as_list_column_expression.alias("inlined_as_list_column")
    )

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_synthetic_schema_module.PanderaSyntheticTable.validate(df_with_nested_dict_type_error, lazy=True)

    error_details = e.value.message["DATA"]["CHECK_ERROR"][0]
    logger.info(f"Details for expected error: {error_details}")

    assert error_details["column"] == "inlined_as_list_column"
    assert error_details["check"] == "check_nested_struct_inlined_as_list_column"
    assert error_details["error"] == "SchemaError(\"expected column 'x' to have type Int64, got Float64\")"


@pytest.mark.parametrize("target_class,schema", [("Organization", "organization")])
def test_cli_simple(cli_runner, test_inputs_dir, target_class, schema):
    schema_path = str(test_inputs_dir / f"{schema}.yaml")
    result = cli_runner.invoke(cli, [schema_path])

    assert result.exit_code == 0
    assert f"class {target_class}(" in result.output


@pytest.mark.parametrize("target_class,schema", [("Organization", "organization")])
def test_linkml_subcommand_cli_simple(cli_runner, test_inputs_dir, target_class, schema):
    schema_path = str(test_inputs_dir / f"{schema}.yaml")
    result = cli_runner.invoke(linkml_cli, ["generate", "pandera", schema_path])

    logger.info(result.output)

    assert result.exit_code == 0
    assert f"class {target_class}(" in result.output
