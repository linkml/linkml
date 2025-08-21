import json

import jsonschema

from linkml.generators.jsonschemagen import JsonSchemaGenerator

schema_str = """
id: http://example.org

types:
  string:
    base: str
    uri: xsd:string
  integer:
    base: int
    uri: xsd:int
classes:
  Container:
    tree_root: true
    attributes:
      persons:
        range: Person
        inlined: true
        multivalued: true
  Person:
    attributes:
      name:
        identifier: true
      age:
        range: integer
        required: true
      gender:
        range: string
        required: true
"""

# https://stackoverflow.com/questions/27357861/dictionary-like-json-schema
json_str = """
{"persons":
 {
     "Bob": {
         "age": 42,
         "gender": "male"
     },
     "Alice": {
         "age": 37,
         "gender": "female"
     }
 }
}

"""


def test_inslined_as_dict():
    """Make sure that enums are generated as part of the output"""
    gen = JsonSchemaGenerator(schema_str)
    jsonschema_str = gen.serialize(not_closed=False)

    obj = json.loads(json_str)
    jsonschema_obj = json.loads(jsonschema_str)
    v = jsonschema.validate(obj, jsonschema_obj)
    assert v is None
