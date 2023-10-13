from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition

from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.utils.schema_builder import SchemaBuilder


def test_monotonic():
    """
    Ensure that a schema which uses attributes can be successfully translated to JSONLD.

    Currently this requires a second pass of the schema through schema loader, after mangled
    names are already introduced

    Tests https://github.com/linkml/linkml/issues/872
    """
    sb = SchemaBuilder()
    sb.add_class(
        "C",
        [SlotDefinition("s1", description="d1")],
        use_attributes=True,
        from_schema="http://x.org",
    )
    sb.add_defaults()
    schema = sb.schema
    s = JSONLDGenerator(yaml_dumper.dumps(schema)).serialize()
    assert s is not None
