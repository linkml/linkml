"""Regression test for ISSUE-curies.md (pythongen).

Add this function inside tests/linkml/test_generators/test_pythongen.py;
imports `PythonGenerator` and `compile_python` are already at top of that file.
"""

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.utils.compile_python import compile_python


def test_imported_subschema_pv_meaning_prefix_is_emitted(tmp_path):
    """
    Regression test: prefixes declared only in imported sub-schemas must be
    emitted as ``CurieNamespace`` bindings when the corresponding permissible
    value ``meaning:`` URIs reference them.
    """
    child = tmp_path / "child.yaml"
    child.write_text(
        """
id: https://example.org/child
name: child
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/child/
  iso3166: https://www.iso.org/iso-3166-country-codes.html#
default_prefix: ex
default_range: string
imports:
  - linkml:types
enums:
  CountryStyleEnum:
    permissible_values:
      Country:
        meaning: "iso3166:"
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
      style:
        range: CountryStyleEnum
"""
    )

    pstr = str(PythonGenerator(str(parent), mergeimports=True).serialize())
    assert "ISO3166 = CurieNamespace('iso3166'," in pstr
    assert "EX = CurieNamespace('ex'," in pstr
    module = compile_python(pstr)
    assert str(module.ISO3166) == "https://www.iso.org/iso-3166-country-codes.html#"
    assert str(module.CountryStyleEnum.Country.meaning) == "https://www.iso.org/iso-3166-country-codes.html#"
