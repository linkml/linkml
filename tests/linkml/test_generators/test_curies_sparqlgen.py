"""Regression test for curies (sparqlgen).

``materialize_schema`` must propagate prefixes contributed by imported
sub-schemas onto the root schema so that generated SPARQL (and any downstream
consumer iterating ``schema.prefixes``) resolves prefixes declared only in
imports.
"""

from linkml.generators.sparqlgen import materialize_schema
from linkml_runtime.utils.schemaview import SchemaView


def test_imported_subschema_prefix_is_materialized(tmp_path):
    child = tmp_path / "child.yaml"
    child.write_text(
        """
id: https://example.org/child
name: child
prefixes:
  linkml: https://w3id.org/linkml/
  iso3166: https://www.iso.org/iso-3166-country-codes.html#
default_prefix: iso3166
default_range: string
imports:
  - linkml:types
"""
    )
    parent = tmp_path / "parent.yaml"
    parent.write_text(
        """
id: https://example.org/parent
name: parent
prefixes:
  linkml: https://w3id.org/linkml/
  parent: https://example.org/parent/
default_prefix: parent
default_range: string
imports:
  - linkml:types
  - ./child
classes:
  Holder:
    attributes:
      name:
        range: string
"""
    )
    sv = SchemaView(str(parent))
    materialize_schema(sv)
    assert "iso3166" in sv.schema.prefixes
    assert sv.schema.prefixes["iso3166"].prefix_reference == "https://www.iso.org/iso-3166-country-codes.html#"
