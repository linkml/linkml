"""Phase 2 tests for https://github.com/linkml/linkml/issues/723.

Verifies that ``pythongen``-generated classes coerce raw strings (and bare
``PermissibleValue`` objects) to enum instances when assigned to an
enum-ranged slot after construction (not only during ``__init__``).
"""

import pytest

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.linkml_model import PermissibleValue
from linkml_runtime.utils.compile_python import compile_python

SCHEMA = """
id: http://example.org/enum-setattr
name: enum-setattr
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
      roles:
        range: Role
        multivalued: true

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


def test_setattr_string_coerces_to_enum(mod) -> None:
    p = mod.Person()
    p.status = "ALIVE"
    assert isinstance(p.status, mod.VitalStatus)
    assert p.status == mod.VitalStatus.ALIVE
    assert p.status == "ALIVE"


def test_setattr_permissible_value_coerces_to_enum(mod) -> None:
    p = mod.Person()
    p.status = PermissibleValue(text="ALIVE")
    assert isinstance(p.status, mod.VitalStatus)
    assert p.status == mod.VitalStatus.ALIVE


def test_setattr_enum_instance_passes_through(mod) -> None:
    p = mod.Person()
    p.status = mod.VitalStatus.ALIVE
    assert p.status is mod.VitalStatus.ALIVE


def test_setattr_none_passes_through(mod) -> None:
    p = mod.Person(status=mod.VitalStatus.ALIVE)
    p.status = None
    assert p.status is None


def test_setattr_multivalued_list_of_strings(mod) -> None:
    p = mod.Person()
    p.roles = ["ANALYST", "INVESTIGATOR"]
    assert all(isinstance(r, mod.Role) for r in p.roles)
    assert sorted(p.roles, key=str) == sorted(
        [mod.Role.ANALYST, mod.Role.INVESTIGATOR], key=str
    )


def test_setattr_multivalued_single_string_wrapped(mod) -> None:
    p = mod.Person()
    p.roles = "ANALYST"
    assert isinstance(p.roles, list)
    assert len(p.roles) == 1
    assert p.roles[0] == mod.Role.ANALYST
    assert isinstance(p.roles[0], mod.Role)


def test_setattr_multivalued_mixed_types(mod) -> None:
    p = mod.Person()
    p.roles = ["ANALYST", mod.Role.INVESTIGATOR, PermissibleValue(text="ANALYST")]
    assert all(isinstance(r, mod.Role) for r in p.roles)


def test_setattr_invalid_string_raises(mod) -> None:
    p = mod.Person()
    with pytest.raises(ValueError):
        p.status = "UNKNOWN"


def test_non_enum_slot_unaffected(mod) -> None:
    """Slots without an enum range must not be touched by the coercion path."""
    p = mod.Person()
    # ``Person`` has no string-typed slot, but assigning a private/internal
    # attribute (not in _enum_slots) must round-trip unchanged.
    p._scratch = "raw"
    assert p._scratch == "raw"


def test_enum_slots_classvar_present(mod) -> None:
    assert mod.Person._enum_slots == {
        "status": ("VitalStatus", False),
        "roles": ("Role", True),
    }
