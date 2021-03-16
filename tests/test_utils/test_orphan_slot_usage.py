import unittest

from linkml.generators.golrgen import GolrSchemaGenerator
from tests.test_utils.environment import env


class OrphanSlotUsageTestCase(unittest.TestCase):

    def test_orphan_slot_usage(self):
        """ Make sure an orphan slot_usage works """
        # The bug is that this goes into an endless loop
        output_dir = env.temp_file_path('slottest')
        GolrSchemaGenerator(env.input_path('orphan_slot_usage.yaml')).serialize(directory=output_dir)


if __name__ == '__main__':
    unittest.main()
