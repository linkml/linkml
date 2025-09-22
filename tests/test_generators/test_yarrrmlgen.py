from pathlib import Path

from linkml.generators.yarrrmlgen import YarrrmlGenerator


# 1) basic: identifier -> subject uses id slot; rdf:type is CURIE
def test_basic_identifier_subject(tmp_path: Path):
    schema = tmp_path / "schema.yaml"
    schema.write_text("""
id: https://example.org/mini
name: mini
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/mini#
imports: [linkml:types]
default_prefix: ex
default_range: string
slots:
  id: {identifier: true, range: string}
  name: {range: string}
classes:
  Person:
    attributes:
      id: {identifier: true}
      name: {}
""")
    out = YarrrmlGenerator(str(schema)).serialize()
    assert "prefixes:" in out
    assert "mappings:" in out
    assert "Person:" in out
    assert "s: ex:$(id)" in out
    assert "p: rdf:type" in out and "o: ex:Person" in out
    assert "p: ex:name" in out and "o: $(name)" in out


# 2) key slot fallback when no identifier
def test_key_slot_subject(tmp_path: Path):
    schema = tmp_path / "schema.yaml"
    schema.write_text("""
id: https://example.org/mini2
name: mini2
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/mini2#
imports: [linkml:types]
default_prefix: ex
default_range: string
slots:
  code: {range: string}
classes:
  Thing:
    tree_root: true
    slots: [code]
    slot_usage:
      code: {key: true}
""")
    out = YarrrmlGenerator(str(schema)).serialize()
    assert "Thing:" in out
    assert "s: ex:$(code)" in out


# 3) no id, no key -> subject_id fallback
def test_no_id_no_key_fallback(tmp_path: Path):
    schema = tmp_path / "schema.yaml"
    schema.write_text("""
id: https://example.org/mini3
name: mini3
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/mini3#
imports: [linkml:types]
default_prefix: ex
default_range: string
classes:
  Orphan:
    description: "no id/key"
""")
    out = YarrrmlGenerator(str(schema)).serialize()
    assert "Orphan:" in out
    assert "s: ex:Orphan/$(subject_id)" in out


# 4) alias on slot -> object template uses alias
def test_slot_alias_template(tmp_path: Path):
    schema = tmp_path / "schema.yaml"
    schema.write_text("""
id: https://example.org/mini4
name: mini4
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/mini4#
imports: [linkml:types]
default_prefix: ex
default_range: string
slots:
  ident: {identifier: true, range: string}
  full_name:
    range: string
    alias: fn
classes:
  Person:
    attributes:
      ident: {identifier: true}
      full_name: {}
""")
    out = YarrrmlGenerator(str(schema)).serialize()
    # predicate is ex:full_name, object is $(fn) because of alias
    assert "p: ex:full_name" in out
    assert "o: $(fn)" in out


# 5) multi-class: two mappings + prefixes kept; rdf prefix auto-added
def test_multiple_classes_and_prefixes(tmp_path: Path):
    schema = tmp_path / "schema.yaml"
    schema.write_text("""
id: https://example.org/mini5
name: mini5
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/mini5#
imports: [linkml:types]
default_prefix: ex
default_range: string
slots:
  id: {identifier: true}
  label: {}
classes:
  A:
    attributes:
      id: {identifier: true}
      label: {}
  B:
    attributes:
      id: {identifier: true}
""")
    out = YarrrmlGenerator(str(schema)).serialize()
    # two mappings present
    assert "A:" in out and "B:" in out
    # given prefix + auto rdf
    assert "ex: https://example.org/mini5#" in out
    assert "rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#" in out


# 6) json mode: jsonpath source + iterator per mapping
def test_json_defaults_iterator(tmp_path: Path):
    schema = tmp_path / "schema.yaml"
    schema.write_text("""
id: https://example.org/mini6
name: mini6
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/mini6#
imports: [linkml:types]
default_prefix: ex
default_range: string
slots:
  id: {identifier: true}
classes:
  Item:
    attributes:
      id: {identifier: true}
""")
    out = YarrrmlGenerator(str(schema)).serialize()
    # default source is jsonpath now
    assert "sources:" in out and "data.json~jsonpath" in out
    # iterator present
    assert "iterator: $.items[*]" in out
    # mapping exists
    assert "Item:" in out
