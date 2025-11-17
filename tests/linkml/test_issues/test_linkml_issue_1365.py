from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator

schema = """
id: http://example.org
name: sth
imports:
  - https://w3id.org/linkml/types
prefixes:
  x: http://example.org/
default_prefix: x
default_range: string
description: test


types:
  type2:
    typeof: category type
  category type:
    typeof: uriorcurie
    description: >-
      a category
  type3:
    typeof: type2
"""


def test_generation_of_type_hierarchies():
    gen = PythonGenerator(schema)
    output = gen.serialize()
    compile_python(output, "testschema")
