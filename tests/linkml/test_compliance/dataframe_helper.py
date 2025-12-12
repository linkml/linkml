import logging

import pytest
import yaml
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
    del polars_only  # to be added in a future PR
    apply_skip_list(schema["name"], _SKIP_LIST)
    pl = pytest.importorskip("polars", minversion=_MIN_POLARS_VERSION, reason="Polars >= 1.0 not installed")

    try:
        mod = compile_python(output)
        py_cls = getattr(mod, target_class)

        logger.info(
            f"Validating {target_class} against {object_to_validate} / {coerced} / {expected_behavior} / "
            f"{valid}\n\n{yaml.dump(schema)}\n\n{output}"
        )

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
    except Exception as e:
        if valid:
            raise e
