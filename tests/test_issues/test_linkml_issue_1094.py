from pydantic.version import VERSION
from typing import Dict, Union

from linkml.generators.pydanticgen import PydanticGenerator

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
  person:
    slots:
      - id
      - has_bikes
    slot_usage:
      - has_bikes:
  bike:
    slots:
      - name
      - color
    slot_usage:
      name:
        identifier: true
        required: true
slots:
  - id:
      required: true
  - name
  - color
  - has_bikes:
      range: bike
      multivalued: true
      inlined: true
      required: true
"""


def test_pydanticgen_inline_dict():
    gen = PydanticGenerator(schema_str)
    mod = gen.compile_module()
    Person = getattr(mod, 'Person')
    Bike = getattr(mod, 'Bike')
    if VERSION.startswith('1'):
        field = Person.__fields__['has_bikes']
    else:
        field = Person.model_fields['has_bikes']

    assert field.annotation == Dict[str, Union[str,Bike]]
