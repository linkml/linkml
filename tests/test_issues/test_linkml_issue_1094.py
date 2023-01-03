import  unittest

from linkml.generators.pydanticgen import PydanticGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase

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


class Issue1094ConstCase(TestEnvironmentTestCase):
    env = env

    def test_pydanticgen_inline_dict(self):
        gen = PydanticGenerator(schema_str)
        output = gen.serialize()

        output_subset = [line for line in output.splitlines() if "has_bikes: " in line]
        assert len(output_subset) == 1
        assert "has_bikes: Dict[str, Bike] = Field(default_factory=dict)" in output_subset[0]


if __name__ == "__main__":
    unittest.main()
