import re

import pytest
from linkml_runtime.utils.compile_python import compile_python
from .model.polymorphism_schema import gen_person_and_organisation_example_data, gen_person_and_organisation_schema, gen_type_hierarchy_example_schema
from pydantic import ValidationError
from linkml.generators.pydanticgen import PydanticGenerator

type_hierarchy_schema_str = """
id: http://example.org
name: inline-dict-test
imports:
  - https://w3id.org/linkml/types
prefixes:
  x: http://example.org/
default_prefix: x
default_range: string
description: test 
"""


class PydanticPolymorphismTestCase(TestEnvironmentTestCase):
    env = env

    def test_pydantic_obey_range(self):
        gen = PydanticGenerator(gen_person_and_organisation_schema())
        output = gen.serialize()
        
        self.assertNotRegex(output, "Union\[[a-zA-Z0-9]*\]", "a python Union should always have more than one option")

        output_subset = [line for line in output.splitlines() if "thingtype" in line]
        self.assertGreater(len(output_subset), 0)
        
        self.assertEqual(len([x for x in output_subset if 'x:Person' in x]),1)

        gen = PydanticGenerator(gen_person_and_organisation_schema("uri"))
        output = gen.serialize()
        output_subset = [line for line in output.splitlines() if "thingtype" in line]
        self.assertGreater(len(output_subset), 0)
        self.assertEqual(len([x for x in output_subset if 'http://example.org/Person' in x]) ,1)

    def test_type_hierarchy(self):
        gen_range_not_specified = PydanticGenerator(gen_type_hierarchy_example_schema())
        output = gen_range_not_specified.serialize()
        mod = compile_python(output, "testschema")
        id = "TEST:1"
        _ = mod.Person(id=id)
        _ = mod.Person(id=id, category=['http://example.org/Person'])
        _ = mod.Person(id=id, category=['x:Person'])
        self.assertRaises(ValidationError, lambda: mod.Person(category=['x:NamedThing']))

def test_pydantic_obey_range():
    gen = PydanticGenerator(schema_str)
    output = gen.serialize()

    assert (
        re.match(r"Union\[[a-zA-Z0-9]*\]", output) is None
    ), "a python Union should always have more than one option"

    output_subset = [line for line in output.splitlines() if "thingtype" in line]
    assert len(output_subset) > 0
    assert len([x for x in output_subset if "x:Person" in x]) == 1

    gen = PydanticGenerator(schema_str.replace("uriorcurie", "uri"))
    output = gen.serialize()
    output_subset = [line for line in output.splitlines() if "thingtype" in line]
    assert len(output_subset) > 0
    assert len([x for x in output_subset if "http://example.org/Person" in x]) == 1
    
def test_pydantic_load_poly_data(self):
  gen = PydanticGenerator(gen_person_and_organisation_schema()
  output = gen.serialize()
  mod = compile_python(output, "testschema")
  data = mod.Container.parse_raw(gen_person_and_organisation_example_data())
  self.assertEqual(len([x for x in data.things if isinstance(x,mod.Person)]),1)
  self.assertEqual(len([x for x in data.things if isinstance(x,mod.Organisation)]),2)


def test_type_hierarchy():
    gen_range_not_specified = PydanticGenerator(type_hierarchy_schema_str)
    output = gen_range_not_specified.serialize()
    mod = compile_python(output, "testschema")
    id = "TEST:1"
    _ = mod.Person(id=id)
    _ = mod.Person(id=id, category=["http://example.org/Person"])
    _ = mod.Person(id=id, category=["x:Person"])
    with pytest.raises(ValidationError):
        mod.Person(category=["x:NamedThing"])


def test_pydantic_load_poly_data():
    gen = PydanticGenerator(schema_str)
    output = gen.serialize()
    mod = compile_python(output, "testschema")
    data = mod.Container.parse_raw(data_str)

    assert len([x for x in data.things if isinstance(x, mod.Person)]) == 1
    assert len([x for x in data.things if isinstance(x, mod.Organisation)]) == 1
