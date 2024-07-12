import pprint

import pytest
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import YAMLLoader
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators import PythonGenerator
from linkml.validator import Validator, ValidationReport

import types
import sys
from importlib import util

minimal_household_schema = """
name: minimal_household_schema
id: http://example.com/minimal_household_schema

prefixes:
  linkml: https://w3id.org/linkml/
    
imports:
  - linkml:types

classes:
  NamedThing:
    slots:
      - id
  
slots:
  id:
    identifier: true
    range: curie
"""

minimal_household_data = """
id: http://example.com/minimal_household_schema/1
"""

minimal_view = SchemaView(minimal_household_schema)

validator_for_minimal = Validator(minimal_view.schema)


class TestLinkmlIssue2202:

    def test_minimal_view(self):
        assert minimal_view is not None

    def test_minimal_validation(self):
        report_from_minimal_validation: ValidationReport = validator_for_minimal.validate(minimal_household_data,
                                                                                          "NamedThing")

        assert len(report_from_minimal_validation.results) == 0

    def test_convert_to_rdf(self):
        gen = PythonGenerator(schema=minimal_household_schema)
        generated_python = gen.serialize()

        # Create a new module
        module_name = 'minimal_household_module'
        spec = util.spec_from_loader(module_name, loader=None)
        minimal_household_module = util.module_from_spec(spec)

        # Execute the code in the newly created module's namespace
        exec(generated_python, minimal_household_module.__dict__)  # todo: doesn't linkml have a compile python method?

        # Now you can access the class NamedThing from dynamic_module
        NamedThing = getattr(minimal_household_module, 'NamedThing')

        my_loader = YAMLLoader()
        minimal_instance = my_loader.load(source=minimal_household_data, target_class=NamedThing,
                                          schema_view=minimal_view)

        assert minimal_instance.id == "http://example.com/minimal_household_schema/1"
