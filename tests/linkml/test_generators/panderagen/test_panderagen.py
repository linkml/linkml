import logging
import re

import pytest

from linkml.cli.main import linkml as linkml_cli
from linkml.generators.panderagen import cli

pl = pytest.importorskip("polars", minversion="1.0", reason="Polars >= 1.0 not installed")
np = pytest.importorskip("numpy", reason="NumPY not installed")
pandera = pytest.importorskip("pandera", reason="Pandera not installed")


logger = logging.getLogger(__name__)


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
]


def test_pandera_basic_class_based(synthetic_pandera_schema):
    """
    Test generation of Pandera for class-based mode

    This test will check the generated python, but does not include a compilation step
    """
    code = synthetic_pandera_schema.serialize()

    classes = []

    class_declaration_re = re.compile(r"class (\S+)\(")

    for item in code.splitlines():
        match = class_declaration_re.search(item)
        if match:
            classes.append(match.group(1))

    expected_classes = [
        "AnyType",
        "ColumnType",
        "SimpleDictType",
        "PanderaSyntheticTableEfficient",
        "PanderaSyntheticTable",
    ]

    assert sorted(expected_classes) == sorted(classes)


def test_dump_schema_code(synthetic_pandera_schema):
    code = synthetic_pandera_schema.serialize()

    logger.info(f"\nGenerated Pandera model:\n{code}")

    assert all(column in code for column in MODEL_COLUMNS)


def test_get_metadata(compiled_synthetic_pandera_schema_module):
    logger.info(compiled_synthetic_pandera_schema_module.PanderaSyntheticTable.get_metadata())


def test_dump_synthetic_df(big_synthetic_dataframe):
    logger.info(big_synthetic_dataframe)


def test_pandera_compile_basic_class_based(
    compiled_synthetic_pandera_schema_module_serialized, big_synthetic_dataframe_serialized
):
    """
    tests compilation and validation of correct class-based schema
    """
    # raises pandera.errors.SchemaErrors, so no assert needed
    compiled_synthetic_pandera_schema_module_serialized.PanderaSyntheticTable.validate(
        big_synthetic_dataframe_serialized, lazy=True
    )


def test_pandera_validation_error_ge(compiled_synthetic_pandera_schema_module, big_synthetic_dataframe):
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
        compiled_synthetic_pandera_schema_module.PanderaSyntheticTable.validate(high_int_dataframe, lazy=True)

    assert "DATAFRAME_CHECK" in str(e.value)
    assert "less_than_or_equal_to(999)" in str(e.value)
    assert "'column': 'integer_column'" in str(e)


@pytest.mark.parametrize("bad_column", MODEL_COLUMNS)
def test_synthetic_dataframe_wrong_datatype(
    compiled_synthetic_pandera_schema_module, big_synthetic_dataframe, bad_column
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

    with pytest.raises((pandera.errors.SchemaError, pandera.errors.SchemaErrors)) as e:
        compiled_synthetic_pandera_schema_module.PanderaSyntheticTable.validate(error_dataframe, lazy=True)

    assert "WRONG_DATATYPE" in str(e.value)
    assert f"expected column '{bad_column}' to have type" in str(e.value)


@pytest.mark.parametrize("drop_column", MODEL_COLUMNS)
def test_synthetic_dataframe_boolean_error(
    compiled_synthetic_pandera_schema_module, big_synthetic_dataframe, drop_column
):
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
        compiled_synthetic_pandera_schema_module.PanderaSyntheticTable.validate(error_dataframe, lazy=True)

    assert "COLUMN_NOT_IN_DATAFRAME" in str(e.value)
    assert f"column '{drop_column}' not in dataframe" in str(e.value)


def test_inlined_object_nested_range_type_error(
    N, compiled_synthetic_pandera_schema_module, big_synthetic_dataframe, invalid_column_type_instances
):
    """Change the object column values from Int64 to Float64"""
    df_with_nested_object_type_error = big_synthetic_dataframe.with_columns(
        pl.Series(
            [
                invalid_column_type_instances[0],
            ]
            * N
        ).alias("inlined_as_object_column")
    )

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_synthetic_pandera_schema_module.PanderaSyntheticTable.validate(
            df_with_nested_object_type_error, lazy=True
        )

    error_details = e.value.message["DATA"]["CHECK_ERROR"][0]
    logger.info(f"Details for expected error: {error_details}")

    assert error_details["column"] == "inlined_as_object_column"
    assert error_details["check"] == "check_nested_struct_inlined_as_object_column"
    assert "'x'" in error_details["error"]
    assert "Float64" in error_details["error"]


def test_inlined_simple_dict_nested_range_type_error(
    compiled_synthetic_pandera_schema_module, big_synthetic_dataframe, invalid_simple_dict_column_expression
):
    """Change the simple dict column values from Int64 to Float64"""
    df_with_nested_simple_dict_type_error = big_synthetic_dataframe.with_columns(
        invalid_simple_dict_column_expression.alias("inlined_simple_dict_column")
    )

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_synthetic_pandera_schema_module.PanderaSyntheticTable.validate(
            df_with_nested_simple_dict_type_error, lazy=True
        )

    error_details = e.value.message["DATA"]["CHECK_ERROR"][0]
    logger.info(f"Details for expected error: {error_details}")

    assert error_details["column"] == "inlined_simple_dict_column"
    assert error_details["check"] == "check_nested_struct_inlined_simple_dict_column"
    assert "'x'" in error_details["error"]
    assert "Float64" in error_details["error"]


def test_inlined_dict_nested_range_type_error(
    compiled_synthetic_pandera_schema_module, big_synthetic_dataframe, invalid_inlined_dict_column_expression
):
    """Change the inlined dict column values from Int64 to Float64"""
    df_with_nested_dict_type_error = big_synthetic_dataframe.with_columns(
        invalid_inlined_dict_column_expression.alias("inlined_class_column")
    )

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_synthetic_pandera_schema_module.PanderaSyntheticTable.validate(
            df_with_nested_dict_type_error, lazy=True
        )

    error_details = e.value.message["DATA"]["CHECK_ERROR"][0]
    logger.info(f"Details for expected error: {error_details}")

    assert error_details["column"] == "inlined_class_column"
    assert error_details["check"] == "check_nested_struct_inlined_class_column"
    assert "'x'" in error_details["error"]
    assert "Float64" in error_details["error"]


def test_inlined_list_nested_range_type_error(
    compiled_synthetic_pandera_schema_module, big_synthetic_dataframe, invalid_inlined_as_list_column_expression
):
    """Change the simple dict column values from Int64 to Float64"""
    df_with_nested_dict_type_error = big_synthetic_dataframe.with_columns(
        invalid_inlined_as_list_column_expression.alias("inlined_as_list_column")
    )

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_synthetic_pandera_schema_module.PanderaSyntheticTable.validate(
            df_with_nested_dict_type_error, lazy=True
        )

    error_details = e.value.message["DATA"]["CHECK_ERROR"][0]
    logger.info(f"Details for expected error: {error_details}")

    assert error_details["column"] == "inlined_as_list_column"
    assert error_details["check"] == "check_nested_struct_inlined_as_list_column"
    assert "'x'" in error_details["error"]
    assert "Float64" in error_details["error"]


@pytest.mark.parametrize("target_class,schema", [("Organization", "organization")])
def test_cli_simple(cli_runner, test_inputs_dir, target_class, schema):
    schema_path = str(test_inputs_dir / f"{schema}.yaml")
    result = cli_runner.invoke(cli, [schema_path])

    assert result.exit_code == 0
    assert f"class {target_class}(" in result.output


def test_cli_package(cli_runner, test_inputs_dir, tmp_path):
    schema_path = str(test_inputs_dir / "organization.yaml")
    package_dir = str(tmp_path / "test_package")

    result = cli_runner.invoke(cli, ["--package", package_dir, schema_path])

    assert result.exit_code == 0
    assert (tmp_path / "test_package").exists()
    assert (tmp_path / "test_package" / "__init__.py").exists()
    assert (tmp_path / "test_package" / "panderagen_polars_schema.py").exists()
    assert (tmp_path / "test_package" / "panderagen_polars_schema_loaded.py").exists()
    assert (tmp_path / "test_package" / "panderagen_polars_schema_transform.py").exists()
    assert (tmp_path / "test_package" / "panderagen_class_based.py").exists()
    assert (tmp_path / "test_package" / "panderagen_schema_loaded.py").exists()


@pytest.mark.parametrize("target_class,schema", [("Organization", "organization")])
def test_linkml_subcommand_cli_simple(cli_runner, test_inputs_dir, target_class, schema):
    schema_path = str(test_inputs_dir / f"{schema}.yaml")
    result = cli_runner.invoke(linkml_cli, ["generate", "pandera", schema_path])

    logger.info(result.output)

    assert result.exit_code == 0
    assert f"class {target_class}(" in result.output
