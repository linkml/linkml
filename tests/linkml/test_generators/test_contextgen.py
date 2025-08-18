import re

from linkml import LOCAL_TYPES_YAML_FILE, METAMODEL_NAMESPACE
from linkml.generators.jsonldcontextgen import ContextGenerator


def test_context(kitchen_sink_path):
    """json schema"""
    ContextGenerator(kitchen_sink_path).serialize()


def test_rdflib_string_handling():
    """
    Ensure that we don't make mistakes expecting rdflib stringlike-classes to behave
    like strings!

    Eg. :class:`rdflib.Namespace` inherits from ``str`` , but overrides the ``contains`` method
    """
    generated = ContextGenerator(LOCAL_TYPES_YAML_FILE).serialize(base=METAMODEL_NAMESPACE)
    assert not re.search(r"http:/[^/]", generated)
    assert not re.search(r"https:/[^/]", generated)
