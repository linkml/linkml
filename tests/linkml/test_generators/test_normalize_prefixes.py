"""Tests for ``--normalize-prefixes`` in every generator that writes prefix names.

The option writes the conventional name of a well-known namespace, such as ``schema`` for
``https://schema.org/`` where a schema declares ``sdo``, and every generator writes the same
name (:mod:`linkml.generators.common.prefixes`). Only names change:

- a self-contained document (OWL, SHACL, ShEx, SPARQL, YARRRML, SSSOM) means the same with and
  without the option, since prefixes are "not a formal part of the RDF data model"
  (RDF 1.1 Concepts §1.4; Turtle 1.1 §2.4);
- a JSON-LD context or a prefix map keeps every declared name and adds the conventional one, so
  data written against it expands the same (JSON-LD 1.1 §4.1.5).

A prefix is scoped to the document that declares it, so a conventional name is unavailable only where
the schema's documents write it for another namespace; a prefix that only an import declares and
nothing uses holds no name.
"""

import json
import logging
import re
import textwrap
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
import yaml
from click.testing import CliRunner
from curies import Converter, Record
from jsonasobj import as_json
from prefixmaps import load_context
from pyparsing import ParseResults
from pyshexc.parser_impl.generate_shexj import parse as parse_shexc
from rdflib import Graph
from rdflib.compare import isomorphic
from rdflib.plugins.shared.jsonld.context import Context
from rdflib.plugins.sparql.parser import parseQuery
from rdflib.plugins.sparql.parserutils import CompValue

from linkml.cli.main import linkml as linkml_cli
from linkml.generators.common.prefixes import (
    added_preferred_prefixes,
    document_prefixes,
    preferred_prefixes,
    prefix_declarations,
    prefix_renames,
    standardize_prefix,
    well_known_prefix_map,
    written_prefixes,
)
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.prefixmapgen import PrefixGenerator
from linkml.generators.shaclgen import ShaclGenerator
from linkml.generators.shexgen import ShExGenerator
from linkml.generators.sparqlgen import SparqlGenerator
from linkml.generators.sssomgen import SSSOMGenerator
from linkml.generators.yarrrmlgen import YarrrmlGenerator
from linkml_runtime.utils.schemaview import SchemaView

SCHEMA_ORG = "https://schema.org/"
SCHEMA_ORG_HTTP = "http://schema.org/"
DC_ELEMENTS = "http://purl.org/dc/elements/1.1/"
DC_TERMS = "http://purl.org/dc/terms/"
FOAF = "http://xmlns.com/foaf/0.1/"
TIME = "http://www.w3.org/2006/time#"
BIBO = "http://purl.org/ontology/bibo/"
PROV = "http://www.w3.org/ns/prov#"
SKOS = "http://www.w3.org/2004/02/skos/core#"
NOT_PROV = "http://example.org/not-prov/"


def _schema(name: str, prefixes: str, body: str, default_prefix: str = "ex", imports: str = "linkml:types") -> str:
    """A schema with the ``ex`` and ``linkml`` prefixes, the given extra prefix lines, imports and elements."""
    return (
        f"id: https://example.org/{name}\nname: {name}\ndefault_prefix: {default_prefix}\nprefixes:\n"
        "  ex: https://example.org/\n  linkml: https://w3id.org/linkml/\n"
        + textwrap.indent(textwrap.dedent(prefixes), "  ")
        + "imports:\n"
        + "".join(f"  - {i}\n" for i in imports.split())
        + textwrap.dedent(body)
    )


# Each case: the schema files (the main one is schema.yaml) and the name every generator writes for each namespace.
CASES: dict[str, tuple[dict[str, str], dict[str, str]]] = {
    "prov_alias": (
        {
            "schema.yaml": _schema(
                "prov",
                "w3prov: http://www.w3.org/ns/prov#\n",
                """\
                classes:
                  Agent:
                    class_uri: w3prov:Agent
                    exact_mappings: [w3prov:Person]
                    attributes:
                      id: {identifier: true, range: uriorcurie}
                      label: {slot_uri: w3prov:value}
                      delegate: {range: Agent, multivalued: true, slot_uri: w3prov:actedOnBehalfOf}
                """,
            )
        },
        {PROV: "prov"},
    ),
    # linkml:types declares ``schema`` for http://schema.org/ and writes it in no document, and the
    # generators do not agree on a schema that declares ``schema`` for https://schema.org/ itself (three
    # refuse it, two read the import's namespace), so the schema declares ``sdo``, which becomes ``schema``
    "schema_org_alias": (
        {
            "schema.yaml": _schema(
                "sdo",
                "sdo: https://schema.org/\n",
                """\
                classes:
                  Person:
                    class_uri: sdo:Person
                    attributes:
                      id: {identifier: true, range: uriorcurie}
                      knows: {range: Person, multivalued: true, slot_uri: sdo:knows}
                """,
            )
        },
        {SCHEMA_ORG: "schema"},
    ),
    # an import declares ``prov`` for another namespace, which nothing uses, so the name is free
    "import_declares_an_unused_name": (
        {
            "module.yaml": _schema("module", "prov: http://example.org/not-prov/\n", ""),
            "schema.yaml": _schema(
                "holder",
                "w3prov: http://www.w3.org/ns/prov#\n",
                """\
                classes:
                  Agent:
                    class_uri: w3prov:Agent
                """,
                imports="linkml:types module",
            ),
        },
        {PROV: "prov"},
    ),
    # an import declares ``prov`` for another namespace and identifies a class with it, so it keeps the name
    "import_uses_a_name": (
        {
            "module.yaml": _schema(
                "module",
                "prov: http://example.org/not-prov/\n",
                """\
                classes:
                  Provision:
                    class_uri: prov:Provision
                    attributes:
                      id: {identifier: true, range: uriorcurie}
                """,
            ),
            "schema.yaml": _schema(
                "holder",
                "w3prov: http://www.w3.org/ns/prov#\n",
                """\
                classes:
                  Agent:
                    class_uri: w3prov:Agent
                    attributes:
                      provision: {range: Provision}
                """,
                imports="linkml:types module",
            ),
        },
        {PROV: "w3prov", NOT_PROV: "prov"},
    ),
    "dce_alias": (
        {
            "schema.yaml": _schema(
                "dce",
                "dce: http://purl.org/dc/elements/1.1/\n",
                """\
                classes:
                  Record:
                    attributes:
                      title: {slot_uri: dce:title}
                """,
            )
        },
        {DC_ELEMENTS: "dc"},
    ),
    # both namespaces want ``schema``, which linkml:types declares for http://schema.org/
    "http_and_https_schema_org": (
        {
            "schema.yaml": _schema(
                "both",
                "sdo: https://schema.org/\nsdohttp: http://schema.org/\n",
                """\
                classes:
                  Person:
                    class_uri: sdo:Person
                    attributes:
                      full_name: {slot_uri: sdo:name}
                      old_name: {slot_uri: sdohttp:alternateName}
                """,
            )
        },
        {SCHEMA_ORG: "sdo", SCHEMA_ORG_HTTP: "schema"},
    ),
    # linkml:types declares ``schema`` for http://schema.org/, which this schema uses
    "imported_name_in_use": (
        {
            "schema.yaml": _schema(
                "imported",
                "sdo: https://schema.org/\n",
                """\
                classes:
                  Person:
                    class_uri: sdo:Person
                    attributes:
                      full_name: {slot_uri: sdo:name}
                      legacy: {slot_uri: "schema:legacyName"}
                """,
            )
        },
        {SCHEMA_ORG: "sdo", SCHEMA_ORG_HTTP: "schema"},
    ),
    # ``dc`` stays DCMI terms' name in shared outputs, so DCMI elements cannot take it
    "dc_terms_and_dce": (
        {
            "schema.yaml": _schema(
                "dcboth",
                "dc: http://purl.org/dc/terms/\ndce: http://purl.org/dc/elements/1.1/\n",
                """\
                classes:
                  Doc:
                    attributes:
                      title: {slot_uri: dc:title}
                      creator: {slot_uri: dce:creator}
                """,
            )
        },
        {DC_TERMS: "dcterms", DC_ELEMENTS: "dce"},
    ),
    "case_only_alias": (
        {
            "schema.yaml": _schema(
                "case",
                "FOAF: http://xmlns.com/foaf/0.1/\n",
                """\
                classes:
                  Agent:
                    class_uri: FOAF:Agent
                    attributes:
                      nick: {slot_uri: FOAF:nick}
                """,
            )
        },
        {FOAF: "foaf"},
    ),
    # ``time`` is a slot, so a JSON-LD context has a term of that name
    "prefix_name_is_a_slot": (
        {
            "schema.yaml": _schema(
                "termclash",
                "owltime: http://www.w3.org/2006/time#\n",
                """\
                classes:
                  Interval:
                    class_uri: owltime:Interval
                    attributes:
                      begin: {slot_uri: owltime:hasBeginning}
                      time: {range: string}
                """,
            )
        },
        {TIME: "owltime"},
    ),
    # ``dc`` is a slot with a class-scoped range
    "scoped_slot_named_like_a_prefix": (
        {
            "schema.yaml": _schema(
                "scoped",
                "dce: http://purl.org/dc/elements/1.1/\n",
                """\
                slots:
                  dc: {range: string}
                classes:
                  Doc:
                    slots: [dc]
                    slot_usage:
                      dc: {range: integer}
                    attributes:
                      title: {slot_uri: dce:title}
                """,
            )
        },
        {DC_ELEMENTS: "dce"},
    ),
    # ``dc`` is a permissible value, which a ``@type: @vocab`` slot reads as a term first
    "enum_value_named_like_a_prefix": (
        {
            "schema.yaml": _schema(
                "vocab",
                "dce: http://purl.org/dc/elements/1.1/\n",
                """\
                classes:
                  Doc:
                    attributes:
                      title: {slot_uri: dce:title}
                      vocabulary: {range: VocabularyEnum}
                enums:
                  VocabularyEnum:
                    permissible_values:
                      dc: {meaning: dce:title}
                      other: {}
                """,
            )
        },
        {DC_ELEMENTS: "dce"},
    ),
    "alias_as_default_prefix": (
        {
            "schema.yaml": _schema(
                "dflt",
                "w3prov: http://www.w3.org/ns/prov#\n",
                """\
                classes:
                  Agent:
                    attributes:
                      id: {identifier: true, range: uriorcurie}
                      label: {range: string}
                      delegate: {range: Agent, slot_uri: w3prov:actedOnBehalfOf}
                """,
                default_prefix="w3prov",
            )
        },
        {PROV: "prov"},
    ),
    "alias_in_type_and_enum_meaning": (
        {
            "schema.yaml": _schema(
                "typeuri",
                "w3prov: http://www.w3.org/ns/prov#\n",
                """\
                types:
                  ProvTime:
                    typeof: string
                    uri: w3prov:InstantaneousEvent
                classes:
                  Activity:
                    class_uri: w3prov:Activity
                    attributes:
                      started: {range: ProvTime}
                      role: {range: RoleEnum, slot_uri: w3prov:hadRole}
                enums:
                  RoleEnum:
                    permissible_values:
                      Author: {meaning: w3prov:Role}
                """,
            )
        },
        {PROV: "prov"},
    ),
    "prefixes_declared_in_an_import": (
        {
            "module.yaml": _schema(
                "module",
                "mybibo: http://purl.org/ontology/bibo/\nw3prov: http://www.w3.org/ns/prov#\n",
                """\
                classes:
                  Book:
                    class_uri: mybibo:Book
                    attributes:
                      source: {slot_uri: w3prov:hadPrimarySource}
                """,
            ),
            "schema.yaml": _schema(
                "main",
                "",
                """\
                classes:
                  Thesis:
                    is_a: Book
                    class_uri: mybibo:Thesis
                """,
                imports="linkml:types module",
            ),
        },
        {BIBO: "bibo", PROV: "prov"},
    ),
    # rdflib binds ``schema`` to https://schema.org/ by default; the schema's own declaration wins
    "conventional_http_schema_org": (
        {
            "schema.yaml": _schema(
                "httpschema",
                "schema: http://schema.org/\n",
                """\
                classes:
                  Person:
                    class_uri: schema:Person
                    attributes:
                      full_name: {slot_uri: schema:name}
                """,
            )
        },
        {SCHEMA_ORG_HTTP: "schema"},
    ),
}


def _write(tmp_path: Path, case: str) -> str:
    """Write the files of *case* to *tmp_path* and return the path of its main schema."""
    for name, text in CASES[case][0].items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    return str(tmp_path / "schema.yaml")


# ── Self-contained documents ──────────────────────────────────────────


def _rdf_prefixes(text: str, rdf_format: str) -> dict[str, str]:
    return {str(p): str(n) for p, n in Graph(bind_namespaces="none").parse(data=text, format=rdf_format).namespaces()}


def _prefix_lines(text: str) -> dict[str, str]:
    """The ``PREFIX name: <iri>`` declarations of ShExC and SPARQL."""
    return dict(re.findall(r"^PREFIX\s+([\w.-]*):\s*<([^>]*)>", text, flags=re.MULTILINE))


def _expand_curies(node: Any, prefixes: dict[str, str]) -> Any:
    """Expand every string of *node* whose prefix *prefixes* declares."""
    if isinstance(node, dict):
        return {key: _expand_curies(value, prefixes) for key, value in node.items()}
    if isinstance(node, list):
        return [_expand_curies(value, prefixes) for value in node]
    if isinstance(node, str):
        prefix, colon, rest = node.partition(":")
        if colon and prefix in prefixes and not rest.startswith("//"):
            return prefixes[prefix] + rest
    return node


def _sparql_meaning(text: str) -> dict[str, Any]:
    """Each query of a SPARQL file as its parse tree, with prefixed names expanded by its own PREFIX lines.

    rdflib's query algebra binds one prefix per namespace, so it cannot read a file that declares
    two names for one namespace, which SPARQL allows; the parse tree has the names as written.
    """

    def expand(node: Any, prefixes: dict[str, str]) -> Any:
        if isinstance(node, CompValue):
            if node.name == "pname":
                return prefixes[node["prefix"] if "prefix" in node else ""] + node.get("localname", "")
            return node.name, tuple((key, expand(value, prefixes)) for key, value in node.items())
        if isinstance(node, list | ParseResults):
            return tuple(expand(value, prefixes) for value in node)
        return str(node)

    meaning = {}
    for name, query in SparqlGenerator.split_sparql(text).items():
        prologue, body = parseQuery(query)
        prefixes = {(d["prefix"] if "prefix" in d else ""): str(d["iri"]) for d in prologue if d.name == "PrefixDecl"}
        meaning[name] = expand(body, prefixes)
    return meaning


def _sssom(text: str) -> tuple[dict[str, str], list[list[str]]]:
    """The ``curie_map`` and the rows of an SSSOM TSV."""
    curie_map, rows, in_map = {}, [], False
    for line in text.splitlines():
        if line.startswith("#curie_map:"):
            in_map = True
        elif in_map and line.startswith("# "):
            name, _, iri = line[2:].partition(": ")
            curie_map[name] = iri
        elif not line.startswith("#"):
            in_map = False
            rows.append(line.split("\t"))
    return curie_map, rows


@dataclass(frozen=True)
class Document:
    """A self-contained output: how to generate it, read its prefixes, and compare its meaning."""

    produce: Callable[[str, bool, Path], str]
    prefixes: Callable[[str], dict[str, str]]
    meaning: Callable[[str], Any]
    same: Callable[[Any, Any], bool] = lambda a, b: a == b


def _rdf_document(generator: type, rdf_format: str, parse_format: str, **flags: Any) -> Document:
    return Document(
        produce=lambda path, normalize, _: generator(
            path, normalize_prefixes=normalize, format=rdf_format, **flags
        ).serialize(),
        prefixes=lambda text: _rdf_prefixes(text, parse_format),
        meaning=lambda text: Graph().parse(data=text, format=parse_format),
        same=isomorphic,
    )


def _sssom_produce(path: str, normalize: bool, tmp_path: Path) -> str:
    output = tmp_path / f"out-{normalize}.sssom.tsv"
    SSSOMGenerator(path, output=str(output), normalize_prefixes=normalize).serialize()
    return output.read_text(encoding="utf-8")


DOCUMENTS = {
    "owl-ttl": _rdf_document(OwlSchemaGenerator, "ttl", "turtle"),
    "owl-xml": _rdf_document(OwlSchemaGenerator, "xml", "xml"),
    "shacl-ttl": _rdf_document(ShaclGenerator, "ttl", "turtle"),
    "shex-rdf": _rdf_document(ShExGenerator, "rdf", "turtle"),
    "shexc": Document(
        produce=lambda path, normalize, _: ShExGenerator(path, normalize_prefixes=normalize).serialize(),
        prefixes=_prefix_lines,
        meaning=lambda text: json.loads(as_json(parse_shexc(text))),
    ),
    "sparql": Document(
        produce=lambda path, normalize, _: SparqlGenerator(path, normalize_prefixes=normalize).serialize(),
        prefixes=_prefix_lines,
        meaning=_sparql_meaning,
    ),
    "yarrrml": Document(
        produce=lambda path, normalize, _: YarrrmlGenerator(path, normalize_prefixes=normalize).serialize(),
        prefixes=lambda text: yaml.safe_load(text)["prefixes"],
        meaning=lambda text: _expand_curies(yaml.safe_load(text)["mappings"], yaml.safe_load(text)["prefixes"]),
    ),
    "sssom": Document(
        produce=_sssom_produce,
        prefixes=lambda text: _sssom(text)[0],
        meaning=lambda text: _expand_curies(_sssom(text)[1], _sssom(text)[0]),
    ),
}

# Formats and options that change which prefixes an RDF output binds or prints.
RDF_VARIANTS = {
    "owl-n3": _rdf_document(OwlSchemaGenerator, "n3", "n3"),
    "owl-json-ld": _rdf_document(OwlSchemaGenerator, "json-ld", "json-ld"),
    "owl-nt": _rdf_document(OwlSchemaGenerator, "nt", "nt"),
    "owl-diff-stable": _rdf_document(OwlSchemaGenerator, "ttl", "turtle", diff_stable=True),
    "owl-mapped-uris": _rdf_document(OwlSchemaGenerator, "ttl", "turtle", use_native_uris=False),
    "owl-no-metaclasses": _rdf_document(OwlSchemaGenerator, "ttl", "turtle", metaclasses=False, type_objects=False),
    "owl-metadata-profile-rdfs": _rdf_document(OwlSchemaGenerator, "ttl", "turtle", metadata_profile="rdfs"),
    "shacl-diff-stable": _rdf_document(ShaclGenerator, "ttl", "turtle", diff_stable=True),
    "shacl-annotations": _rdf_document(ShaclGenerator, "ttl", "turtle", include_annotations=True),
}


# gen-shex's RDF output reads the ShEx JSON-LD context, which the network marker serves from local files.
DOCUMENT_NAMES = [pytest.param(d, marks=pytest.mark.network) if d == "shex-rdf" else d for d in sorted(DOCUMENTS)]


@pytest.mark.parametrize("case", sorted(CASES))
@pytest.mark.parametrize("document", DOCUMENT_NAMES)
def test_document_means_the_same(tmp_path, document, case):
    """With the option a self-contained document denotes the same IRIs as without it."""
    doc = DOCUMENTS[document]
    path = _write(tmp_path, case)
    off, on = (doc.produce(path, normalize, tmp_path) for normalize in (False, True))
    assert doc.same(doc.meaning(off), doc.meaning(on))


@pytest.mark.parametrize("case", sorted(CASES))
@pytest.mark.parametrize("document", DOCUMENT_NAMES)
def test_document_writes_the_planned_names(tmp_path, document, case):
    """Every generator writes the same name for a namespace, and no other name for it."""
    doc = DOCUMENTS[document]
    path = _write(tmp_path, case)
    planned = CASES[case][1]
    off = doc.prefixes(doc.produce(path, False, tmp_path))
    on = doc.prefixes(doc.produce(path, True, tmp_path))
    for namespace, name in planned.items():
        names = {prefix for prefix, iri in on.items() if iri == namespace}
        assert names <= {name}, f"{namespace} is written as {names}"
        if namespace in off.values():
            assert on.get(name) == namespace


@pytest.mark.parametrize("variant", sorted(RDF_VARIANTS))
@pytest.mark.parametrize("case", ["prov_alias", "conventional_http_schema_org", "prefixes_declared_in_an_import"])
def test_rdf_variants(tmp_path, variant, case):
    """Other formats and options of gen-owl and gen-shacl keep the graph and use the planned names."""
    doc = RDF_VARIANTS[variant]
    path = _write(tmp_path, case)
    off, on = (doc.produce(path, normalize, tmp_path) for normalize in (False, True))
    assert doc.same(doc.meaning(off), doc.meaning(on))
    for namespace, name in CASES[case][1].items():
        assert {p for p, iri in doc.prefixes(on).items() if iri == namespace} <= {name}


@pytest.mark.parametrize("generator", [OwlSchemaGenerator, ShaclGenerator])
def test_no_rdflib_generated_names(tmp_path, generator):
    """A declared conventional name wins over the name rdflib binds by default, so no ``schema1`` appears."""
    path = _write(tmp_path, "conventional_http_schema_org")
    prefixes = _rdf_prefixes(generator(path, normalize_prefixes=True).serialize(), "turtle")
    assert prefixes["schema"] == SCHEMA_ORG_HTTP
    assert not [p for p in prefixes if re.fullmatch(r"schema\d+", p)]


# ── JSON-LD contexts and prefix maps ──────────────────────────────────


def _context(path: str, normalize: bool, **flags: Any) -> dict:
    return json.loads(ContextGenerator(path, normalize_prefixes=normalize, **flags).serialize())["@context"]


def _context_prefixes(context: dict) -> dict[str, str]:
    """The prefix definitions of a context: IRIs as strings or ``@prefix`` term definitions."""
    prefixes = {}
    for key, value in context.items():
        if key.startswith("@") or ":" in key:
            continue
        if isinstance(value, str):
            prefixes[key] = value
        elif isinstance(value, dict) and value.get("@prefix") is True:
            prefixes[key] = value["@id"]
    return prefixes


def _expanded_terms(context: dict, parent: Context | None = None) -> set:
    """The IRIs each term of a JSON-LD context expands to, without the term names.

    Uses rdflib's JSON-LD context processing; scoped contexts are expanded within their parent.
    """
    ctx = Context(context) if parent is None else parent.subcontext(context)
    expanded = {("@vocab", ctx.vocab)}
    for name in context:
        term = ctx.terms.get(name)
        if term is not None:
            scoped = frozenset(_expanded_terms(term.context, ctx)) if isinstance(term.context, dict) else None
            expanded.add((term.id, term.type, str(term.container), term.reverse, scoped))
    return expanded


def _terms(context: dict) -> dict:
    """The term definitions of a context, without its prefix definitions."""
    return {
        key: value
        for key, value in context.items()
        if not key.startswith("@") and isinstance(value, dict) and value.get("@prefix") is not True
    }


def _data_graph(context: Any, terms: dict, prefixes: list[str], vocabulary: list[str]) -> Graph:
    """Parse, with *context*, a document that uses every term of *terms* (term definitions).

    It has one node per prefix of *prefixes*, identified by a compact IRI with that prefix.
    IRI-valued terms get a compact IRI and a relative IRI, vocabulary-valued ones every name of
    *vocabulary* (the permissible values, the only names valid data uses there), and the others a
    string. Every term is also a type of every node.
    """

    def value(definition: dict, prefix: str) -> Any:
        coercion = definition.get("@type")
        if coercion == "@id":
            return [f"{prefix}:object", "relative"]
        if coercion == "@vocab":
            return vocabulary
        return "text"

    nodes = [
        {"@id": f"{prefix}:node", "@type": sorted(terms), **{t: value(d, prefix) for t, d in terms.items()}}
        for prefix in prefixes
    ]
    document = {"@context": context, "@graph": nodes}
    return Graph().parse(data=json.dumps(document), format="json-ld", base="http://base.test/")


def _schema_namespaces(path: str) -> dict[str, str]:
    """The prefixes of a schema and its imports, with which LinkML expands the CURIEs of data."""
    sv = SchemaView(path)
    sv.imports_closure()
    return {str(prefix): str(namespace) for prefix, namespace in sv.namespaces().items()}


def _vocabulary(path: str) -> list[str]:
    sv = SchemaView(path)
    return sorted(text for enum in sv.all_enums().values() for text in enum.permissible_values)


CONTEXT_FLAGS = {
    "default": {},
    "use-curies": {"use_curies": True},
    "flatprefixes": {"flatprefixes": True},
    "fix-multivalue-containers": {"fix_multivalue_containers": True},
    "no-mergeimports": {"mergeimports": False},
}


@pytest.mark.parametrize("case", sorted(CASES))
@pytest.mark.parametrize("flags", sorted(CONTEXT_FLAGS))
def test_context_terms_expand_the_same(tmp_path, flags, case):
    """Every term of the context expands to the IRIs it expands to without the option."""
    path = _write(tmp_path, case)
    off, on = (_context(path, normalize, **CONTEXT_FLAGS[flags]) for normalize in (False, True))
    assert _expanded_terms(on) == _expanded_terms(off)
    assert _terms(on).keys() == _terms(off).keys()


@pytest.mark.parametrize("case", sorted(CASES))
@pytest.mark.parametrize("flags", sorted(CONTEXT_FLAGS))
def test_context_keeps_declared_names_and_adds_planned_ones(tmp_path, flags, case):
    path = _write(tmp_path, case)
    off, on = (_context_prefixes(_context(path, normalize, **CONTEXT_FLAGS[flags])) for normalize in (False, True))
    assert off.items() <= on.items()
    for namespace, name in CASES[case][1].items():
        if namespace in off.values():
            assert on.get(name) == namespace


@pytest.mark.parametrize("case", sorted(CASES))
@pytest.mark.parametrize("use_curies", [False, True])
def test_data_expands_the_same(tmp_path, case, use_curies):
    """Data written with a prefix that the default context defines means the same under both contexts,
    and so does data written with a prefix of the schema or its imports that neither defines. A name
    only the normalized context defines is the conventional name of a namespace that the default
    context defines under another name. Where the schema's documents write that name, it denotes the
    namespace LinkML expands it to; where only an import declares it for a namespace nothing uses, the
    context and LinkML differ. Data written with the planned names means the same as with the declared
    ones."""
    path = _write(tmp_path, case)
    off, on = (_context(path, normalize, use_curies=use_curies) for normalize in (False, True))
    off_prefixes, on_prefixes = _context_prefixes(off), _context_prefixes(on)
    schema_prefixes = _schema_namespaces(path)
    terms, vocabulary = _terms(off), _vocabulary(path)
    sv = SchemaView(path)
    plan, written = preferred_prefixes(sv), written_prefixes(sv)
    for prefix in sorted(off_prefixes.keys() | schema_prefixes.keys()):
        expected_context = off
        if prefix not in off_prefixes and prefix in on_prefixes:
            namespace = on_prefixes[prefix]
            assert namespace in off_prefixes.values()
            assert well_known_prefix_map()[namespace] == prefix
            if prefix in written:
                assert namespace == schema_prefixes[prefix]
            else:
                # the accepted difference: only an import declares the name, for a namespace nothing uses
                assert schema_prefixes.get(prefix) != namespace
            expected_context = [{prefix: namespace}, off]
        expected = _data_graph(expected_context, terms, [prefix], vocabulary)
        assert isomorphic(_data_graph(on, terms, [prefix], vocabulary), expected), prefix
        planned = plan.standardize_prefix(prefix) or prefix
        assert isomorphic(_data_graph(on, terms, [planned], vocabulary), expected), planned


@pytest.mark.parametrize("case", ["prov_alias", "prefix_name_is_a_slot", "prefixes_declared_in_an_import"])
@pytest.mark.parametrize("prefixes_normalized", [False, True])
@pytest.mark.parametrize("model_normalized", [False, True])
def test_prefix_and_model_contexts_combine(tmp_path, case, prefixes_normalized, model_normalized):
    """A prefix-only context (``--no-model``) and a model-only context (``--no-prefixes``) combine to the
    same meaning, whichever of them was normalized."""
    path = _write(tmp_path, case)
    full = _context(path, False)
    combined = [
        _context(path, prefixes_normalized, model=False),
        _context(path, model_normalized, prefixes=False),
    ]
    declared = sorted(_context_prefixes(full))
    vocabulary = _vocabulary(path)
    expected = _data_graph(full, _terms(full), declared, vocabulary)
    assert isomorphic(_data_graph(combined, _terms(full), declared, vocabulary), expected)


@pytest.mark.parametrize("case", ["prov_alias", "prefixes_declared_in_an_import"])
def test_prefix_map_combines_with_a_model_only_context(tmp_path, case):
    """The prefixes of ``--no-prefixes`` come from gen-prefix-map, whose names the context then keeps."""
    path = _write(tmp_path, case)
    full = _context(path, False)
    prefix_map = json.loads(PrefixGenerator(path).serialize())
    combined = [prefix_map, _context(path, True, prefixes=False)]
    declared = sorted(_context_prefixes(full))
    expected = _data_graph(full, _terms(full), declared, _vocabulary(path))
    assert isomorphic(_data_graph(combined, _terms(full), declared, _vocabulary(path)), expected)


def test_no_prefixes_context_is_unchanged(tmp_path):
    """Without prefix definitions a context writes compact IRIs only with the names other contexts define."""
    path = _write(tmp_path, "prov_alias")
    assert _context(path, True, prefixes=False) == _context(path, False, prefixes=False)


@pytest.mark.parametrize("base_normalized", [False, True])
@pytest.mark.parametrize("extension_normalized", [False, True])
@pytest.mark.parametrize("exclude", ["exclude_imports", "exclude_external_imports"])
def test_contexts_of_an_import_and_its_importer_combine(tmp_path, base_normalized, extension_normalized, exclude):
    """The context of an importing schema, without the imported elements, combines with the imported
    schema's context, whichever was normalized; the importer's ``time`` slot shares the name ``time``."""
    (tmp_path / "base.yaml").write_text(
        _schema(
            "base",
            "owltime: http://www.w3.org/2006/time#\n",
            """\
            classes:
              Interval:
                class_uri: owltime:Interval
                attributes:
                  begin: {slot_uri: owltime:hasBeginning}
            """,
        ),
        encoding="utf-8",
    )
    (tmp_path / "schema.yaml").write_text(
        _schema(
            "extension",
            "owltime: http://www.w3.org/2006/time#\n",
            """\
            classes:
              Meeting:
                is_a: Interval
                attributes:
                  time: {range: string}
            """,
            imports="linkml:types base",
        ),
        encoding="utf-8",
    )
    base, extension = str(tmp_path / "base.yaml"), str(tmp_path / "schema.yaml")
    expected_contexts = [_context(base, False), _context(extension, False, **{exclude: True})]
    contexts = [_context(base, base_normalized), _context(extension, extension_normalized, **{exclude: True})]
    terms = _terms(expected_contexts[0]) | _terms(expected_contexts[1])
    declared = sorted(_context_prefixes(expected_contexts[0]) | _context_prefixes(expected_contexts[1]))
    expected = _data_graph(expected_contexts, terms, declared, [])
    assert isomorphic(_data_graph(contexts, terms, declared, []), expected)


@pytest.mark.parametrize("embed", [False, True])
def test_frame_type_expands_the_same(tmp_path, embed):
    """The frame's ``@type`` is written with the planned name and denotes the same class."""
    (tmp_path / "schema.yaml").write_text(
        _schema(
            "frame",
            "w3prov: http://www.w3.org/ns/prov#\n",
            """\
            classes:
              Activity:
                tree_root: true
                class_uri: w3prov:Activity
                attributes:
                  association: {range: Association, inlined: true, slot_uri: w3prov:qualifiedAssociation}
              Association:
                class_uri: w3prov:Association
                attributes:
                  role: {slot_uri: w3prov:hadRole}
            """,
        ),
        encoding="utf-8",
    )
    path = str(tmp_path / "schema.yaml")
    frames = []
    for normalize in (False, True):
        output = tmp_path / f"out-{normalize}.context.jsonld"
        gen = ContextGenerator(path, normalize_prefixes=normalize, emit_frame=True, embed_context_in_frame=embed)
        gen.serialize(output=str(output))
        frame = json.loads(output.with_suffix(".frame.jsonld").read_text(encoding="utf-8"))
        context = frame["@context"] if embed else json.loads(output.read_text(encoding="utf-8"))["@context"]
        frames.append((frame, Context(context)))
    (off, off_ctx), (on, on_ctx) = frames
    assert on["@type"] == "prov:Activity"
    assert on_ctx.expand(on["@type"]) == off_ctx.expand(off["@type"]) == PROV + "Activity"
    assert on.keys() == off.keys()


@pytest.mark.parametrize("generator", [ContextGenerator, ShExGenerator])
def test_yaml_text_input_with_local_imports(tmp_path, generator):
    """A schema given as YAML text resolves its local imports against ``base_dir``, as without the option."""
    path = Path(_write(tmp_path, "prefixes_declared_in_an_import"))
    from_text = generator(path.read_text(encoding="utf-8"), base_dir=str(tmp_path), normalize_prefixes=True)
    assert from_text.serialize() == generator(str(path), normalize_prefixes=True).serialize()


def test_sssom_keeps_a_name_it_writes_undeclared(tmp_path):
    """gen-sssom writes ``skos:exactMatch`` without declaring ``skos``, so a declared ``skosx`` for SKOS keeps
    its name there, while documents that declare what they write use ``skos``."""
    (tmp_path / "schema.yaml").write_text(
        _schema(
            "skos",
            "skosx: http://www.w3.org/2004/02/skos/core#\n",
            """\
            classes:
              Topic:
                exact_mappings: [skosx:Concept]
            """,
        ),
        encoding="utf-8",
    )
    path = str(tmp_path / "schema.yaml")
    sssom = DOCUMENTS["sssom"]
    off, on = (sssom.produce(path, normalize, tmp_path) for normalize in (False, True))
    assert sssom.same(sssom.meaning(off), sssom.meaning(on))
    assert sssom.prefixes(on)["skosx"] == SKOS
    assert _rdf_prefixes(OwlSchemaGenerator(path, normalize_prefixes=True).serialize(), "turtle")["skos"] == SKOS


def test_sssom_rewrites_only_curie_columns(tmp_path):
    (tmp_path / "schema.yaml").write_text(
        _schema(
            "label",
            "w3prov: http://www.w3.org/ns/prov#\n",
            """\
            classes:
              Agent:
                title: "w3prov:Agent as used in the old feed"
                class_uri: w3prov:Agent
                exact_mappings: [w3prov:Person]
            """,
        ),
        encoding="utf-8",
    )
    _, rows = _sssom(_sssom_produce(str(tmp_path / "schema.yaml"), True, tmp_path))
    assert ["prov:Agent", "w3prov:Agent as used in the old feed", "skos:exactMatch", "", "prov:Person"] == rows[1][:5]


# ── The plan ──────────────────────────────────────────────────────────


@pytest.mark.parametrize("case", sorted(CASES))
def test_plan(tmp_path, case):
    """One plan per schema gives each namespace its name."""
    plan = preferred_prefixes(SchemaView(_write(tmp_path, case)))
    assert {ns: plan.reverse_prefix_map[ns] for ns in CASES[case][1]} == CASES[case][1]


def test_plan_warns_when_a_prefix_keeps_its_name(tmp_path, caplog):
    with caplog.at_level(logging.WARNING):
        preferred_prefixes(SchemaView(_write(tmp_path, "http_and_https_schema_org")))
    assert "Prefix 'sdo' is not renamed to 'schema'" in caplog.text
    assert "Prefix 'sdohttp' is not renamed" not in caplog.text


def test_plan_warns_when_a_name_is_taken_from_an_unused_import_prefix(tmp_path, caplog):
    """LinkML keeps expanding the name in data as the import declares it, so the plan says so."""
    with caplog.at_level(logging.WARNING):
        preferred_prefixes(SchemaView(_write(tmp_path, "schema_org_alias")))
    assert (
        f"Prefix 'schema' is written for <{SCHEMA_ORG}>. An import declares it for <{SCHEMA_ORG_HTTP}>" in caplog.text
    )
    assert "is not renamed" not in caplog.text


@pytest.mark.parametrize("case", ["prov_alias", "imported_name_in_use", "import_uses_a_name"])
def test_plan_is_silent_when_no_import_prefix_is_taken(tmp_path, caplog, case):
    with caplog.at_level(logging.WARNING):
        preferred_prefixes(SchemaView(_write(tmp_path, case)))
    assert "An import declares it" not in caplog.text


def test_plan_warning_names_only_the_other_namespaces_of_the_name(tmp_path, caplog):
    """One import declares ``schema`` for https://schema.org/ and linkml:types for http://schema.org/;
    the name is written for the former, so the warning is about the latter alone."""
    (tmp_path / "module.yaml").write_text(
        _schema("module", f"schema: {SCHEMA_ORG}\n", "", imports=""), encoding="utf-8"
    )
    (tmp_path / "schema.yaml").write_text(
        _schema("main", f"sdo: {SCHEMA_ORG}\n", "classes:\n  Person: {}\n", imports="linkml:types module"),
        encoding="utf-8",
    )
    with caplog.at_level(logging.WARNING):
        plan = preferred_prefixes(SchemaView(str(tmp_path / "schema.yaml")))
    assert plan.reverse_prefix_map[SCHEMA_ORG] == "schema"
    assert f"An import declares it for <{SCHEMA_ORG_HTTP}>, which nothing uses" in caplog.text


def test_plan_is_silent_when_the_import_declares_the_name_for_the_same_namespace(tmp_path, caplog):
    (tmp_path / "module.yaml").write_text(_schema("module", f"schema: {SCHEMA_ORG}\n", ""), encoding="utf-8")
    (tmp_path / "schema.yaml").write_text(
        _schema("main", f"sdo: {SCHEMA_ORG}\n", "classes:\n  Person:\n    class_uri: sdo:Person\n", imports="module"),
        encoding="utf-8",
    )
    with caplog.at_level(logging.WARNING):
        plan = preferred_prefixes(SchemaView(str(tmp_path / "schema.yaml")))
    assert plan.reverse_prefix_map[SCHEMA_ORG] == "schema"
    assert "An import declares it" not in caplog.text


UNDECLARED_DC = {
    # nothing declares ``dc``: the import's slot gets its namespace from a default CURIE map
    "module.yaml": textwrap.dedent(
        """\
        id: https://example.org/module
        name: module
        prefixes:
          ex: https://example.org/
        default_prefix: ex
        default_curi_maps: [semweb_context]
        types:
          string: {uri: xsd:string, base: str}
          uriorcurie: {uri: xsd:anyURI, base: URIorCURIE, repr: str}
        slots:
          title: {slot_uri: "dc:title", range: string}
        classes:
          Document:
            slots: [title]
        """
    ),
    "schema.yaml": textwrap.dedent(
        """\
        id: https://example.org/main
        name: main
        prefixes:
          ex: https://example.org/
          dce: http://purl.org/dc/elements/1.1/
        default_prefix: ex
        default_curi_maps: [semweb_context]
        imports: [module]
        classes:
          Book:
            is_a: Document
            attributes:
              id: {identifier: true, range: uriorcurie}
              creator: {slot_uri: dce:creator, range: string}
        """
    ),
}


@pytest.mark.parametrize("flags", [{}, {"exclude_imports": True}, {"exclude_imports": True, "mergeimports": False}])
def test_a_prefix_written_undeclared_is_given_to_no_namespace(tmp_path, flags):
    """A CURIE written with a prefix that nothing declares is read with a default CURIE map, here ``dc``
    as DCMI terms. The name is not given to DCMI elements, whose conventional name it is: the contexts
    of the schema define it for one namespace at most, whichever flags they are generated with."""
    for name, text in UNDECLARED_DC.items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    path = str(tmp_path / "schema.yaml")
    assert preferred_prefixes(SchemaView(path)).reverse_prefix_map[DC_ELEMENTS] == "dce"
    defined = {
        _context_prefixes(_context(path, normalize, **f)).get("dc") for normalize in (False, True) for f in ({}, flags)
    }
    assert defined - {None} == {DC_TERMS}


DIRECT_SCHEMA_ORG = _schema(
    "direct",
    "schema: https://schema.org/\n",
    """\
    classes:
      Person:
        class_uri: schema:Person
        attributes:
          id: {identifier: true, range: uriorcurie}
    """,
)


@pytest.mark.parametrize("generator", [ContextGenerator, ShExGenerator])
def test_a_schema_that_declares_schema_for_https_does_not_load(tmp_path, generator):
    """Why a schema writes ``sdo``: declaring ``schema`` for https://schema.org/ next to linkml:types,
    which declares it for http://schema.org/, is refused by the generators built on SchemaLoader."""
    (tmp_path / "schema.yaml").write_text(DIRECT_SCHEMA_ORG, encoding="utf-8")
    with pytest.raises(ValueError, match="Prefix: schema mismatch"):
        generator(str(tmp_path / "schema.yaml")).serialize()


@pytest.mark.parametrize("generator", [OwlSchemaGenerator, ShaclGenerator])
def test_a_schema_that_declares_schema_for_https_gets_the_imports_namespace(tmp_path, generator):
    """... and gen-owl and gen-shacl read the name as the import declares it, so they write
    http://schema.org/ IRIs for a class the schema puts in https://schema.org/."""
    (tmp_path / "schema.yaml").write_text(DIRECT_SCHEMA_ORG, encoding="utf-8")
    graph = Graph().parse(data=generator(str(tmp_path / "schema.yaml")).serialize(), format="turtle")
    iris = {str(term) for triple in graph for term in triple}
    assert f"{SCHEMA_ORG_HTTP}Person" in iris
    assert f"{SCHEMA_ORG}Person" not in iris


# How an import can use a prefix that only it declares, and what is no use of it.
IMPORT_USES = {
    "class_uri": ("classes:\n  Thing:\n    class_uri: other:Thing\n", True),
    "slot_uri": ("slots:\n  part:\n    slot_uri: other:part\n", True),
    "attribute_slot_uri": ("classes:\n  Thing:\n    attributes:\n      part: {slot_uri: other:part}\n", True),
    "slot_usage_slot_uri": (
        "slots:\n  part: {}\nclasses:\n  Thing:\n    slots: [part]\n"
        "    slot_usage:\n      part: {slot_uri: other:part}\n",
        True,
    ),
    "class_mapping": ("classes:\n  Thing:\n    exact_mappings: [other:Thing]\n", True),
    "slot_mapping": ("slots:\n  part:\n    close_mappings: [other:part]\n", True),
    "enum_uri": ("enums:\n  Kind:\n    enum_uri: other:Kind\n    permissible_values:\n      a: {}\n", True),
    "permissible_value_meaning": ("enums:\n  Kind:\n    permissible_values:\n      a: {meaning: other:a}\n", True),
    "permissible_value_mapping": (
        "enums:\n  Kind:\n    permissible_values:\n      a: {exact_mappings: [other:a]}\n",
        True,
    ),
    "type_uri": ("types:\n  Code:\n    typeof: string\n    uri: other:Code\n", True),
    "id_prefixes": ("classes:\n  Thing:\n    id_prefixes: [other]\n", True),
    "emit_prefixes": ("emit_prefixes: [other]\n", True),
    "default_prefix": ("classes:\n  Thing: {}\n", True),
    "name_derived_iri": ("classes:\n  Thing:\n    class_uri: ex:Thing\n", True),
    "attribute_mapping": (
        "classes:\n  Thing:\n    attributes:\n      part: {exact_mappings: [other:part]}\n",
        True,
    ),
    "enum_mapping": ("enums:\n  Kind:\n    exact_mappings: [other:Kind]\n    permissible_values:\n      a: {}\n", True),
    "iri_instead_of_a_curie": ("classes:\n  Thing:\n    class_uri: http://example.org/other/Thing\n", True),
    "curie_with_a_colon_in_its_local_part": ("slots:\n  part:\n    slot_uri: other:part:one\n", True),
    "type_mapping": (
        "types:\n  Code:\n    typeof: string\n    uri: xsd:string\n    exact_mappings: [other:Code]\n",
        False,
    ),
    "description": ("classes:\n  Thing:\n    description: see other:Thing\n", False),
    "nothing": ("", False),
}


OTHER = "http://example.org/other/"


def _write_import_use(tmp_path: Path, use: str) -> str:
    """Write a schema that imports a module using its prefix ``other`` as *use* says; return its path."""
    body, _ = IMPORT_USES[use]
    default_prefix = "other" if use in {"default_prefix", "name_derived_iri"} else "ex"
    (tmp_path / "module.yaml").write_text(
        _schema("module", f"other: {OTHER}\nxsd: http://www.w3.org/2001/XMLSchema#\n", body, default_prefix),
        encoding="utf-8",
    )
    (tmp_path / "schema.yaml").write_text(_schema("main", "", "", imports="linkml:types module"), encoding="utf-8")
    return str(tmp_path / "schema.yaml")


@pytest.mark.parametrize("use", sorted(IMPORT_USES))
def test_a_prefix_only_an_import_declares_is_written_when_in_use(tmp_path, use):
    """A prefix that only an import declares holds its name when an element is identified by, or
    mapped to, an IRI of its namespace, or names the prefix; the mappings of a type are no use."""
    written = written_prefixes(SchemaView(_write_import_use(tmp_path, use)))
    assert ("other" in written) is IMPORT_USES[use][1]
    assert "schema" not in written


# The generators that write each kind of use; the others leave the namespace out.
IMPORT_USE_DOCUMENTS = {
    "owl-ttl": lambda path: _iris(
        Graph().parse(data=OwlSchemaGenerator(path, use_native_uris=False).serialize(), format="turtle")
    ),
    "owl-native": lambda path: _iris(Graph().parse(data=OwlSchemaGenerator(path).serialize(), format="turtle")),
    "shacl-ttl": lambda path: _iris(Graph().parse(data=ShaclGenerator(path).serialize(), format="turtle")),
    "shexc": lambda path: _iris(json.loads(as_json(parse_shexc(ShExGenerator(path).serialize())))),
    "context": lambda path: set(_context_prefixes(_context(path, False)).values())
    | {str(iri) for iri in _expanded_terms(_context(path, False))},
}


# Such a CURIE is no IRI of the namespace to these generators; gen-sparql writes it as it stands
# (test_sparql_keeps_what_the_prefixes_of_its_queries_denote).
@pytest.mark.parametrize("use", sorted(IMPORT_USES.keys() - {"curie_with_a_colon_in_its_local_part"}))
def test_the_generators_write_what_the_plan_counts_as_use(tmp_path, use):
    """What the plan counts as a use of an import's prefix is what a generator writes: where it holds
    the name some document has an IRI of the namespace, and where it frees the name none has."""
    path = _write_import_use(tmp_path, use)
    writers = {name for name, iris in IMPORT_USE_DOCUMENTS.items() if any(i.startswith(OTHER) for i in iris(path))}
    assert bool(writers) is IMPORT_USES[use][1], writers


@pytest.mark.parametrize("class_uri", ["prov:Provision", f"{NOT_PROV}Provision"], ids=["curie", "iri"])
@pytest.mark.parametrize("imports", ["linkml:types module leaf", "linkml:types leaf module"])
@pytest.mark.parametrize("using", ["module", "leaf"])
def test_a_name_two_imports_declare_is_held_when_either_namespace_is_in_use(tmp_path, using, imports, class_uri):
    """Imports may declare one name for two namespaces; which one LinkML reads depends on the import
    order. The name is held whichever import uses its namespace and whichever is read first, by the
    prefix of a CURIE or by an IRI of either namespace."""
    for name in ("module", "leaf"):
        namespace = NOT_PROV if name == using else "http://example.org/unused/"
        body = f"classes:\n  Provision:\n    class_uri: {class_uri}\n" if name == using else ""
        module_imports = "linkml:types leaf" if name == "module" else "linkml:types"
        (tmp_path / f"{name}.yaml").write_text(
            _schema(name, f"prov: {namespace}\n", body, imports=module_imports), encoding="utf-8"
        )
    (tmp_path / "schema.yaml").write_text(
        _schema("holder", "w3prov: http://www.w3.org/ns/prov#\n", "", imports=imports), encoding="utf-8"
    )
    sv = SchemaView(str(tmp_path / "schema.yaml"))
    written = written_prefixes(sv)
    assert "prov" in written
    if class_uri.startswith(NOT_PROV):
        assert written["prov"] == NOT_PROV
    assert preferred_prefixes(sv).reverse_prefix_map[PROV] == "w3prov"


def test_plan_does_not_depend_on_what_the_view_expanded_before(tmp_path):
    """SchemaView caches its namespaces, also when asked before the imports are loaded; the plan reads
    the prefixes of the CURIEs as written and holds the import's name all the same."""
    path = _write(tmp_path, "import_uses_a_name")
    fresh, used = SchemaView(path), SchemaView(path)
    used.namespaces()
    used.expand_curie("ex:anything")
    assert written_prefixes(used) == written_prefixes(fresh)
    assert preferred_prefixes(used).reverse_prefix_map[PROV] == "w3prov"


# Schemas whose SPARQL uses a prefix that the plan gives to another namespace, or that nothing declares.
SPARQL_KEEPS = {
    # the local part has a colon, so the slot's IRI is not in the namespace the prefix is checked against
    "colon_in_the_local_part": _schema(
        "colon",
        "sdo: https://schema.org/\n",
        """\
        slots:
          legacy: {slot_uri: "schema:legacy:name", range: string}
        classes:
          Person:
            class_uri: sdo:Person
            slots: [legacy]
        """,
    ),
    # the schema declares ``schema`` itself, which the generator reads as the import declares it
    "name_declared_for_two_namespaces": DIRECT_SCHEMA_ORG,
    # nothing declares ``schema``
    "undeclared_prefix": textwrap.dedent(
        """\
        id: https://example.org/undeclared
        name: undeclared
        default_prefix: ex
        prefixes:
          ex: https://example.org/
          sdo: https://schema.org/
        default_curi_maps: [semweb_context]
        types:
          string: {uri: xsd:string, base: str}
        slots:
          legacy: {slot_uri: "schema:legacy", range: string}
        classes:
          Person:
            class_uri: sdo:Person
            slots: [legacy]
        """
    ),
}


def _sparql_names(text: str) -> dict[str, str | None]:
    """Each prefix that the queries of a SPARQL file use, with the namespace the file declares for it."""
    declared = _prefix_lines(text)
    used = set(re.findall(r"(?<![\w<:/#])([A-Za-z][\w.-]*):(?=[A-Za-z_])", text.split("\n\n", 1)[1]))
    return {prefix: declared.get(prefix) for prefix in used}


@pytest.mark.parametrize("case", sorted(SPARQL_KEEPS))
def test_sparql_keeps_what_the_prefixes_of_its_queries_denote(tmp_path, case):
    """A prefix that a query uses denotes the same namespace with the option, or stays undeclared:
    the generator renames around the prefixes its queries use, whatever the plan gives away."""
    (tmp_path / "schema.yaml").write_text(SPARQL_KEEPS[case], encoding="utf-8")
    off, on = (SparqlGenerator(str(tmp_path / "schema.yaml"), normalize_prefixes=n).serialize() for n in (False, True))
    names_off, names_on = _sparql_names(off), _sparql_names(on)
    assert "schema" in names_off
    for prefix, namespace in names_off.items():
        assert names_on.get(prefix) == namespace, prefix


NOTHING_TO_RENAME = _schema(
    "plain",
    "zed: https://example.org/zed/\nabc: https://example.org/abc/\n",
    """\
    classes:
      Thing:
        class_uri: zed:Thing
        exact_mappings: [abc:Thing]
        attributes:
          id: {identifier: true, range: uriorcurie}
          part: {slot_uri: abc:part}
    """,
)


# gen-shex's RDF output binds no prefix of the schema by default and the planned ones with the option.
@pytest.mark.parametrize("document", sorted(DOCUMENTS.keys() - {"shex-rdf"}))
def test_document_with_nothing_to_rename_is_unchanged(tmp_path, document):
    """Without a well-known namespace the option changes no byte, the order of the prefix
    declarations included."""
    (tmp_path / "schema.yaml").write_text(NOTHING_TO_RENAME, encoding="utf-8")
    doc = DOCUMENTS[document]
    off, on = (doc.produce(str(tmp_path / "schema.yaml"), normalize, tmp_path) for normalize in (False, True))
    assert on == off


def test_prefix_declarations_keep_the_order_of_the_document():
    plan = Converter([Record(prefix="schema", uri_prefix=SCHEMA_ORG, prefix_synonyms=["sdo"])])
    declared = {"zed": "https://example.org/zed/", "sdo": SCHEMA_ORG, "abc": "https://example.org/abc/"}
    declarations = prefix_declarations(document_prefixes(declared, plan), declared)
    assert list(declarations.items()) == [
        ("zed", "https://example.org/zed/"),
        ("schema", SCHEMA_ORG),
        ("abc", "https://example.org/abc/"),
    ]


def test_sparql_template_prefixes_are_those_the_template_writes():
    from linkml.generators.sparqlgen import _TEMPLATE_PREFIXES, template

    static = re.sub(r"{{.*?}}|{%.*?%}", "", template)
    assert set(re.findall(r"(?<![\w{.])([A-Za-z][\w.-]*):[A-Za-z]", static)) == _TEMPLATE_PREFIXES


def test_sparql_keeps_the_prefixes_of_named_graphs_declared(tmp_path):
    """Named graphs are written as given, so the prefixes they use stay declared beside the planned names."""
    path = _write(tmp_path, "schema_org_alias")
    graphs = ["sdo:graph1", "ex:graph2"]
    off, on = (SparqlGenerator(path, named_graphs=graphs, normalize_prefixes=n).serialize() for n in (False, True))
    assert "sdo:graph1" in on
    assert _prefix_lines(on)["sdo"] == _prefix_lines(on)["schema"] == SCHEMA_ORG
    assert _sparql_meaning(on) == _sparql_meaning(off)


@pytest.mark.parametrize("schema", ["linkml_issue_388.yaml", "not_required.yaml"])
def test_sparql_writes_the_same_queries_and_leaves_its_input(input_path, monkeypatch, schema):
    """Attributes of one name in several classes: computing the plan fills the view's caches, and the
    generator's working copy of the view must not be served from them, or it rewrites the input."""
    import copy

    from linkml.generators import sparqlgen

    def attributes(view: SchemaView) -> dict[str, list[str]]:
        return {name: sorted(cls.attributes) for name, cls in view.all_classes().items()}

    inputs = []
    monkeypatch.setattr(sparqlgen, "deepcopy", lambda view: inputs.append(view) or copy.deepcopy(view))
    off, on = (SparqlGenerator(input_path(schema), normalize_prefixes=n) for n in (False, True))
    assert on.queries.keys() == off.queries.keys()
    assert _sparql_names(on.serialize()) == _sparql_names(off.serialize())
    assert any(attributes(SchemaView(input_path(schema))).values())
    for view in inputs:
        assert attributes(view) == attributes(SchemaView(input_path(schema)))


def _iris(meaning: Any) -> set[str]:
    """Every IRI or expanded string in the meaning of a document."""
    if isinstance(meaning, Graph):
        return {str(term) for triple in meaning for term in triple}
    if isinstance(meaning, dict):
        return set().union(*(_iris(key) | _iris(value) for key, value in meaning.items()))
    if isinstance(meaning, list | tuple):
        return set().union(*(_iris(value) for value in meaning))
    return {meaning} if isinstance(meaning, str) else set()


def _unwritten_namespaces(path: str) -> set[str]:
    """The namespaces of the prefixes that only an import declares and the plan leaves out as unused."""
    sv = SchemaView(path)
    written = set(written_prefixes(sv).values())
    return set(_schema_namespaces(path).values()) - written


ALL_DOCUMENTS = (
    DOCUMENTS
    | RDF_VARIANTS
    | {
        "owl-type-objects": _rdf_document(OwlSchemaGenerator, "ttl", "turtle", type_objects=True),
        "owl-no-mergeimports": _rdf_document(OwlSchemaGenerator, "ttl", "turtle", mergeimports=False),
    }
)


@pytest.mark.parametrize("case", sorted(CASES))
@pytest.mark.parametrize(
    "document", [pytest.param(d, marks=pytest.mark.network) if d == "shex-rdf" else d for d in sorted(ALL_DOCUMENTS)]
)
def test_no_document_writes_a_namespace_the_plan_leaves_out(tmp_path, document, case):
    """The plan treats a prefix that only an import declares as unused when no element is written with
    its namespace; no generator then writes an IRI of that namespace, with or without the option."""
    doc = ALL_DOCUMENTS[document]
    path = _write(tmp_path, case)
    unwritten = _unwritten_namespaces(path)
    assert SCHEMA_ORG_HTTP in unwritten or case in {
        "http_and_https_schema_org",
        "imported_name_in_use",
        "conventional_http_schema_org",
    }
    for normalize in (False, True):
        iris = _iris(doc.meaning(doc.produce(path, normalize, tmp_path)))
        assert not {iri for iri in iris for namespace in unwritten if iri.startswith(namespace)}


@pytest.mark.parametrize("case", sorted(CASES))
@pytest.mark.parametrize("flags", sorted(CONTEXT_FLAGS))
def test_no_context_defines_a_namespace_the_plan_leaves_out(tmp_path, flags, case):
    path = _write(tmp_path, case)
    unwritten = _unwritten_namespaces(path)
    for normalize in (False, True):
        context = _context(path, normalize, **CONTEXT_FLAGS[flags])
        iris = set(_context_prefixes(context).values()) | {str(iri) for iri in _expanded_terms(context)}
        assert not {iri for iri in iris for namespace in unwritten if iri.startswith(namespace)}


@pytest.mark.parametrize("base_normalized", [False, True])
@pytest.mark.parametrize("exclude", ["exclude_imports", "exclude_external_imports"])
def test_context_of_an_importer_leaves_a_name_its_import_uses(tmp_path, base_normalized, exclude):
    """An import's context defines ``prov`` for the namespace its class is in. The importer's context,
    without the imported elements, does not redefine it, so data that names both contexts and writes
    ``prov:`` keeps its meaning."""
    module, schema = (str(tmp_path / name) for name in ("module.yaml", "schema.yaml"))
    _write(tmp_path, "import_uses_a_name")
    expected_contexts = [_context(module, False), _context(schema, False, **{exclude: True})]
    contexts = [_context(module, base_normalized), _context(schema, True, **{exclude: True})]
    assert _context_prefixes(contexts[0])["prov"] == NOT_PROV
    assert _context_prefixes(contexts[1]).get("prov", NOT_PROV) == NOT_PROV
    terms = _terms(expected_contexts[0]) | _terms(expected_contexts[1])
    declared = sorted(_context_prefixes(expected_contexts[0]) | _context_prefixes(expected_contexts[1]))
    expected = _data_graph(expected_contexts, terms, declared, [])
    assert isomorphic(_data_graph(contexts, terms, declared, []), expected)


@pytest.mark.parametrize(
    "prefixes,taken,expected",
    [
        ({"sdo": SCHEMA_ORG}, set(), {"sdo": "schema"}),
        ({"schema": SCHEMA_ORG}, set(), {}),
        ({"ex": "http://example.org/"}, set(), {}),
        ({"sdo": SCHEMA_ORG, "schema": SCHEMA_ORG}, set(), {"sdo": "schema"}),
        ({"sdo": SCHEMA_ORG, "sdohttp": SCHEMA_ORG_HTTP}, set(), {}),
        ({"sdo": SCHEMA_ORG, "schema": "http://example.org/s/"}, set(), {}),
        ({"sdo": SCHEMA_ORG}, {"schema"}, {}),
        ({"dc": DC_TERMS, "dce": DC_ELEMENTS}, set(), {"dc": "dcterms"}),
        ({"FOAF": FOAF}, set(), {"FOAF": "foaf"}),
    ],
    ids=[
        "alias",
        "conventional",
        "unknown",
        "alias_and_conventional",
        "two_namespaces",
        "name_declared_elsewhere",
        "name_taken",
        "declared_name_stays",
        "case_only",
    ],
)
def test_prefix_renames(prefixes, taken, expected):
    assert prefix_renames(prefixes, taken) == expected


def test_document_prefixes_rename_only_declared_names():
    """A document renames the prefixes it declares, not one that only the plan knows."""
    plan = Converter(
        [
            Record(prefix="schema", uri_prefix=SCHEMA_ORG, prefix_synonyms=["sdo"]),
            Record(prefix="bibo", uri_prefix=BIBO, prefix_synonyms=["mybibo"]),
        ]
    )
    document = document_prefixes({"sdo": SCHEMA_ORG, "ex": "http://example.org/"}, plan)
    assert {r.prefix: r.uri_prefix for r in document.records} == {"schema": SCHEMA_ORG, "ex": "http://example.org/"}
    assert document.standardize_prefix("mybibo") is None


@pytest.mark.parametrize(
    "declared,used,expected",
    [
        # the alias is in use and still renamed: the name it gets is free
        ({"sdo": SCHEMA_ORG}, {"sdo"}, {"schema": SCHEMA_ORG}),
        # the document writes ``schema`` without declaring it: no namespace gets that name
        ({"sdo": SCHEMA_ORG}, {"sdo", "schema"}, {"sdo": SCHEMA_ORG}),
        # the document declares and writes ``schema`` for another namespace: both keep their names
        (
            {"sdo": SCHEMA_ORG, "schema": SCHEMA_ORG_HTTP},
            {"sdo", "schema"},
            {"sdo": SCHEMA_ORG, "schema": SCHEMA_ORG_HTTP},
        ),
        # it declares ``schema`` for another namespace without writing it: the declaration goes
        ({"sdo": SCHEMA_ORG, "schema": SCHEMA_ORG_HTTP}, {"sdo"}, {"schema": SCHEMA_ORG}),
    ],
    ids=["alias_in_use", "name_written_undeclared", "name_in_use_for_another_namespace", "name_declared_unused"],
)
def test_document_prefixes_keep_what_the_used_prefixes_denote(declared, used, expected):
    plan = Converter([Record(prefix="schema", uri_prefix=SCHEMA_ORG, prefix_synonyms=["sdo"])])
    document = document_prefixes(declared, plan, used)
    assert {r.prefix: r.uri_prefix for r in document.records} == expected
    for prefix in used & declared.keys():
        assert document.expand(f"{prefix}:x") == declared[prefix] + "x"


def test_standardize_prefix_leaves_absolute_iris_alone():
    """A suffix starting with ``//`` makes a value an absolute IRI, not a compact one (JSON-LD 1.1 §4.1.5)."""
    converter = Converter([Record(prefix="web", uri_prefix="http://example.org/", prefix_synonyms=["http"])])
    assert standardize_prefix("http://schema.org/Person", converter) == "http://schema.org/Person"
    assert standardize_prefix("http:Person", converter) == "web:Person"


def test_added_preferred_prefixes_skip_terms_and_other_namespaces():
    plan = Converter([Record(prefix="schema", uri_prefix=SCHEMA_ORG, prefix_synonyms=["sdo"])])
    assert not added_preferred_prefixes(plan, {"sdo": SCHEMA_ORG}, terms={"schema"}).records
    assert not added_preferred_prefixes(plan, {"sdo": SCHEMA_ORG, "schema": SCHEMA_ORG_HTTP}).records


# ── Where the names come from ─────────────────────────────────────────


@pytest.mark.parametrize(
    "namespace,expected",
    [
        ("http://www.opengis.net/ont/geosparql#", "geo"),
        (SCHEMA_ORG, "schema"),
        ("https://www.w3.org/2003/01/geo/wgs84_pos#", "wgs"),
        (SCHEMA_ORG_HTTP, "schema"),
        ("http://www.w3.org/ns/shacl#", "sh"),
        (DC_ELEMENTS, "dc"),
    ],
)
def test_well_known_prefix_map_names(namespace, expected):
    assert well_known_prefix_map()[namespace] == expected


def test_well_known_prefix_map_uses_curated_sources_only():
    """The names are those of prefixmaps' curated ``linked_data`` context and of rdflib; no name of
    another registry, such as prefix.cc's ``ex`` for http://example.org/."""
    curated = {rec.namespace: rec.prefix for rec in load_context("linked_data").prefix_expansions}
    rdflib_map = {str(ns): str(pfx) for pfx, ns in Graph(bind_namespaces="rdflib").namespaces() if str(pfx)}
    wk = well_known_prefix_map()
    assert wk == {**curated, **rdflib_map}
    assert "http://example.org/" not in wk


def test_well_known_prefix_map_returns_a_copy():
    well_known_prefix_map()["http://never-in-any-real-prefix-map.test/"] = "test"
    assert "http://never-in-any-real-prefix-map.test/" not in well_known_prefix_map()


# ── Command line ──────────────────────────────────────────────────────

OFFERING = ["owl", "shacl", "shex", "sparql", "yarrrml", "sssom", "jsonld-context"]


@pytest.mark.parametrize("command", OFFERING)
def test_cli_applies_the_option(command, tmp_path):
    path = _write(tmp_path, "prov_alias")
    out = tmp_path / "out"
    extra = {"sssom": ["-o", str(out)], "sparql": ["-d", str(out)]}.get(command, [])
    runner = CliRunner()
    outputs = {}
    for flag in ("--normalize-prefixes", "--no-normalize-prefixes", None):
        args = ["generate", command, *extra, *([flag] if flag else []), path]
        result = runner.invoke(linkml_cli, args)
        assert result.exit_code == 0, result.output
        if command == "sssom":
            outputs[flag] = out.read_text(encoding="utf-8")
        elif command == "sparql":
            outputs[flag] = "".join(f.read_text(encoding="utf-8") for f in sorted(out.glob("*.rq")))
        else:
            outputs[flag] = result.output
    assert outputs["--no-normalize-prefixes"] == outputs[None]
    assert re.search(r"\bprov:\w", outputs["--normalize-prefixes"])
    assert not re.search(r"\bprov:\w", outputs[None])


@pytest.mark.parametrize("command", ["prefix-map", "rdf", "jsonld", "python", "pydantic", "json-schema"])
def test_cli_rejects_the_option_where_names_are_data_or_api(command, tmp_path):
    """A prefix map gives each namespace one name, the schema's; gen-rdf and gen-jsonld write CURIEs as
    literal data; gen-python and gen-pydantic make prefix names part of the generated code; gen-json-schema
    writes none."""
    path = _write(tmp_path, "prov_alias")
    result = CliRunner().invoke(linkml_cli, ["generate", command, "--normalize-prefixes", path])
    assert result.exit_code == 2 and "No such option" in result.output
