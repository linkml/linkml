import  unittest

from linkml.generators.pydanticgen import PydanticGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase
from linkml_runtime.utils.compile_python import compile_python

schema_str = """
id: http://example.org
name: inline-dict-test
imports:
  - https://w3id.org/linkml/types
prefixes:
  x: http://example.org/
default_prefix: x
default_range: string
description: test

classes:
  NamedThing:
    slots:
      - id
      - full_name
      - thingtype
  Person:
    is_a: NamedThing
    slots:
      - height
  Organisation:
    is_a: NamedThing
    slots:
      - number_of_employees
  Container:
    tree_root: true
    slots:
      - things
slots:
  id:
    identifier: true
    range: string
    required: true
  thingtype:
    designates_type: true
    range: uriorcurie
  full_name:
    range: string
  height:
    range: integer
  number_of_employees:
    range: integer
  things:
    range: NamedThing
    multivalued: true
    inlined_as_list: true
"""

data_str = """
{
  "things": [
    {
      "id": 1,
      "thingtype": "x:Person",
      "full_name": "phoebe",
      "height": 10
    },
    {
      "id": 2,
      "thingtype": "x:Organisation",
      "full_name": "University of Earth",
      "number_of_employees": 2
    }
  ]
}
"""


class PydanticPolymorphismTestCase(TestEnvironmentTestCase):
    env = env

    def test_pydantic_obey_range(self):
        gen = PydanticGenerator(schema_str)
        output = gen.serialize()
        output_subset = [line for line in output.splitlines() if "thingtype" in line]
        self.assertGreater(len(output_subset), 0)
        
        self.assertTrue("const=True" in output_subset[0])
        self.assertEqual(len([x for x in output_subset if 'x:Person' in x]),1)

        gen = PydanticGenerator(schema_str.replace("uriorcurie","uri"))
        output = gen.serialize()
        output_subset = [line for line in output.splitlines() if "thingtype" in line]
        self.assertGreater(len(output_subset), 0)
        self.assertTrue("const=True" in output_subset[0])
        self.assertEqual(len([x for x in output_subset if 'http://example.org/Person' in x]) ,1)

    def test_pydantic_load_poly_data(self):
        gen = PydanticGenerator(schema_str)
        output = gen.serialize()
        mod = compile_python(output, "testschema")
        data = mod.Container.parse_raw(data_str)
        
        self.assertEqual(len([x for x in data.things if isinstance(x,mod.Person)]),1)
        self.assertEqual(len([x for x in data.things if isinstance(x,mod.Organisation)]),1)





if __name__ == "__main__":
    unittest.main()
