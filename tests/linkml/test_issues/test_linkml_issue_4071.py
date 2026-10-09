"""
Tests for https://github.com/linkml/linkml/issues/4071

``minimum_value``, ``maximum_value`` and ``equals_number`` on a multivalued slot were generated on the
``Field`` of the list itself, so pydantic raised a ``TypeError`` for every value, valid or not.
They apply to each element of the list.
"""

import pytest
from pydantic import ValidationError

from linkml.generators.pydanticgen import PydanticGenerator
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.schema_builder import SchemaBuilder


@pytest.mark.parametrize(
    "value,required,minimum_value,maximum_value,equals_number,valid",
    (
        ([10, 20, 30], False, 0, 100, None, True),
        ([10, 200, 30], False, 0, 100, None, False),
        ([10, -1, 30], False, 0, 100, None, False),
        ([10, 20, 30], True, 0, 100, None, True),
        ([10, 200, 30], True, 0, 100, None, False),
        ([], False, 0, 100, None, True),
        ([10, 20], False, 10, None, None, True),
        ([9, 20], False, 10, None, None, False),
        ([10, 20], False, None, 20, None, True),
        ([10, 21], False, None, 20, None, False),
        ([0.5, 1.5], False, 0.5, None, None, True),
        ([0.25, 1.5], False, 0.5, None, None, False),
        ([5, 5], False, None, None, 5, True),
        ([5, 6], False, None, None, 5, False),
    ),
)
def test_value_range_applies_to_elements(value, required, minimum_value, maximum_value, equals_number, valid):
    """
    Ensure that the value constraints of a multivalued slot apply to each element of the list
    in the generated pydantic model, and not to the list itself.
    """
    schema_builder = SchemaBuilder("value_range_test")
    schema_builder.add_class(
        "ValueRangeArray",
        slots=[
            SlotDefinition(
                "value_range_array",
                range="float",
                multivalued=True,
                required=required,
                minimum_value=minimum_value,
                maximum_value=maximum_value,
                equals_number=equals_number,
            )
        ],
    )
    schema_builder.add_defaults()

    mod = compile_python(PydanticGenerator(schema=schema_builder.schema).serialize())

    if valid:
        mod.ValueRangeArray(value_range_array=value)
    else:
        with pytest.raises(ValidationError):
            mod.ValueRangeArray(value_range_array=value)


@pytest.mark.parametrize(
    "value,valid",
    (
        ([1, 2], True),
        ([1], False),  # too short
        ([1, 200], False),  # element out of range
    ),
)
def test_value_range_and_cardinality(value, valid):
    """
    Ensure that value constraints apply to the elements and cardinality constraints to the list
    when a multivalued slot has both.
    """
    schema_builder = SchemaBuilder("value_range_cardinality_test")
    schema_builder.add_class(
        "ValueRangeArray",
        slots=[
            SlotDefinition(
                "value_range_array",
                range="integer",
                multivalued=True,
                minimum_cardinality=2,
                minimum_value=0,
                maximum_value=100,
            )
        ],
    )
    schema_builder.add_defaults()

    mod = compile_python(PydanticGenerator(schema=schema_builder.schema).serialize())

    if valid:
        mod.ValueRangeArray(value_range_array=value)
    else:
        with pytest.raises(ValidationError):
            mod.ValueRangeArray(value_range_array=value)
