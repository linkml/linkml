from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper

from linkml.generators.linkmlgen import LinkmlGenerator

schema_yaml = """
name: test_schema
id: https://w3id.org/nmdc/test_schema
enums:
  SomeEnum:
    permissible_values:
      some_pv:
        structured_aliases:
          some_alias:
            literal_form: some_alias
            predicate: NARROW_SYNONYM
            contexts:
              - https://example.com/
"""


def test_without_contexts():
    current_generator = LinkmlGenerator(schema_yaml)
    assert current_generator.schemaview.schema.name == "test_schema"