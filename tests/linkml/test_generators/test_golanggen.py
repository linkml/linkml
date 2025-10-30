import re

from linkml.generators.golanggen import GolangGenerator


def test_golanggen(kitchen_sink_path):
    """golang"""
    code = GolangGenerator(kitchen_sink_path, mergeimports=True).serialize()

    def assert_in(s: str) -> None:
        assert s.replace(" ", "") in code.replace(" ", "").replace("\t", "")

    assert "package kitchen" in code
    assert_in("type Person struct {")
    assert_in("HasFamilialRelationships []FamilialRelationship")
    assert_in("CodeSystems []CodeSystem")
    assert_in("type ActivityId string")
    assert_in("Id *string")
    assert_in("WasInformedBy *ActivityId")
    assert_in("StartedAtTime *time.Time")
    assert_in("Aliases []string")
    assert_in("""
type Place struct {
    /*
     * parent types
     */
    HasAliases
    Id string `json:"id"`
    Name *string `json:"name"`
}
""")

    # for reproducible codegen, we check that the generated structs are in sorted order
    matches = re.findall(r"^type\s+(\w+)\s+struct", code, re.MULTILINE)
    assert matches == sorted(matches)


def test_multivalued_non_id(tmp_path):
    schema = tmp_path / "multivalued_non_id.yaml"
    schema.write_text(
        """
id: http://example.org/test_multivalued_non_id
name: test_multivalued_non_id

imports:
  - https://w3id.org/linkml/types

slots:
  int_dict:
    range: KeyedInt
    multivalued: true

  id:
    range: string
    identifier: true

  value:
    range: integer
    required: true

classes:
  KeyedInt:
    slots:
      - id
      - value
  Test:
    tree_root: true
    slots:
      - int_dict
""",
        encoding="utf-8",
    )

    code = GolangGenerator(schema, mergeimports=True).serialize()
    assert 'IntDict []KeyedIntId `json:"int_dict"`' in code
