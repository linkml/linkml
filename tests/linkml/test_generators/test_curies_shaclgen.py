"""Regression test for curies (shaclgen)."""

from rdflib.namespace import SH

from linkml.generators.shaclgen import ShaclGenerator


def test_imported_subschema_prefix_is_bound_in_shacl(tmp_path):
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
    g = ShaclGenerator(str(parent)).as_graph()
    bound = dict(g.namespaces())
    assert "iso3166" in bound
    assert str(bound["iso3166"]) == "https://www.iso.org/iso-3166-country-codes.html#"


def test_builtin_datatype_expands_with_curie_import_before_types(tmp_path):
    """Repro from https://github.com/linkml/linkml/issues/3933.

    The import order below resolves the CURIE import ``childns:child`` before
    ``linkml:types`` has loaded. ``xsd:string`` must still be expanded in
    ``sh:datatype``, which relies on SchemaView not caching its namespaces while
    imports load.
    """
    child_dir = tmp_path / "child"
    child_dir.mkdir()
    (child_dir / "child.yaml").write_text(
        """
id: https://example.org/child
name: child
prefixes:
  linkml: https://w3id.org/linkml/
  child: https://example.org/child/
default_range: string
default_prefix: child
imports:
  - linkml:types
classes:
  Thing:
    class_uri: child:Thing
    attributes:
      label:
        range: string
"""
    )
    child_ns = child_dir.as_uri() + "/"
    (tmp_path / "local_helper.yaml").write_text(
        f"""
id: https://example.org/local-helper
name: local-helper
prefixes:
  linkml: https://w3id.org/linkml/
  helper: https://example.org/helper/
  childns: {child_ns}
default_range: string
default_prefix: helper
imports:
  - linkml:types
  - childns:child
classes:
  HelperThing:
    class_uri: helper:HelperThing
    attributes:
      note:
        range: string
"""
    )
    root = tmp_path / "root.yaml"
    root.write_text(
        f"""
id: https://example.org/root
name: root
prefixes:
  linkml: https://w3id.org/linkml/
  root: https://example.org/root/
  childns: {child_ns}
default_range: string
default_prefix: root
imports:
  - linkml:types
  - childns:child
  - ./local_helper
classes:
  RootThing:
    is_a: Thing
"""
    )
    g = ShaclGenerator(str(root)).as_graph()
    datatypes = {str(o) for o in g.objects(predicate=SH.datatype)}
    assert "http://www.w3.org/2001/XMLSchema#string" in datatypes
    assert "xsd:string" not in datatypes
