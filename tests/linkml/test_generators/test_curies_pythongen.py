"""Regression test for curies (pythongen).

Add this function inside tests/linkml/test_generators/test_pythongen.py;
imports `PythonGenerator` and `compile_python` are already at top of that file.
"""

import pytest

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, TypeDefinition
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


def test_enum_uri_and_code_set_prefixes_are_emitted(tmp_path):
    """``visit_enum`` must emit the prefixes referenced by ``enum_uri`` and ``code_set``.

    Both slots can reference a prefix that no class/slot uses directly, so without
    explicit collection the corresponding ``CurieNamespace`` binding would be
    missing from the generated module.
    """
    schema = tmp_path / "enum_uris.yaml"
    schema.write_text(
        """
id: https://example.org/enum_uris
name: enum_uris
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/ex/
  myenum: https://example.org/myenum/
  cs: https://example.org/codeset/
default_prefix: ex
default_range: string
imports:
  - linkml:types
enums:
  MyEnum:
    enum_uri: myenum:MyEnum
    code_set: cs:someCodeSet
    permissible_values:
      A: {}
"""
    )
    pstr = str(PythonGenerator(str(schema)).serialize())
    assert "MYENUM = CurieNamespace('myenum'," in pstr
    assert "CS = CurieNamespace('cs'," in pstr
    module = compile_python(pstr)
    assert str(module.MYENUM) == "https://example.org/myenum/"
    assert str(module.CS) == "https://example.org/codeset/"


@pytest.fixture
def prefix_generator(tmp_path):
    """A PythonGenerator whose namespaces know several prefixes not yet emitted.

    The returned generator's ``emit_prefixes`` set does *not* yet contain
    ``myt``/``myenum``/``cs``/``mean`` so that calling ``visit_type`` /
    ``visit_enum`` can be observed to add them.
    """
    schema = tmp_path / "u.yaml"
    schema.write_text(
        """
id: https://example.org/u
name: u
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/ex/
  myt: https://example.org/myt/
  myenum: https://example.org/myenum/
  cs: https://example.org/codeset/
  mean: https://example.org/mean/
default_prefix: ex
default_range: string
imports:
  - linkml:types
"""
    )
    gen = PythonGenerator(str(schema))
    # Preconditions: none of the prefixes under test are already collected.
    assert {"myt", "myenum", "cs", "mean"}.isdisjoint(gen.emit_prefixes)
    return gen


def test_visit_type_collects_type_uri_prefix(prefix_generator):
    """visit_type: a non-imported type whose ``uri`` resolves to a prefix (line 140)."""
    prefix_generator.visit_type(TypeDefinition("MyThing", uri="myt:MyThing"))
    assert "myt" in prefix_generator.emit_prefixes


def test_visit_enum_collects_enum_uri_code_set_and_meaning_prefixes(prefix_generator):
    """visit_enum: enum_uri (152), code_set (156) and pv meaning (161) prefixes."""
    enum = EnumDefinition("MyEnum", enum_uri="myenum:MyEnum", code_set="cs:someCodeSet")
    enum.permissible_values["A"] = PermissibleValue(text="A", meaning="mean:A")

    prefix_generator.visit_enum(enum)

    assert "myenum" in prefix_generator.emit_prefixes  # line 152 -> 153
    assert "cs" in prefix_generator.emit_prefixes  # line 156 -> 157
    assert "mean" in prefix_generator.emit_prefixes  # line 161 -> 162


def test_visit_enum_skips_imported_enum(prefix_generator):
    """visit_enum returns early for imported enums (line 149), collecting nothing."""
    before = set(prefix_generator.emit_prefixes)
    prefix_generator.visit_enum(EnumDefinition("Imported", enum_uri="myenum:Imported", imported_from="child"))
    assert prefix_generator.emit_prefixes == before
