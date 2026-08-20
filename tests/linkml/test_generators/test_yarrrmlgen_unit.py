"""Dependency-free unit tests for the YARRRML generator.

The companion module :mod:`test_yarrrmlgen` materialises RDF with ``morph_kgc``
and validates it with ``pyshacl``; that whole module is skipped whenever the
optional ``morph_kgc`` dependency is absent (which is the default), so it
contributes almost no line coverage for
:mod:`linkml.generators.yarrrmlgen`.

These tests instead drive :class:`~linkml.generators.yarrrmlgen.YarrrmlGenerator`
directly on small in-memory schemas and assert on the structure of the emitted
YARRRML document. They have no heavyweight dependencies, run in well under a
second, and exercise every code path of the generator.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml
from click.testing import CliRunner

from linkml.generators.yarrrmlgen import (
    DEFAULT_ITERATOR,
    DEFAULT_SOURCE_JSON,
    YarrrmlGenerator,
    cli,
)

pytestmark = pytest.mark.yarrrml


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_schema(
    classes: dict[str, Any],
    *,
    slots: dict[str, Any] | None = None,
    enums: dict[str, Any] | None = None,
    prefixes: dict[str, str] | None = None,
    default_prefix: str | None = "ex",
    default_range: str | None = "string",
) -> str:
    """Assemble a minimal LinkML schema document as a YAML string.

    Keeping schema construction declarative (a dict dumped to YAML) keeps each
    test focused on the single feature it covers rather than on boilerplate.
    """
    if prefixes is None:
        prefixes = {
            "ex": "https://example.org/test#",
            "linkml": "https://w3id.org/linkml/",
        }
    schema: dict[str, Any] = {
        "id": "https://example.org/test",
        "name": "test",
        "prefixes": prefixes,
        "imports": ["linkml:types"],
    }
    if default_prefix is not None:
        schema["default_prefix"] = default_prefix
    if default_range is not None:
        schema["default_range"] = default_range
    if slots:
        schema["slots"] = slots
    if enums:
        schema["enums"] = enums
    schema["classes"] = classes
    return yaml.safe_dump(schema, sort_keys=False)


def _gen(schema: str, **kwargs: Any) -> YarrrmlGenerator:
    """Build a generator from an inline schema string."""
    return YarrrmlGenerator(schema, **kwargs)


def _mappings(schema: str, **kwargs: Any) -> dict[str, Any]:
    """Return the ``mappings`` block of the generated YARRRML document."""
    return _gen(schema, **kwargs).as_dict()["mappings"]


def _po_map(po: list[dict[str, Any]]) -> dict[str, Any]:
    """Index a predicate-object list by its predicate for easy assertions.

    Every predicate is unique within the small fixtures used here, so a plain
    dict keyed on ``p`` is an unambiguous view of the list. The guard fails loudly
    if a future fixture emits duplicate predicates rather than silently dropping one.
    """
    predicates = [entry["p"] for entry in po]
    assert len(predicates) == len(set(predicates)), f"duplicate predicate(s) in {predicates}"
    return {entry["p"]: entry["o"] for entry in po}


_SIMPLE_PERSON = _make_schema({"Person": {"attributes": {"id": {"identifier": True}, "name": {}}}})


# ---------------------------------------------------------------------------
# Source inference and constructor defaults
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("data.json~jsonpath", "data.json~jsonpath"),  # already has a "~" suffix
        ("data.json", "data.json~jsonpath"),  # .json -> jsonpath
        ("data.csv", "data.csv~csv"),  # .csv -> csv
        ("data.tsv", "data.tsv~csv"),  # .tsv -> csv
        ("DATA.JSON", "DATA.JSON~jsonpath"),  # suffix match is case-insensitive
        ("data.parquet", "data.parquet"),  # unknown suffix is left untouched
        ("s3://bucket/data.json~jsonpath", "s3://bucket/data.json~jsonpath"),
    ],
)
def test_infer_source_suffix(raw: str, expected: str) -> None:
    """``--source`` shorthand gains the right reference-formulation suffix."""
    gen = _gen(_SIMPLE_PERSON, source=raw)
    assert gen.source == expected


def test_default_source_is_json() -> None:
    """With no ``source`` the generator defaults to a JSONPath source."""
    gen = _gen(_SIMPLE_PERSON)
    assert gen.source == DEFAULT_SOURCE_JSON
    assert gen._is_json_source() is True


def test_default_iterator_without_tree_root() -> None:
    """Absent a tree root the iterator walks a top-level array (``$[*]``)."""
    gen = _gen(_SIMPLE_PERSON)
    assert gen.iterator_template == DEFAULT_ITERATOR


def test_iterator_is_root_when_schema_has_tree_root() -> None:
    """A ``tree_root`` class makes the default iterator the document root."""
    schema = _make_schema(
        {
            "Container": {
                "tree_root": True,
                "attributes": {"persons": {"range": "Person", "inlined": True, "multivalued": True}},
            },
            "Person": {"attributes": {"id": {"identifier": True}}},
        }
    )
    assert _gen(schema).iterator_template == "$"


def test_explicit_iterator_template_overrides_default() -> None:
    """An explicit ``iterator_template`` is used verbatim for the source."""
    gen = _gen(_SIMPLE_PERSON, iterator_template="$.records[*]")
    assert gen.iterator_template == "$.records[*]"
    assert gen.as_dict()["mappings"]["Person"]["sources"] == [["data.json~jsonpath", "$.records[*]"]]


def test_iterator_template_substitutes_class_name() -> None:
    """``{Class}`` in the iterator template is replaced with the class name."""
    gen = _gen(_SIMPLE_PERSON, iterator_template="$.{Class}[*]")
    assert gen.as_dict()["mappings"]["Person"]["sources"] == [["data.json~jsonpath", "$.Person[*]"]]


@pytest.mark.parametrize("source,expected", [("data.csv", "data.csv~csv"), ("data.parquet", "data.parquet")])
def test_non_json_source_emits_single_element_sources(source: str, expected: str) -> None:
    """Non-JSON sources are emitted without an iterator element."""
    gen = _gen(_SIMPLE_PERSON, source=source)
    assert gen._is_json_source() is False
    assert gen.as_dict()["mappings"]["Person"]["sources"] == [[expected]]


# ---------------------------------------------------------------------------
# Subject templates
# ---------------------------------------------------------------------------


def test_subject_uses_identifier_slot() -> None:
    """An identifier slot becomes the subject template."""
    m = _mappings(_make_schema({"Person": {"attributes": {"person_id": {"identifier": True}, "name": {}}}}))
    assert m["Person"]["s"] == "ex:$(person_id)"


def test_subject_uses_key_slot_when_no_identifier() -> None:
    """A ``key`` slot is used when no identifier is present."""
    m = _mappings(_make_schema({"Person": {"attributes": {"code": {"key": True}, "name": {}}}}))
    assert m["Person"]["s"] == "ex:$(code)"


def test_subject_omitted_for_class_without_identifier_or_key() -> None:
    """A class lacking id/key is a blank node — YARRRML omits the subject key."""
    m = _mappings(_make_schema({"Record": {"attributes": {"value": {}}}}))
    assert "s" not in m["Record"]


# ---------------------------------------------------------------------------
# Scalar / datatype predicate-objects
# ---------------------------------------------------------------------------


def test_scalar_slot_carries_datatype() -> None:
    """A typed scalar slot emits a value/datatype object."""
    m = _mappings(_make_schema({"Person": {"attributes": {"id": {"identifier": True}, "name": {}}}}))
    po = _po_map(m["Person"]["po"])
    assert po["a"] == "ex:Person"  # single rdf:type emitted as a scalar
    assert po["ex:name"] == {"value": "$(name)", "datatype": "xsd:string"}


def test_scalar_slot_with_enum_range_has_no_datatype() -> None:
    """An enum-ranged slot is neither an object nor a type, so no datatype."""
    schema = _make_schema(
        {"Person": {"attributes": {"id": {"identifier": True}, "status": {"range": "StatusEnum"}}}},
        enums={"StatusEnum": {"permissible_values": {"active": {}, "inactive": {}}}},
    )
    po = _po_map(_mappings(schema)["Person"]["po"])
    assert po["ex:status"] == "$(status)"


def test_slot_without_range_has_no_datatype() -> None:
    """A slot with no range at all also yields a bare value reference."""
    schema = _make_schema(
        {"Person": {"attributes": {"id": {"identifier": True}, "note": {}}}},
        default_range=None,
    )
    po = _po_map(_mappings(schema)["Person"]["po"])
    assert po["ex:note"] == "$(note)"


# ---------------------------------------------------------------------------
# Predicate resolution (slot_uri vs computed URI)
# ---------------------------------------------------------------------------


def test_top_level_slot_uri_is_used_as_predicate() -> None:
    """A ``slot_uri`` on a top-level slot definition becomes the predicate."""
    schema = _make_schema(
        {"Person": {"slots": ["id", "homepage"]}},
        slots={"id": {"identifier": True}, "homepage": {"slot_uri": "foaf:homepage"}},
        prefixes={
            "ex": "https://example.org/test#",
            "linkml": "https://w3id.org/linkml/",
            "foaf": "http://xmlns.com/foaf/0.1/",
        },
    )
    po = _po_map(_mappings(schema)["Person"]["po"])
    # the slot_uri becomes the predicate and the slot still carries its scalar payload
    assert po["foaf:homepage"] == {"value": "$(homepage)", "datatype": "xsd:string"}


def test_attribute_slot_uri_is_used_as_predicate() -> None:
    """A ``slot_uri`` declared inline on an attribute becomes the predicate."""
    schema = _make_schema(
        {"Person": {"attributes": {"id": {"identifier": True}, "name": {"slot_uri": "schema:name"}}}},
        prefixes={
            "ex": "https://example.org/test#",
            "linkml": "https://w3id.org/linkml/",
            "schema": "http://schema.org/",
        },
    )
    po = _po_map(_mappings(schema)["Person"]["po"])
    assert po["schema:name"] == {"value": "$(name)", "datatype": "xsd:string"}


# ---------------------------------------------------------------------------
# Object references (non-inlined): IRI links
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "multivalued,expected",
    [
        (False, {"value": "ex:$(employer)", "type": "iri"}),
        (True, [{"value": "ex:$(employer)", "type": "iri"}]),
    ],
)
def test_noninlined_reference_is_iri(multivalued: bool, expected: Any) -> None:
    """A non-inlined object slot links by IRI — a list of IRIs when multivalued."""
    employer = {"range": "Org", "inlined": False, "multivalued": multivalued}
    schema = _make_schema(
        {
            "Person": {"attributes": {"id": {"identifier": True}, "employer": employer}},
            "Org": {"attributes": {"org_id": {"identifier": True}}},
        }
    )
    po = _po_map(_mappings(schema)["Person"]["po"])
    assert po["ex:employer"] == expected


# ---------------------------------------------------------------------------
# Inlined objects with their own identifier: RML joins
# ---------------------------------------------------------------------------


def test_inlined_single_with_id_emits_join_and_child_mapping() -> None:
    """An inlined single object with its own id produces a join condition."""
    schema = _make_schema(
        {
            "Person": {"attributes": {"id": {"identifier": True}, "address": {"range": "Address", "inlined": True}}},
            "Address": {"attributes": {"address_id": {"identifier": True}, "city": {}}},
        }
    )
    m = _mappings(schema)
    po = _po_map(m["Person"]["po"])
    assert po["ex:address"] == {
        "mapping": "Address",
        "condition": {
            "function": "equal",
            "parameters": [["str1", "$(address.address_id)", "s"], ["str2", "$(address_id)", "o"]],
        },
    }
    # the child mapping uses its own id and iterates the nested object
    assert m["Address"]["s"] == "ex:$(address_id)"
    assert m["Address"]["sources"] == [["data.json~jsonpath", "$..address"]]


def test_inlined_multivalued_with_id_emits_join_list() -> None:
    """An inlined multivalued object with its own id joins over the array."""
    schema = _make_schema(
        {
            "Person": {
                "attributes": {
                    "id": {"identifier": True},
                    "addresses": {"range": "Address", "inlined": True, "multivalued": True},
                }
            },
            "Address": {"attributes": {"address_id": {"identifier": True}, "city": {}}},
        }
    )
    m = _mappings(schema)
    po = _po_map(m["Person"]["po"])
    assert po["ex:addresses"] == [
        {
            "mapping": "Address",
            "condition": {
                "function": "equal",
                "parameters": [["str1", "$(addresses[*].address_id)", "s"], ["str2", "$(address_id)", "o"]],
            },
        }
    ]
    assert m["Address"]["sources"] == [["data.json~jsonpath", "$..addresses[*]"]]


def test_inlined_single_without_id_synthesizes_subject_and_dotpath() -> None:
    """An id-less inlined child borrows its parent's id for subject and join."""
    schema = _make_schema(
        {
            "Person": {"attributes": {"id": {"identifier": True}, "address": {"range": "Address", "inlined": True}}},
            "Address": {"attributes": {"street": {}, "city": {}}},
        }
    )
    m = _mappings(schema)
    # the parent->child join falls back to the parent id on both sides
    po = _po_map(m["Person"]["po"])
    assert po["ex:address"] == {
        "mapping": "Address",
        "condition": {
            "function": "equal",
            "parameters": [["str1", "$(id)", "s"], ["str2", "$(id)", "o"]],
        },
    }
    # the child subject is synthesised from the parent id and the child iterates
    # at the parent level, reaching its own properties by dot notation
    assert m["Address"]["s"] == "ex:Address_$(id)"
    assert m["Address"]["sources"] == [["data.json~jsonpath", "$[*]"]]
    address_po = _po_map(m["Address"]["po"])
    assert address_po["ex:street"] == {"value": "$(address.street)", "datatype": "xsd:string"}
    assert address_po["ex:city"] == {"value": "$(address.city)", "datatype": "xsd:string"}


def test_inlined_without_id_and_no_parent_id_uses_bare_mapping() -> None:
    """When neither parent nor child has an id, the link is a bare mapping."""
    schema = _make_schema(
        {
            "Record": {"attributes": {"label": {}, "detail": {"range": "Detail", "inlined": True}}},
            "Detail": {"attributes": {"info": {}}},
        }
    )
    m = _mappings(schema)
    assert _po_map(m["Record"]["po"])["ex:detail"] == {"mapping": "Detail"}
    # neither class has an id, so both are blank nodes (subject key omitted)
    assert "s" not in m["Record"]
    assert "s" not in m["Detail"]


def test_po_list_multivalued_idless_inline_uses_bare_mapping_list() -> None:
    """Exercise the defensive multivalued bare-mapping branch directly.

    ``as_dict`` rejects a multivalued inlined slot whose range has no
    identifier, so this branch of ``_po_list_for_class`` is unreachable through
    the public API. We call the method directly (no mocking) to document and
    pin its behaviour.
    """
    schema = _make_schema(
        {
            "Record": {"attributes": {"items": {"range": "Item", "inlined": True, "multivalued": True}}},
            "Item": {"attributes": {"label": {}}},
        }
    )
    gen = _gen(schema)  # construction is fine; as_dict() is never called
    record = gen.schemaview.get_class("Record")
    po = _po_map(gen._po_list_for_class(record, inline_owners={}))
    assert po["ex:items"] == [{"mapping": "Item"}]


# ---------------------------------------------------------------------------
# Mixins and rdf:type
# ---------------------------------------------------------------------------


def test_mixin_adds_extra_type_and_mixin_class_is_skipped() -> None:
    """A mixin contributes a second rdf:type and yields no mapping of its own."""
    schema = _make_schema(
        {
            "NamedThing": {"mixin": True, "attributes": {"name": {}}},
            "Person": {"mixins": ["NamedThing"], "attributes": {"id": {"identifier": True}}},
        }
    )
    m = _mappings(schema)
    assert "NamedThing" not in m
    assert _po_map(m["Person"]["po"])["a"] == ["ex:Person", "ex:NamedThing"]


# ---------------------------------------------------------------------------
# Prefix handling
# ---------------------------------------------------------------------------


def test_user_prefixes_preserved_and_rdf_added() -> None:
    """Declared prefixes are carried through and rdf is always present."""
    px = _gen(_SIMPLE_PERSON).as_dict()["prefixes"]
    assert px["ex"] == "https://example.org/test#"
    assert px["linkml"] == "https://w3id.org/linkml/"
    assert px["rdf"] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#"


def test_default_example_prefix_added_when_no_user_prefix() -> None:
    """With only reserved prefixes and no default, an ``ex`` default is injected."""
    schema = _make_schema(
        {"Person": {"attributes": {"id": {"identifier": True}}}},
        prefixes={"linkml": "https://w3id.org/linkml/"},
        default_prefix=None,
    )
    gen = _gen(schema)
    # LinkML synthesises a (truthy) default_prefix from the schema IRI when none
    # is declared, so this fallback is unreachable via the public as_dict() API;
    # clear it to exercise the generator's own fallback logic in isolation.
    gen.schema.default_prefix = None
    px = gen._prefixes_with_defaults()
    assert px["ex"] == "https://example.org/default#"
    assert px["rdf"] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    assert gen.schema.default_prefix == "ex"


def test_default_prefix_falls_back_to_first_user_prefix() -> None:
    """The first non-reserved prefix becomes the default when none is declared.

    ``linkml`` is listed first so the fallback loop must skip a reserved prefix
    before settling on the user-defined ``foo``. This method is tested directly
    because the fallback branch is unreachable through the public ``as_dict``
    API: LinkML always synthesises a (truthy) ``default_prefix`` from the schema
    IRI, so the generator's ``if not self.schema.default_prefix`` guard never
    fires there. We null it out to exercise the fallback in isolation.
    """
    schema = _make_schema(
        {"Person": {"attributes": {"id": {"identifier": True}}}},
        prefixes={"linkml": "https://w3id.org/linkml/", "foo": "https://foo.example/#"},
        default_prefix=None,
    )
    gen = _gen(schema)
    gen.schema.default_prefix = None
    px = gen._prefixes_with_defaults()
    assert "ex" not in px
    assert px["foo"] == "https://foo.example/#"
    assert gen.schema.default_prefix == "foo"


def test_omitted_default_prefix_resolves_to_real_curie_prefix() -> None:
    """An omitted default_prefix is normalised to a declared prefix in mappings.

    LinkML synthesises default_prefix as the full schema IRI when it is omitted;
    the generator must emit a real CURIE prefix (here the sole user prefix
    ``foo``) in subject/predicate/type positions, never the raw IRI. Exercises
    the public ``as_dict`` path, complementing the isolated ``_prefixes_with_defaults``
    tests above.
    """
    schema = _make_schema(
        {"Person": {"attributes": {"id": {"identifier": True}, "name": {}}}},
        prefixes={"foo": "https://foo.example/#", "linkml": "https://w3id.org/linkml/"},
        default_prefix=None,
    )
    m = _mappings(schema)
    assert m["Person"]["s"] == "foo:$(id)"
    po = _po_map(m["Person"]["po"])
    assert po["a"] == "foo:Person"
    assert po["foo:id"] == {"value": "$(id)", "datatype": "xsd:string"}
    assert po["foo:name"] == {"value": "$(name)", "datatype": "xsd:string"}
    # no raw schema IRI leaks into a predicate position
    assert not any(str(predicate).startswith("http") for predicate in po)


def test_omitted_default_prefix_without_user_prefix_resolves_to_ex() -> None:
    """With no user prefix and no declared default, mappings fall back to ``ex``."""
    schema = _make_schema(
        {"Person": {"attributes": {"id": {"identifier": True}}}},
        prefixes={"linkml": "https://w3id.org/linkml/"},
        default_prefix=None,
    )
    m = _mappings(schema)
    assert m["Person"]["s"] == "ex:$(id)"
    assert _po_map(m["Person"]["po"])["a"] == "ex:Person"


# ---------------------------------------------------------------------------
# tree_root filtering
# ---------------------------------------------------------------------------


def test_tree_root_skips_unreferenced_top_level_classes() -> None:
    """With a tree root, only the root and inlined targets are mapped."""
    schema = _make_schema(
        {
            "Container": {
                "tree_root": True,
                "attributes": {"persons": {"range": "Person", "inlined": True, "multivalued": True}},
            },
            "Person": {"attributes": {"person_id": {"identifier": True}, "name": {}}},
            "Orphan": {"attributes": {"orphan_id": {"identifier": True}}},
        }
    )
    m = _mappings(schema)
    assert set(m) == {"Container", "Person"}
    assert m["Container"]["sources"] == [["data.json~jsonpath", "$"]]
    assert "s" not in m["Container"]  # id-less root container is a blank node
    assert m["Person"]["sources"] == [["data.json~jsonpath", "$..persons[*]"]]


# ---------------------------------------------------------------------------
# Validation errors
# ---------------------------------------------------------------------------


def test_error_noninlined_reference_without_identifier() -> None:
    """A non-inlined reference to an id-less class is rejected."""
    schema = _make_schema(
        {
            "Person": {"attributes": {"id": {"identifier": True}, "org": {"range": "Org", "inlined": False}}},
            "Org": {"attributes": {"name": {}}},
        }
    )
    with pytest.raises(ValueError, match="lacks an identifier"):
        _gen(schema).as_dict()


def test_error_multivalued_inlined_list_without_identifier() -> None:
    """A multivalued inlined list whose target lacks an id is rejected."""
    schema = _make_schema(
        {
            "Person": {
                "attributes": {
                    "id": {"identifier": True},
                    "addrs": {"range": "Addr", "inlined": True, "multivalued": True},
                }
            },
            "Addr": {"attributes": {"street": {}}},
        }
    )
    with pytest.raises(ValueError, match="inlined list"):
        _gen(schema).as_dict()


def test_error_idless_inline_class_with_multiple_owners() -> None:
    """An id-less inlined class shared by multiple owners is rejected."""
    schema = _make_schema(
        {
            "Person": {"attributes": {"id": {"identifier": True}, "addr": {"range": "Addr", "inlined": True}}},
            "Company": {"attributes": {"cid": {"identifier": True}, "addr": {"range": "Addr", "inlined": True}}},
            "Addr": {"attributes": {"street": {}}},
        }
    )
    with pytest.raises(ValueError, match="multiple owners"):
        _gen(schema).as_dict()


# ---------------------------------------------------------------------------
# Serialisation
# ---------------------------------------------------------------------------


def test_serialize_emits_flow_style_sources_and_round_trips() -> None:
    """``serialize`` renders sources in flow style and parses back losslessly."""
    gen = _gen(_SIMPLE_PERSON)
    expected = gen.as_dict()
    out = gen.serialize()
    # the source list renders in flow style (one bracketed line) rather than as a
    # block sequence — see FlowList / flow_list_representer. Assert structurally so
    # the test survives PyYAML spacing/quoting changes.
    source_line = next(line for line in out.splitlines() if "data.json~jsonpath" in line)
    assert source_line.lstrip().startswith("- [")
    assert "$[*]" in source_line
    assert yaml.safe_load(out) == expected


# ---------------------------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------------------------


@pytest.fixture
def schema_file(tmp_path: Path) -> Path:
    """Write the simple person schema to disk for CLI invocation."""
    path = tmp_path / "schema.yaml"
    path.write_text(_SIMPLE_PERSON, encoding="utf-8")
    return path


def test_cli_default(schema_file: Path) -> None:
    """The CLI emits a parseable YARRRML document with default options."""
    result = CliRunner().invoke(cli, [str(schema_file)])
    assert result.exit_code == 0, result.output
    doc = yaml.safe_load(result.output)
    assert doc["mappings"]["Person"]["sources"] == [["data.json~jsonpath", "$[*]"]]


def test_cli_with_source_option(schema_file: Path) -> None:
    """``--source`` flows through to the generated source shorthand."""
    result = CliRunner().invoke(cli, [str(schema_file), "--source", "data.csv"])
    assert result.exit_code == 0, result.output
    doc = yaml.safe_load(result.output)
    assert doc["mappings"]["Person"]["sources"] == [["data.csv~csv"]]


def test_cli_with_iterator_template_option(schema_file: Path) -> None:
    """``--iterator-template`` flows through to the generated iterator."""
    result = CliRunner().invoke(cli, [str(schema_file), "--iterator-template", "$.items[*]"])
    assert result.exit_code == 0, result.output
    doc = yaml.safe_load(result.output)
    assert doc["mappings"]["Person"]["sources"] == [["data.json~jsonpath", "$.items[*]"]]


# ---------------------------------------------------------------------------
# Defaulting and defensive edges
# ---------------------------------------------------------------------------


def test_object_reference_defaults_to_noninlined_when_inlined_unset() -> None:
    """An object slot with no explicit ``inlined`` and an identified range is
    treated as a non-inlined IRI reference (``inlined`` is left as ``None``)."""
    schema = _make_schema(
        {
            "Person": {"attributes": {"id": {"identifier": True}, "employer": {"range": "Org"}}},
            "Org": {"attributes": {"org_id": {"identifier": True}}},
        }
    )
    po = _po_map(_mappings(schema)["Person"]["po"])
    assert po["ex:employer"] == {"value": "ex:$(employer)", "type": "iri"}


def test_slot_usage_slot_uri_used_as_predicate() -> None:
    """A ``slot_uri`` added through ``slot_usage`` (absent on the base slot) is
    picked up from the induced slot."""
    schema = _make_schema(
        {"Person": {"slots": ["id", "name"], "slot_usage": {"name": {"slot_uri": "schema:name"}}}},
        slots={"id": {"identifier": True}, "name": {}},
        prefixes={
            "ex": "https://example.org/test#",
            "linkml": "https://w3id.org/linkml/",
            "schema": "http://schema.org/",
        },
    )
    po = _po_map(_mappings(schema)["Person"]["po"])
    # the slot_usage-induced slot_uri replaces — not supplements — the computed
    # ``ex:name`` predicate the base slot would otherwise produce
    assert po["schema:name"] == {"value": "$(name)", "datatype": "xsd:string"}
    assert "ex:name" not in po


def test_prefixes_defaulted_when_schema_declares_none() -> None:
    """With no declared prefixes, only the rdf and ex defaults are emitted.

    Reaches the empty-prefixes path directly: a loadable schema cannot omit the
    ``linkml`` prefix (the ``linkml:types`` import needs it), so the empty state
    is set up in isolation rather than through the public API.
    """
    gen = _gen(_SIMPLE_PERSON)
    gen.schema.prefixes = {}
    gen.schema.default_prefix = None
    px = gen._prefixes_with_defaults()
    assert px == {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "ex": "https://example.org/default#",
    }
    assert gen.schema.default_prefix == "ex"


def test_prefix_without_reference_is_skipped() -> None:
    """A prefix lacking a reference is dropped from the output prefix map."""
    schema = _make_schema(
        {"Person": {"attributes": {"id": {"identifier": True}}}},
        prefixes={
            "ex": "https://example.org/test#",
            "linkml": "https://w3id.org/linkml/",
            "bad": "",
        },
    )
    px = _gen(schema).as_dict()["prefixes"]
    assert "bad" not in px
    assert px["ex"] == "https://example.org/test#"


def test_mixin_uri_equal_to_class_uri_is_not_duplicated() -> None:
    """A mixin whose URI equals the class URI does not add a duplicate type."""
    schema = _make_schema(
        {
            "Shared": {"mixin": True, "class_uri": "ex:Common", "attributes": {"label": {}}},
            "Person": {"class_uri": "ex:Common", "mixins": ["Shared"], "attributes": {"id": {"identifier": True}}},
        }
    )
    assert _po_map(_mappings(schema)["Person"]["po"])["a"] == "ex:Common"
