import json
import logging
import unittest

import jsonschema
import yaml
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.loaders import yaml_loader

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from tests.test_generators.environment import env
from tests.test_generators.test_pythongen import make_python

SCHEMA = env.input_path("kitchen_sink.yaml")
DATA = env.input_path("kitchen_sink_inst_01.yaml")
COMPLIANCE_CASES = env.input_path("kitchen_sink_compliance_inst_01.yaml")
RULES_CASES = env.input_path("jsonschema_conditional_cases.yaml")
RANGE_UNION_CASES = env.input_path("jsonschema_range_union_cases.yaml")

class JsonSchemaTestCase(unittest.TestCase):
    """
    Tests generation of JSON-Schema
    """

    def setUp(self):
        generator = JsonSchemaGenerator(
            SCHEMA, 
            mergeimports=True, 
            top_class="Dataset", 
            not_closed=False
        )
        self.kitchen_sink_json_schema = json.loads(generator.serialize())

        generator.not_closed = True
        self.kitchen_sink_json_schema_not_closed = json.loads(generator.serialize())


    def test_jsonschema_integration(self):
        """Integration test for JsonSchemaGenerator.
        
        This test loads an instance object adhering to the kitchen sink schema from
        a YAML file (input/kitchen_sink_inst_01.yaml), performs sanity checks on the
        instance data, constructs a JsonSchemaGenerator from the kitchen sink schema, 
        and uses the jsonschema library to verify that the generated JSON Schema is 
        able to validate the instance data.
        """

        kitchen_module = make_python(False)
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
        del json_instance['@type']

        jsonschema.validate(json_instance, self.kitchen_sink_json_schema)
        

    def test_class_uri_any(self):
        """Test that class_ur: linkml:Any results in a JSON Schema with 
        "additionalProperties": true.
        
        See also https://github.com/linkml/linkml/issues/579
        """

        self.assertIn("$defs", self.kitchen_sink_json_schema)
        self.assertTrue(self.kitchen_sink_json_schema["$defs"]["AnyObject"]["additionalProperties"])


    def test_compliance_cases(self):
        """Tests various validation compliance cases.

        The file input/kitchen_sink_compliance_inst_01.yaml has multiple documents describing various
        compliance test cases. Minimally each document contains a `dataset` object which will be
        validated against the kitchen sink schema. By default each instance is expected to *fail*
        validation, but cases can also be marked with valid: true if validation should pass.
        """
        with open(COMPLIANCE_CASES, "r") as io:
            cases = yaml.load(io, Loader=yaml.loader.SafeLoader)

        for case in cases:
            with self.subTest(msg=case['description']):
                skip_reason = case.get("skip", None)
                if skip_reason is not None:
                    self.skipTest(skip_reason)

                dataset = case["dataset"]
                expected_valid = case.get("valid", False)
                
                if case.get("closed", True):
                    schema = self.kitchen_sink_json_schema
                else:
                    schema = self.kitchen_sink_json_schema_not_closed
                
                do_validate = lambda: jsonschema.validate(dataset, schema, format_checker=jsonschema.Draft7Validator.FORMAT_CHECKER)
                if expected_valid:
                    # this will raise an exception and fail the test if the 
                    # instance does *not* validate
                    do_validate()
                else:
                    self.assertRaises(jsonschema.ValidationError, do_validate)

    def test_type_inheritance(self):
        # TODO: can this be a compliance case too?
        schema = """
id: http://example.org/test_type_inheritance
name: test_type_inheritance

types:
  alpha:
    base: double 
  beta:
    typeof: alpha

slots:
  alpha_slot:
    range: alpha
  beta_slot:
    range: beta

classes:
  Test:
    slots:
      - alpha_slot
      - beta_slot
"""
        generator = JsonSchemaGenerator(schema, top_class="Test")
        json_schema = json.loads(generator.serialize())
        test_def_properties = json_schema['$defs']['Test']['properties']
        self.assertEqual(test_def_properties['alpha_slot']['type'], 'number')
        self.assertEqual(test_def_properties['beta_slot']['type'], 'number')

    def test_top_class_identifier(self):
        """Test that an identifier slot on the top_class becomes a required
        property in the JSON Schema."""

        schema = """
id: http://example.org/test_top_class_identifier
name: test_top_class_identifier

slots:
  id:
    identifier: true

classes:
  Test:
    slots:
      - id
"""
        generator = JsonSchemaGenerator(schema, top_class="Test")
        json_schema = json.loads(generator.serialize())

        self.assertIn("id", json_schema["$defs"]["Test"]["required"])
        self.assertIn("id", json_schema["required"])


    def test_value_constraints(self):
        with open(env.input_path("jsonschema_value_constraints.yaml")) as f:
            test_def = yaml.safe_load(f)
        
        generator = JsonSchemaGenerator(yaml.dump(test_def["schema"]), stacktrace=True, not_closed=False)
        json_schema = json.loads(generator.serialize())

        for data_case in test_def.get('data_cases', []):
            data = data_case['data']
            with self.subTest(data=data):
                if 'error_message' in data_case:
                    self.assertRaisesRegex(
                        jsonschema.ValidationError, 
                        data_case['error_message'],
                        lambda: jsonschema.validate(data, json_schema),
                    )
                else:
                    jsonschema.validate(data, json_schema)


    def test_rules(self):
        with open(RULES_CASES) as cases_file:
            cases = yaml.safe_load(cases_file)

        for case in cases:
            with self.subTest(name=case['name']):
                ncname = case['name'].replace(' ', '_')
                schema = SchemaDefinition(
                    id=f"http://example.org/test_rule_{ncname}",
                    name=ncname,
                    imports=[
                        "https://w3id.org/linkml/types"
                    ],
                    slots={
                        "s1": { "range": "integer" },
                        "s2": { "range": "integer" },
                        "s3": { "range": "integer" },
                        "s4": { "range": "integer" },
                    },
                    classes={
                        "Test": {
                            "slots": ["s1", "s2", "s3", "s4"],
                            "rules": case['linkml_rules']
                        }
                    }
                )
                generator = JsonSchemaGenerator(schema, top_class="Test")
                actual_json_schema = json.loads(generator.serialize())

                # Validate the structure of the generated JSON Schema
                expected_json_schema_subset = case["json_schema"]
                self.assertDictContainsSubset(expected_json_schema_subset, actual_json_schema)

                # Validate data instances against the JSON Schema
                for data_case in case.get('data_cases', []):
                    data = data_case['data']
                    with self.subTest(data=data):
                        if 'error_message' in data_case:
                            self.assertRaisesRegex(
                                jsonschema.ValidationError, 
                                data_case['error_message'],
                                lambda: jsonschema.validate(data, actual_json_schema),
                            )
                        else:
                            jsonschema.validate(data, actual_json_schema)


    def test_range_unions(self):
        with open(RANGE_UNION_CASES, "r") as f:
            cases = yaml.safe_load(f)

        generator = JsonSchemaGenerator(yaml.dump(cases["schema"]), top_class="Test")
        json_schema = json.loads(generator.serialize())

        for valid_case in cases.get("valid_cases", []):
            with self.subTest(valid_case=valid_case):
                jsonschema.validate(valid_case, json_schema)

        for invalid_case in cases.get("invalid_cases", []):
            with self.subTest(invalid_case=invalid_case):
                self.assertRaises(jsonschema.ValidationError, lambda: jsonschema.validate(invalid_case, json_schema))

if __name__ == "__main__":
    unittest.main()
