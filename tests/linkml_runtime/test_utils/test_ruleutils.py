from pathlib import Path

import pytest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.ruleutils import get_range_as_disjunction, subclass_to_rules
from linkml_runtime.utils.schemaview import SchemaView
from tests.test_utils import INPUT_DIR


@pytest.fixture
def rules_schema():
    """SchemaView loaded with rules example schema."""
    return SchemaView(Path(INPUT_DIR) / "rules-example.yaml")


def test_disjunction(rules_schema):
    """Test get_range_as_disjunction with schema view fixture."""
    analyte = rules_schema.induced_slot("analyte", "Sample")
    # print(analyte)
    # print(analyte.any_of)
    disj = get_range_as_disjunction(analyte)
    # print(disj)
    assert sorted(disj) == sorted({"MissingValueEnum", "AnalyteEnum"})

    # Test all slots for debugging
    for s in rules_schema.all_slots().values():
        disj = get_range_as_disjunction(s)
        print(f"{s.name} DISJ: {disj}")


def test_roll_up(rules_schema):
    """Test subclass_to_rules with schema view fixture."""
    c = rules_schema.get_class("ProteinCodingGene")
    rules = subclass_to_rules(rules_schema, "ProteinCodingGene", "SeqFeature")
    rule = rules[0]
    print(f"IF: {rule.preconditions}")
    print(f"THEN: {rule.postconditions}")
    print(yaml_dumper.dumps(rule))
