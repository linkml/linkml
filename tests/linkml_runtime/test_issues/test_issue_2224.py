import unittest
from unittest import TestCase
from linkml_runtime.utils.schemaview import SchemaView
from jsonasobj2 import JsonObj

from tests.test_issues.environment import env


class Issue2224TestCase(TestCase):
    env = env

    def test_issue_2224_slot_classes(self):
        sv = SchemaView(env.input_path("linkml_issue_2224.yaml"))
        cls = sv.induced_class("DJController")

        # jog_wheels is a slot asserted at the schema level
        # check that the range (scalar value) is being materialized properly
        self.assertEqual(cls.attributes["jog_wheels"].range, "integer")
        # check that the examples (list) is being materialized properly
        self.assertIsInstance(cls.attributes["jog_wheels"].examples, list)
        for example in cls.attributes["jog_wheels"].examples:
            self.assertEqual(example.value, "2")
        for example in cls.attributes["volume_faders"].examples:
            self.assertEqual(example.value, "4")
        for example in cls.attributes["crossfaders"].examples:
            self.assertEqual(example.value, "1")
        # check that the annotations (dictionary) is being materialized properly
        self.assertIsInstance(cls.attributes["jog_wheels"].annotations, JsonObj)
        self.assertEqual(
            cls.attributes["jog_wheels"].annotations.expected_value.value,
            "an integer between 0 and 4",
        )
        self.assertEqual(
            cls.attributes["volume_faders"].annotations.expected_value.value,
            "an integer between 0 and 8",
        )

        # examples being overriden by slot_usage modification
        for example in cls.attributes["tempo"].examples:
            self.assertIn(example.value, ["120.0", "144.0", "126.8", "102.6"])
        # annotations being overriden by slot_usage modification
        self.assertEqual(
            cls.attributes["tempo"].annotations.expected_value.value,
            "a number between 0 and 300",
        )
        self.assertEqual(
            cls.attributes["tempo"].annotations.preferred_unit.value, "BPM"
        )


if __name__ == "__main__":
    unittest.main()
