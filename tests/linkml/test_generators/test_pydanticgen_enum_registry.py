"""Tests for the pydanticgen ``register_enum_class`` emission and the
``SchemaView`` lookup helpers when the generated module uses stdlib enums
(linkml/linkml#723, phase 4).
"""

from __future__ import annotations

import pytest

from linkml.generators.pydanticgen import PydanticGenerator
from linkml.generators.pydanticgen.template import EnumValue, PydanticEnum, PydanticModule
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.schemaview import SchemaView

SCHEMA_ID = "http://example.org/pydantic-enum-registry"

SCHEMA = f"""
id: {SCHEMA_ID}
name: pydantic_enum_registry
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string
classes:
  Person:
    attributes:
      status:
        range: VitalStatus
enums:
  VitalStatus:
    permissible_values:
      ALIVE:
      DEAD:
  Role:
    permissible_values:
      ANALYST:
      INVESTIGATOR:
"""


@pytest.fixture(autouse=True)
def _isolate_registry():
    snapshot = dict(EnumDefinitionImpl._registry)
    yield
    EnumDefinitionImpl._registry.clear()
    EnumDefinitionImpl._registry.update(snapshot)


@pytest.fixture
def generated():
    return compile_python(PydanticGenerator(SCHEMA).serialize())


@pytest.fixture
def view():
    return SchemaView(SCHEMA)


def test_serialized_output_contains_registration_lines():
    out = PydanticGenerator(SCHEMA).serialize()
    assert "from linkml_runtime.utils.enumerations import register_enum_class" in out
    assert f'register_enum_class("{SCHEMA_ID}", "VitalStatus", VitalStatus)' in out
    assert f'register_enum_class("{SCHEMA_ID}", "Role", Role)' in out


def test_import_populates_registry(generated):
    assert EnumDefinitionImpl.for_schema_element(SCHEMA_ID, "VitalStatus") is generated.VitalStatus
    assert EnumDefinitionImpl.for_schema_element(SCHEMA_ID, "Role") is generated.Role


def test_schemaview_enum_class_for(generated, view):
    assert view.enum_class_for("VitalStatus") is generated.VitalStatus
    assert view.enum_class_for("Role") is generated.Role


def test_schemaview_enum_class_for_unknown_enum(generated, view):
    assert view.enum_class_for("Missing") is None


def test_schemaview_enum_member_for_stdlib_enum(generated, view):
    pv = view.get_enum("VitalStatus").permissible_values["ALIVE"]
    member = view.enum_member_for(pv, "VitalStatus")
    assert member is generated.VitalStatus.ALIVE
    assert isinstance(member, generated.VitalStatus)


def test_schemaview_enum_member_for_unregistered_returns_none(view):
    pv = view.get_enum("VitalStatus").permissible_values["ALIVE"]
    assert view.enum_member_for(pv, "VitalStatus") is None


def test_no_registration_block_when_no_enums():
    schema = f"""
id: {SCHEMA_ID}-noenums
name: noenums
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string
classes:
  Person:
    attributes:
      name: {{}}
"""
    out = PydanticGenerator(schema).serialize()
    assert "register_enum_class" not in out


def test_enum_registrations_computed_field_skips_enums_without_schema_id():
    module = PydanticModule(
        enums={
            "A": PydanticEnum(name="A", schema_id="s1", values={"X": EnumValue(label="X", value="X")}),
            "B": PydanticEnum(name="B", values={"Y": EnumValue(label="Y", value="Y")}),
        }
    )
    entries = module.enum_registrations
    assert entries == [{"name": "A", "schema_id": "s1"}]
