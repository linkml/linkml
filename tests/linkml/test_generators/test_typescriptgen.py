from unittest.mock import patch

from click.testing import CliRunner

from linkml.generators.typescriptgen import TypescriptGenerator, cli
from linkml.utils.schema_builder import SchemaBuilder
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import SlotDefinition


def test_tsgen(kitchen_sink_path):
    """typescript"""
    tss = TypescriptGenerator(kitchen_sink_path, mergeimports=True).serialize()

    def assert_in(s: str) -> None:
        assert s.replace(" ", "") in tss.replace(" ", "")

    assert "export type OrganizationId" in tss
    assert_in("export interface Person  extends HasAliases")
    assert_in("has_familial_relationships?: FamilialRelationship[]")
    assert_in("code_systems?: CodeSystem[]")


def test_required_slots():
    """typescript"""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    id = SlotDefinition(name="id", multivalued=False, range="string", required=True)
    description = SlotDefinition(name="description", multivalued=False, range="string")
    sb.add_class("Person", slots=[id, description])
    schema = sb.schema
    tss = TypescriptGenerator(schema, gen_type_utils=True, mergeimports=True).serialize()
    assert "id: string" in tss
    assert "'id' in o" in tss
    assert "description?: string" in tss
    assert "description: o.description ?? ''" in tss

    tss = TypescriptGenerator(schema, mergeimports=True).serialize()
    assert "id: string" in tss
    assert "'id' in o" not in tss
    assert "description?: string" in tss
    assert "description: o.description ?? ''" not in tss


def test_mutlivalued_string():
    """Test that multivalued string slots are generated as string arrays"""

    sb = SchemaBuilder("test")
    sb.add_defaults()
    aliases = SlotDefinition(name="aliases", multivalued=True, range="string")
    descriptions = SlotDefinition(name="descriptions", multivalued=True, range="string", required=True)
    sb.add_class("Person", slots=[aliases, descriptions])
    schema = sb.schema
    tss = TypescriptGenerator(schema, gen_type_utils=True, mergeimports=True).serialize()
    assert "aliases?: string[]" in tss
    assert "descriptions: string[]" in tss
    assert "'descriptions' in o" in tss
    assert "descriptions: o.descriptions ?? []" in tss

    tss = TypescriptGenerator(schema, mergeimports=True).serialize()
    assert "aliases?: string[]" in tss
    assert "descriptions: string[]" in tss
    assert "'descriptions' in o" not in tss
    assert "descriptions: o.descriptions ?? []" not in tss


def test_enums():
    unit_test_schema = """
id: unit_test
name: unit_test

prefixes:
  ex: https://example.org/
default_prefix: ex

enums:
  TestEnum:
    permissible_values:
      123:
      +:
      This & that, plus maybe a 🎩:
      Ohio:
"""

    sv = SchemaView(unit_test_schema)
    gen = TypescriptGenerator(schema=unit_test_schema)
    enums = gen.generate_enums(sv.all_enums())
    assert enums
    enum = enums["TestEnum"]
    assert enum
    assert enum["values"]["number_123"]["value"] == "123"
    assert enum["values"]["PLUS_SIGN"]["value"] == "+"
    assert enum["values"]["This_AMPERSAND_that_plus_maybe_a_TOP_HAT"]["value"] == "This & that, plus maybe a 🎩"
    assert enum["values"]["Ohio"]["value"] == "Ohio"


def test_output_option(kitchen_sink_path, tmp_path):
    tss = TypescriptGenerator(kitchen_sink_path, mergeimports=True)

    tss.serialize(output=tmp_path / "kitchen_sink.ts")
    assert (tmp_path / "kitchen_sink.ts").exists()


def test_cli_print_stdout_without_output(kitchen_sink_path):
    # assert that print is called when output is None

    runner = CliRunner()
    with patch("builtins.print") as mock_print:
        result = runner.invoke(cli, [kitchen_sink_path])
        assert result.exit_code == 0
        mock_print.assert_called_once()


def test_cli_no_print_with_output(kitchen_sink_path, tmp_path):
    # assert that print is not called when output is set

    runner = CliRunner()
    with patch("builtins.print") as mock_print:
        result = runner.invoke(cli, [kitchen_sink_path, "--output", tmp_path / "kitchen_sink.ts"])
        assert result.exit_code == 0
        mock_print.assert_not_called()


def test_subproperty_of_generates_union_type():
    """Test that subproperty_of generates TypeScript union type with slot descendants."""
    schema_yaml = """
id: https://example.org/test
name: test

prefixes:
  ex: https://example.org/

default_prefix: ex

slots:
  related_to:
    description: Root predicate
    slot_uri: ex:related_to
  causes:
    is_a: related_to
    slot_uri: ex:causes
  treats:
    is_a: related_to
    slot_uri: ex:treats

  predicate:
    range: uriorcurie
    subproperty_of: related_to

classes:
  Association:
    slots:
      - predicate
"""
    gen = TypescriptGenerator(schema_yaml)
    tss = gen.serialize()

    # Should generate union type with CURIEs
    assert '"ex:causes"' in tss
    assert '"ex:related_to"' in tss
    assert '"ex:treats"' in tss
    # Should use union operator
    assert "|" in tss


def test_subproperty_of_with_deeper_hierarchy():
    """Test that subproperty_of includes all descendants, not just direct children."""
    schema_yaml = """
id: https://example.org/test
name: test

prefixes:
  ex: https://example.org/

default_prefix: ex

slots:
  related_to:
    slot_uri: ex:related_to
  causes:
    is_a: related_to
    slot_uri: ex:causes
  directly_causes:
    is_a: causes
    slot_uri: ex:directly_causes
  treats:
    is_a: related_to
    slot_uri: ex:treats

  predicate:
    range: uriorcurie
    subproperty_of: related_to

classes:
  Association:
    slots:
      - predicate
"""
    gen = TypescriptGenerator(schema_yaml)
    tss = gen.serialize()

    # Should include grandchild (directly_causes)
    assert '"ex:causes"' in tss
    assert '"ex:directly_causes"' in tss
    assert '"ex:related_to"' in tss
    assert '"ex:treats"' in tss


def test_subproperty_of_with_string_range():
    """Test that subproperty_of with string range uses snake_case slot names."""
    schema_yaml = """
id: https://example.org/test
name: test

prefixes:
  ex: https://example.org/

default_prefix: ex

slots:
  related_to:
    slot_uri: ex:related_to
  causes:
    is_a: related_to
    slot_uri: ex:causes
  treats:
    is_a: related_to
    slot_uri: ex:treats

  predicate:
    range: string
    subproperty_of: related_to

classes:
  Association:
    slots:
      - predicate
"""
    gen = TypescriptGenerator(schema_yaml)
    tss = gen.serialize()

    # Should use snake_case slot names for string range
    assert '"causes"' in tss
    assert '"related_to"' in tss
    assert '"treats"' in tss


def test_subproperty_of_can_be_disabled():
    """Test that expand_subproperty_of=False disables union type generation."""
    schema_yaml = """
id: https://example.org/test
name: test

prefixes:
  ex: https://example.org/

default_prefix: ex

slots:
  related_to:
    slot_uri: ex:related_to
  causes:
    is_a: related_to
    slot_uri: ex:causes

  predicate:
    range: uriorcurie
    subproperty_of: related_to

classes:
  Association:
    slots:
      - predicate
"""
    gen = TypescriptGenerator(schema_yaml, expand_subproperty_of=False)
    tss = gen.serialize()

    # Should NOT generate union type when disabled
    assert '"ex:causes"' not in tss
    assert '"ex:related_to"' not in tss
    # Should use regular string type instead
    assert "string" in tss


def test_subproperty_of_with_slot_usage():
    """Test that slot_usage subproperty_of narrows the constraint."""
    schema_yaml = """
id: https://example.org/test
name: test

prefixes:
  ex: https://example.org/

default_prefix: ex

slots:
  related_to:
    slot_uri: ex:related_to
  causes:
    is_a: related_to
    slot_uri: ex:causes
  directly_causes:
    is_a: causes
    slot_uri: ex:directly_causes
  treats:
    is_a: related_to
    slot_uri: ex:treats

  predicate:
    range: uriorcurie

classes:
  Association:
    slots:
      - predicate
  CausalAssociation:
    is_a: Association
    slot_usage:
      predicate:
        subproperty_of: causes
"""
    # Use include_induced_slots=True to ensure slot_usage overrides are rendered
    gen = TypescriptGenerator(schema_yaml, include_induced_slots=True)
    tss = gen.serialize()

    # CausalAssociation should have constrained predicate type
    # It should only include causes and its descendants, not treats
    # Find the CausalAssociation interface section
    lines = tss.split("\n")
    in_causal = False
    causal_section = []
    for line in lines:
        if "interface CausalAssociation" in line:
            in_causal = True
        if in_causal:
            causal_section.append(line)
            if line.strip() == "}":
                break

    causal_text = "\n".join(causal_section)
    # CausalAssociation should have the constrained type
    assert '"ex:causes"' in causal_text or '"ex:directly_causes"' in causal_text
    # Should NOT include treats in CausalAssociation
    assert '"ex:treats"' not in causal_text
