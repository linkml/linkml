from linkml.generators.jsonldcontextgen import ContextGenerator


def test_context(kitchen_sink_path):
    """json schema"""
    ContextGenerator(kitchen_sink_path).serialize()
