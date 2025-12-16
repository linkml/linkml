import logging
import sys

import pytest
import yaml

from linkml.generators.panderagen.dict_compare import deep_compare_dicts
from linkml_runtime.utils.compile_python import compile_python

_MIN_POLARS_VERSION = "1.29.0"

logger = logging.getLogger(__name__)


def apply_skip_list(skip_value: str, skip_list: list[str]) -> None:
    """Skip tests that match a string (for example schema name)"""
    for n in skip_list:
        if skip_value.startswith(n):
            pytest.skip(reason=f"Skipping test due to match on {n}")


_SKIP_LIST = [
    "test_inlined-INLTrue_IALFalse_MVTrue_FKFalse",
    "test_inlined-INLTrue_IALTrue_MVTrue_FKFalse",
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


def check_data_pandera(
    schema, output, target_class, object_to_validate, coerced, expected_behavior, valid, polars_only=False
):
    apply_skip_list(schema["name"], _SKIP_LIST)
    if sys.version_info < (3, 11):
        pytest.skip("typing.Optional issue for polars generator in python < 3.11")
    pl = pytest.importorskip("polars", minversion=_MIN_POLARS_VERSION, reason="Polars >= 1.0 not installed")

    try:
        mod = compile_python(output)
        py_cls = getattr(mod, target_class)

        logger.info(
            f"Validating {target_class} against {object_to_validate} / {coerced} / {expected_behavior} / "
            f"{valid}\n\n{yaml.dump(schema)}\n\n{output}"
        )

        if polars_only:
            dataframe_to_validate = pl.DataFrame([object_to_validate], schema=py_cls, strict=True)
            actual_data = dataframe_to_validate.to_dicts()[0]
            same = deep_compare_dicts(object_to_validate, actual_data)
            if same:
                if not valid:
                    logger.warning("Polars schema accepted an invalid object. Note the schema is not a full validator.")
                else:
                    logger.info(f"polars round-trip: {object_to_validate} == {actual_data}")
            else:
                if valid:
                    assert same

            # in a future PR this will fall through to pandera when polars_only is False
            return
        else:
            dataframe_to_validate = pl.DataFrame([object_to_validate])

        try:
            schema_name = schema.get("name", "")
            polars_schema = py_cls.generate_polars_schema(object_to_validate, parser=True)

            if schema_name.startswith("test_date_types") or schema_name.startswith("test_enum_alias"):
                dataframe_to_validate = pl.DataFrame(object_to_validate, schema=polars_schema, strict=False)
            elif dataframe_to_validate.item() is None:
                dataframe_to_validate = pl.DataFrame(object_to_validate, schema=polars_schema, strict=False)
        except Exception:
            pass

        logger.info(dataframe_to_validate)
        py_cls.validate(dataframe_to_validate, lazy=True)
        py_cls.validate(dataframe_to_validate)
    except Exception as e:
        if valid:
            raise e
