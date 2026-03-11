import json


def gen_person_and_organisation_schema(type_descriptor_range: str = "uriorcurie") -> str:
    return f"""
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
    class_uri: "http://testbreaker/not-the-uri-you-expect"
    slots:
      - height
  Organisation:
    is_a: NamedThing
    slots:
      - number_of_employees
  NonProfit:
    is_a: Organisation
  ForProfit:
    is_a: Organisation
    slots:
      - target_profit_margin
  Container:
    tree_root: true
    slots:
      - things
  ContainerWithOneSibling:
    slots:
      - persons
slots:
  id:
    identifier: true
    range: string
    required: true
  thingtype:
    designates_type: true
    range: {type_descriptor_range}
  full_name:
    range: string
  target_profit_margin:
    range: float
  height:
    range: integer
  number_of_employees:
    range: integer
  things:
    range: NamedThing
    multivalued: true
    inlined_as_list: true
  persons:
    range: Person
    multivalued: true
    inlined_as_list: true
"""


def gen_person_and_organisation_example_data(type_descriptor_range: str = "uriorcurie") -> str:
    person_td = "http://testbreaker/not-the-uri-you-expect"
    pfx = "x:"
    if type_descriptor_range == "string":
        pfx = ""
        person_td = "Person"
    elif type_descriptor_range == "uri":
        pfx = "http://example.org/"

    data = {
        "things": [
            {"id": "1", "thingtype": f"{person_td}", "full_name": "phoebe", "height": 10},
            {
                "id": "2",
                "thingtype": f"{pfx}Organisation",
                "full_name": "University of Earth",
                "number_of_employees": 2,
            },
            {
                "id": "3",
                "thingtype": f"{pfx}ForProfit",
                "full_name": "Company",
                "target_profit_margin": 0.1,
            },
        ]
    }

    return json.dumps(data)


def gen_type_hierarchy_example_schema(type_descriptor_range: str = "uriorcurie") -> str:
    return f"""
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
      - category
  Person:
    is_a: NamedThing

types:
  category type:
    typeof: {type_descriptor_range}
    description: >-
      see biolink model

slots:
  id:
    identifier: true
    range: string
    required: true
  type:
    slot_uri: rdf:type
    multivalued: true
  category:
    is_a: type
    range: category type
    designates_type: true
    is_class_field: true
    multivalued: true
"""
