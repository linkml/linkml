import unittest

from linkml_runtime.utils.compile_python import compile_python
from pydantic import ValidationError

from linkml.generators.pydanticgen import PydanticGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase

SCHEMA = env.input_path("linkml_issue_1429.yaml")


class Issue1429ConstCase(TestEnvironmentTestCase):
    env = env

    def test_pydanticgen_required_slots(self):
        """
        Test for https://github.com/linkml/linkml/issues/1429

        Ensures that required slots are required in the generated pydantic class
        """
        id = "ORCID:1234"
        full_name = "a b"
        gen = PydanticGenerator(SCHEMA)
        output = gen.serialize()
        mod = compile_python(output, "testschema")
        with self.assertRaises(ValidationError):
            p = mod.Person()
        with self.assertRaises(ValidationError):
            p = mod.Person(id=id)
        with self.assertRaises(ValidationError):
            p = mod.Person(full_name=full_name)
        p = mod.Person(id=id, full_name=full_name)
        self.assertEqual(id, p.id)
        self.assertEqual(full_name, p.full_name)


if __name__ == "__main__":
    unittest.main()
