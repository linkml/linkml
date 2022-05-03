import unittest
from dataclasses import dataclass
from enum import Enum

import rdflib
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper, yaml_dumper, rdflib_dumper
from linkml_runtime.linkml_model import PermissibleValue
from linkml_runtime.loaders import json_loader
from linkml_runtime.utils.compile_python import compile_python
from rdflib import URIRef, Graph, Literal

from linkml.generators.pydanticgen import PydanticGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.reporting.model import RDF

from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env

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

EXAMPLE = rdflib.Namespace('http://example.org/')

class StatusEnumDC(Enum):
    ALIVE = "ALIVE"
    DEAD = "ALIVE"

@dataclass
class PersonDC:
    status: StatusEnumDC = None


class Issue723ExportCase(TestEnvironmentTestCase):
    env = env

    def setUp(self) -> None:
        gen = PythonGenerator(schema_str)
        output = gen.serialize()
        #print(output)
        mod = compile_python(output)
        self.mod = mod
        self.schemaview = SchemaView(schema_str)
        gen = PydanticGenerator(schema_str)
        output = gen.serialize()
        #print(output)
        self.pydantic_mod = compile_python(output)

    def test_plain_dataclasses(self):
        """
        Tests the behavior of plain non-linkml enums
        """
        p = PersonDC(status=StatusEnumDC.ALIVE)
        self.assertEqual(p.status, StatusEnumDC.ALIVE)
        self.assertEqual(p.status.value, StatusEnumDC.ALIVE.value)
        self.assertEqual(p.status.value, "ALIVE")
        self.assertNotEqual(p.status, "ALIVE")
        self.assertEqual(type(p.status), StatusEnumDC)
        self.assertEqual(type(p.status.value), str)

    def test_raises(self):
        mod = self.mod
        with self.assertRaises(ValueError) as e:
            p = mod.Person(status="FAKE")


    def test_initialized_enums(self):
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
        mod = self.mod
        p = mod.Person(status=mod.VitalStatus.ALIVE, roles=[mod.Role.ANALYST, mod.Role.INVESTIGATOR])
        # Test behavior of dumpers
        pd = json_dumper.to_dict(p)
        #print(pd)
        self.assertEqual(pd['status'], 'ALIVE')
        self.assertCountEqual(pd['roles'], ['ANALYST', 'INVESTIGATOR'])
        p_json = json_dumper.dumps(p)
        p_roundtrip = json_loader.loads(p_json, target_class=mod.Person)
        self.assertEqual(p_roundtrip, p)
        #print(yaml_dumper.dumps(p))
        # Current behavior: when enums are created at time of initialization,
        # they are created as Enum instances, NOT permissible value instances
        self.assertEqual(p.status, mod.VitalStatus(mod.VitalStatus.ALIVE))
        self.assertNotEqual(p.status, mod.VitalStatus.ALIVE)
        self.assertCountEqual(p.roles, [mod.Role(mod.Role.INVESTIGATOR), mod.Role(mod.Role.ANALYST)])
        self.assertEqual(type(p.status), mod.VitalStatus)
        self.assertNotEqual(type(p.status), PermissibleValue)
        self.assertEqual(type(p.roles[0]), mod.Role)
        g = rdflib_dumper.as_rdf_graph(p, schemaview=self.schemaview)
        [subj] = list(g.subjects(RDF.type, EXAMPLE.Person))
        #for t in g.triples((None,None,None)):
        #    print(t)
        self.assertEqual(list(g.objects(subj, EXAMPLE.status)), [EXAMPLE.Alive])
        self.assertCountEqual(list(g.objects(subj, EXAMPLE.roles)), [Literal('INVESTIGATOR'), Literal('ANALYST')])

    def test_assigned_enum(self):
        """
        Test the behavior of enums that are created post-initialization:

        .. code:: python

           p = Person()
           p.status = VitalStatus.ALIVE

        In this case, the dict/json/yaml is inconveniently expanded

        .. code:: python

            {'status': {'text': 'ALIVE'}, 'roles': [{'text': 'ANALYST'}, {'text': 'INVESTIGATOR'}]}
        """
        mod = self.mod
        p = mod.Person()
        p.status = mod.VitalStatus.ALIVE
        p.roles = [mod.Role.ANALYST, mod.Role.INVESTIGATOR]
        pd = json_dumper.to_dict(p)
        print(pd)
        # we might expect this
        #self.assertEqual(pd['status'], 'ALIVE')
        self.assertCountEqual(pd['roles'], [{'text': 'ANALYST'}, {'text': 'INVESTIGATOR'}])
        p_json = json_dumper.dumps(p)
        # this does NOT roundtrip:
        #p_roundtrip = json_loader.loads(p_json, target_class=mod.Person)
        #self.assertEqual(p_roundtrip, p)
        print(yaml_dumper.dumps(p))
        self.assertEqual(p.status, mod.VitalStatus.ALIVE)
        self.assertCountEqual(p.roles, [mod.Role.INVESTIGATOR, mod.Role.ANALYST])
        self.assertEqual(type(p.status), PermissibleValue)
        self.assertNotEqual(type(p.status), mod.VitalStatus)
        self.assertEqual(type(p.roles[0]), PermissibleValue)
        # currently fails
        #g = rdflib_dumper.as_rdf_graph(p, schemaview=self.schemaview)
        #for t in g.triples((None,None,None)):
        #    print(t)

    def test_assigned_wrapped_enums(self):
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
        mod = self.mod
        p = mod.Person()
        p.status = mod.VitalStatus(mod.VitalStatus.ALIVE)
        p.roles = [mod.Role(mod.Role.ANALYST), mod.Role(mod.Role.INVESTIGATOR)]
        p2 = mod.Person(status=mod.VitalStatus.ALIVE, roles=[mod.Role.ANALYST, mod.Role.INVESTIGATOR])
        self.assertEqual(p2, p)
        p3 = mod.Person(status="ALIVE", roles=["ANALYST", "INVESTIGATOR"])
        self.assertEqual(p3, p)
        # Test behavior of dumpers
        pd = json_dumper.to_dict(p)
        #print(pd)
        self.assertEqual(pd['status'], 'ALIVE')
        self.assertCountEqual(pd['roles'], ['ANALYST', 'INVESTIGATOR'])
        p_json = json_dumper.dumps(p)
        p_roundtrip = json_loader.loads(p_json, target_class=mod.Person)
        self.assertEqual(p_roundtrip, p)
        self.assertEqual(p.status, mod.VitalStatus(mod.VitalStatus.ALIVE))
        self.assertNotEqual(p.status, mod.VitalStatus.ALIVE)
        self.assertCountEqual(p.roles, [mod.Role(mod.Role.INVESTIGATOR), mod.Role(mod.Role.ANALYST)])
        self.assertEqual(type(p.status), mod.VitalStatus)
        self.assertNotEqual(type(p.status), PermissibleValue)
        self.assertEqual(type(p.roles[0]), mod.Role)
        g = rdflib_dumper.as_rdf_graph(p, schemaview=self.schemaview)
        [subj] = list(g.subjects(RDF.type, EXAMPLE.Person))
        #for t in g.triples((None,None,None)):
        #    print(t)
        self.assertEqual(list(g.objects(subj, EXAMPLE.status)), [EXAMPLE.Alive])
        self.assertCountEqual(list(g.objects(subj, EXAMPLE.roles)), [Literal('INVESTIGATOR'), Literal('ANALYST')])

    def test_pydantic(self):
        mod = self.pydantic_mod
        p = mod.Person(status="ALIVE", roles=["ANALYST", "INVESTIGATOR"])
        print(p)
        with self.assertRaises(ValueError) as e:
            p = mod.Person(status="FAKE")
        #with self.assertRaises(ValueError) as e:
        #    p = mod.Person()
        #    p.status = "FAKE"
        p2 = mod.Person(status=mod.VitalStatus.ALIVE, roles=[mod.Role.ANALYST, mod.Role.INVESTIGATOR])
        self.assertEqual(p, p2)
        p3 = mod.Person()
        p3.status = mod.VitalStatus.ALIVE
        p3.roles = [mod.Role.ANALYST, mod.Role.INVESTIGATOR]
        self.assertEqual(p, p3)
        self.assertEqual(p.status, mod.VitalStatus.ALIVE)
        self.assertEqual(type(p.status), mod.VitalStatus)
        self.assertEqual(p.roles, [mod.Role.ANALYST, mod.Role.INVESTIGATOR])
        # test the "double wrap" code
        p.status = mod.VitalStatus(mod.VitalStatus.ALIVE)
        self.assertEqual(p.status, mod.VitalStatus.ALIVE)
        # TODO: not implemented?
        #print(p.dict())
        #not supported yet
        #pd = json_dumper.to_dict(p)


if __name__ == '__main__':
    unittest.main()
