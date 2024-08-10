import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

import jsonschema
import pytest
import yaml
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from tests.test_generators.test_pythongen import make_python

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
            logging.debug(f"{p.id} address = {a.street}")
            if a.street.startswith("1 foo"):
                ok_address = True
        for h in p.has_medical_history:
            logging.debug(f"{p.id} history = {h}")
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

    with open(input_path("kitchen_sink_compliance_inst_01.yaml"), "r") as io:
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


def external_file_test(subtests, file: Union[str, Path], generator_args: Optional[Dict] = None) -> None:
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
    expected_json_schema_subset: Optional[Dict] = None,
    data_cases: Optional[List] = None,
    generator_args: Optional[Dict] = None,
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
