import logging
import sys

import pytest
import yaml

from linkml.generators.panderagen.dict_compare import deep_compare_dicts

_MIN_POLARS_VERSION = "1.29.0"

logger = logging.getLogger(__name__)


def apply_skip_list(skip_value: str, skip_list: list[str]) -> None:
    """Skip tests that match a string (for example schema name)"""
    for n in skip_list:
        if skip_value.startswith(n):
            pytest.skip(reason=f"Skipping test due to match on {n}")


_SKIP_LIST = [
    "test_jsonpointer",
    "test_inlined_unique_keys",
    "test_nested_key",
    "test_date_types",
    "test_array",
    "test_slot_any_of",
    "test_membership",
    "test_class_boolean",
    "test_non_standard",
    "test_equals_string",
    "test_value_presence",
    "test_cardinality-MVTrue_REQFalse",
    "test_cardinality-MVTrue_REQTrue",
    "test_cardinality-ClassNameEQ_C__SlotNameEQ_sSPACE1__TypeNameEQ_tSPACE1",
    "test_cardinality-ClassNameEQ_C__SlotNameEQ_1s__TypeNameEQ_T1",
    "test_cardinality-ClassNameEQ_C__SlotNameEQ_1s__TypeNameEQ_T1",
]


class PackageHelper:
    def __init__(self, compiled_modules):
        self.compiled_modules = compiled_modules

    def class_from_module(self, module_name, class_name):
        module = self.compiled_modules[module_name]
        return getattr(module, class_name)


def check_data_pandera(
    schema, output, target_class, object_to_validate, coerced, expected_behavior, valid, polars_only=False
):
    apply_skip_list(schema["name"], _SKIP_LIST)
    if sys.version_info < (3, 11):
        pytest.skip("typing.Optional issue for polars generator in python < 3.11")
    pl = pytest.importorskip("polars", minversion=_MIN_POLARS_VERSION, reason="Polars >= 1.0 not installed")
    from linkml.generators.panderagen.dataframe_generator import DataframeGenerator
    from linkml.generators.panderagen.panderagen import PANDERA_GROUP, POLARS_GROUP

    if polars_only:
        group = POLARS_GROUP
    else:
        group = PANDERA_GROUP

    schema_yaml = yaml.dump(schema)

    logger.info(f"Validating {target_class} / {coerced}\n\n{schema_yaml}\n\n{output}")

    try:
        compiled_modules = DataframeGenerator.compile_package_from_specification(
            group, "test_pandera_package", schema_yaml
        )
        package_helper = PackageHelper(compiled_modules)

        logger.info(f"Behavior: {expected_behavior}")
        logger.info(f"Valid: {valid}")
        logger.info(f"Expected: {object_to_validate}")

        strict_schema = polars_only
        pl_schema = package_helper.class_from_module("panderagen_polars_schema", target_class)
        dataframe_serialized_form = pl.from_dicts([object_to_validate], schema=pl_schema, strict=strict_schema)

        actual_data = dataframe_serialized_form.to_dicts()[0]
        same = deep_compare_dicts(object_to_validate, actual_data)

        logger.info(f"Actual: {actual_data}")
        logger.info(f"Same: {same}")

        if same and not valid:
            logger.warning("PolaRS schema accepted an invalid object. Note the schema is not a full validator.")

        if polars_only:
            assert same
        else:
            if not same and not valid:
                logger.info("PolaRS schema did not load invalid object to validate properly")

            logger.info(dataframe_serialized_form)

            XForm = package_helper.class_from_module("panderagen_polars_schema_transform", target_class)
            dataframe_to_validate = XForm().load(dataframe_serialized_form)

            py_cls = package_helper.class_from_module("panderagen_schema_loaded", target_class)
            py_cls.validate(dataframe_to_validate, lazy=True)
    except Exception as e:
        logger.info("Actual: EXCEPTION")
        logger.info("Same: N/A")
        logger.info(f"Schema Name: {schema['name']}")
        if valid:
            logger.info(output)
            raise e
    finally:
        DataframeGenerator.cleanup_package("test_pandera_package")
