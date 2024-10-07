import unittest
from dataclasses import dataclass
from enum import Enum

import pytest
import rdflib
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper, rdflib_dumper
from linkml_runtime.linkml_model import PermissibleValue
from linkml_runtime.loaders import json_loader
from linkml_runtime.utils.compile_python import compile_python
from rdflib import Literal

from linkml.generators.pydanticgen import PydanticGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.reporting.model import RDF

# reported in https://github.com/linkml/linkml/issues/723

schema_str = """
id: http://example.org
name: issue-723
imports:
  - https://w3id.org/linkml/types
prefixes:
  x: http://example.org/
default_prefix: x
default_range: string
description: test

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
        meaning: x:Alive
      DEAD:
        meaning: x:Dead

  Role:
    permissible_values:
      INVESTIGATOR:
      SAMPLE_COLLECTOR:
      ANALYST:
"""

EXAMPLE = rdflib.Namespace("http://example.org/")


class StatusEnumDC(Enum):
    ALIVE = "ALIVE"
    DEAD = "ALIVE"


@dataclass
class PersonDC:
    status: StatusEnumDC = None


@pytest.fixture(scope="module")
def pythongen_module():
    gen = PythonGenerator(schema_str)
    output = gen.serialize()
    return compile_python(output)


@pytest.fixture(scope="module")
def schemaview():
    return SchemaView(schema_str)


@pytest.fixture(scope="module")
def pydanticgen_module():
    gen = PydanticGenerator(schema_str)
    output = gen.serialize()
    return compile_python(output)


def test_plain_dataclasses():
    """
    Tests the behavior of plain non-linkml enums
    """
    p = PersonDC(status=StatusEnumDC.ALIVE)
    assert p.status == StatusEnumDC.ALIVE
    assert p.status.value == StatusEnumDC.ALIVE.value
    assert p.status.value == "ALIVE"
    assert p.status != "ALIVE"
    assert isinstance(p.status, StatusEnumDC)
    assert isinstance(p.status.value, str)


def test_raises(pythongen_module):
    with pytest.raises(ValueError):
        pythongen_module.Person(status="FAKE")


def test_initialized_enums(pythongen_module, schemaview):
    """
    Test the behavior of enums that are created on initialization:

    .. code:: python

        p = Person(status=VitalStatus.ALIVE, roles=[...])

    In this case the dictionary/json/yaml serialization is compact

    .. code:: python

        {'status': 'ALIVE', 'roles': ['ANALYST', 'INVESTIGATOR']}

    However, the user should be aware that the type of person.role
    is NOT PermissibleValue, it is the enum, i.e

    .. code:: python

        p.status != mod.VitalStatus.ALIVE
        p.status == mod.VitalStatus(mod.VitalStatus.ALIVE)

    """
    mod = pythongen_module
    p = mod.Person(
        status=mod.VitalStatus.ALIVE,
        roles=[mod.Role.ANALYST, mod.Role.INVESTIGATOR],
    )
    # Test behavior of dumpers
    pd = json_dumper.to_dict(p)
    tc = unittest.TestCase()
    assert pd["status"] == "ALIVE"
    tc.assertCountEqual(pd["roles"], ["ANALYST", "INVESTIGATOR"])
    p_json = json_dumper.dumps(p)
    p_roundtrip = json_loader.loads(p_json, target_class=mod.Person)
    assert p_roundtrip == p
    # Current behavior: when enums are created at time of initialization,
    # they are created as Enum instances, NOT permissible value instances
    assert p.status == mod.VitalStatus(mod.VitalStatus.ALIVE)
    assert p.status != mod.VitalStatus.ALIVE
    tc.assertCountEqual(p.roles, [mod.Role(mod.Role.INVESTIGATOR), mod.Role(mod.Role.ANALYST)])
    assert type(p.status) is mod.VitalStatus
    assert type(p.status) is not PermissibleValue
    assert type(p.roles[0]) is mod.Role
    g = rdflib_dumper.as_rdf_graph(p, schemaview=schemaview)
    [subj] = list(g.subjects(RDF.type, EXAMPLE.Person))
    assert list(g.objects(subj, EXAMPLE.status)) == [EXAMPLE.Alive]
    tc.assertCountEqual(list(g.objects(subj, EXAMPLE.roles)), [Literal("INVESTIGATOR"), Literal("ANALYST")])


def test_assigned_enum(pythongen_module):
    """
    Test the behavior of enums that are created post-initialization:

    .. code:: python

        p = Person()
        p.status = VitalStatus.ALIVE

    In this case, the dict/json/yaml is inconveniently expanded

    .. code:: python

        {'status': {'text': 'ALIVE'}, 'roles': [{'text': 'ANALYST'}, {'text': 'INVESTIGATOR'}]}
    """
    mod = pythongen_module
    p = mod.Person()
    p.status = mod.VitalStatus.ALIVE
    p.roles = [mod.Role.ANALYST, mod.Role.INVESTIGATOR]
    pd = json_dumper.to_dict(p)
    # we might expect this
    # self.assertEqual(pd['status'], 'ALIVE')
    tc = unittest.TestCase()
    tc.assertCountEqual(pd["roles"], [{"text": "ANALYST"}, {"text": "INVESTIGATOR"}])
    json_dumper.dumps(p)
    # this does NOT roundtrip:
    # p_roundtrip = json_loader.loads(p_json, target_class=mod.Person)
    # self.assertEqual(p_roundtrip, p)
    assert p.status == mod.VitalStatus.ALIVE
    tc.assertCountEqual(p.roles, [mod.Role.INVESTIGATOR, mod.Role.ANALYST])
    assert type(p.status) is PermissibleValue
    assert type(p.status) is not mod.VitalStatus
    assert type(p.roles[0]) is PermissibleValue


def test_assigned_wrapped_enums(pythongen_module, schemaview):
    """
    Test the behavior of enums that are created post-initialization,
    but using an additional "wrap" of the enum

    .. code:: python

        p = mod.Person()
        p.status = mod.VitalStatus(mod.VitalStatus.ALIVE)
        p.roles = [mod.Role(mod.Role.ANALYST), mod.Role(mod.Role.INVESTIGATOR)]

    Here the behavior should be identical to doing this on initialization:

    .. code:: python

        mod.Person(status=mod.VitalStatus.ALIVE, roles=[mod.Role.ANALYST, mod.Role.INVESTIGATOR])

    or using strings as shorthand

    .. code:: python

        mod.Person(status="ALIVE", roles=["ANALYST", "INVESTIGATOR"])


    """
    mod = pythongen_module
    p = mod.Person()
    p.status = mod.VitalStatus(mod.VitalStatus.ALIVE)
    p.roles = [mod.Role(mod.Role.ANALYST), mod.Role(mod.Role.INVESTIGATOR)]
    p2 = mod.Person(
        status=mod.VitalStatus.ALIVE,
        roles=[mod.Role.ANALYST, mod.Role.INVESTIGATOR],
    )
    assert p2 == p
    p3 = mod.Person(status="ALIVE", roles=["ANALYST", "INVESTIGATOR"])
    assert p3 == p
    # Test behavior of dumpers
    pd = json_dumper.to_dict(p)
    tc = unittest.TestCase()
    assert pd["status"] == "ALIVE"
    tc.assertCountEqual(pd["roles"], ["ANALYST", "INVESTIGATOR"])
    p_json = json_dumper.dumps(p)
    p_roundtrip = json_loader.loads(p_json, target_class=mod.Person)
    assert p_roundtrip == p
    assert p.status == mod.VitalStatus(mod.VitalStatus.ALIVE)
    assert p.status != mod.VitalStatus.ALIVE
    tc.assertCountEqual(p.roles, [mod.Role(mod.Role.INVESTIGATOR), mod.Role(mod.Role.ANALYST)])
    assert type(p.status) is mod.VitalStatus
    assert type(p.status) is not PermissibleValue
    assert type(p.roles[0]) is mod.Role
    g = rdflib_dumper.as_rdf_graph(p, schemaview=schemaview)
    [subj] = list(g.subjects(RDF.type, EXAMPLE.Person))
    assert list(g.objects(subj, EXAMPLE.status)) == [EXAMPLE.Alive]
    tc.assertCountEqual(
        list(g.objects(subj, EXAMPLE.roles)),
        [Literal("INVESTIGATOR"), Literal("ANALYST")],
    )


def test_pydantic(pydanticgen_module):
    mod = pydanticgen_module
    p = mod.Person(status="ALIVE", roles=["ANALYST", "INVESTIGATOR"])
    with pytest.raises(ValueError):
        mod.Person(status="FAKE")

    p2 = mod.Person(
        status=mod.VitalStatus.ALIVE,
        roles=[mod.Role.ANALYST, mod.Role.INVESTIGATOR],
    )
    assert p == p2
    p3 = mod.Person()
    p3.status = mod.VitalStatus.ALIVE
    p3.roles = [mod.Role.ANALYST, mod.Role.INVESTIGATOR]
    assert p == p3
    assert p.status == mod.VitalStatus.ALIVE
    assert p.roles == [mod.Role.ANALYST, mod.Role.INVESTIGATOR]
    # test the "double wrap" code
    p.status = mod.VitalStatus(mod.VitalStatus.ALIVE)
    assert p.status == mod.VitalStatus.ALIVE
    # TODO: not implemented?
    # not supported yet
    # pd = json_dumper.to_dict(p)
