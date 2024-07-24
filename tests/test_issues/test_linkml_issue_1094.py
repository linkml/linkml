from typing import Dict, List, Union

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
      - has_bike_list
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
  - has_bike_list:
      range: bike
      multivalued: true
      inlined: true
      required: true
      inlined_as_list: true
"""


def test_pydanticgen_inline_dict():
    gen = PydanticGenerator(schema_str)
    mod = gen.compile_module()
    Person = getattr(mod, "Person")
    Bike = getattr(mod, "Bike")

    dict_field = Person.model_fields["has_bikes"]
    list_field = Person.model_fields["has_bike_list"]

    assert dict_field.annotation == Dict[str, Union[str, Bike]]
    assert list_field.annotation == List[Bike]

    assert dict_field.default_factory is None
    assert list_field.default_factory is None

    assert str(dict_field.default) == "PydanticUndefined"
    assert str(list_field.default) == "PydanticUndefined"
