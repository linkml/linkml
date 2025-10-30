import json
import logging
from collections.abc import Iterable
from pathlib import Path
from typing import Optional, Union

import jsonschema
import pytest
import yaml
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.linkml_model import (
    ClassDefinition,
    EnumDefinition,
    PermissibleValue,
    SchemaDefinition,
    SlotDefinition,
)
from linkml_runtime.loaders import yaml_loader

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from tests.test_generators.test_pythongen import make_python

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.jsonschemagen


def test_jsonschema_integration(kitchen_sink_path, input_path):
    """Integration test for JsonSchemaGenerator.

    This test loads an instance object adhering to the kitchen sink schema from
    a YAML file (input/kitchen_sink_inst_01.yaml), performs sanity checks on the
    instance data, constructs a JsonSchemaGenerator from the kitchen sink schema,
    and uses the jsonschema library to verify that the generated JSON Schema is
    able to validate the instance data.
    """

    generator = JsonSchemaGenerator(kitchen_sink_path, mergeimports=True, top_class="Dataset", not_closed=False)
    kitchen_sink_json_schema = json.loads(generator.serialize())

    kitchen_module = make_python(kitchen_sink_path)
    data = input_path("kitchen_sink_inst_01.yaml")
    inst: kitchen_module.Dataset
    inst = yaml_loader.load(data, target_class=kitchen_module.Dataset)
    # p = [p for p in persons if p.id == 'P:002'][0]
    ok_address = False
    ok_history = False
    ok_metadata = True
    for p in inst.persons:
        for a in p.addresses:
            logger.debug(f"{p.id} address = {a.street}")
            if a.street.startswith("1 foo"):
                ok_address = True
        for h in p.has_medical_history:
            logger.debug(f"{p.id} history = {h}")
            if h.in_location == "GEO:1234" and h.diagnosis.name == "headache":
                ok_history = True
            # test the metadata slot, which has an unconstrained range
            if h.metadata:
                if h.metadata.anything.goes:
                    ok_metadata = True
    assert ok_address
    assert ok_history
    assert ok_metadata

    json_instance = json.loads(json_dumper.dumps(inst))
    del json_instance["@type"]

    jsonschema.validate(json_instance, kitchen_sink_json_schema)


def test_class_uri_any(kitchen_sink_path, subtests):
    """Test that class_ur: linkml:Any results in a JSON Schema with
    "additionalProperties": true.

    See also https://github.com/linkml/linkml/issues/579
    """

    expected_json_schema_subset = {"$defs": {"AnyObject": {"additionalProperties": True}}}
    data_cases = [
        {"data": {"metadata": {"anything": {"goes": "here"}}}},
        {"data": {"metadata": "anything goes here"}},
        {"data": {"metadata": 0}},
        {"data": {"metadata": None}},
        {"data": {"metadata": True}},
        {
            "data": {"metadata": ["array", "not", "allowed"]},
            "error_message": "is not valid under any of the given schemas",
        },
    ]
    assert_schema_validates(subtests, kitchen_sink_path, expected_json_schema_subset, data_cases)


def test_compliance_cases(kitchen_sink_path, input_path, subtests):
    """Tests various validation compliance cases.

    The file input/kitchen_sink_compliance_inst_01.yaml has multiple documents describing various
    compliance test cases. Minimally each document contains a `dataset` object which will be
    validated against the kitchen sink schema. By default each instance is expected to *fail*
    validation, but cases can also be marked with valid: true if validation should pass.
    """

    generator = JsonSchemaGenerator(kitchen_sink_path, mergeimports=True, top_class="Dataset", not_closed=False)
    kitchen_sink_json_schema = json.loads(generator.serialize())

    generator.not_closed = True
    kitchen_sink_json_schema_not_closed = json.loads(generator.serialize())

    with open(input_path("kitchen_sink_compliance_inst_01.yaml")) as io:
        cases = yaml.load(io, Loader=yaml.loader.SafeLoader)

    for case in cases:
        with subtests.test(msg=case["description"]):
            skip_reason = case.get("skip", None)
            if skip_reason is not None:
                pytest.skip(skip_reason)

            dataset = case["dataset"]
            expected_valid = case.get("valid", False)

            if case.get("closed", True):
                schema = kitchen_sink_json_schema
            else:
                schema = kitchen_sink_json_schema_not_closed

            def do_validate():
                jsonschema.validate(
                    dataset,
                    schema,
                    format_checker=jsonschema.Draft201909Validator.FORMAT_CHECKER,
                )

            if expected_valid:
                # this will raise an exception and fail the test if the
                # instance does *not* validate
                do_validate()
            else:
                with pytest.raises(jsonschema.ValidationError):
                    do_validate()


def test_type_inheritance(input_path, subtests):
    """Tests that a type definition's typeof slot is correctly accounted for."""

    external_file_test(subtests, input_path("jsonschema_type_inheritance.yaml"))


def test_class_inheritance(subtests, input_path):
    """Tests that a class definition's is_a slot is correctly accounted for."""

    external_file_test(
        subtests,
        input_path("jsonschema_class_inheritance.yaml"),
        {"not_closed": False, "include_range_class_descendants": True},
    )


def test_class_inheritance_multivalued(subtests, input_path):
    """Tests that a class hierarchy is accounted for when the hierarchy root is used
    as the range of a multivalued (either inlined or inlined_as_list) slot."""

    external_file_test(
        subtests,
        input_path("jsonschema_class_inheritance_multivalued.yaml"),
        {"not_closed": False, "include_range_class_descendants": True, "include_null": False},
    )


def test_top_class_identifier(subtests, input_path):
    """Test that an identifier slot on the top_class becomes a required
    property in the JSON Schema."""

    external_file_test(subtests, input_path("jsonschema_top_class_identifier.yaml"))


def test_value_constraints(subtests, input_path):
    """Test the translation of metaslots that constrain values.

    Tests the translation of equals_string, equals_number, pattern, maximum_value,
    and minimum_value metaslots. Additionally contains one test case that verifies
    these work with multiple ranges as well.
    """
    external_file_test(subtests, input_path("jsonschema_value_constraints.yaml"))


def test_rules(subtests, input_path):
    """Tests translation of various types of class rules.

    The external YAML file holds various test cases. Each test case defines
    the `rules` that will be inserted into a class of the baseline schema,
    some expected JSON Schema, and various data instances. The test iterates
    through each test case and:
      1) constructs a LinkML schema and passes it to JsonSchemaGenerator
      2) verifies that the expected JSON Schema is a subset of the actual
         JSON Schema that was generated
      3) validates each data instance against the JSON Schema and verifies
         that it either successfully validates or does not validate with
         the expected error message
    """
    with open(input_path("jsonschema_conditional_cases.yaml")) as cases_file:
        cases = yaml.safe_load(cases_file)

    for case in cases:
        with subtests.test(name=case["name"]):
            ncname = case["name"].replace(" ", "_")
            schema = SchemaDefinition(
                id=f"http://example.org/test_rule_{ncname}",
                name=ncname,
                imports=["https://w3id.org/linkml/types"],
                slots={
                    "s1": {"range": "integer"},
                    "s2": {"range": "integer"},
                    "s3": {"range": "integer"},
                    "s4": {"range": "integer"},
                },
                classes={
                    "Test": {
                        "tree_root": True,
                        "slots": ["s1", "s2", "s3", "s4"],
                        "rules": case["linkml_rules"],
                    }
                },
            )

            assert_schema_validates(subtests, schema, case["json_schema"], case.get("data_cases", []))


def test_rules_in_non_root_class(subtests, input_path):
    """Tests that rules are applied to slots in non-root classes."""

    external_file_test(subtests, input_path("jsonschema_rules_in_non_root_class.yaml"))


def test_range_unions(subtests, input_path):
    """Tests various permutations of range unions.

    The external YAML files holds a complete LinkML schema and various data
    instances. The schema defines one class with numerous slots. Each slot
    represents a combination of:
      * simple range vs range union
      * ranges of enums, types, classes
      * multivalued true vs false
    """

    external_file_test(subtests, input_path("jsonschema_range_union_cases.yaml"))


def test_multivalued_slot_cardinality(subtests, input_path):
    """Tests that cardinality constrains on multivalued slots are translated correctly."""

    external_file_test(subtests, input_path("jsonschema_multivalued_slot_cardinality.yaml"))


def test_multivalued_element_constraints(subtests, input_path):
    """Tests that atomic checks on instances are applied to elements of multivalued slots."""

    external_file_test(subtests, input_path("jsonschema_multivalued_element_constraints.yaml"))


def test_collection_forms(subtests, input_path):
    """Tests that expanded, compact, and simple dicts can be validated"""

    external_file_test(subtests, input_path("jsonschema_collection_forms.yaml"))


def test_empty_inlined_as_dict_objects(subtests, input_path):
    """Tests that inlined objects with no non-key required slots can be null/empty"""

    external_file_test(subtests, input_path("jsonschema_empty_inlined_as_dict_objects.yaml"))


def test_required_slot_condition_in_rule(subtests, input_path):
    """Tests required: true/false on slot conditions in rules"""

    external_file_test(subtests, input_path("jsonschema_required_slot_condition_in_rule.yaml"))


def test_missing_top_class(input_path, caplog):
    JsonSchemaGenerator(input_path("kitchen_sink.yaml"), top_class="NotARealClass")
    assert "No class in schema named NotARealClass" in caplog.text


def test_rule_inheritance(subtests, input_path):
    """Tests that rules are inherited from superclasses"""

    external_file_test(subtests, input_path("jsonschema_rule_inheritance.yaml"))


def test_title_from_name_slot(subtests, input_path):
    """Tests that the JSON Schema title is taken from name slot."""
    external_file_test(subtests, input_path("jsonschema_title_from_name.yaml"))


def test_title_from_name_slot_when_title_missing(subtests, input_path):
    """Tests that the JSON Schema title is taken from name slot when title is missing."""
    external_file_test(subtests, input_path("jsonschema_title_from_name_missing_title.yaml"), {"title_from": "title"})


def test_schama_title_from_title_slot(subtests, input_path):
    """Tests that the JSON Schema title is taken from title slot if option specified."""
    external_file_test(subtests, input_path("jsonschema_title_from_title.yaml"), {"title_from": "title"})


def test_class_title_from_title_slot(subtests, input_path):
    """Tests that the class-based sub-schema title is taken from title slot if option specified."""
    external_file_test(subtests, input_path("jsonschema_class_title_from_title.yaml"), {"title_from": "title"})


def test_enum_title_from_title_slot(subtests, input_path):
    """Tests that the enum-based sub-schema title is taken from title slot if option specified."""
    external_file_test(subtests, input_path("jsonschema_enum_title_from_title.yaml"), {"title_from": "title"})


def test_slot_title_from_title_slot(subtests, input_path):
    """Tests that the slot-based sub-schema title is taken from title slot if option specified."""
    external_file_test(subtests, input_path("jsonschema_slot_title_from_title.yaml"), {"title_from": "title"})


@pytest.mark.parametrize("not_closed", [True, False])
def test_slot_not_required_nullability(input_path, not_closed):
    """
    Non-required slots should also have an allowed "null" type so that the key can be present
    in data without a value (in addition to the key being allowed to be absent)

    References:
        - https://github.com/linkml/linkml/issues/2155
    """
    schema = input_path("not_required.yaml")
    generator = JsonSchemaGenerator(schema, mergeimports=True, top_class="Optionals", not_closed=not_closed)
    generated = json.loads(generator.serialize())
    properties = generated["$defs"]["Optionals"]["properties"]
    for key, prop in properties.items():
        if "type" in prop:
            assert "null" in prop["type"], f"{key} does not allow null"
        elif "anyOf" in prop:
            assert {"type": "null"} in prop["anyOf"], f"{key} does not allow null"


def test_lifecycle_classes(kitchen_sink_path):
    """We can modify the generation process by subclassing lifecycle hooks"""

    class TestJsonSchemaGen(JsonSchemaGenerator):
        def before_generate_classes(self, cls: Iterable[ClassDefinition], sv: SchemaView) -> Iterable[ClassDefinition]:
            cls = [c for c in cls]

            # delete a class and make sure we don't get it in the output
            assert cls[0].name == "activity"
            del cls[0]
            return cls

        def before_generate_class(self, cls: ClassDefinition, sv: SchemaView) -> ClassDefinition:
            # change all the descriptions, idk
            cls.description = "TEST MODIFYING CLASSES"
            return cls

        def after_generate_class(self, cls, sv: SchemaView):
            # make additionalProperties True
            cls.schema_["additionalProperties"] = True
            return cls

    generator = TestJsonSchemaGen(kitchen_sink_path, mergeimports=True, top_class="Dataset", not_closed=False)
    schema = json.loads(generator.serialize())
    assert "Activity" not in schema["$defs"]
    for cls in schema["$defs"].values():
        if "enum" in cls:
            continue
        assert cls["additionalProperties"]
        assert cls["description"] == "TEST MODIFYING CLASSES"


def test_lifecycle_slots(kitchen_sink_path):
    """We can modify the generation process by subclassing lifecycle hooks"""

    class TestJsonSchemaGen(JsonSchemaGenerator):
        def before_generate_class_slots(
            self, slot: Iterable[SlotDefinition], cls, sv: SchemaView
        ) -> Iterable[SlotDefinition]:
            # make a new slot that's the number of slots for some reason
            slot = [s for s in slot]
            slot.append(SlotDefinition(name="number_of_slots", range="integer", ifabsent=f"integer({len(slot)})"))
            return slot

        def before_generate_class_slot(self, slot: SlotDefinition, cls, sv: SchemaView) -> SlotDefinition:
            slot.description = "TEST MODIFYING SLOTS"
            return slot

        def after_generate_class_slot(self, slot, cls, sv: SchemaView):
            # make em all required
            if "type" not in slot.schema_:
                slot.schema_["type"] = ["faketype"]
            elif isinstance(slot.schema_["type"], list):
                slot.schema_["type"].append("faketype")
            else:
                slot.schema_["type"] = [slot.schema_["type"], "faketype"]

            return slot

    generator = TestJsonSchemaGen(kitchen_sink_path, mergeimports=True, top_class="Dataset", not_closed=False)
    schema = json.loads(generator.serialize())

    for cls in schema["$defs"].values():
        if "enum" in cls:
            continue
        assert "number_of_slots" in cls["properties"]
        for prop in cls["properties"].values():
            assert prop["description"] == "TEST MODIFYING SLOTS"
            assert "faketype" in prop["type"]


def test_extra_slots_false(input_path):
    """
    No extra slots allowed
    """
    valid_data = {"not_allowed": {"x": 1}}
    invalid_data = {
        "not_allowed": {
            "x": 1,
            "y": 2,
        }
    }
    schema = input_path("extra_slots.yaml")
    generator = JsonSchemaGenerator(schema, top_class="Container", mergeimports=True)
    generated = json.loads(generator.serialize())

    jsonschema.validate(valid_data, generated)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(invalid_data, generated)


@pytest.mark.parametrize("test_model", ["allowed", "any_class"])
def test_extra_slots_true(input_path, test_model: str):
    """
    Extra slots allowed
    """
    valid_data = {
        test_model: {"x": 1, "whatever": "else", "we": {"want": ["in", "here", True]}},
    }
    schema = input_path("extra_slots.yaml")
    generator = JsonSchemaGenerator(schema, top_class="Container", mergeimports=True)
    generated = json.loads(generator.serialize())

    jsonschema.validate(valid_data, generated)


def test_extra_slots_string(input_path):
    """
    Extra slots allowed if they are strings
    """
    valid_data = {
        "extra_string": {"x": 1, "y": "string"},
    }
    invalid_data = {
        "extra_string": {
            "x": 1,
            "y": 2,
        }
    }
    schema = input_path("extra_slots.yaml")
    generator = JsonSchemaGenerator(schema, top_class="Container", mergeimports=True)
    generated = json.loads(generator.serialize())

    jsonschema.validate(valid_data, generated)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(invalid_data, generated)


def test_extra_slots_class(input_path):
    """
    Extra slots allowed if they match some classdef
    """
    valid_data = {
        "extra_class": {"x": 1, "another": {"y": "string"}, "third": {"y": "some string"}},
    }
    invalid_data = {
        "extra_class": {
            "x": 1,
            "another": {"y": 1},
        }
    }
    schema = input_path("extra_slots.yaml")
    generator = JsonSchemaGenerator(schema, top_class="Container", mergeimports=True)
    generated = json.loads(generator.serialize())

    jsonschema.validate(valid_data, generated)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(invalid_data, generated)


def test_extra_slots_anyof(input_path):
    """
    Extra slots allowed if they match a union of types
    """
    valid_data = {
        "extra_anyof": {"x": 1, "another": "hey", "third": 2},
    }
    invalid_data = {
        "extra_anyof": {
            "x": 1,
            "another": True,
        }
    }
    schema = input_path("extra_slots.yaml")
    generator = JsonSchemaGenerator(schema, top_class="Container", mergeimports=True)
    generated = json.loads(generator.serialize())

    jsonschema.validate(valid_data, generated)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(invalid_data, generated)


def test_extra_slots_cardinality(input_path):
    """
    Extra slots allowed if they match some extended slot expression like `AnyOf`
    """
    valid_data = {
        "extra_cardinality": {"x": 1, "another": [1, 2, 3, 4, 5]},
    }
    invalid_data = {"extra_cardinality": {"x": 1, "another": [1, 2, 3, 4, 5, 6]}}
    schema = input_path("extra_slots.yaml")
    generator = JsonSchemaGenerator(schema, top_class="Container", mergeimports=True)
    generated = json.loads(generator.serialize())

    jsonschema.validate(valid_data, generated)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(invalid_data, generated)


# **********************************************************
#
#    Utility functions
#
#    TODO: in the conversion from unittest to pytest, the
#    unittest.subTest method was replaced by the pytest-subtests
#    plugin which provides a `subtests` fixture. The most
#    straightforward port was to pass this fixture from each
#    test_ function to these utility functions. We should see
#    if pytest provides a more elegant mechanism to avoid always
#    passing this fixture around.
#
# **********************************************************


def external_file_test(subtests, file: Union[str, Path], generator_args: Optional[dict] = None) -> None:
    if generator_args is None:
        generator_args = {"not_closed": False, "include_null": False}

    with open(file) as f:
        test_definition = yaml.safe_load(f)

    assert_schema_validates(
        subtests,
        yaml.dump(test_definition["schema"]),
        test_definition.get("json_schema", {}),
        test_definition.get("data_cases", []),
        generator_args=generator_args,
    )


def assert_schema_validates(
    subtests,
    schema: Union[str, SchemaDefinition],
    expected_json_schema_subset: Optional[dict] = None,
    data_cases: Optional[list] = None,
    generator_args: Optional[dict] = None,
):
    if generator_args is None:
        generator_args = {}
    if data_cases is None:
        data_cases = []
    if expected_json_schema_subset is None:
        expected_json_schema_subset = {}

    generator = JsonSchemaGenerator(schema, **generator_args)
    json_schema = json.loads(generator.serialize())

    assert_dict_subset(expected_json_schema_subset, json_schema)

    for data_case in data_cases:
        data = data_case["data"]
        with subtests.test(data=data):
            if "error_message" in data_case:
                with pytest.raises(jsonschema.ValidationError, match=data_case["error_message"]):
                    jsonschema.validate(data, json_schema)
            else:
                jsonschema.validate(data, json_schema)


def assert_dict_subset(subset: dict, full: dict, path=""):
    for key in subset.keys():
        assert key in full, f"in path {path}"

        new_path = f'{path}["{key}"]'

        assert isinstance(full[key], subset[key].__class__), f"in path {new_path}"

        if isinstance(full[key], dict):
            assert_dict_subset(subset[key], full[key], new_path)
        else:
            assert full[key] == subset[key], f"in path {new_path}"


def test_preserve_names():
    """Test that preserve_names option preserves original LinkML names in JSON Schema.

    Tests both class names and property names with underscores and mixed case.
    """
    schema = SchemaDefinition(
        id="https://example.com/test",
        name="test_schema",
        classes={
            "foo": ClassDefinition(name="foo", slots=["_bar", "mySlot"]),
            "My_Class": ClassDefinition(name="My_Class", slots=["other"]),
        },
        slots={
            "_bar": SlotDefinition(name="_bar", range="string"),
            "mySlot": SlotDefinition(name="mySlot", range="integer"),
            "other": SlotDefinition(name="other", range="My_Class", inlined=True),
        },
    )

    # Test default behavior (names are normalized)
    generator_default = JsonSchemaGenerator(schema=schema)
    json_schema_default = json.loads(generator_default.serialize())

    assert "Foo" in json_schema_default["$defs"]
    assert "MyClass" in json_schema_default["$defs"]
    assert "foo" not in json_schema_default["$defs"]
    assert "My_Class" not in json_schema_default["$defs"]

    properties_default = json_schema_default["$defs"]["Foo"]["properties"]
    assert "_bar" in properties_default
    assert "mySlot" in properties_default

    # Test preserve_names behavior (names are preserved)
    generator_preserve = JsonSchemaGenerator(schema=schema, preserve_names=True)
    json_schema_preserve = json.loads(generator_preserve.serialize())

    assert "foo" in json_schema_preserve["$defs"]
    assert "My_Class" in json_schema_preserve["$defs"]
    assert "Foo" not in json_schema_preserve["$defs"]
    assert "MyClass" not in json_schema_preserve["$defs"]

    properties_preserve = json_schema_preserve["$defs"]["foo"]["properties"]
    assert "_bar" in properties_preserve
    assert "mySlot" in properties_preserve

    # Test that references also use preserved names
    other_property = json_schema_preserve["$defs"]["My_Class"]["properties"]["other"]
    assert "anyOf" in other_property
    assert other_property["anyOf"][0]["$ref"] == "#/$defs/My_Class"

    # Test top-level schema selection with preserve_names
    generator_preserve_top = JsonSchemaGenerator(schema=schema, preserve_names=True, top_class="My_Class")
    json_schema_preserve_top = json.loads(generator_preserve_top.serialize())

    # When preserve_names=True, top_class should match exactly with class name
    # The schema should have the preserved class name in $defs and reference it
    assert "My_Class" in json_schema_preserve_top["$defs"]
    if "$ref" in json_schema_preserve_top:
        assert json_schema_preserve_top["$ref"] == "#/$defs/My_Class"

    # Test default behavior for top-level schema selection
    generator_default_top = JsonSchemaGenerator(schema=schema, top_class="My_Class")
    json_schema_default_top = json.loads(generator_default_top.serialize())

    # When preserve_names=False (default), top_class should be normalized for comparison
    assert "MyClass" in json_schema_default_top["$defs"]
    if "$ref" in json_schema_default_top:
        assert json_schema_default_top["$ref"] == "#/$defs/MyClass"

    # Test additional edge cases for coverage

    # Test with enum for coverage
    enum_schema = SchemaDefinition(
        id="https://example.com/test_enum",
        name="test_enum_schema",
        classes={
            "Test_Class": ClassDefinition(name="Test_Class", slots=["enum_slot"]),
        },
        slots={
            "enum_slot": SlotDefinition(name="enum_slot", range="Test_Enum"),
        },
        enums={
            "Test_Enum": EnumDefinition(
                name="Test_Enum",
                permissible_values={
                    "VALUE_ONE": PermissibleValue(text="VALUE_ONE"),
                },
            ),
        },
    )

    # Test preserve_names with enum
    generator_enum = JsonSchemaGenerator(schema=enum_schema, preserve_names=True)
    json_schema_enum = json.loads(generator_enum.serialize())

    # Check that enum names are preserved
    assert "Test_Enum" in json_schema_enum["$defs"]
    assert "Test_Class" in json_schema_enum["$defs"]

    # Check that enum values are handled correctly
    enum_def = json_schema_enum["$defs"]["Test_Enum"]
    assert "VALUE_ONE" in enum_def["enum"]

    # Test add_lax_def canonical name assignment
    gen_lax = JsonSchemaGenerator(schema=enum_schema, preserve_names=False)
    json_obj = gen_lax.generate()
    json_obj.add_lax_def(["Test_Name"], "id")
    assert "TestName" in json_obj._lax_forward_refs

    gen_preserve = JsonSchemaGenerator(schema=enum_schema, preserve_names=True)
    json_obj_preserve = gen_preserve.generate()
    json_obj_preserve.add_lax_def(["Test_Name"], "id")
    assert "Test_Name" in json_obj_preserve._lax_forward_refs
