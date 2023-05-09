import sys
import unittest

from linkml_runtime.linkml_model import SlotDefinition
from linkml.generators.typescriptgen import TypescriptGenerator
from linkml.utils.schema_builder import SchemaBuilder
from tests.test_generators.environment import env

SCHEMA = env.input_path("kitchen_sink.yaml")
OUT = env.expected_path("kitchen_sink.ts")


class TypescriptGeneratorTestCase(unittest.TestCase):
    def test_tsgen(self):
        """typescript"""
        tss = TypescriptGenerator(SCHEMA, mergeimports=True).serialize()
        with open(OUT, "w") as stream:
            stream.write(tss)

        def assert_in(s: str) -> None:
            assert s.replace(" ", "") in tss.replace(" ", "")

        assert "export type OrganizationId" in tss
        assert_in("export interface Person  extends HasAliases")
        assert_in("has_familial_relationships?: FamilialRelationship[]")
        assert_in("code_systems?: {[index: CodeSystemId]: CodeSystem }")


    def test_mutlivalued_string(self):
        """ Test that multivalued string slots are generated as string arrays """

        sb = SchemaBuilder("test")
        sb.add_defaults()
        aliases = SlotDefinition(name="aliases", multivalued=True, range="string")
        sb.add_class("Person", slots=[aliases])
        schema = sb.schema
        tss = TypescriptGenerator(schema, mergeimports=True).serialize()
        assert("aliases?: string[]" in tss)

if __name__ == "__main__":
    unittest.main()
