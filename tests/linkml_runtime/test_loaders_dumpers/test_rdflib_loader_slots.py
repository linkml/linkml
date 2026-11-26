"""Regression tests for per-class predicate resolution in RDFLibLoader.

Covers:
- #4285: two slots sharing the same ``slot_uri`` on different classes.
- #4286: a class attribute sharing its name with a global slot that has a different ``slot_uri``.
"""

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.loaders import rdflib_loader
from linkml_runtime.utils.schemaview import SchemaView

SHARED_SLOT_URI_SCHEMA = """
id: https://example.org/s
name: s
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
default_prefix: ex
default_range: string
imports:
  - linkml:types
slots:
  id:
    identifier: true
    range: uriorcurie
  title:
    slot_uri: ex:title
  title_literal:
    slot_uri: ex:title
classes:
  Catalog:
    tree_root: true
    slots:
      - id
      - title
  Dataset:
    slots:
      - id
      - title_literal
"""

SHADOWED_ATTRIBUTE_SCHEMA = """
id: https://example.org/s
name: s
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
default_prefix: ex
default_range: string
imports:
  - linkml:types
slots:
  id:
    identifier: true
    range: uriorcurie
  items:
    slot_uri: ex:globalItems
    range: Item
    multivalued: true
classes:
  Item:
    slots:
      - id
  Container:
    tree_root: true
    attributes:
      items:
        range: Item
        multivalued: true
        inlined_as_list: true
"""


def test_shared_slot_uri_across_classes() -> None:
    """RDFLibLoader resolves a shared slot_uri against the subject class's own slots (#4285)."""
    sv = SchemaView(SHARED_SLOT_URI_SCHEMA)
    mod = PythonGenerator(SHARED_SLOT_URI_SCHEMA).compile_module()

    catalog = mod.Catalog(id="ex:c1", title="My catalog")
    catalog_graph = rdflib_dumper.as_rdf_graph(catalog, schemaview=sv)
    loaded_catalog = rdflib_loader.from_rdf_graph(catalog_graph, target_class=mod.Catalog, schemaview=sv)
    assert loaded_catalog == [catalog]

    dataset = mod.Dataset(id="ex:d1", title_literal="My dataset")
    dataset_graph = rdflib_dumper.as_rdf_graph(dataset, schemaview=sv)
    loaded_dataset = rdflib_loader.from_rdf_graph(dataset_graph, target_class=mod.Dataset, schemaview=sv)
    assert loaded_dataset == [dataset]


def test_attribute_shadowing_global_slot_name() -> None:
    """RDFLibLoader resolves an attribute's own URI when a global slot shares its name (#4286)."""
    sv = SchemaView(SHADOWED_ATTRIBUTE_SCHEMA)
    mod = PythonGenerator(SHADOWED_ATTRIBUTE_SCHEMA).compile_module()

    container = mod.Container(items=[mod.Item(id="ex:i1")])
    graph = rdflib_dumper.as_rdf_graph(container, schemaview=sv)
    loaded = rdflib_loader.from_rdf_graph(graph, target_class=mod.Container, schemaview=sv)
    assert loaded == [container]
