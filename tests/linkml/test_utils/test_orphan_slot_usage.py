from linkml.generators.golrgen import GolrSchemaGenerator


def test_orphan_slot_usage(input_path, tmp_path):
    """Make sure an orphan slot_usage works"""
    # The bug is that this goes into an endless loop
    GolrSchemaGenerator(input_path("orphan_slot_usage.yaml")).serialize(directory=tmp_path)
