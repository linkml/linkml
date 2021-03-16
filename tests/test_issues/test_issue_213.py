import unittest

from tests.utils.test_environment import TestEnvironmentTestCase

from linkml.utils.schemaloader import SchemaLoader
from tests.test_issues.environment import env


class SlotUsageDefaultTest(TestEnvironmentTestCase):
    env = env

    def test_slot_usage_range(self):
        """ Test to make the absolute minimal model work """
        schema = SchemaLoader(env.input_path('issue_213.yaml')).resolve()
        self.assertEqual('string', schema.slots['my slot'].range)


if __name__ == '__main__':
    unittest.main()
