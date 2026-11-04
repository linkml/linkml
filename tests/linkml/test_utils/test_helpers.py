import jsonschema
import pytest

from linkml.generators.jsonschemagen import json_schema_types
from linkml.utils.helpers import format_checker_for, is_simple_dict
from linkml_runtime.linkml_model import ClassDefinition, SchemaDefinition, SlotDefinition
from linkml_runtime.utils.schema_builder import SchemaBuilder
from linkml_runtime.utils.schemaview import SchemaView

SCHEMA = SchemaDefinition(
    id="testschema",
    name="testschema",
    classes=[
        ClassDefinition(name="MyClass"),
    ],
)


def test_is_simple_dict():
    sb = SchemaBuilder()
    sb.add_class(
        "SimpleDictItem",
        [
            SlotDefinition("id", identifier=True),
            SlotDefinition("value", range="string"),
        ],
        use_attributes=True,
    )
    sb.add_class(
        "DictionaryItem1",
        [
            SlotDefinition("id", identifier=True),
            SlotDefinition("value", range="string"),
            SlotDefinition("another_value", range="string"),
        ],
        use_attributes=True,
    )
    sb.add_class(
        "DictionaryItem2",
        [
            SlotDefinition("id", range="string"),
            SlotDefinition("value", range="string"),
            SlotDefinition("another_value", range="string"),
        ],
        use_attributes=True,
    )
    simple_dict_slot = SlotDefinition(
        "simple_dict", inlined=True, inlined_as_list=False, multivalued=True, range="SimpleDictItem"
    )
    no_simple_dict_slot_1 = SlotDefinition(
        "no_simple_dict1", inlined=True, inlined_as_list=False, multivalued=True, range="DictionaryItem1"
    )
    no_simple_dict_slot_2 = SlotDefinition(
        "no_simple_dict2", inlined=True, inlined_as_list=False, multivalued=True, range="DictionaryItem2"
    )
    sb.add_class("C", [simple_dict_slot, no_simple_dict_slot_1, no_simple_dict_slot_2])

    sv = SchemaView(sb.schema)

    assert is_simple_dict(sv, simple_dict_slot)
    assert not is_simple_dict(sv, no_simple_dict_slot_1)
    assert not is_simple_dict(sv, no_simple_dict_slot_2)


FORMAT_SAMPLES = {
    "date": "2020-01-01",
    "date-time": "2020-01-01T00:00:00Z",
    "time": "00:00:00Z",
    "uri": "https://example.org/x",
}
EMITTED_FORMATS = sorted({format_name for _, format_name in json_schema_types.values() if format_name})
DRAFTS = [jsonschema.Draft7Validator, jsonschema.Draft201909Validator, jsonschema.Draft202012Validator]


@pytest.mark.parametrize("validator_cls", DRAFTS)
@pytest.mark.parametrize("format_name", EMITTED_FORMATS)
def test_every_format_the_generator_emits_refuses_a_final_newline(validator_cls, format_name):
    """A format that the JSON Schema generator starts to emit needs a sample here, and this check."""
    checker = format_checker_for(validator_cls)
    assert checker.conforms(FORMAT_SAMPLES[format_name], format_name)
    assert not checker.conforms(FORMAT_SAMPLES[format_name] + "\n", format_name)


@pytest.mark.parametrize(
    ("format_name", "value"),
    [("uri", "not a uri"), ("date-time", "yesterday"), ("time", "25:00:00Z")],
)
def test_format_checker_still_asks_the_library(format_name, value):
    """A wrapped check still fails a bad value, and still catches what the library raises for one."""
    assert not format_checker_for(jsonschema.Draft201909Validator).conforms(value, format_name)


@pytest.mark.parametrize("format_name", ["uri", "date-time", "time"])
def test_format_checker_passes_other_json_types_through(format_name):
    """A format constrains strings only; the ``type`` keyword deals with the rest."""
    checker = format_checker_for(jsonschema.Draft201909Validator)
    assert checker.conforms(1, format_name)
    assert checker.conforms(None, format_name)


def test_format_checker_leaves_the_library_checker_alone():
    """The draft's own checker is shared by the process, so it must not change."""
    shared = jsonschema.Draft201909Validator.FORMAT_CHECKER
    before = dict(shared.checkers)
    checker = format_checker_for(jsonschema.Draft201909Validator)
    assert checker is not shared
    assert shared.checkers == before
    assert set(checker.checkers) == set(before)


def test_format_checker_skips_a_format_the_validator_does_not_have():
    """``uri`` needs an optional library, and without it the format goes unchecked, as it did before."""
    bare = jsonschema.validators.extend(jsonschema.Draft7Validator, format_checker=jsonschema.FormatChecker(formats=()))
    checker = format_checker_for(bare)
    assert checker.checkers == {}
    assert checker.conforms("https://example.org/x\n", "uri")
