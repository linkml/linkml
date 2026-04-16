"""Tests for the ClassRule validation plugin."""

import pytest

from linkml.validator.plugins.rules_validation_plugin import RulesValidationPlugin
from linkml.validator.report import Severity
from linkml.validator.validation_context import ValidationContext
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader

SCHEMA = """\
id: https://w3id.org/test/rules
name: rules_test
prefixes:
  xsd: http://www.w3.org/2001/XMLSchema#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string

classes:
  Container:
    tree_root: true
    attributes:
      organizations:
        range: Organization
        multivalued: true
        inlined_as_list: true

  Organization:
    attributes:
      name:
        identifier: true
      min_salary:
        range: decimal
      score:
        range: decimal
      category:
    rules:
      - description: low-salary orgs must have non-positive score
        preconditions:
          slot_conditions:
            min_salary:
              maximum_value: 80000
        postconditions:
          slot_conditions:
            score:
              maximum_value: 0

  Measurement:
    attributes:
      id:
        identifier: true
      observation_type:
      unit:
      value:
        range: decimal
    rules:
      - description: height measurements must use cm
        preconditions:
          slot_conditions:
            observation_type:
              equals_string: height
        postconditions:
          slot_conditions:
            unit:
              equals_string: cm
      - description: weight measurements must use kg
        preconditions:
          slot_conditions:
            observation_type:
              equals_string: weight
        postconditions:
          slot_conditions:
            unit:
              equals_string: kg

  Person:
    attributes:
      name:
        identifier: true
      status:
      age:
        range: integer
    rules:
      - description: active persons must have an age
        preconditions:
          slot_conditions:
            status:
              equals_string: active
        postconditions:
          slot_conditions:
            age:
              required: true

  Contact:
    attributes:
      name:
        identifier: true
      email:
      contact_type:
    rules:
      - description: internal contacts must have company email
        preconditions:
          slot_conditions:
            contact_type:
              equals_string: internal
        postconditions:
          slot_conditions:
            email:
              pattern: "^[^@]+@example\\\\.com$"
"""


@pytest.fixture(scope="module")
def org_context():
    """Validation context targeting Organization."""
    schema = yaml_loader.load(SCHEMA, SchemaDefinition)
    return ValidationContext(schema, "Organization")


@pytest.fixture(scope="module")
def container_context():
    """Validation context targeting Container (for nested object tests)."""
    schema = yaml_loader.load(SCHEMA, SchemaDefinition)
    return ValidationContext(schema, "Container")


@pytest.fixture(scope="module")
def measurement_context():
    """Validation context targeting Measurement."""
    schema = yaml_loader.load(SCHEMA, SchemaDefinition)
    return ValidationContext(schema, "Measurement")


@pytest.fixture(scope="module")
def person_context():
    """Validation context targeting Person."""
    schema = yaml_loader.load(SCHEMA, SchemaDefinition)
    return ValidationContext(schema, "Person")


@pytest.fixture(scope="module")
def contact_context():
    """Validation context targeting Contact."""
    schema = yaml_loader.load(SCHEMA, SchemaDefinition)
    return ValidationContext(schema, "Contact")


class TestPreconditionsDoNotMatch:
    """When preconditions don't match, no rule violation should be reported."""

    def test_precondition_not_met(self, org_context):
        """An org with salary above threshold should not trigger the rule."""
        plugin = RulesValidationPlugin()
        instance = {"name": "HighPay Corp", "min_salary": 100000, "score": 5}
        results = list(plugin.process(instance, org_context))
        assert len(results) == 0

    def test_precondition_field_absent(self, org_context):
        """An org without the precondition field should not trigger the rule."""
        plugin = RulesValidationPlugin()
        instance = {"name": "No Salary Info", "score": 5}
        results = list(plugin.process(instance, org_context))
        assert len(results) == 0


class TestPreconditionsMatch:
    """When preconditions match, postconditions must hold or a violation is reported."""

    def test_postcondition_satisfied(self, org_context):
        """Low salary org with acceptable score should pass."""
        plugin = RulesValidationPlugin()
        instance = {"name": "LowPay Org", "min_salary": 50000, "score": -1}
        results = list(plugin.process(instance, org_context))
        assert len(results) == 0

    def test_postcondition_violated(self, org_context):
        """Low salary org with high score should fail."""
        plugin = RulesValidationPlugin()
        instance = {"name": "LowPay Org", "min_salary": 50000, "score": 3}
        results = list(plugin.process(instance, org_context))
        assert len(results) == 1
        assert results[0].severity == Severity.ERROR
        assert "score" in results[0].message

    def test_postcondition_boundary_value(self, org_context):
        """Boundary: salary exactly at 80000, score exactly at 0 should pass."""
        plugin = RulesValidationPlugin()
        instance = {"name": "Boundary Org", "min_salary": 80000, "score": 0}
        results = list(plugin.process(instance, org_context))
        assert len(results) == 0


class TestEqualsStringRules:
    """Test rules using equals_string constraints."""

    def test_matching_type_correct_unit(self, measurement_context):
        """Height measurement with cm unit should pass."""
        plugin = RulesValidationPlugin()
        instance = {"id": "m1", "observation_type": "height", "unit": "cm", "value": 170}
        results = list(plugin.process(instance, measurement_context))
        assert len(results) == 0

    def test_matching_type_wrong_unit(self, measurement_context):
        """Height measurement with inches should fail."""
        plugin = RulesValidationPlugin()
        instance = {"id": "m2", "observation_type": "height", "unit": "inches", "value": 67}
        results = list(plugin.process(instance, measurement_context))
        assert len(results) == 1
        assert "unit" in results[0].message

    def test_non_matching_type_any_unit(self, measurement_context):
        """Non-height/weight measurement with any unit should pass (no rule applies)."""
        plugin = RulesValidationPlugin()
        instance = {"id": "m3", "observation_type": "temperature", "unit": "fahrenheit", "value": 98}
        results = list(plugin.process(instance, measurement_context))
        assert len(results) == 0

    def test_multiple_rules_only_one_applies(self, measurement_context):
        """Weight measurement with wrong unit should only trigger the weight rule."""
        plugin = RulesValidationPlugin()
        instance = {"id": "m4", "observation_type": "weight", "unit": "lbs", "value": 150}
        results = list(plugin.process(instance, measurement_context))
        assert len(results) == 1
        assert "unit" in results[0].message


class TestRequiredPostcondition:
    """Test rules where postcondition requires a slot to be present."""

    def test_required_slot_present(self, person_context):
        """Active person with age should pass."""
        plugin = RulesValidationPlugin()
        instance = {"name": "Alice", "status": "active", "age": 30}
        results = list(plugin.process(instance, person_context))
        assert len(results) == 0

    def test_required_slot_missing(self, person_context):
        """Active person without age should fail."""
        plugin = RulesValidationPlugin()
        instance = {"name": "Bob", "status": "active"}
        results = list(plugin.process(instance, person_context))
        assert len(results) == 1

    def test_inactive_no_requirement(self, person_context):
        """Inactive person without age should pass (precondition not met)."""
        plugin = RulesValidationPlugin()
        instance = {"name": "Charlie", "status": "inactive"}
        results = list(plugin.process(instance, person_context))
        assert len(results) == 0


class TestNestedObjectRecursion:
    """Test that rules are evaluated on nested objects within a container."""

    def test_violation_in_nested_object(self, container_context):
        """A Container with an invalid nested Organization should report the violation."""
        plugin = RulesValidationPlugin()
        instance = {
            "organizations": [
                {"name": "Good Org", "min_salary": 50000, "score": -1},
                {"name": "Bad Org", "min_salary": 50000, "score": 3},
            ]
        }
        results = list(plugin.process(instance, container_context))
        assert len(results) == 1
        assert "score" in results[0].message
        assert "organizations/1" in results[0].message

    def test_no_violation_in_nested_objects(self, container_context):
        """A Container with all valid nested Organizations should pass."""
        plugin = RulesValidationPlugin()
        instance = {
            "organizations": [
                {"name": "Org A", "min_salary": 50000, "score": -1},
                {"name": "Org B", "min_salary": 90000, "score": 4},
            ]
        }
        results = list(plugin.process(instance, container_context))
        assert len(results) == 0

    def test_empty_container(self, container_context):
        """A Container with no organizations should pass."""
        plugin = RulesValidationPlugin()
        instance = {"organizations": []}
        results = list(plugin.process(instance, container_context))
        assert len(results) == 0


class TestPatternRules:
    """Test rules using pattern constraints."""

    def test_matching_pattern(self, contact_context):
        """Internal contact with company email should pass."""
        plugin = RulesValidationPlugin()
        instance = {"name": "Alice", "contact_type": "internal", "email": "alice@example.com"}
        results = list(plugin.process(instance, contact_context))
        assert len(results) == 0

    def test_non_matching_pattern(self, contact_context):
        """Internal contact with non-company email should fail."""
        plugin = RulesValidationPlugin()
        instance = {"name": "Bob", "contact_type": "internal", "email": "bob@gmail.com"}
        results = list(plugin.process(instance, contact_context))
        assert len(results) == 1
        assert "email" in results[0].message

    def test_precondition_not_met_pattern_ignored(self, contact_context):
        """External contact with any email should pass (precondition not met)."""
        plugin = RulesValidationPlugin()
        instance = {"name": "Charlie", "contact_type": "external", "email": "charlie@gmail.com"}
        results = list(plugin.process(instance, contact_context))
        assert len(results) == 0
