"""Phase 2 tests for https://github.com/linkml/linkml/issues/723.

Verifies that ``pythongen``-generated classes coerce raw strings (and bare
``PermissibleValue`` objects) to enum instances when assigned to an
enum-ranged slot after construction (not only during ``__init__``).
"""

import dataclasses

import pytest
from jsonasobj2 import JsonObj

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.dumpers import json_dumper
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
  Any:
    class_uri: linkml:Any
  Person:
    attributes:
      status:
        range: VitalStatus
      roles:
        range: Role
        multivalued: true
      extra:
        description: free-form slot with no __post_init__ coercion
        range: Any
      dyn:
        description: ranged on an enum with no permissible values
        range: DynamicStatus
      class:
        description: python keyword -- emitted field is ``class_``
        range: VitalStatus
      vital:
        alias: vital_state
        range: VitalStatus
  HasClearance:
    mixin: true
    attributes:
      clearance:
        range: Clearance
  Employee:
    is_a: Person
    mixins:
      - HasClearance
    attributes:
      name:

enums:
  VitalStatus:
    permissible_values:
      ALIVE:
      DEAD:
  Role:
    permissible_values:
      ANALYST:
      INVESTIGATOR:
  Clearance:
    permissible_values:
      LOW:
      HIGH:
  Color:
    description: shares the text DEAD with VitalStatus
    permissible_values:
      RED:
      DEAD:
  DynamicStatus:
    reachable_from:
      source_ontology: obo:hp
      source_nodes:
        - HP:0000118
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
    assert sorted(p.roles, key=str) == sorted([mod.Role.ANALYST, mod.Role.INVESTIGATOR], key=str)


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
    p.extra = "raw"
    assert p.extra == "raw"
    p._scratch = "raw"
    assert p._scratch == "raw"


@pytest.mark.parametrize("via_constructor", [True, False])
def test_dict_on_non_enum_slot_is_still_wrapped_as_jsonobj(mod, via_constructor) -> None:
    """The emitted ``__setattr__`` must delegate to ``super()``.

    ``YAMLRoot`` inherits ``JsonObj.__setattr__``, which wraps ``dict`` values
    so they support attribute access.  Bypassing it (``object.__setattr__``)
    silently changes the type of every non-enum slot on the class.
    """
    if via_constructor:
        p = mod.Person(extra={"k": "v"})
    else:
        p = mod.Person()
        p.extra = {"k": "v"}
    assert isinstance(p.extra, JsonObj)
    assert p.extra.k == "v"


def test_subclass_coerces_inherited_and_mixin_enum_slots(mod) -> None:
    e = mod.Employee(name="x")
    e.status = "ALIVE"
    e.roles = "ANALYST"
    e.clearance = "HIGH"
    assert isinstance(e.status, mod.VitalStatus)
    assert isinstance(e.roles[0], mod.Role)
    assert isinstance(e.clearance, mod.Clearance)
    assert set(mod.Employee._enum_slots) >= {"status", "roles", "clearance"}


def test_enum_without_permissible_values_is_left_untouched(mod) -> None:
    """Dynamic enums have no members to coerce into; matches ``__post_init__``."""
    assert "dyn" not in mod.Person._enum_slots
    p = mod.Person()
    p.dyn = "HP:0000118"
    assert p.dyn == "HP:0000118"
    assert isinstance(p.dyn, str)


def test_setattr_then_dump_round_trips(mod) -> None:
    p = mod.Person()
    p.status = "DEAD"
    p.roles = "ANALYST"
    as_dict = json_dumper.to_dict(p)
    assert as_dict == {"status": "DEAD", "roles": ["ANALYST"]}
    assert mod.Person(**as_dict) == p


@pytest.mark.parametrize("name", ["text", "code", "meaning", "_defn", "__init__"])
def test_setattr_enum_class_attribute_name_is_not_a_code(mod, name) -> None:
    """Names of properties/methods on the enum MRO must be rejected like any other unknown code."""
    p = mod.Person()
    with pytest.raises(ValueError, match="Unknown VitalStatus enumeration code"):
        p.status = name


def test_enum_slots_classvar_present(mod) -> None:
    assert (
        mod.Person._enum_slots.items()
        >= {
            "status": ("VitalStatus", False),
            "roles": ("Role", True),
            "class_": ("VitalStatus", False),
        }.items()
    )


def test_enum_slots_keys_match_emitted_field_names(mod) -> None:
    """Keys must use pythongen's field mangling; a mismatch means coercion silently never fires."""
    field_names = {f.name for f in dataclasses.fields(mod.Person)}
    assert set(mod.Person._enum_slots) <= field_names
    assert "class_" in mod.Person._enum_slots and "class" not in mod.Person._enum_slots


def test_setattr_keyword_named_slot_coerces(mod) -> None:
    p = mod.Person()
    p.class_ = "ALIVE"
    assert isinstance(p.class_, mod.VitalStatus)


def test_no_runtime_import_for_coercion(mod) -> None:
    """The helper is emitted into the module, so generated code needs no new runtime symbol."""
    src = PythonGenerator(SCHEMA).serialize()
    assert "def _coerce_enum_slot(" in src
    assert "import _coerce_enum_slot" not in src and "coerce_enum_slot," not in src.split("class ")[0].replace(
        "def _coerce_enum_slot", ""
    )


def test_mixin_class_gets_the_hook(mod) -> None:
    """Mixins are instantiable; with __post_init__ no longer coercing, the hook must cover them."""
    m = mod.HasClearance()
    m.clearance = "HIGH"
    assert isinstance(m.clearance, mod.Clearance)
    assert mod.HasClearance(clearance="LOW").clearance == mod.Clearance.LOW


def test_post_init_no_longer_repeats_enum_coercion() -> None:
    src = PythonGenerator(SCHEMA).serialize()
    assert "self.status = VitalStatus(self.status)" not in src
    assert "self.roles = [v if isinstance(v, Role)" not in src
    # list normalisation stays in __post_init__: None -> [] is not the hook's job
    assert "self.roles = [self.roles] if self.roles is not None else []" in src


def test_construction_still_coerces_and_validates(mod) -> None:
    p = mod.Person(status="ALIVE", roles="ANALYST")
    assert p.status == mod.VitalStatus.ALIVE
    assert isinstance(p.status, mod.VitalStatus)
    assert p.roles == [mod.Role.ANALYST]
    assert mod.Person(roles=None).roles == []
    with pytest.raises(ValueError, match="Unknown VitalStatus enumeration code"):
        mod.Person(status="BOGUS")
