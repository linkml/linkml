import unittest

from linkml.generators.yamlgen import YAMLGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class IssueInheritMetaslotsTestCase(TestEnvironmentTestCase):
    """
    Tests: https://github.com/linkml/linkml/issues/270

    """

    env = env

    def test_metaslot_inheritance(self):
        name = "linkml_issue_270"
        infile = env.input_path(f"{name}.yaml")
        gen = YAMLGenerator(infile)
        schema = gen.schema
        s = schema.slots["s1"]
        c2_s1 = schema.slots["C2_s1"]
        self.assertEqual(c2_s1.alias, s.name)
        self.assertEqual(c2_s1.owner, "C2")

        for k in [
            "description",
            "comments",
            "todos",
            "pattern",
            "recommended",
            "slot_uri",
        ]:
            self.assertEqual(getattr(s, k), getattr(c2_s1, k))


if __name__ == "__main__":
    unittest.main()
