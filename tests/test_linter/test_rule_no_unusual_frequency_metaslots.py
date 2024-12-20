import unittest

from linkml.linter.rules import NoUnusualFrequencyMetaslotsRule
from linkml.utils.schema_builder import SchemaBuilder
from linkml_runtime import SchemaView
from linkml.linter.config.datamodel.config import RuleConfig, RuleLevel


class TestRuleNoUnusualFrequencyMetaslots(unittest.TestCase):
    def setUp(self) -> None:
        schema_builder = SchemaBuilder()
        desired_slot_names = [
            'slot_1',
            'slot_2',
            'slot_3',
            'slot_4',
            'slot_5',
            'slot_6',
            'slot_7',
            'slot_8',
            'slot_9',
            'slot_10',
        ]

        for slot_name in desired_slot_names:
            schema_builder.add_slot(
                slot_name,
            )

        self.schema_view = SchemaView(schema_builder.schema)

    def test_slots_created(self):
        view_slots = self.schema_view.all_slots()
        view_slots_keys = list(view_slots.keys())
        self.assertIn('slot_1', view_slots_keys)

    def test_unusual_frequency_metaslots(self):
        config = RuleConfig(level=RuleLevel.error)
        rule = NoUnusualFrequencyMetaslotsRule(config)
        problems = list(rule.check(self.schema_view))

        self.assertEqual(len(problems), 1)
        # currently hardcoded to yield LinterProblem(message="Unusual frequency metaslots check not implemented yet")
