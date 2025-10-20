from pathlib import Path

import pytest

from linkml_runtime.utils.ruleutils import get_range_as_disjunction, subclass_to_rules
from linkml_runtime.utils.schemaview import SchemaView
from tests.test_utils import INPUT_DIR


@pytest.fixture
def rules_schema():
    """SchemaView loaded with rules example schema."""
    return SchemaView(Path(INPUT_DIR) / "rules-example.yaml")


def test_disjunction_analyte_slot(rules_schema):
    """Test get_range_as_disjunction for analyte slot with any_of."""
    analyte = rules_schema.induced_slot("analyte", "Sample")
    disj = get_range_as_disjunction(analyte)
    assert disj == {"MissingValueEnum", "AnalyteEnum"}


@pytest.mark.parametrize(
    "slot_name,expected_disjunction",
    [
        ("vital_status", {"MissingValueEnum", "VitalStatusEnum"}),  # any_of with two enums
        ("primary_address", {"Address"}),  # explicit range to class
        ("age", {"int"}),  # int range
        ("encodes", {"SeqFeature"}),  # class range
        ("id", None),  # no explicit range specified
        ("name", None),  # no explicit range specified
        ("telephone", None),  # no explicit range specified
    ],
)
def test_disjunction_various_slots(rules_schema, slot_name, expected_disjunction):
    """Test get_range_as_disjunction for various slot types."""
    slot = rules_schema.get_slot(slot_name)
    disj = get_range_as_disjunction(slot)
    assert disj == expected_disjunction


def test_roll_up_protein_coding_gene(rules_schema):
    """Test subclass_to_rules for ProteinCodingGene to SeqFeature."""
    rules = subclass_to_rules(rules_schema, "ProteinCodingGene", "SeqFeature")

    # Should generate one rule
    assert len(rules) == 1

    rule = rules[0]

    # Check preconditions - uses type designator slot
    assert rule.preconditions is not None
    assert rule.preconditions.slot_conditions is not None
    assert "type" in rule.preconditions.slot_conditions

    # Check the type slot condition
    type_condition = rule.preconditions.slot_conditions["type"]
    assert type_condition.equals_string == "ProteinCodingGene"

    # Check postconditions - should have slot assignments
    assert rule.postconditions is not None
    assert rule.postconditions.slot_conditions is not None
    # Should include slots from the class
    assert "encodes" in rule.postconditions.slot_conditions
    assert "id" in rule.postconditions.slot_conditions


def test_roll_up_noncoding_gene(rules_schema):
    """Test subclass_to_rules for NoncodingGene to SeqFeature."""
    rules = subclass_to_rules(rules_schema, "NoncodingGene", "SeqFeature")

    # Should generate one rule
    assert len(rules) == 1

    rule = rules[0]

    # Check preconditions - uses type designator slot
    assert rule.preconditions is not None
    assert rule.preconditions.slot_conditions is not None
    assert "type" in rule.preconditions.slot_conditions

    # Check the type slot condition
    type_condition = rule.preconditions.slot_conditions["type"]
    assert type_condition.equals_string == "NoncodingGene"

    # Check postconditions - should have slot assignments
    assert rule.postconditions is not None
    assert rule.postconditions.slot_conditions is not None
    assert "encodes" in rule.postconditions.slot_conditions
    assert "id" in rule.postconditions.slot_conditions


def test_roll_up_genomic_sample(rules_schema):
    """Test subclass_to_rules for GenomicSample to Sample."""
    rules = subclass_to_rules(rules_schema, "GenomicSample", "Sample")

    # Should generate one rule
    assert len(rules) == 1

    rule = rules[0]

    # Check preconditions - uses type designator slot
    assert rule.preconditions is not None
    assert rule.preconditions.slot_conditions is not None
    assert "type" in rule.preconditions.slot_conditions

    # Check the type slot condition
    type_condition = rule.preconditions.slot_conditions["type"]
    assert type_condition.equals_string == "GenomicSample"

    # Check postconditions - should have slot assignments
    assert rule.postconditions is not None
    assert rule.postconditions.slot_conditions is not None
    # Should include slots from the class
    assert "id" in rule.postconditions.slot_conditions
    assert "analyte" in rule.postconditions.slot_conditions
