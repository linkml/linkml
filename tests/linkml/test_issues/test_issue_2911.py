import pytest

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.utils.schemaview import SchemaView

SCHEMA_TEMPLATE = """
id: http://example.org/test
name: test
imports:
- https://w3id.org/linkml/types

slots:
  {slot_name}:
    {slot_extra}
    range: string

classes:
  TestClass:
    slots:
      - {slot_name}
"""


@pytest.mark.pythongen
@pytest.mark.parametrize(
    "slot_name,slot_extra,expected_alias",
    [
        ("slot_a", "", "slot_a"),
        ("slot-a", "", "slot_a"),
        ("slotA", "alias: slot_a", "slot_a"),
    ],
)
def test_issue_2911(slot_name: str, slot_extra: str, expected_alias: str):
    """Self-alias in induced_slot should not raise error."""
    schema = SCHEMA_TEMPLATE.format(slot_name=slot_name, slot_extra=slot_extra)
    view = SchemaView(schema)

    induced = view.induced_slot(slot_name, "TestClass")
    assert induced.alias == expected_alias

    PythonGenerator(view.schema).serialize()
