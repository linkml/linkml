"""Regression test for ISSUE-curies.md (yarrrmlgen)."""

import yaml

from linkml.generators.yarrrmlgen import YarrrmlGenerator


def test_imported_subschema_prefix_is_emitted_in_yarrrml(tmp_path):
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
    out = yaml.safe_load(YarrrmlGenerator(str(parent)).serialize())
    assert "iso3166" in out["prefixes"]
    assert out["prefixes"]["iso3166"] == "https://www.iso.org/iso-3166-country-codes.html#"
