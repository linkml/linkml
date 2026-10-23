import pytest

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.utils.schemaview import SchemaView


@pytest.mark.pythongen
@pytest.mark.parametrize(
    "slot_name,expected_alias",
    [
        ("slot_a", None),
        ("slot-a", "slot_a"),
    ],
)
def test_issue_2911(slot_name: str, expected_alias: str):
    """Induced slot with self-alias must not raise error."""
    source = SchemaView(f"""
id: http://example.org/source
name: source
imports:
- https://w3id.org/linkml/types

slots:
  {slot_name}:
    range: string

classes:
  SourceClass:
    slots:
      - {slot_name}
""")

    target = SchemaView("""
id: http://example.org/target
name: target
imports:
- https://w3id.org/linkml/types

classes:
  TargetClass:
""")

    induced = source.induced_slot(slot_name, "SourceClass")
    assert induced.alias == expected_alias

    target.add_slot(induced)
    target.get_class("TargetClass").slots.append(slot_name)
    target.set_modified()

    PythonGenerator(target.schema).serialize()
