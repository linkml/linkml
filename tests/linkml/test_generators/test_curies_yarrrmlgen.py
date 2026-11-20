"""Regression test for curies (yarrrmlgen)."""

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
    # A genuine user prefix is present, so the fallback default must NOT be added.
    assert "ex" not in out["prefixes"]


def test_only_builtin_prefixes_triggers_ex_fallback(tmp_path):
    """A schema declaring only built-in prefixes gets the ``ex`` default namespace.

    ``linkml``/``xsd``/``shex``/``schema``/``rdf`` propagated from ``linkml:types``
    must not count as user-declared, otherwise no default namespace would be
    emitted and the YARRRML would have nowhere to hang generated subjects.
    """
    schema = tmp_path / "only_builtins.yaml"
    schema.write_text(
        """
id: https://example.org/only_builtins
name: only_builtins
prefixes:
  linkml: https://w3id.org/linkml/
  xsd: http://www.w3.org/2001/XMLSchema#
default_prefix: linkml
default_range: string
imports:
  - linkml:types
classes:
  Holder:
    attributes:
      name:
        range: string
"""
    )
    out = yaml.safe_load(YarrrmlGenerator(str(schema)).serialize())
    assert out["prefixes"]["ex"] == "https://example.org/default#"
