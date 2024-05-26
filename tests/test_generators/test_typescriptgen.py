from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import SlotDefinition

from linkml.generators.typescriptgen import TypescriptGenerator
from linkml.utils.schema_builder import SchemaBuilder


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
