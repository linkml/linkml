"""Tests for the linkml rollup transformer."""

from pathlib import Path

import pytest

from linkml.transformers.rollup_transformer import (
    FlattenTransformerConfiguration,
    RollupTransformer,
)
from linkml.utils.schema_builder import SchemaBuilder

THIS_DIR = Path(__file__).parent
OUTPUT_DIR = THIS_DIR / "output"


def test_no_schema():
    """Simple brainless test to ensure that RollupTransformer will not transform without a schema set."""
    transformer = RollupTransformer(target_class="Association")
    with pytest.raises(ValueError, match="SchemaView not set"):
        transformer.transform()


def test_flatten_simple():
    """
    Test a simple schema with a base 'Association' class and two descendant classes.
    The descendant slots should be rolled up into the base class and descendant classes removed.
    """
    sb = SchemaBuilder()
    # Base class: Association with basic properties.
    sb.add_class("Association", slots=["id", "subject", "predicate", "object", "category"])
    # Descendant 1: GeneticAssociation adds gene-specific slots.
    sb.add_class(
        "GeneticAssociation",
        slots={"gene_variant": {"range": "str"}, "inheritance_mode": {"range": "str"}},
        is_a="Association",
    )
    # Descendant 2: ChemicalAssociation adds chemical-specific slots.
    sb.add_class(
        "ChemicalAssociation",
        slots={"drug_dosage": {"range": "float"}, "concentration": {"range": "float"}},
        is_a="Association",
    )
    sb.add_slot("id", identifier=True, replace_if_present=True, range="str")
    sb.add_slot("subject", replace_if_present=True, range="str")
    sb.add_slot("predicate", replace_if_present=True, range="str")
    sb.add_slot("object", replace_if_present=True, range="str")
    sb.add_slot("category", replace_if_present=True, range="str", description="Original class designator")
    sb.add_slot("gene_variant", replace_if_present=True, range="str")
    sb.add_slot("inheritance_mode", replace_if_present=True, range="str")
    sb.add_slot("drug_dosage", replace_if_present=True, range="float")
    sb.add_slot("concentration", replace_if_present=True, range="float")

    sb.add_defaults()
    schema = sb.schema
    config = FlattenTransformerConfiguration(
        preserve_class_designator=True, class_designator_slot="category", include_all_classes=False
    )
    transformer = RollupTransformer(target_class="Association", config=config)
    transformer.set_schema(schema)
    flattened_schema = transformer.transform()

    # In the flattened schema, the target class should have rolled up slots from both descendants.
    assoc = flattened_schema.classes["Association"]
    expected_slots = {
        "id",
        "subject",
        "predicate",
        "object",
        "category",
        "gene_variant",
        "inheritance_mode",
        "drug_dosage",
        "concentration",
    }
    assert set(assoc.slots) == expected_slots

    # Descendant classes should be removed.
    descendants = {"GeneticAssociation", "ChemicalAssociation"}
    for descendant in descendants:
        assert descendant not in flattened_schema.classes


def test_multi_level_inheritance():
    """Test flattening with multiple levels of inheritance."""
    sb = SchemaBuilder()

    # Create a hierarchy: Entity -> Association -> GeneAssociation -> SpecificGeneAssociation
    sb.add_class("Entity", slots=["id", "name"])
    sb.add_class("Association", is_a="Entity", slots=["subject", "object"])
    sb.add_class("GeneAssociation", is_a="Association", slots=["gene"])
    sb.add_class("SpecificGeneAssociation", is_a="GeneAssociation", slots=["specificity"])

    for slot in ["id", "name", "subject", "object", "gene", "specificity"]:
        sb.add_slot(slot, replace_if_present=True, range="str")

    transformer = RollupTransformer(target_class="Association")
    transformer.set_schema(sb.schema)
    flattened_schema = transformer.transform()

    # Verify Association has rolled up all slots from descendants
    association_class = flattened_schema.classes["Association"]
    expected_slots = {"id", "name", "subject", "object", "gene", "specificity"}

    assert set(association_class.slots) == expected_slots
    # Verify Entity is still there (not a descendant of Association)
    assert "Entity" in flattened_schema.classes

    descendants = {"GeneAssociation", "SpecificGeneAssociation"}
    for descendant in descendants:
        assert descendant not in flattened_schema.classes


def test_include_all_classes_option():
    """Test that include_all_classes=True keeps descendant classes."""
    sb = SchemaBuilder()

    # Base and descendant classes
    sb.add_class("Association", slots=["id", "relation"])
    sb.add_class("GeneAssociation", is_a="Association", slots=["gene"])

    for slot in ["id", "relation", "gene"]:
        sb.add_slot(slot, replace_if_present=True, range="str")

    # Transform with include_all_classes=True
    config = FlattenTransformerConfiguration(include_all_classes=True)
    transformer = RollupTransformer(target_class="Association", config=config)
    transformer.set_schema(sb.schema)
    flattened_schema = transformer.transform()

    # Verify Association has all slots
    association_class = flattened_schema.classes["Association"]
    expected_slots = {"id", "relation", "gene"}
    assert set(association_class.slots) == expected_slots
    # Verify descendant classes are still present
    assert "GeneAssociation" in flattened_schema.classes


def test_mixin_flattening():
    """Test that slots from mixins are correctly incorporated."""
    sb = SchemaBuilder()

    # Create mixin class
    sb.add_class("Metadata", mixin=True, slots=["created_at", "updated_at"])

    # Base class without mixin
    sb.add_class("BaseEntity", slots=["id"])

    # Class that inherits from base and uses mixin
    sb.add_class("Person", is_a="BaseEntity", mixins=["Metadata"], slots=["name"])

    for slot in ["id", "created_at", "updated_at", "name"]:
        sb.add_slot(slot, replace_if_present=True, range="str")

    config = FlattenTransformerConfiguration(include_mixins=True)
    transformer = RollupTransformer(target_class="BaseEntity", config=config)
    transformer.set_schema(sb.schema)
    flattened_schema = transformer.transform()

    # Verify BaseEntity has all slots including those from mixin
    base_entity_class = flattened_schema.classes["BaseEntity"]
    expected_slots = {"id", "name", "created_at", "updated_at"}
    assert set(base_entity_class.slots) == expected_slots


def test_designator_slot_handling():
    """Test that the class designator slot is handled correctly."""
    sb = SchemaBuilder()

    # Base class with designator slot
    sb.add_class("Association", slots=["id", "category"])
    sb.add_class("GeneAssociation", is_a="Association", slots=["gene"])

    sb.add_slot("id", replace_if_present=True, range="str")
    sb.add_slot("gene", replace_if_present=True, range="str")
    sb.add_slot(
        "category", replace_if_present=True, range="str", description="Indicates the specific type of association"
    )

    # Transform with preserve_class_designator=True
    config = FlattenTransformerConfiguration(preserve_class_designator=True, class_designator_slot="category")
    transformer = RollupTransformer(target_class="Association", config=config)
    transformer.set_schema(sb.schema)
    flattened_schema = transformer.transform()

    # Verify designator slot is preserved and description maintained
    category_slot = flattened_schema.slots["category"]
    assert category_slot.description == "Indicates the specific type of association"
    assert "GeneAssociation" not in flattened_schema.classes


def test_conflicting_slot_ranges():
    """Test handling of conflicting slot ranges in inherited classes."""
    sb = SchemaBuilder()

    # Base class with a string slot
    sb.add_class("Base", slots=["common_slot"])
    sb.add_slot("common_slot", replace_if_present=True, range="string")

    # Descendant with same slot name but different range
    sb.add_class("Descendant", is_a="Base", slots=["common_slot"])
    sb.add_slot("common_slot", range="integer", replace_if_present=True)

    transformer = RollupTransformer(target_class="Base")
    transformer.set_schema(sb.schema)

    flattened_schema = transformer.transform()
    assert flattened_schema.slots["common_slot"].range == "integer"
    assert "Descendant" not in flattened_schema.classes


def test_union_type_handling():
    """Test handling of union types in slots."""
    sb = SchemaBuilder()

    sb.add_class("Association", slots=["id", "value"])

    # Descendant with a slot having any_of
    sb.add_class("SpecialAssociation", is_a="Association", slots=["special_value"])

    sb.add_slot("id", replace_if_present=True, range="string")
    sb.add_slot("value", replace_if_present=True, range="string")

    # Union type slot
    sb.add_slot("special_value", replace_if_present=True, range="string")
    sb.schema.slots["special_value"].multivalued = True

    transformer = RollupTransformer(target_class="Association")
    transformer.set_schema(sb.schema)
    flattened_schema = transformer.transform()

    association_class = flattened_schema.classes["Association"]
    assert "special_value" in association_class.slots
    special_value_slot = flattened_schema.slots["special_value"]
    assert special_value_slot.range == "string"
    assert special_value_slot.multivalued is True
    assert "SpecialAssociation" not in flattened_schema.classes


def test_indirect_descendants():
    """Test that slots from indirect descendants are included."""
    sb = SchemaBuilder()

    # Create multi-level hierarchy
    sb.add_class("A", slots=["slot_a"])
    sb.add_class("B", is_a="A", slots=["slot_b"])
    sb.add_class("C", is_a="B", slots=["slot_c"])
    sb.add_class("D", is_a="C", slots=["slot_d"])

    for slot in ["slot_a", "slot_b", "slot_c", "slot_d"]:
        sb.add_slot(slot, replace_if_present=True, range="string")

    transformer = RollupTransformer(target_class="B")
    transformer.set_schema(sb.schema)
    flattened_schema = transformer.transform()

    # B should have its own slot plus slots from C and D
    b_class = flattened_schema.classes["B"]
    expected_slots = {"slot_a", "slot_b", "slot_c", "slot_d"}
    assert set(b_class.slots) == expected_slots

    # A should remain unchanged
    a_class = flattened_schema.classes["A"]
    assert a_class.slots == ["slot_a"]


def test_slot_merging_with_multiple_descendants():
    """Test merging slots from multiple descendants with the same slot name."""
    sb = SchemaBuilder()

    sb.add_class("Base", slots=["id"])

    # Two descendants with a common slot
    sb.add_class("Child1", is_a="Base", slots=["common"])
    sb.add_class("Child2", is_a="Base", slots=["common"])

    sb.add_slot("id", replace_if_present=True, range="string")
    sb.add_slot("common", replace_if_present=True, range="string", description="A common slot")

    transformer = RollupTransformer(target_class="Base")
    transformer.set_schema(sb.schema)
    flattened_schema = transformer.transform()

    base_class = flattened_schema.classes["Base"]
    assert set(base_class.slots) == {"id", "common"}

    # Common slot should be present only once
    assert base_class.slots.count("common") == 1
    descendants = {"Child1", "Child2"}
    for descendant in descendants:
        assert descendant not in flattened_schema.classes
