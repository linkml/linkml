import re
from pathlib import Path

import pytest

from linkml.utils.schema_builder import SchemaBuilder
from tests.test_compliance.runner import (
    PYDANTIC_ROOT_CLASS,
    PYDANTIC,
    CLASS_C,
    SLOT_S1,
    SLOT_S2,
    SLOT_S3,
    EXAMPLE_STRING_VALUE_1,
    EXAMPLE_STRING_VALUE_2,
    EXAMPLE_STRING_VALUE_3,
    Snippet,
    FeatureCheck,
    _as_dict,
    run,
    GeneratorCheck,
    PYTHON_DATACLASSES,
    PYTHON_DATACLASSES_ROOT_CLASS,
    JSON_SCHEMA,
    SLOT_S4,
)


@pytest.fixture
def schema_builder() -> SchemaBuilder:
    sb = SchemaBuilder()
    sb.add_defaults()
    return sb


def attach(schema_builder: SchemaBuilder, t: FeatureCheck):
    t.example_schema = _as_dict(schema_builder.schema)


# NOTES:
# - formatting of indented code TBD, see https://github.com/psf/black/issues/1540

def test_attributes(schema_builder):
    schema_builder.add_class(CLASS_C, slots=[SLOT_S1, SLOT_S2], use_attributes=True)
    t = FeatureCheck(
        feature="attributes",
        type="attributes",
        generator_checks={
            PYDANTIC: GeneratorCheck(
                snippets=[
                    Snippet(
                        text=f"""
                               class C({PYDANTIC_ROOT_CLASS}):
                                   s1: Optional[str] = Field(None)
                                   s2: Optional[str] = Field(None)
                               """
                    ),
                ],
            ),
            PYTHON_DATACLASSES: GeneratorCheck(
                snippets=[
                    Snippet(
                        text=f"""
                               @dataclass
                               class C({PYTHON_DATACLASSES_ROOT_CLASS}):
                               """
                    ),
                ],
            ),
            JSON_SCHEMA: GeneratorCheck(
                snippets=[
                    Snippet(
                        object={
                            "$defs": {
                                "C": {
                                    "additionalProperties": False,
                                    "description": "",
                                    "properties": {
                                        "s1": {"type": "string"},
                                        "s2": {"type": "string"},
                                    },
                                    "title": "C",
                                    "type": "object",
                                }
                            }
                        }
                    ),
                ],
            ),
        },
    )
    t.add_instance_test(
        CLASS_C,
        {},
        True,
        "object may be empty",
    )
    t.add_instance_test(
        CLASS_C,
        {
            SLOT_S1: EXAMPLE_STRING_VALUE_1,
        },
        True,
        "not all attributes need to be specified",
    )
    t.add_instance_test(
        CLASS_C,
        {
            SLOT_S1: EXAMPLE_STRING_VALUE_1,
            SLOT_S2: EXAMPLE_STRING_VALUE_2,
        },
        True,
        "all attributes can be specified",
    )
    t.add_instance_test(
        CLASS_C,
        {
            SLOT_S1: EXAMPLE_STRING_VALUE_1,
            SLOT_S2: EXAMPLE_STRING_VALUE_2,
            SLOT_S3: EXAMPLE_STRING_VALUE_3,
        },
        False,
        "attributes not in the class are not allowed",
    )
    attach(schema_builder, t)
    run(t)


def test_required(schema_builder):
    schema_builder.add_slot(SLOT_S1, required=True)
    schema_builder.add_class(CLASS_C, slots=[SLOT_S1, SLOT_S2])
    t = FeatureCheck(
        feature="required",
        type="required",
        generator_checks={
            PYDANTIC: GeneratorCheck(
                snippets=[
                    Snippet(
                        text=("class C({PYDANTIC_ROOT_CLASS}):\n" "   s1: str"),
                    ),
                ],
            ),
            PYTHON_DATACLASSES: GeneratorCheck(
                snippets=[
                    Snippet(text=("@dataclass\n" 
                                  "class C({PYTHON_DATACLASSES_ROOT_CLASS}):\n")),
                ],
            ),
        },
    )
    t.add_instance_test(
        CLASS_C,
        {
            SLOT_S1: EXAMPLE_STRING_VALUE_1,
        },
        True,
        "required attribute is specified",
    )
    t.add_instance_test(
        CLASS_C,
        {},
        False,
        "required attributes omitted",
    )
    attach(schema_builder, t)
    run(t)


def test_cardinality(schema_builder):
    schema_builder.add_slot(SLOT_S1)
    schema_builder.add_slot(SLOT_S2, multivalued=True)
    schema_builder.add_slot(SLOT_S3, required=True)
    schema_builder.add_slot(SLOT_S4, multivalued=True, required=True)
    schema_builder.add_class(CLASS_C, slots=[SLOT_S1, SLOT_S2, SLOT_S3, SLOT_S4])
    t = FeatureCheck(
        feature="cardinality",
        type="cardinality",
        generator_checks={
            PYDANTIC: GeneratorCheck(
                snippets=[
                    Snippet(
                        text=f"""
                              class C({PYDANTIC_ROOT_CLASS}):
                                  s1: Optional[str] = Field(None)
                                  s2: Optional[List[str]] = Field(default_factory=list)
                                  s3: str = Field(...)
                                  s4: List[str] = Field(default_factory=list)
                              """
                    ),
                ],
            ),
            PYTHON_DATACLASSES: GeneratorCheck(
                snippets=[
                    Snippet(
                        text=f"""
                             @dataclass
                             class C({PYTHON_DATACLASSES_ROOT_CLASS}):
                             """
                    ),
                ],
            ),
        },
    )
    t.add_instance_test(
        CLASS_C,
        {
            SLOT_S3: "",
            SLOT_S4: [EXAMPLE_STRING_VALUE_1],
        },
        True,
        "s4 is multivalued. Empty string is allowed for required",
    )
    t.add_instance_test(
        CLASS_C,
        {
            SLOT_S3: ["a", "b"],
            SLOT_S4: [EXAMPLE_STRING_VALUE_1],
        },
        False,
        "s3 is single-valued yet a list is provided",
    ).add_implementation_status(PYTHON_DATACLASSES, False)
    t.add_instance_test(
        CLASS_C,
        {
            SLOT_S1: "...",
            SLOT_S2: [],
            SLOT_S3: "...",
            SLOT_S4: [],
        },
        False,
        "one or more values are required for s4",
    ).add_implementation_status(PYTHON_DATACLASSES, False).add_implementation_status(PYDANTIC, False)
    attach(schema_builder, t)
    run(t)


@pytest.mark.parametrize("pattern,values", [(r"^\S+$", ["ab", "a b"])])
def test_pattern(schema_builder, pattern, values):
    print(pattern, values)
    schema_builder.add_class(CLASS_C, slots=[SLOT_S1], use_attributes=True)
    t = FeatureCheck(
        feature="pattern",
        type="pattern",
        generator_checks={
            PYDANTIC: GeneratorCheck(supported=False),
        },
    )
    attach(schema_builder, t)
    for v in values:
        is_valid = bool(re.match(pattern, v))
        t.add_instance_test(CLASS_C, {SLOT_S1: v}, is_valid, "check for matching of regex pattern")
    run(t)
