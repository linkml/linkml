"""Tests for ``--normalize-prefixes`` in every generator that writes prefix names.

The option writes the conventional name of a well-known namespace, such as ``schema`` for
``https://schema.org/`` where a schema declares ``sdo``, and every generator writes the same
name (:mod:`linkml.generators.common.prefixes`). Only names change:

- a self-contained document (OWL, SHACL, ShEx, SPARQL, YARRRML, SSSOM) means the same with and
  without the option, since prefixes are "not a formal part of the RDF data model"
  (RDF 1.1 Concepts §1.4; Turtle 1.1 §2.4);
- a JSON-LD context or a prefix map keeps every declared name and adds the conventional one, so
  data written against it expands the same (JSON-LD 1.1 §4.1.5).
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
    prefix_renames,
    standardize_prefix,
    well_known_prefix_map,
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
    # linkml:types declares ``schema`` for http://schema.org/, so https://schema.org/ keeps ``sdo``
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
        {SCHEMA_ORG: "sdo", SCHEMA_ORG_HTTP: "schema"},
    ),
    # an import declares ``prov`` for another namespace, although nothing uses it
    "import_holds_a_name": (
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
        {PROV: "w3prov"},
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
    """Data written with a prefix of the schema or its imports means the same under both contexts. Where
    the default context leaves such a prefix out and the normalized one defines it, the data gets the
    namespace the schema declares, with which LinkML expands it. Data written with the planned names
    means the same as with the declared ones."""
    path = _write(tmp_path, case)
    off, on = (_context(path, normalize, use_curies=use_curies) for normalize in (False, True))
    off_prefixes, on_prefixes = _context_prefixes(off), _context_prefixes(on)
    schema_prefixes = _schema_namespaces(path)
    terms, vocabulary = _terms(off), _vocabulary(path)
    plan = preferred_prefixes(SchemaView(path))
    for prefix in sorted(off_prefixes.keys() | schema_prefixes.keys()):
        expected_context = off
        if prefix not in off_prefixes and prefix in on_prefixes:
            assert on_prefixes[prefix] == schema_prefixes[prefix]
            expected_context = [{prefix: schema_prefixes[prefix]}, off]
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
    """A document renames the prefixes it declares; a CURIE with an undeclared prefix keeps its meaning."""
    plan = Converter(
        [
            Record(prefix="schema", uri_prefix=SCHEMA_ORG, prefix_synonyms=["sdo"]),
            Record(prefix="bibo", uri_prefix=BIBO, prefix_synonyms=["mybibo"]),
        ]
    )
    document = document_prefixes({"sdo": SCHEMA_ORG, "ex": "http://example.org/"}, plan)
    assert {r.prefix: r.uri_prefix for r in document.records} == {"schema": SCHEMA_ORG, "ex": "http://example.org/"}
    assert document.standardize_prefix("mybibo") is None


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
    """The names are those of prefixmaps' curated ``linked_data`` context and of rdflib, which wins;
    no name of a crowd-sourced registry, such as prefix.cc's ``alice`` for http://example.org/."""
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
