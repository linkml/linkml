"""Conventional prefix names for ``--normalize-prefixes``.

A schema may declare its own name for a well-known namespace, such as ``sdo`` for
``https://schema.org/``. With ``--normalize-prefixes`` every generator that prints
prefix names writes the conventional name, ``schema``, and all of them write the
same name for each namespace: :func:`preferred_prefixes` computes one plan per
schema, as a :class:`curies.Converter` whose records hold the preferred name and
the other declared names as synonyms.

How a generator applies the plan depends on what its prefixes are:

- In a self-contained document (Turtle, RDF/XML, ShExC, SPARQL, YARRRML, SSSOM) a
  prefix only abbreviates IRIs in that document; prefixes "are not a formal part
  of the RDF data model" (RDF 1.1 Concepts §1.4). Such a document uses the
  preferred names only.
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

logger = logging.getLogger(__name__)


def well_known_prefix_map() -> dict[str, str]:
    """Return a mapping from namespace URI to its conventional prefix name.

    The names come from two curated sources, which agree wherever both name a
    namespace:

    - the ``linked_data`` context of `prefixmaps <https://github.com/linkml/prefixmaps>`_,
      curated by the LinkML maintainers (``sh`` for SHACL, ``schema`` for
      ``http://schema.org/``);
    - the names rdflib binds by default (``Graph(bind_namespaces="rdflib")``),
      which the RDF generators serialize with, and which therefore take precedence
      (``schema`` for ``https://schema.org/``, ``dc`` for DCMI elements).

    prefixmaps' broader ``merged`` context is not used: it gives a namespace the
    name of the first registry that lists it, such as ``alice`` for
    ``http://example.org/`` from prefix.cc, which is no convention.
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
    """Return the renames ``{prefix: conventional name}`` for the declared *prefixes*.

    *prefixes* maps each declared prefix to its namespace. A prefix is renamed to
    the conventional name of its namespace (:func:`well_known_prefix_map`) when that
    name belongs to the namespace alone: a declared name belongs to the namespaces
    that declare it, because shared outputs keep every declared name, and any other
    name to the namespaces that want it. A name in *taken*, the other names of the
    outputs such as JSON-LD terms, belongs to none. A prefix that is not renamed
    keeps its name, with a warning.

    >>> prefix_renames({"sdo": "https://schema.org/", "ex": "http://example.org/"})
    {'sdo': 'schema'}
    >>> prefix_renames({"sdo": "https://schema.org/", "schema": "http://schema.org/"})
    {}
    >>> prefix_renames({"sdo": "https://schema.org/"}, taken={"schema"})
    {}
    """
    known = well_known_prefix_map()
    wanted = {prefix: known[str(ns)] for prefix, ns in prefixes.items() if known.get(str(ns), prefix) != prefix}
    declared: dict[str, set[str]] = {}
    for prefix, ns in prefixes.items():
        declared.setdefault(prefix, set()).add(str(ns))
    wanting: dict[str, set[str]] = {}
    for prefix, name in wanted.items():
        wanting.setdefault(name, set()).add(str(prefixes[prefix]))
    renames = {}
    for prefix, name in sorted(wanted.items()):
        owners = declared.get(name) or wanting[name]
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
    its synonyms are the namespace's other declared names, which shared outputs keep.
    The plan is computed from the schema, not from one output, so all generators
    agree: a name that the schema or an import declares stays with its namespace,
    and a conventional name that is a term of the schema's JSON-LD context, such as
    the name of a slot, is not given to a prefix in any output.
    """
    declared = _declared_prefixes(sv)
    renames = prefix_renames(declared, taken=_term_names(sv))
    names: dict[str, list[str]] = {}
    for prefix, ns in declared.items():
        names.setdefault(ns, []).append(prefix)
    records = []
    for ns, ns_names in names.items():
        preferred = next((renames[name] for name in ns_names if name in renames), ns_names[0])
        records.append(Record(prefix=preferred, uri_prefix=ns, prefix_synonyms=[n for n in ns_names if n != preferred]))
    return Converter(records)


def _declared_prefixes(sv: SchemaView) -> dict[str, str]:
    """Return every prefix that the schema of *sv* and its imports declare, with its namespace.

    LinkML expands the CURIEs of data with all of them (``SchemaView.namespaces()``
    once the imports are loaded), so each keeps denoting its namespace in every
    output: ``linkml:types`` declares ``schema`` for ``http://schema.org/``, so no
    other namespace gets that name. The schema's own declaration wins over an
    import's, as in SchemaLoader.
    """
    declared = {str(p.prefix_prefix): str(p.prefix_reference) for p in sv.schema.prefixes.values()}
    for schema_name in sv.imports_closure():
        for p in sv.schema_map[schema_name].prefixes.values():
            declared.setdefault(str(p.prefix_prefix), str(p.prefix_reference))
    return declared


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


def document_prefixes(
    declared: Mapping[str, str], plan: Converter, undeclared: Collection[str] = frozenset()
) -> Converter:
    """Return the prefixes of a self-contained document that declares *declared* (name to namespace) under *plan*.

    Each record's prefix is the name the document uses for a namespace it declares,
    the preferred one of *plan* where the plan has one, and its synonyms are the
    declared names it replaces. A declaration of a name that *plan* gives to another
    namespace is dropped. Only declared prefixes are renamed, and not to a name in
    *undeclared*, the prefixes the document writes without declaring them, so such a
    CURIE keeps what it denotes.

    >>> plan = Converter([Record(prefix="schema", uri_prefix="https://schema.org/", prefix_synonyms=["sdo"])])
    >>> doc = document_prefixes({"sdo": "https://schema.org/", "schema": "http://schema.org/"}, plan)
    >>> [(r.prefix, r.uri_prefix, r.prefix_synonyms) for r in doc.records]
    [('schema', 'https://schema.org/', ['sdo'])]
    """
    names: dict[str, list[str]] = {}
    for name, namespace in declared.items():
        planned = plan.prefix_map.get(name)
        if planned is None or planned == str(namespace):
            names.setdefault(str(namespace), []).append(name)
    records = []
    for namespace, ns_names in names.items():
        preferred = plan.reverse_prefix_map.get(namespace, ns_names[0])
        if preferred in undeclared and preferred not in ns_names:
            preferred = ns_names[0]
        records.append(
            Record(prefix=preferred, uri_prefix=namespace, prefix_synonyms=[n for n in ns_names if n != preferred])
        )
    return Converter(records)


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
        "where the schema declares sdo) in every generator alike.",
    )(f)
