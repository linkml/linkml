"""
Tests for issue 1731: Documentation pages for classes should indicate whether any rules are applied
"""

from linkml.generators.docgen import DocGenerator
from tests.test_generators.test_docgen import assert_mdfile_contains


def test_class_rules_section_rendering(input_path, tmp_path):
    """
    Tests that the contents of the ## Rules section are rendered properly
    in the Markdown output/class documentation pages of the supplied Pokemon
    schema in linkml_issue_1731.yaml.
    """
    schema_path = str(input_path("linkml_issue_1731.yaml"))
    gen = DocGenerator(schema_path, mergeimports=True)
    gen.serialize(directory=str(tmp_path))

    pokemon_class_md_file = tmp_path / "Pokemon.md"

    # Check that the Rules section exists in Pokemon documentation
    assert_mdfile_contains(pokemon_class_md_file, "## Rules", after="## Slots")

    # Check that the rules table is properly structured
    assert_mdfile_contains(
        pokemon_class_md_file,
        "| Rule Applied | Preconditions | Postconditions | Elseconditions |",
        after="## Rules",
    )

    # Check for preconditions showing Water type
    assert_mdfile_contains(
        pokemon_class_md_file,
        "Water",
        after="| Rule Applied | Preconditions | Postconditions | Elseconditions |",
    )

    # Check that postconditions correctly show strong_against and weak_against
    assert_mdfile_contains(
        pokemon_class_md_file,
        "Fire",
        after="| Rule Applied | Preconditions | Postconditions | Elseconditions |",
    )
    assert_mdfile_contains(
        pokemon_class_md_file,
        "Rock",
        after="| Rule Applied | Preconditions | Postconditions | Elseconditions |",
    )
    assert_mdfile_contains(
        pokemon_class_md_file,
        "Electric",
        after="| Rule Applied | Preconditions | Postconditions | Elseconditions |",
    )
    assert_mdfile_contains(
        pokemon_class_md_file,
        "Grass",
        after="| Rule Applied | Preconditions | Postconditions | Elseconditions |",
    )


def test_classrule_to_dict_view_method(input_path, tmp_path):
    """
    Unit tests for classrule_to_dict_view() in linkml/generators/docgen.py.
    """
    schema_path = str(input_path("linkml_issue_1731.yaml"))
    gen = DocGenerator(schema_path, mergeimports=True)
    gen.serialize(directory=str(tmp_path))

    # Test the specific methods for rule processing
    pokemon_class = gen.schemaview.get_class("Pokemon")

    # Test classrule_to_dict_view method
    processed_rules = gen.classrule_to_dict_view(pokemon_class)
    assert len(processed_rules) == 1
    assert processed_rules[0]["title"] == ""  # The rule doesn't have a title

    # Get the first rule for further testing
    rule_dict = processed_rules[0]

    # Test that preconditions are properly processed
    assert "slot_conditions" in rule_dict["preconditions"]
    assert "type" in rule_dict["preconditions"]["slot_conditions"]
    assert "exactly_one_of" in rule_dict["preconditions"]["slot_conditions"]["type"]
    assert rule_dict["preconditions"]["slot_conditions"]["type"]["exactly_one_of"][0]["equals_string"] == "Water"

    # Test that postconditions are properly processed for strong_against
    assert "slot_conditions" in rule_dict["postconditions"]
    assert "strong_against" in rule_dict["postconditions"]["slot_conditions"]
    assert "any_of" in rule_dict["postconditions"]["slot_conditions"]["strong_against"]

    # Check for specific values in the strong_against postconditions
    strong_against_conditions = rule_dict["postconditions"]["slot_conditions"]["strong_against"]["any_of"]
    strong_against_values = [c.get("equals_string") for c in strong_against_conditions if "equals_string" in c]
    assert "Fire" in strong_against_values
    assert "Rock" in strong_against_values

    # Check for specific values in the weak_against postconditions
    assert "weak_against" in rule_dict["postconditions"]["slot_conditions"]
    assert "any_of" in rule_dict["postconditions"]["slot_conditions"]["weak_against"]

    weak_against_conditions = rule_dict["postconditions"]["slot_conditions"]["weak_against"]["any_of"]
    weak_against_values = [c.get("equals_string") for c in weak_against_conditions if "equals_string" in c]
    assert "Electric" in weak_against_values
    assert "Grass" in weak_against_values

    # Test that elseconditions is None since it's not defined in the rule
    assert rule_dict["elseconditions"] is None
