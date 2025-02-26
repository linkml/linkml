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
"""


@pytest.fixture(scope="module")
def np():
    """The numpy package is optional? so use fixtures and importorskip to only run tests when it's installed
    """
    return pytest.importorskip("numpy", minversion="1.0", reason="Polars >= 1.0 not installed")


@pytest.fixture(scope="module")
def pl():
    """The PolaRS package is optional, so use fixtures and importorskip to only run tests when it's installed
    """
    return pytest.importorskip("polars", minversion="1.0", reason="Polars >= 1.0 not installed")


@pytest.fixture(scope="module")
def pandera():
    """The pandera package is optional, so use fixtures and importorskip to only run tests when it's installed
    """
    return pytest.importorskip("pandera", reason="Pandera not installed")


@pytest.fixture(scope="module")
def N():
    """Number of rows in the test dataframes, 100K is enough to be real but not strain most machines.
    """
    return 100000


@pytest.fixture(scope="module")
def big_synthetic_dataframe(pl, np, N):
    return pl.DataFrame({
        "bool_column": np.random.choice([True, False], size=N),
        "integer_column": np.random.choice(range(100), size=N),
        "float_column": np.random.choice([1.0, 2.0, 3.0], size=N),
        "string_column": np.random.choice(["this", "that"], size=N)
    })


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

    logger.info(f"generated Pandera model:\n{code}")

    classes = []

    class_declaration_re = re.compile(r"class (\S+)\(")

    for item in code.splitlines():
        match = class_declaration_re.search(item)
        if match:
            classes.append(match.group(1))

    expected_classes = [
        "PanderaSyntheticTable"
    ]

    assert sorted(expected_classes) == sorted(classes)


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
    high_int_dataframe = (
        big_synthetic_dataframe
        .with_columns(
            pl.lit(1000, pl.Int64).alias("integer_column")
        )
    )

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_synthetic_schema_module.PanderaSyntheticTable.validate(high_int_dataframe, lazy=True)

    assert "DATAFRAME_CHECK" in str(e.value)
    assert "less_than_or_equal_to(999)" in str(e.value)
    assert "'column': 'integer_column'" in str(e)


@pytest.mark.parametrize(
    "bad_column",
    ["bool_column", "integer_column", "float_column", "string_column"]
)
def test_synthetic_dataframe_wrong_datatype(pl, pandera, compiled_synthetic_schema_module, big_synthetic_dataframe, bad_column):
    if bad_column == "bool_column":
        bad_value = None
    else:
        bad_value = False

    error_dataframe = (
        big_synthetic_dataframe
        .with_columns(
            pl.lit(bad_value).alias(bad_column)
        )
    )

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_synthetic_schema_module.PanderaSyntheticTable.validate(error_dataframe, lazy=True)

    assert "WRONG_DATATYPE" in str(e.value)
    assert f"expected column '{bad_column}' to have type" in str(e.value)


@pytest.mark.parametrize(
    "drop_column",
    ["bool_column", "integer_column", "float_column", "string_column"]
)
def test_synthetic_dataframe_boolean_error(pl, pandera, compiled_synthetic_schema_module, big_synthetic_dataframe, drop_column):
    error_dataframe = (
        big_synthetic_dataframe
        .drop(
            pl.col(drop_column)
        )
    )

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_synthetic_schema_module.PanderaSyntheticTable.validate(error_dataframe, lazy=True)

    assert "COLUMN_NOT_IN_DATAFRAME" in str(e.value)
    assert f"column '{drop_column}' not in dataframe" in str(e.value)
