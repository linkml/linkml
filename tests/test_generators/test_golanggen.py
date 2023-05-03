import sys
import unittest

from linkml.generators.golanggen import GolangGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path("kitchen_sink.yaml")
OUT = env.expected_path("kitchen_sink.go")


class GolangGeneratorTestCase(unittest.TestCase):
    def test_golanggen(self):
        """typescript"""
        code = GolangGenerator(SCHEMA, mergeimports=True).serialize()
        with open(OUT, "w") as stream:
            stream.write(code)

        def assert_in(s: str) -> None:
            assert s.replace(" ", "") in code.replace(" ", "")

        assert "package kitchen" in code
        assert_in("type Person struct {")
        assert_in("HasFamilialRelationships []FamilialRelationship")
        assert_in("CodeSystems []CodeSystem")


if __name__ == "__main__":
    unittest.main()
