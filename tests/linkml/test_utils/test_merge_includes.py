"""Tests for merge_includes and merge_class_rules in mergeutils."""

import pytest

from linkml.utils.mergeutils import merge_class_rules, merge_includes
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader

BASE_SCHEMA = """\
id: https://w3id.org/test/base
name: base
prefixes:
  xsd: http://www.w3.org/2001/XMLSchema#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string

classes:
  Organization:
    attributes:
      name:
        identifier: true
      min_salary:
        range: decimal
      score:
        range: decimal
    rules:
      - description: existing base rule
        preconditions:
          slot_conditions:
            score:
              minimum_value: 0
        postconditions:
          slot_conditions:
            min_salary:
              minimum_value: 0

  Person:
    attributes:
      name:
        identifier: true
      age:
        range: integer

slots:
  shared_slot:
    range: string
"""

OVERLAY_SCHEMA = """\
id: https://w3id.org/test/overlay
name: overlay
prefixes:
  xsd: http://www.w3.org/2001/XMLSchema#
  custom: http://example.org/custom/

classes:
  Organization:
    rules:
      - description: overlay rule for low-salary orgs
        preconditions:
          slot_conditions:
            min_salary:
              maximum_value: 80000
        postconditions:
          slot_conditions:
            score:
              maximum_value: 0

  NewClass:
    attributes:
      id:
        identifier: true
      value:

slots:
  new_slot:
    range: integer
"""


@pytest.fixture
def base_schema():
    return yaml_loader.load(BASE_SCHEMA, SchemaDefinition)


@pytest.fixture
def overlay_schema():
    return yaml_loader.load(OVERLAY_SCHEMA, SchemaDefinition)


class TestMergeClassRules:
    """Test merge_class_rules appends rules from source to target."""

    def test_appends_rules(self, base_schema, overlay_schema):
        base_org = base_schema.classes["Organization"]
        overlay_org = overlay_schema.classes["Organization"]
        assert len(base_org.rules) == 1

        merge_class_rules(base_org, overlay_org)

        assert len(base_org.rules) == 2
        assert base_org.rules[0].description == "existing base rule"
        assert base_org.rules[1].description == "overlay rule for low-salary orgs"

    def test_no_rules_in_source(self, base_schema, overlay_schema):
        """Merging from a class with no rules should be a no-op."""
        base_person = base_schema.classes["Person"]
        # Person has no rules, use it as target; use NewClass (no rules) as source
        new_class = overlay_schema.classes["NewClass"]
        original_count = len(base_person.rules)

        merge_class_rules(base_person, new_class)

        assert len(base_person.rules) == original_count

    def test_deepcopy_isolation(self, base_schema, overlay_schema):
        """Merged rules should be independent copies."""
        base_org = base_schema.classes["Organization"]
        overlay_org = overlay_schema.classes["Organization"]

        merge_class_rules(base_org, overlay_org)

        # Mutate the overlay rule — base should not be affected
        overlay_org.rules[0].description = "mutated"
        assert base_org.rules[1].description == "overlay rule for low-salary orgs"


class TestMergeIncludes:
    """Test merge_includes for full schema composition."""

    def test_rules_merged_on_shared_class(self, base_schema, overlay_schema):
        merge_includes(base_schema, overlay_schema)

        org = base_schema.classes["Organization"]
        assert len(org.rules) == 2

    def test_new_class_added(self, base_schema, overlay_schema):
        assert "NewClass" not in base_schema.classes

        merge_includes(base_schema, overlay_schema)

        assert "NewClass" in base_schema.classes

    def test_existing_class_not_replaced(self, base_schema, overlay_schema):
        """Base class attributes should be preserved when overlay adds rules."""
        merge_includes(base_schema, overlay_schema)

        org = base_schema.classes["Organization"]
        assert "name" in org.attributes
        assert "min_salary" in org.attributes
        assert "score" in org.attributes

    def test_new_slot_added(self, base_schema, overlay_schema):
        assert "new_slot" not in base_schema.slots

        merge_includes(base_schema, overlay_schema)

        assert "new_slot" in base_schema.slots

    def test_existing_slot_not_replaced(self, base_schema, overlay_schema):
        merge_includes(base_schema, overlay_schema)

        assert "shared_slot" in base_schema.slots
        assert base_schema.slots["shared_slot"].range == "string"

    def test_new_prefix_added(self, base_schema, overlay_schema):
        assert "custom" not in base_schema.prefixes

        merge_includes(base_schema, overlay_schema)

        assert "custom" in base_schema.prefixes

    def test_existing_prefix_not_replaced(self, base_schema, overlay_schema):
        merge_includes(base_schema, overlay_schema)

        assert base_schema.prefixes["xsd"].prefix_reference == "http://www.w3.org/2001/XMLSchema#"

    def test_unmatched_overlay_class_ignored_for_rules(self, base_schema, overlay_schema):
        """Person exists only in base; NewClass only in overlay. No cross-contamination."""
        merge_includes(base_schema, overlay_schema)

        person = base_schema.classes["Person"]
        assert len(person.rules) == 0

    def test_multiple_includes(self, base_schema, overlay_schema):
        """Multiple overlays should compose additively."""
        second_overlay = yaml_loader.load(
            """\
id: https://w3id.org/test/overlay2
name: overlay2
classes:
  Organization:
    rules:
      - description: second overlay rule
        preconditions:
          slot_conditions:
            score:
              maximum_value: 5
        postconditions:
          slot_conditions:
            min_salary:
              maximum_value: 200000
""",
            SchemaDefinition,
        )

        merge_includes(base_schema, overlay_schema)
        merge_includes(base_schema, second_overlay)

        org = base_schema.classes["Organization"]
        assert len(org.rules) == 3
        assert org.rules[2].description == "second overlay rule"

    def test_conflicting_prefix_raises(self, base_schema):
        """Conflicting prefix references should raise ValueError."""
        conflicting_overlay = yaml_loader.load(
            """\
id: https://w3id.org/test/conflicting
name: conflicting
prefixes:
  xsd: https://example.org/conflicting-xsd/
""",
            SchemaDefinition,
        )

        with pytest.raises(ValueError):
            merge_includes(base_schema, conflicting_overlay)
