import json

from linkml.generators.jsonschemagen import JsonSchemaGenerator

# reported in https://github.com/linkml/linkml/issues/726

schema_str = """
id: http://example.org
name: issue-726
imports:
  - https://w3id.org/linkml/types
prefixes:
  x: http://example.org/
default_prefix: x
default_range: string
description: test

classes:
  C:
    tree_root: true
    slots:
      - s1
      - s2
      - s3
      - s4
    slot_usage:
      s1:
        equals_string: foo
      s3:
        equals_number: 32
  D:
    slots:
      - s1
      - s2
      - s3
      - s4
slots:
  s1:
    description: test slot that can be overridden with specific values
  s2:
    equals_string: bar
  s3:
    description: test override for equals_number
    range: integer
  s4:
    equals_number: 7
    range: integer
"""


def test_jsonschema():
    gen = JsonSchemaGenerator(schema_str)
    output = gen.serialize()
    js = json.loads(output)
    top_props = js["properties"]
    s1C = top_props["s1"]
    s2C = top_props["s2"]
    s3C = top_props["s3"]
    s4C = top_props["s4"]
    D = js["$defs"]["D"]["properties"]
    s1D = D["s1"]
    s2D = D["s2"]
    s3D = D["s3"]
    s4D = D["s4"]

    assert s1C["const"] == "foo"
    assert s2C["const"] == "bar"
    assert "const" not in s1D
    assert s2D["const"] == "bar"

    assert s3C["const"] == 32
    assert s4C["const"] == 7
    assert "const" not in s3D
    assert s4D["const"] == 7
