"""Phase 3 tests for https://github.com/linkml/linkml/issues/723.

Verifies the ``EnumDefinitionImpl._registry`` populated by ``pythongen``
emitted ``_register`` calls and the ``SchemaView.enum_class_for`` /
``enum_member_for`` lookup helpers.
"""

import pytest

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.linkml_model import PermissibleValue
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.schemaview import SchemaView

SCHEMA_ID = "http://example.org/enum-registry"

SCHEMA = f"""
id: {SCHEMA_ID}
name: enum-registry
imports:
  - https://w3id.org/linkml/types
prefixes:
  x: http://example.org/
default_prefix: x
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


@pytest.fixture(scope="module")
def mod():
    return compile_python(PythonGenerator(SCHEMA).serialize())


@pytest.fixture(scope="module")
def view():
    return SchemaView(SCHEMA)


def test_register_populates_registry(mod) -> None:
    assert EnumDefinitionImpl._registry.get((SCHEMA_ID, "VitalStatus")) is mod.VitalStatus
    assert EnumDefinitionImpl._registry.get((SCHEMA_ID, "Role")) is mod.Role


def test_for_schema_element_returns_class(mod) -> None:
    assert EnumDefinitionImpl.for_schema_element(SCHEMA_ID, "VitalStatus") is mod.VitalStatus


def test_for_schema_element_unknown_returns_none() -> None:
    assert EnumDefinitionImpl.for_schema_element("nope://nope", "Nope") is None


def test_schemaview_enum_class_for(mod, view) -> None:
    assert view.enum_class_for("VitalStatus") is mod.VitalStatus
    assert view.enum_class_for("Role") is mod.Role


def test_schemaview_enum_class_for_unknown_enum(view) -> None:
    assert view.enum_class_for("DoesNotExist") is None


def test_schemaview_enum_member_for(mod, view) -> None:
    pv = PermissibleValue(text="ALIVE")
    member = view.enum_member_for(pv, "VitalStatus")
    assert isinstance(member, mod.VitalStatus)
    assert member == mod.VitalStatus.ALIVE


def test_re_register_overwrites(mod) -> None:
    # Re-registering with the same key updates the entry; importing/reloading
    # a generated module must not leave stale references.
    mod.VitalStatus._register(SCHEMA_ID, "VitalStatus")
    assert EnumDefinitionImpl._registry[(SCHEMA_ID, "VitalStatus")] is mod.VitalStatus


def test_gen_enum_registry_uses_from_schema_when_set() -> None:
    """When ``EnumDefinition.from_schema`` is set, the emitted ``_register``
    cites that owning schema id rather than the generator's current schema id.
    """
    from linkml_runtime.linkml_model.meta import EnumDefinition

    gen = PythonGenerator(SCHEMA)
    foreign = "http://other.example.org/foreign"
    enums = [
        EnumDefinition(name="Foreign", from_schema=foreign),
        EnumDefinition(name="Native"),
    ]
    registry = gen.gen_enum_registry(enums)
    assert f'Foreign._register({foreign!r}, "Foreign")' in registry
    assert f'Native._register({SCHEMA_ID!r}, "Native")' in registry
