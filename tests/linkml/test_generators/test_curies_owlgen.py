"""Regression test for ISSUE-curies.md (owlgen)."""

from linkml.generators.owlgen import OwlSchemaGenerator


def test_imported_subschema_prefix_is_bound_in_owl(tmp_path):
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

    # Check the graph's namespace bindings directly rather than round-tripping
    # through turtle: rdflib's turtle serializer drops prefix declarations that
    # are not used by any triple, so a bound-but-unused prefix would be lost on
    # serialization. The feature under test is that the imported prefix is
    # *bound* on the generated graph (matching the sibling shacl/yarrrml tests).
    g = OwlSchemaGenerator(str(parent)).as_graph()
    bound = dict(g.namespaces())
    assert "iso3166" in bound
    assert str(bound["iso3166"]) == "https://www.iso.org/iso-3166-country-codes.html#"
