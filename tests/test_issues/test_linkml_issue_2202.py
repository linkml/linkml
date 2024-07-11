import pytest
from linkml_runtime import SchemaView
from linkml.validator import Validator, ValidationReport

minimal_household_schema = """
name: minimal_household_schema
id: http://example.com/minimal_household_schema

classes:
    NamedThing:
        slots:
            - id
  
slots:
    id:
        identifier: true
"""

minimal_household_data = """
id: xxx
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
