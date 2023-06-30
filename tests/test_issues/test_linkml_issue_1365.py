import json
import unittest

from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.schemaview import SchemaDefinition, SchemaView

from linkml.generators.pythongen import PythonGenerator
from linkml.validators import JsonSchemaDataValidator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase

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


class Issue1365TestCase(TestEnvironmentTestCase):
    env = env

    def test_generation_of_type_hierarchies(self):
        gen = PythonGenerator(schema)
        output = gen.serialize()
        mod = compile_python(output, "testschema")
