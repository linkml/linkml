import pytest
from linkml_runtime.utils.schemaview import SchemaView

schema = """
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
prefixes:
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/
imports:
  - linkml:types
default_range: string

classes:
  Person:
    class_uri: schema:Person
    attributes:
      id:
        identifier: true
      employed:
        range: EmploymentStatusEnum
      past_relationship:
        range: RelationshipStatusEnum
    slots:
      - type
      - past_employer
  Programmer:
    attributes:
        employed:
            range: EmploymentStatusEnum
    slots:
      - type
      - past_employer
    slot_usage:
      type:
        range: TypeEnum
      
slots:
    status:
      range: PersonStatusEnum
    relationship:
      range: RelationshipStatusEnum
    type:
    past_employer:
        range: EmploymentStatusEnum
enums:
  PersonStatusEnum:
    permissible_values:
      ALIVE:
      DEAD:
      UNKNOWN:
  EmployedStatusEnum:
    permissible_values:
      EMPLOYED:
      UNEMPLOYED:
      UNKNOWN:
  RelationshipStatusEnum:
    permissible_values:
      UNKNOWN:
  TypeEnum:
    permissible_values:
      UNKNOWN:
"""


@pytest.fixture
def view():
    return SchemaView(schema)


def test_issue_998_schema_slot(view):
    enum_slots = view.get_slots_by_enum("EmploymentStatusEnum")
    assert len(enum_slots) == 2


def test_slots_are_not_duplicated(view):
    enum_slots = view.get_slots_by_enum("PersonStatusEnum")
    assert len(enum_slots) == 1
    assert enum_slots[0].name == "status"


def test_issue_998_attribute_slot(view):
    enum_slots = view.get_slots_by_enum("EmploymentStatusEnum")
    assert len(enum_slots) == 2
    assert sorted([slot.name for slot in enum_slots]) == ["employed", "past_employer"]


def test_issue_998_schema_and_attribute_slots(view):
    enum_slots = view.get_slots_by_enum("RelationshipStatusEnum")
    assert len(enum_slots) == 2
    assert enum_slots[0].name == "relationship"
    assert enum_slots[1].name == "past_relationship"


def test_issue_998_slot_usage_range(view):
    enum_slots = view.get_slots_by_enum("TypeEnum")
    assert len(enum_slots) == 1
    assert enum_slots[0].name == "type"
