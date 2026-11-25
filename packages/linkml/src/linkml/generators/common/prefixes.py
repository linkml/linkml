"""Conventional prefix names for ``--normalize-prefixes``.

A schema may declare its own name for a well-known namespace, such as ``sdo`` for
``https://schema.org/``. With ``--normalize-prefixes`` every generator that prints
prefix names writes the conventional name, ``schema``, and all of them write the
same name for each namespace: :func:`preferred_prefixes` computes one plan per
schema, as a :class:`curies.Converter` whose records hold the preferred name and
the other declared names as synonyms.

In each output format a prefix declaration reaches no further than the document
that carries it: a Turtle or SPARQL directive "associates a prefix label with an
IRI" in that document (Turtle 1.1 §2.4, SPARQL 1.1 §4.1.1.1), a JSON-LD context
defines terms for the data that names the context (JSON-LD 1.1 §3.1), and a CURIE
is read with the "prefix binding ... in scope" where it is written (CURIE Syntax
1.0 §3). A declaration in an imported schema binds nothing in a generated
document that does not repeat it. So what a conventional name can collide with
is another namespace that the schema's own documents write under that name
(:func:`written_prefixes`), not a prefix that an import declares and nothing
uses: ``linkml:types`` declares ``schema`` for ``http://schema.org/``
and uses it only in the mappings of its types, which none of the generators
offering the option writes, so a schema's ``sdo`` for ``https://schema.org/``
becomes ``schema``. LinkML itself keeps reading ``schema`` in data as the
import declares it, which the plan reports as a warning.

How a generator applies the plan depends on what its prefixes are:

- In a self-contained document (Turtle, RDF/XML, ShExC, SPARQL, YARRRML, SSSOM) a
  prefix only abbreviates IRIs in that document; prefixes "are not a formal part
  of the RDF data model" (RDF 1.1 Concepts §1.4). Such a document uses the
  preferred names only, except that a prefix its own CURIEs are written with
  keeps what it denotes (:func:`document_prefixes`).
- A JSON-LD context is shared with the data written against it, and a compact
  IRI whose prefix the context no longer defines is read as an IRI of its own
  (JSON-LD 1.1 §4.1.5). The context keeps every declared name and adds the
  preferred one.

>>> from linkml_runtime.utils.schemaview import SchemaView
>>> sv = SchemaView('''
... id: http://example.org/s
... name: s
... prefixes: {ex: http://example.org/, sdo: https://schema.org/}
... default_prefix: ex
... classes:
...   Person: {class_uri: sdo:Person}
... ''')
>>> converter = preferred_prefixes(sv)
>>> converter.standardize_curie("sdo:Person")
'schema:Person'
>>> converter.expand("sdo:Person") == converter.expand("schema:Person") == "https://schema.org/Person"
True
"""

import logging
from collections.abc import Callable, Collection, Mapping
from functools import lru_cache
from typing import TYPE_CHECKING, Any

import click
from curies import Converter, Record

from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

if TYPE_CHECKING:
    from rdflib import Graph

    from linkml_runtime.linkml_model.meta import ClassDefinition, EnumDefinition, PermissibleValue, SlotDefinition

logger = logging.getLogger(__name__)


def well_known_prefix_map() -> dict[str, str]:
    """Return a mapping from namespace URI to its conventional prefix name.

    The names come from two curated sources, which name no namespace differently:

    - the ``linked_data`` context of `prefixmaps <https://github.com/linkml/prefixmaps>`_,
      curated by the LinkML maintainers (``sh`` for SHACL, ``schema`` for
      ``http://schema.org/``);
    - the names rdflib binds by default (``Graph(bind_namespaces="rdflib")``),
      which the RDF generators serialize with (``schema`` for
      ``https://schema.org/``, ``dc`` for DCMI elements).

    prefixmaps' broader ``merged`` context is not used: it gives a namespace the
    name of the first registry in its merge order that lists it, which for W3C
    vocabularies is often the upper-cased Bioregistry name, such as ``ADMS`` for
    ``http://www.w3.org/ns/adms#`` or ``TIME`` for ``http://www.w3.org/2006/time#``.
    """
    return dict(_cached_well_known_prefix_map())


@lru_cache(maxsize=1)
def _cached_well_known_prefix_map() -> dict[str, str]:
    """Internal cached builder for well_known_prefix_map()."""
    from prefixmaps import load_context
    from rdflib import Graph

    ns_to_prefix = {rec.namespace: rec.prefix for rec in load_context("linked_data").prefix_expansions}
    for prefix, namespace in Graph(bind_namespaces="rdflib").namespaces():
        if str(prefix):
            ns_to_prefix[str(namespace)] = str(prefix)
    return ns_to_prefix


def prefix_renames(prefixes: Mapping[str, str], taken: Collection[str] = frozenset()) -> dict[str, str]:
    """Return the renames ``{prefix: conventional name}`` for the *prefixes* that documents write.

    *prefixes* maps each prefix that the documents write to its namespace
    (:func:`written_prefixes`). A prefix is renamed to the conventional name of its
    namespace (:func:`well_known_prefix_map`) when that name belongs to the
    namespace alone: a name among *prefixes* belongs to the namespaces written
    under it, because shared outputs keep every such name, and any other name to
    the namespaces that want it. A name in *taken*, the other names of the outputs
    such as JSON-LD terms, belongs to none. A prefix that is not renamed keeps its
    name, with a warning.

    >>> prefix_renames({"sdo": "https://schema.org/", "ex": "http://example.org/"})
    {'sdo': 'schema'}
    >>> prefix_renames({"sdo": "https://schema.org/", "schema": "http://schema.org/"})
    {}
    >>> prefix_renames({"sdo": "https://schema.org/"}, taken={"schema"})
    {}
    """
    known = well_known_prefix_map()
    wanted = {prefix: known[str(ns)] for prefix, ns in prefixes.items() if known.get(str(ns), prefix) != prefix}
    held: dict[str, set[str]] = {}
    for prefix, ns in prefixes.items():
        held.setdefault(prefix, set()).add(str(ns))
    wanting: dict[str, set[str]] = {}
    for prefix, name in wanted.items():
        wanting.setdefault(name, set()).add(str(prefixes[prefix]))
    renames = {}
    for prefix, name in sorted(wanted.items()):
        owners = held.get(name) or wanting[name]
        if name in taken or owners != {str(prefixes[prefix])}:
            logger.warning(
                "Prefix %r is not renamed to %r: that name also denotes another namespace or term", prefix, name
            )
        else:
            renames[prefix] = name
    return renames


def preferred_prefixes(sv: SchemaView) -> Converter:
    """Return the prefix names that ``--normalize-prefixes`` writes for the schema of *sv*.

    Each record's prefix is the name every generator writes for its namespace, and
    its synonyms are the namespace's other names, which shared outputs keep. The
    plan is computed from the schema, not from one output, so all generators
    agree: a name that the schema's documents write (:func:`written_prefixes`)
    stays with its namespace, and a conventional name that is a term of the
    schema's JSON-LD context, such as the name of a slot, is not given to a prefix
    in any output.

    A conventional name that only an import declares, for a namespace nothing
    uses, is given away with a warning: LinkML's loaders and dumpers expand the
    CURIEs of data with the prefixes of the schema and its imports, so they keep
    reading that name as the import declares it. A name that nothing declares
    and a CURIE, ``id_prefixes`` or ``emit_prefixes`` uses all the same is read
    with a default CURIE map or as an unknown namespace, and is given to no
    namespace.
    """
    imported = _imported_prefixes(sv)
    used_names, iris = _written_references(sv)
    written = _written_prefixes(sv, imported, used_names, iris)
    renames = prefix_renames(written, taken=_term_names(sv) | (used_names - written.keys()))
    for prefix, name in renames.items():
        others = [ns for ns in imported.get(name, ()) if ns != written[prefix]]
        if others and name not in written:
            logger.warning(
                "Prefix %r is written for <%s>. An import declares it for <%s>, which nothing uses; LinkML "
                "still reads it so in data",
                name,
                written[prefix],
                ">, <".join(others),
            )
    names: dict[str, list[str]] = {}
    for prefix, ns in written.items():
        names.setdefault(ns, []).append(prefix)
    records = []
    for ns, ns_names in names.items():
        preferred = next((renames[name] for name in ns_names if name in renames), ns_names[0])
        records.append(Record(prefix=preferred, uri_prefix=ns, prefix_synonyms=[n for n in ns_names if n != preferred]))
    return Converter(records)


def written_prefixes(sv: SchemaView) -> dict[str, str]:
    """Return the prefixes that the documents generated for the schema of *sv* write, with their namespaces.

    A prefix is scoped to the document that declares it, so these are the names a
    conventional name can collide with:

    - every prefix the schema declares itself, which its JSON-LD context defines
      for the data written against it, and
    - a prefix that only an import declares, when it is in use: an element of the
      schema or its imports is identified by an IRI of its namespace or mapped to
      one, or is written with the prefix in a CURIE, or names it among its
      ``id_prefixes``, or a schema lists it in ``emit_prefixes``. The context of
      the importing schema defines such a prefix too, and data may combine it with
      the context of the import.

    A prefix that only an import declares and nothing uses is needed by no
    document generated for the schema, so its name is free: ``linkml:types``
    declares ``schema`` for ``http://schema.org/`` and uses it only in the mappings
    of its types, which none of the generators offering the option writes.

    >>> sv = SchemaView('''
    ... id: http://example.org/s
    ... name: s
    ... prefixes: {ex: http://example.org/, linkml: https://w3id.org/linkml/, sdo: https://schema.org/}
    ... default_prefix: ex
    ... imports: [linkml:types]
    ... classes:
    ...   Person: {class_uri: sdo:Person}
    ... ''')
    >>> "schema" in written_prefixes(sv), "xsd" in written_prefixes(sv)
    (False, True)
    >>> preferred_prefixes(sv).standardize_curie("sdo:Person")
    'schema:Person'
    """
    return _written_prefixes(sv, _imported_prefixes(sv), *_written_references(sv))


def _written_prefixes(
    sv: SchemaView, imported: Mapping[str, list[str]], names: Collection[str], iris: Collection[str]
) -> dict[str, str]:
    """Implement :func:`written_prefixes` for the prefixes *imported* that the imports declare and
    the *names* and *iris* that the elements are written with (:func:`_written_references`)."""
    written = {str(p.prefix_prefix): str(p.prefix_reference) for p in sv.schema.prefixes.values()}
    for name, namespaces in imported.items():
        if name not in written:
            in_use = [ns for ns in namespaces if any(iri.startswith(ns) for iri in iris)]
            if in_use or name in names:
                written[name] = (in_use or namespaces)[0]
    return written


def _imported_prefixes(sv: SchemaView) -> dict[str, list[str]]:
    """Return the prefixes that the imports of *sv*'s schema declare, each with its namespaces.

    Imports may declare one name for several namespaces; all are kept, in the order of the
    imports closure, so that the name is held if any of them is in use.
    """
    imported: dict[str, list[str]] = {}
    for schema_name in sv.imports_closure():
        if schema_name != sv.schema.name:
            for p in sv.schema_map[schema_name].prefixes.values():
                namespaces = imported.setdefault(str(p.prefix_prefix), [])
                if str(p.prefix_reference) not in namespaces:
                    namespaces.append(str(p.prefix_reference))
    return imported


_MAPPING_SLOTS = (
    "mappings",
    "exact_mappings",
    "close_mappings",
    "related_mappings",
    "narrow_mappings",
    "broad_mappings",
)


def _written_references(sv: SchemaView) -> tuple[set[str], set[str]]:
    """Return what the elements of *sv*'s schema and its imports are written with: the prefix names
    of the CURIEs and the IRIs.

    These are the references that identify an element: the IRI of a class, slot, type, enum or
    subset, as declared (``class_uri``, ``slot_uri``, ``uri``, ``enum_uri``) and as derived from its
    name, and the ``meaning`` of a permissible value; and the mappings of a class, slot, enum or
    permissible value. None of the generators offering the option writes the mappings of a type.
    A CURIE counts by the prefix it is written with, so it needs no expansion; the names in
    ``id_prefixes`` and ``emit_prefixes`` count too.
    """
    references: list[str] = []
    names: set[str] = set()
    for schema in sv.schema_map.values():
        names.update(str(prefix) for prefix in schema.emit_prefixes)

    def add_mappings(definition: "ClassDefinition | SlotDefinition | EnumDefinition | PermissibleValue") -> None:
        for slot in _MAPPING_SLOTS:
            references.extend(str(mapping) for mapping in getattr(definition, slot))
        names.update(str(prefix) for prefix in getattr(definition, "id_prefixes", ()))

    for element in sv.all_elements().values():
        references.extend(sv.get_uri(element, expand=True, native=native) for native in (False, True))
    for type_ in sv.all_types().values():
        references.append(str(type_.uri or ""))
    nested_slots: list[SlotDefinition] = []
    for cls in sv.all_classes().values():
        references.append(str(cls.class_uri or ""))
        add_mappings(cls)
        nested_slots += [*cls.attributes.values(), *cls.slot_usage.values()]
    for slot in [*sv.all_slots(attributes=False).values(), *nested_slots]:
        references.append(str(slot.slot_uri or ""))
        add_mappings(slot)
    for enum in sv.all_enums().values():
        references.append(str(enum.enum_uri or ""))
        add_mappings(enum)
        for value in enum.permissible_values.values():
            references.append(str(value.meaning or ""))
            add_mappings(value)
    names |= curie_prefixes(references)
    return names, {reference for reference in references if curie_prefixes(reference) == set()}


def _term_names(sv: SchemaView) -> set[str]:
    """Return the names a JSON-LD context of *sv*'s schema uses as terms or bare values.

    These are the class and slot names as the context generator writes them and
    the texts of permissible values, which a ``@type: @vocab`` slot reads as terms
    first (JSON-LD 1.1 API, IRI Expansion, step 5).
    """
    names = {camelcase(name) for name in sv.all_classes()}
    names |= {underscore(slot.alias or slot.name) for slot in sv.all_slots().values()}
    names |= {text for enum in sv.all_enums().values() for text in enum.permissible_values}
    return names


def document_prefixes(declared: Mapping[str, str], plan: Converter, used: Collection[str] = frozenset()) -> Converter:
    """Return the prefixes of a self-contained document that declares *declared* (name to namespace) under *plan*.

    Each record's prefix is the name the document uses for a namespace it declares,
    the preferred one of *plan* where the plan has one, and its synonyms are the
    declared names it replaces. *used* are the prefixes of the CURIEs the document
    writes. A declaration of a name that *plan* gives to another namespace is
    dropped unless the document uses it; a name the document uses, declared or not,
    is given to no other namespace. A CURIE rewritten with the returned converter
    (:func:`standardize_prefix`) then denotes what it did; one that the document
    writes as it stands needs the declaration of its own prefix kept beside.

    >>> plan = Converter([Record(prefix="schema", uri_prefix="https://schema.org/", prefix_synonyms=["sdo"])])
    >>> declared = {"sdo": "https://schema.org/", "schema": "http://schema.org/"}
    >>> [(r.prefix, r.uri_prefix, r.prefix_synonyms) for r in document_prefixes(declared, plan).records]
    [('schema', 'https://schema.org/', ['sdo'])]
    >>> sorted((r.prefix, r.uri_prefix) for r in document_prefixes(declared, plan, used={"sdo", "schema"}).records)
    [('schema', 'http://schema.org/'), ('sdo', 'https://schema.org/')]
    """
    names: dict[str, list[str]] = {}
    for name, namespace in declared.items():
        planned = plan.prefix_map.get(name)
        if planned is None or planned == str(namespace) or name in used:
            names.setdefault(str(namespace), []).append(name)
    records = []
    for namespace, ns_names in names.items():
        preferred = plan.reverse_prefix_map.get(namespace, ns_names[0])
        if preferred in used and preferred not in ns_names:
            preferred = ns_names[0]
        records.append(
            Record(prefix=preferred, uri_prefix=namespace, prefix_synonyms=[n for n in ns_names if n != preferred])
        )
    return Converter(records)


def prefix_declarations(document: Converter, declared: Mapping[str, str]) -> dict[str, str]:
    """Return the declarations of *document* (:func:`document_prefixes`), name to namespace, in the
    order in which *declared* names the namespaces.

    A converter keeps its records sorted by name; a document that has nothing to rename is
    written as it is without the option, its declarations in the order the generator gives them.

    >>> plan = Converter([Record(prefix="schema", uri_prefix="https://schema.org/", prefix_synonyms=["sdo"])])
    >>> declared = {"zed": "http://example.org/z/", "sdo": "https://schema.org/", "abc": "http://example.org/a/"}
    >>> prefix_declarations(document_prefixes(declared, plan), declared)
    {'zed': 'http://example.org/z/', 'schema': 'https://schema.org/', 'abc': 'http://example.org/a/'}
    """
    order = {str(namespace): position for position, namespace in enumerate(dict.fromkeys(declared.values()))}
    records = sorted(document.records, key=lambda record: order[record.uri_prefix])
    return {record.prefix: record.uri_prefix for record in records}


def added_preferred_prefixes(
    plan: Converter, defined: Mapping[str, str], terms: Collection[str] = frozenset()
) -> Converter:
    """Return the preferred names that an output keeping its *defined* prefixes adds.

    A JSON-LD context is shared with the data written against it, so it keeps every
    prefix it defines (name to namespace) and adds the preferred name of the
    namespace from *plan* (:func:`preferred_prefixes`); data using either name
    expands alike. Each record's synonyms are the defined names it stands for.
    A preferred name in *terms*, or defined for another namespace, is not added.

    >>> plan = Converter([Record(prefix="schema", uri_prefix="https://schema.org/", prefix_synonyms=["sdo"])])
    >>> [(r.prefix, r.prefix_synonyms) for r in added_preferred_prefixes(plan, {"sdo": "https://schema.org/"}).records]
    [('schema', ['sdo'])]
    """
    synonyms: dict[str, list[str]] = {}
    for prefix in sorted(defined):
        name = plan.standardize_prefix(prefix)
        if name in (None, prefix) or name in terms or defined.get(name, defined[prefix]) != defined[prefix]:
            continue
        synonyms.setdefault(name, []).append(prefix)
    return Converter(
        [Record(prefix=name, uri_prefix=defined[names[0]], prefix_synonyms=names) for name, names in synonyms.items()]
    )


def standardize_prefix(text: str, converter: Converter) -> str:
    """Return *text* with the prefix of a compact IRI replaced by its preferred name.

    Only the part before the first colon changes, so templates such as
    ``ex:Person/$(id)`` keep their rest. A suffix starting with ``//`` makes *text*
    an absolute IRI (JSON-LD 1.1 §4.1.5), which is left alone.

    >>> converter = Converter([Record(prefix="schema", uri_prefix="https://schema.org/", prefix_synonyms=["sdo"])])
    >>> standardize_prefix("sdo:Person", converter), standardize_prefix("https://schema.org/x", converter)
    ('schema:Person', 'https://schema.org/x')
    """
    prefix, colon, rest = text.partition(":")
    if colon and not rest.startswith("//"):
        preferred = converter.standardize_prefix(prefix)
        if preferred is not None:
            return preferred + colon + rest
    return text


def curie_prefixes(node: Any) -> set[str]:
    """Return the prefixes of the compact IRIs among the string values of the JSON structure *node*.

    >>> sorted(curie_prefixes({"s": "ex:a/$(id)", "o": ["sdo:Person", "https://schema.org/x", "text"]}))
    ['ex', 'sdo']
    """
    if isinstance(node, dict):
        return set().union(*(curie_prefixes(value) for value in node.values()))
    if isinstance(node, list):
        return set().union(*(curie_prefixes(value) for value in node))
    if isinstance(node, str):
        prefix, colon, rest = node.partition(":")
        if colon and not rest.startswith("//"):
            return {prefix}
    return set()


def standardize_values(node: Any, converter: Converter) -> Any:
    """Return the JSON structure *node* with :func:`standardize_prefix` applied to its string values.

    Keys are left alone: in a JSON-LD context they are the terms data refers to.
    Dicts and lists keep their type, such as a list that a YAML dumper writes in
    flow style.
    """
    if isinstance(node, dict):
        return type(node)((key, standardize_values(value, converter)) for key, value in node.items())
    if isinstance(node, list):
        return type(node)(standardize_values(value, converter) for value in node)
    if isinstance(node, str):
        return standardize_prefix(node, converter)
    return node


def bind_preferred_prefixes(graph: "Graph", converter: Converter) -> None:
    """Bind the preferred name of each namespace of *converter* in *graph*.

    A name that rdflib or the metamodel bound for another namespace is taken over;
    prefixes only abbreviate IRIs in the serialization (Turtle 1.1 §2.4), so no IRI
    changes.
    """
    from rdflib import Namespace

    for record in converter.records:
        graph.bind(record.prefix, Namespace(record.uri_prefix), override=True, replace=True)


def normalize_prefixes_option(f: Callable) -> Callable:
    """Add ``--normalize-prefixes`` to the command line of a generator that honours it."""
    return click.option(
        "--normalize-prefixes/--no-normalize-prefixes",
        default=False,
        show_default=True,
        help="Write the conventional names of well-known namespaces (e.g. schema for https://schema.org/ "
        "where the schema declares sdo), the same in every generator that offers the option.",
    )(f)
