import json
import unittest

from linkml.generators.jsonschemagen import JsonSchemaGenerator

from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env

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

class Issue726ConstCase(TestEnvironmentTestCase):
    env = env

    def test_jsonschema(self):
        gen = JsonSchemaGenerator(schema_str)
        output = gen.serialize()
        print(output)
        js = json.loads(output)
        top_props = js['properties']
        s1C = top_props['s1']
        s2C = top_props['s2']
        s3C = top_props['s3']
        s4C = top_props['s4']
        D = js['$defs']['D']['properties']
        s1D = D['s1']
        s2D = D['s2']
        s3D = D['s3']
        s4D = D['s4']

        self.assertEqual(s1C['const'], 'foo')
        self.assertEqual(s2C['const'], 'bar')
        self.assertNotIn('const', s1D)
        self.assertEqual(s2D['const'], 'bar')

        self.assertEqual(s3C['const'], 32)
        self.assertEqual(s4C['const'], 7)
        self.assertNotIn('const', s3D)
        self.assertEqual(s4D['const'], 7)


if __name__ == '__main__':
    unittest.main()
