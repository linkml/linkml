from rdflib import Graph, URIRef
from rdflib.namespace import DCTERMS, RDFS

from linkml.generators.owlgen import MetadataProfile, OwlSchemaGenerator

# reported in https://github.com/linkml/linkml/issues/692
# description metaproperty is not being exported with owl-gen

schema_str = """
id: http://example.org/description-export
name: descriptionexport
imports:
  - https://w3id.org/linkml/types
default_range: string
default_prefix: ex
prefixes:
  ex: http://example.org/description-export/

classes:
  Person:
    title: A person
    description: A person (alive, dead, undead, or fictional).
    slots:
        - name
        - family name

slots:
  name:
    title: Name
    description: The name of the item.

  family name:
    title: Family name
    description: Family name. In the U.S., the last name of a Person.
"""


def test_owlgen_rdfs_profile():
    # export the source schema containing both title and description
    gen = OwlSchemaGenerator(
        schema_str,
        ontology_uri_suffix=None,
        type_objects=False,
        metaclasses=False,
        add_ols_annotations=True,
        metadata_profile=MetadataProfile.rdfs,
        format="ttl",
    )
    output = gen.serialize()
    print(output)

    # load back via rdflib
    graph = Graph(base="http://example.org/description-export")
    graph.parse(data=output, format="ttl")

    # check if graph contains dcterms:title for class 'Person'
    person_class = URIRef(f"{graph.base}/Person")
    assert (person_class, DCTERMS.title, None) in graph

    # check if graph contains dcterms:title for property 'name'
    name_prop = URIRef(f"{graph.base}/name")
    assert (name_prop, DCTERMS.title, None) in graph

    # now check rdfs:comment for class 'Person'
    assert (person_class, RDFS.comment, None) in graph

    # and check rdfs:comment for property 'name' too
    assert (name_prop, RDFS.comment, None) in graph


def test_owlgen_xsd_prefixes_from_imported_schema_are_expanded():
    """Prefixes declared only in imported sub-schemas (e.g. xsd: from
    https://w3id.org/linkml/types) must be resolved to full URIs by SchemaView.

    This detects a premature-namespace-cache bug: SchemaView.namespaces() is
    @lru_cache'd. When it is called before imports_closure() has fully populated
    schema_map, prefixes declared only in imported schemas (e.g. xsd: from
    https://w3id.org/linkml/types) are absent from the cache.  Subsequent calls
    to get_uri(expand=True) on built-in types then silently return unexpanded
    CURIEs like 'xsd:string' instead of the full
    http://www.w3.org/2001/XMLSchema#string URI.

    The fix is to call imports_closure() followed by namespaces.cache_clear()
    at the start of as_graph() so the namespace cache is always seeded with the
    complete schema_map before any URI expansion takes place.
    """
    gen = OwlSchemaGenerator(
        schema_str,
        ontology_uri_suffix=None,
        type_objects=False,
        metaclasses=False,
        format="ttl",
        skip_vacuous_min_zero_cardinality_axioms=True,
        skip_vacuous_local_range_axioms=True,
        consolidate_cardinality_axioms=True,
    )
    # Trigger the full generation pipeline so as_graph() applies the fix
    gen.serialize()

    sv = gen.schemaview
    string_type = sv.get_type("string")
    expanded = sv.get_uri(string_type, expand=True)
    assert "://" in expanded, (
        f"get_uri(expand=True) for built-in type 'string' returned {expanded!r} — "
        "an unexpanded CURIE rather than a full URI. "
        "The xsd: prefix from the imported schema was not in the namespace cache."
    )
