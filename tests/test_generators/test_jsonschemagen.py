import json
import logging
import unittest
from typing import Union

import jsonschema
import yaml
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from tests.test_generators.environment import env
from tests.test_generators.test_pythongen import make_python

SCHEMA = env.input_path("kitchen_sink.yaml")
PYTHON = env.expected_path("kitchen_sink.py")
DATA = env.input_path("kitchen_sink_inst_01.yaml")
COMPLIANCE_CASES = env.input_path("kitchen_sink_compliance_inst_01.yaml")
RULES_CASES = env.input_path("jsonschema_conditional_cases.yaml")
RANGE_UNION_CASES = env.input_path("jsonschema_range_union_cases.yaml")


class JsonSchemaTestCase(unittest.TestCase):
    """
    Tests generation of JSON-Schema
    """

    def test_jsonschema_integration(self):
        """Integration test for JsonSchemaGenerator.

        This test loads an instance object adhering to the kitchen sink schema from
        a YAML file (input/kitchen_sink_inst_01.yaml), performs sanity checks on the
        instance data, constructs a JsonSchemaGenerator from the kitchen sink schema,
        and uses the jsonschema library to verify that the generated JSON Schema is
        able to validate the instance data.
        """

        generator = JsonSchemaGenerator(
            SCHEMA, mergeimports=True, top_class="Dataset", not_closed=False
        )
        kitchen_sink_json_schema = json.loads(generator.serialize())

        kitchen_module = make_python(SCHEMA, PYTHON, False)
        inst: Dataset
        inst = yaml_loader.load(DATA, target_class=kitchen_module.Dataset)
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

        json_instance = json.loads(json_dumper.dumps(inst))
        del json_instance["@type"]

        jsonschema.validate(json_instance, kitchen_sink_json_schema)

    def test_class_uri_any(self):
        """Test that class_ur: linkml:Any results in a JSON Schema with
        "additionalProperties": true.

        See also https://github.com/linkml/linkml/issues/579
        """

        self.assertSchemaValidates(
            SCHEMA, {"$defs": {"AnyObject": {"additionalProperties": True}}}
        )

    def test_compliance_cases(self):
        """Tests various validation compliance cases.

        The file input/kitchen_sink_compliance_inst_01.yaml has multiple documents describing various
        compliance test cases. Minimally each document contains a `dataset` object which will be
        validated against the kitchen sink schema. By default each instance is expected to *fail*
        validation, but cases can also be marked with valid: true if validation should pass.
        """

        generator = JsonSchemaGenerator(
            SCHEMA, mergeimports=True, top_class="Dataset", not_closed=False
        )
        kitchen_sink_json_schema = json.loads(generator.serialize())

        generator.not_closed = True
        kitchen_sink_json_schema_not_closed = json.loads(generator.serialize())

        with open(COMPLIANCE_CASES, "r") as io:
            cases = yaml.load(io, Loader=yaml.loader.SafeLoader)

        for case in cases:
            with self.subTest(msg=case["description"]):
                skip_reason = case.get("skip", None)
                if skip_reason is not None:
                    self.skipTest(skip_reason)

                dataset = case["dataset"]
                expected_valid = case.get("valid", False)

                if case.get("closed", True):
                    schema = kitchen_sink_json_schema
                else:
                    schema = kitchen_sink_json_schema_not_closed

                do_validate = lambda: jsonschema.validate(
                    dataset,
                    schema,
                    format_checker=jsonschema.Draft7Validator.FORMAT_CHECKER,
                )
                if expected_valid:
                    # this will raise an exception and fail the test if the
                    # instance does *not* validate
                    do_validate()
                else:
                    self.assertRaises(jsonschema.ValidationError, do_validate)

    def test_type_inheritance(self):
        """Tests that a type definition's typeof slot is correctly accounted for."""

        self.externalFileTest("jsonschema_type_inheritance.yaml")

    def test_class_inheritance(self):
        """Tests that a class definition's is_a slot is correctly accounted for."""

        self.externalFileTest("jsonschema_class_inheritance.yaml", {'not_closed': False, 'include_range_class_descendants': True})

    def test_top_class_identifier(self):
        """Test that an identifier slot on the top_class becomes a required
        property in the JSON Schema."""

        self.externalFileTest("jsonschema_top_class_identifier.yaml")

    def test_value_constraints(self):
        """Test the translation of metaslots that constrain values.
        
        Tests the translation of equals_string, equals_number, pattern, maximum_value,
        and minimum_value metaslots. Additionally contains one test case that verifies
        these work with multiple ranges as well.
        """
        self.externalFileTest("jsonschema_value_constraints.yaml")

    def test_rules(self):
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
        with open(RULES_CASES) as cases_file:
            cases = yaml.safe_load(cases_file)

        for case in cases:
            with self.subTest(name=case["name"]):
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

                self.assertSchemaValidates(
                    schema, case["json_schema"], case.get("data_cases", [])
                )

    def test_rules_in_non_root_class(self):
        """Tests that rules are applied to slots in non-root classes. """

        self.externalFileTest("jsonschema_rules_in_non_root_class.yaml")

    def test_range_unions(self):
        """Tests various permutations of range unions.

        The external YAML files holds a complete LinkML schema and various data
        instances. The schema defines one class with numerous slots. Each slot
        represents a combination of:
          * simple range vs range union
          * ranges of enums, types, classes
          * multivalued true vs false
        """

        self.externalFileTest("jsonschema_range_union_cases.yaml")

    def test_multivalued_slot_cardinality(self):
        """Tests that cardinality constrains on multivalued slots are translated correctly."""

        self.externalFileTest("jsonschema_multivalued_slot_cardinality.yaml")

    def test_multivalued_element_constraints(self):
        """Tests that atomic checks on instances are applied to elements of multivalued slots."""

        self.externalFileTest("jsonschema_multivalued_element_constraints.yaml")

    def test_collection_forms(self):
        """Tests that expanded, compact, and simple dicts can be validated"""

        self.externalFileTest("jsonschema_collection_forms.yaml")

    def test_empty_inlined_as_dict_objects(self):
        """Tests that inlined objects with no non-key required slots can be null/empty"""

        self.externalFileTest("jsonschema_empty_inlined_as_dict_objects.yaml")


    # **********************************************************
    #
    #    Utility methods
    #
    # **********************************************************

    def externalFileTest(self, file: str, generator_args={'not_closed': False}) -> None:
        with open(env.input_path(file)) as f:
            test_definition = yaml.safe_load(f)

        self.assertSchemaValidates(
            yaml.dump(test_definition["schema"]),
            test_definition.get("json_schema", {}),
            test_definition.get("data_cases", []),
            generator_args=generator_args
        )

    def assertSchemaValidates(
        self,
        schema: Union[str, SchemaDefinition],
        expected_json_schema_subset={},
        data_cases=[],
        generator_args={},
    ):
        generator = JsonSchemaGenerator(schema, **generator_args)
        json_schema = json.loads(generator.serialize())
        print(generator.serialize())

        self.assertDictSubset(expected_json_schema_subset, json_schema)

        for data_case in data_cases:
            data = data_case["data"]
            with self.subTest(data=data):
                if "error_message" in data_case:
                    self.assertRaisesRegex(
                        jsonschema.ValidationError,
                        data_case["error_message"],
                        lambda: jsonschema.validate(data, json_schema),
                    )
                else:
                    jsonschema.validate(data, json_schema)

    def assertDictSubset(self, subset: dict, full: dict, path=""):
        for key in subset.keys():
            self.assertIn(key, full, f"in path {path}")

            new_path = f'{path}["{key}"]'

            self.assertIsInstance(
                full[key], subset[key].__class__, f"in path {new_path}"
            )

            if isinstance(full[key], dict):
                self.assertDictSubset(subset[key], full[key], new_path)
            else:
                self.assertEqual(full[key], subset[key], f"in path {new_path}")


if __name__ == "__main__":
    unittest.main()
