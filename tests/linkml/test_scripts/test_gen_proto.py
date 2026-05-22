"""Tests for ``gen-proto`` / ``ProtoGenerator``.

Covers the helpers in isolation plus end-to-end assertions for the eleven
defects fixed in the proto generator overhaul (see ``ISSUE.md``):

  1.  Bare ``package`` line
  2.  Field number 0 / schema mutation via ``slot.rank = 0``
  3.  Missing ``;`` on field statements
  4.  LinkML built-in types emitted verbatim instead of proto3 scalars
  5.  Range references in lcamelcase (don't match declared CamelCase names)
  6.  Enums referenced but never declared
  7.  Reserved field-number range 19000-19999 not skipped
  8.  Identifiers violating the proto3 style guide
  9.  Mixin / abstract / slot-less classes silently dropped
  10. Enum without ``_UNSPECIFIED = 0`` first value
  11. No protoc-compile coverage at all

The snapshot test continues to act as the aggregate regression baseline.
"""

import re
import subprocess
import sys
import textwrap

import pytest
from click.testing import CliRunner

from linkml.generators.protogen import (
    ProtoGenerator,
    _to_proto_ident,
    _to_upper_snake,
    cli,
)
from tests.conftest import KITCHEN_SINK_PATH

# ---------------------------------------------------------------------------
# Existing baseline tests
# ---------------------------------------------------------------------------


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate proto representation of LinkML model" in result.output


def test_metamodel(snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, [KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == snapshot("genproto/meta.proto")


# ---------------------------------------------------------------------------
# Helper-level unit tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("foo", "foo"),
        ("FooBar", "FooBar"),
        ("foo bar", "foo_bar"),
        ("a b c", "a_b_c"),
        # collapse consecutive underscores (no `__`)
        ("foo__bar", "foo_bar"),
        ("foo___bar", "foo_bar"),
        # `_` immediately before a digit gets an `N` inserted (no `_<digit>`),
        # non-destructively so `foo_2bar` stays distinct from `foo2bar`
        ("foo_2bar", "foo_N2bar"),
        ("foo___2bar", "foo_N2bar"),
        ("foo2bar", "foo2bar"),
        # strip leading/trailing underscores
        ("_foo", "foo"),
        ("foo_", "foo"),
        ("__foo__", "foo"),
        # leading digit gets an `N` prefix (not `_`)
        ("2foo", "N2foo"),
        # empty / non-identifier input falls back to `N`
        ("", "N"),
        ("@@", "N"),
        ("   ", "N"),
    ],
)
def test_to_proto_ident_follows_style_guide(raw, expected):
    """Every identifier produced must obey the proto3 style guide: no leading
    or trailing ``_``, no ``__``, and no ``_`` immediately followed by a digit."""
    assert _to_proto_ident(raw) == expected


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("foo", "FOO"),
        ("foo bar", "FOO_BAR"),
        ("FooBar", "FOO_BAR"),  # CamelCase splits at word boundaries
        ("fooBar", "FOO_BAR"),
        ("2foo", "N2FOO"),
        ("", "N"),
    ],
)
def test_to_upper_snake_for_enum_values(raw, expected):
    assert _to_upper_snake(raw) == expected


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("kitchen_sink", "kitchen_sink"),
        ("biolink-model", "biolink_model"),
        ("FooBar", "foobar"),  # lower-cased
        ("foo__bar", "foo_bar"),  # consecutive `_` collapsed
        ("foo_2bar", "foo_n2bar"),  # `_` before digit gets `N` inserted (lower-cased)
        ("foo2bar", "foo2bar"),  # stays distinct from foo_2bar
        ("foo.bar", "foo.bar"),  # dotted package preserved
        ("2foo", None),  # leading digit -> None
        ("", None),
        ("@@", None),  # no identifier chars -> None
    ],
)
def test_sanitise_proto_package(raw, expected):
    assert ProtoGenerator._sanitise_proto_package(raw) == expected


@pytest.mark.parametrize(
    "start,used,expected",
    [
        (1, set(), 1),  # input is free, return it
        (1, {1, 2}, 3),  # walk past used
        (5, {5, 6, 7}, 8),  # walk past a run
        (19000, set(), 20000),  # skip the reserved range entirely
        (19500, set(), 20000),  # mid-reserved -> jump out
        (18999, {18999}, 20000),  # used edge then reserved range
    ],
)
def test_next_field_number_skips_used_and_reserved(start, used, expected):
    """``_next_field_number`` must avoid both already-claimed numbers and the
    proto3-reserved range 19000-19999."""
    assert ProtoGenerator._next_field_number(start, used) == expected


# ---------------------------------------------------------------------------
# End-to-end behaviour against small inline schemas
# ---------------------------------------------------------------------------


def _schema(*, name: str = "min_schema", body: str) -> str:
    """Build a minimal valid LinkML schema YAML with *body* appended.

    The schema-loader requires ``default_prefix`` to be present in the
    ``prefixes`` map, so we keep the boilerplate in one place. *body* is
    appended verbatim — it must already be left-aligned.
    """
    header = textwrap.dedent(
        f"""
        id: https://example.com/{name}
        name: {name}
        prefixes:
          linkml: https://w3id.org/linkml/
          ex: https://example.com/
        default_prefix: ex
        default_range: string
        imports:
          - linkml:types
        """
    ).strip()
    return header + "\n" + body


MIN_SCHEMA = _schema(
    body=textwrap.dedent(
        """
        classes:
          Person:
            attributes:
              id:
                identifier: true
              name:
                required: true
              age:
                range: integer
              alive:
                range: boolean
              status:
                range: Status
        enums:
          Status:
            permissible_values:
              ACTIVE:
              INACTIVE:
        """
    ).strip(),
)


def _gen(yaml_text: str, tmp_path) -> str:
    """Write ``yaml_text`` to a temp file, invoke ``gen-proto``, return its stdout."""
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(yaml_text)
    result = CliRunner().invoke(cli, [str(schema_path)])
    assert result.exit_code == 0, result.output
    return result.output


def test_header_has_syntax_and_sanitised_package(tmp_path):
    out = _gen(MIN_SCHEMA, tmp_path)
    assert out.startswith('syntax = "proto3";')
    assert "package min_schema;" in out


def test_no_bare_package_line(tmp_path):
    """Defect #1: the pre-fix output had a bare ``package`` line with no value."""
    out = _gen(MIN_SCHEMA, tmp_path)
    assert "\npackage\n" not in out
    assert "package ;" not in out


def test_package_omitted_when_name_unsanitisable(tmp_path):
    """If ``schema.name`` cannot yield a valid identifier, omit the package line.

    Constructed via ``_sanitise_proto_package`` directly because the LinkML
    schema-loader rejects un-prefix-mapped names — so we can't easily ship a
    schema named e.g. ``2bad`` end-to-end. The end-to-end behaviour is
    exercised by the package-omission branch of ``generate_header``, which
    only triggers when ``_sanitise_proto_package`` returns None.
    """
    assert ProtoGenerator._sanitise_proto_package("2bad") is None
    assert ProtoGenerator._sanitise_proto_package("@@") is None


def test_dotted_package_preserved(tmp_path):
    """Dotted schema names produce dotted proto packages (phenopackets-style)."""
    yaml_text = MIN_SCHEMA.replace("name: min_schema", "name: org.example.min")
    out = _gen(yaml_text, tmp_path)
    assert "package org.example.min;" in out


def test_no_field_number_zero(tmp_path):
    """Defect #2: pre-fix every field had ``= 0`` (forbidden in proto3).

    Enum value lines legitimately use ``= 0`` for the UNSPECIFIED sentinel —
    we filter those out by matching only lowercase-prefixed identifiers, which
    are field names (proto3 fields are snake/lcamelCase; enum values are UPPER).
    """
    out = _gen(MIN_SCHEMA, tmp_path)
    bad = re.findall(
        r"^\s+(?:repeated\s+)?\S+\s+[a-z]\w*\s*=\s*0\s*;?\s*$",
        out,
        re.MULTILINE,
    )
    assert not bad, f"field declarations with `= 0`: {bad!r}"


def test_field_statements_end_with_semicolon(tmp_path):
    """Defect #3: pre-fix field statements were emitted without trailing ``;``."""
    out = _gen(MIN_SCHEMA, tmp_path)
    missing = re.findall(r"^\s+\S+\s+[a-z]\w*\s*=\s*\d+\s*$", out, re.MULTILINE)
    assert not missing, f"field lines missing `;`: {missing!r}"


@pytest.mark.parametrize(
    "linkml_range,proto_scalar",
    [
        ("string", "string"),
        ("integer", "int32"),
        ("boolean", "bool"),
        ("float", "float"),
        ("double", "double"),  # name override — LinkML's `double` shares base=float
        ("decimal", "string"),  # proto3 has no decimal
        ("date", "string"),  # proto3 has no date
        ("datetime", "string"),
        ("uri", "string"),
        ("uriorcurie", "string"),
    ],
)
def test_linkml_builtin_types_map_to_proto_scalars(linkml_range, proto_scalar, tmp_path):
    """Defect #4: LinkML built-in types must be mapped to proto3 scalars,
    not emitted verbatim. ``integer`` -> ``int32``, ``boolean`` -> ``bool``, etc."""
    yaml_text = _schema(
        name="types_schema",
        body=textwrap.dedent(
            f"""
            classes:
              Holder:
                attributes:
                  value:
                    range: {linkml_range}
            """
        ).strip(),
    )
    out = _gen(yaml_text, tmp_path)
    assert f"{proto_scalar} value =" in out, out


def test_derived_double_type_maps_to_proto_double(tmp_path):
    """A user-defined type ``typeof: double`` must resolve to proto ``double``,
    even though LinkML's ``double`` shares ``base: float`` with ``float``.

    Exercises the name-override lookup in ``_proto_scalar_for_type``.
    """
    yaml_text = _schema(
        name="derived_double_schema",
        body=textwrap.dedent(
            """
            classes:
              Holder:
                attributes:
                  value:
                    range: Coordinate64
            types:
              Coordinate64:
                typeof: double
            """
        ).strip(),
    )
    out = _gen(yaml_text, tmp_path)
    assert "double value =" in out


def test_class_reference_uses_camelcase(tmp_path):
    """Defect #5: references to messages/enums must match declared CamelCase
    names. Pre-fix the generator used lcamelcase, producing dangling references."""
    out = _gen(MIN_SCHEMA, tmp_path)
    assert "Status status =" in out
    # CamelCase reference, NOT lcamelcase (`status status` would be a problem
    # only because the type matches the field name; check the declaration too).
    assert "enum Status {" in out


def test_enum_block_emitted_with_unspecified_first(tmp_path):
    """Defect #6 + #10: enums must be declared (not just referenced) and the
    first value must be ``<NAME>_UNSPECIFIED = 0`` per proto3 best practice."""
    out = _gen(MIN_SCHEMA, tmp_path)
    assert "enum Status {" in out
    assert "STATUS_UNSPECIFIED = 0;" in out
    # Real permissible values shift to start at 1
    assert "STATUS_ACTIVE = 1;" in out
    assert "STATUS_INACTIVE = 2;" in out


def test_enum_values_dedupe_with_letter_suffix(tmp_path):
    """When two permissible values sanitise to the same identifier, the suffix
    must be ``_V<n>`` (letter then digit), not ``_<n>`` — to comply with the
    proto3 style guide rule that underscore must be followed by a letter."""
    yaml_text = _schema(
        name="dup_schema",
        body=textwrap.dedent(
            """
            classes:
              Holder:
                attributes:
                  value:
                    range: Dup
            enums:
              Dup:
                permissible_values:
                  "a b":
                  "a-b":     # sanitises to the same identifier as "a b"
            """
        ).strip(),
    )
    out = _gen(yaml_text, tmp_path)
    # First instance gets the plain name, second gets a `_V2` suffix.
    assert "DUP_A_B = 1;" in out
    assert "DUP_A_B_V2 = 2;" in out


def test_mixin_class_emitted_so_references_resolve(tmp_path):
    """Defect #9: mixin classes must be emitted as messages so that any field
    referencing them resolves at protoc time."""
    yaml_text = _schema(
        name="mix_schema",
        body=textwrap.dedent(
            """
            classes:
              HasName:
                mixin: true
                attributes:
                  name:
                    range: string
              Container:
                attributes:
                  item:
                    range: HasName
            """
        ).strip(),
    )
    out = _gen(yaml_text, tmp_path)
    assert "message HasName {" in out
    assert "HasName item =" in out


def test_abstract_class_emitted_so_references_resolve(tmp_path):
    """Defect #9: abstract classes must also be emitted (proto3 has no abstract)."""
    yaml_text = _schema(
        name="abs_schema",
        body=textwrap.dedent(
            """
            classes:
              NamedThing:
                abstract: true
                attributes:
                  id:
                    identifier: true
              Container:
                attributes:
                  item:
                    range: NamedThing
            """
        ).strip(),
    )
    out = _gen(yaml_text, tmp_path)
    assert "message NamedThing {" in out
    assert "NamedThing item =" in out


def test_slot_less_class_emitted_as_empty_message(tmp_path):
    """Defect #9: concrete classes with no slots must still emit ``message X {}``
    so that any field referencing them resolves."""
    yaml_text = _schema(
        name="empty_schema",
        body=textwrap.dedent(
            """
            classes:
              Empty:
                description: a class with no slots
              Holder:
                attributes:
                  one:
                    range: Empty
            """
        ).strip(),
    )
    out = _gen(yaml_text, tmp_path)
    assert "message Empty {" in out
    assert "Empty one =" in out


def test_explicit_rank_honoured_and_collisions_skipped(tmp_path):
    """Field numbers from ``slot.rank`` are pinned; auto-assigned numbers skip
    over the pinned ones to keep numbers unique within the message."""
    yaml_text = _schema(
        name="rank_schema",
        body=textwrap.dedent(
            """
            classes:
              Item:
                attributes:
                  a:
                    range: string
                  b:
                    range: string
                    rank: 5
                  c:
                    range: string
                  d:
                    range: string
                    rank: 7
                  e:
                    range: string
            """
        ).strip(),
    )
    out = _gen(yaml_text, tmp_path)
    # Explicit ranks honoured exactly
    assert "string b = 5;" in out
    assert "string d = 7;" in out
    # Auto-assigned numbers: 1, 2, 3 (none collide with {5, 7})
    assert "string a = 1;" in out
    assert "string c = 2;" in out
    assert "string e = 3;" in out


def test_repeated_emitted_for_multivalued(tmp_path):
    """Multivalued slots produce ``repeated`` proto fields."""
    yaml_text = _schema(
        name="many_schema",
        body=textwrap.dedent(
            """
            classes:
              Person:
                attributes:
                  aliases:
                    range: string
                    multivalued: true
            """
        ).strip(),
    )
    out = _gen(yaml_text, tmp_path)
    assert "repeated string aliases =" in out


# ---------------------------------------------------------------------------
# Field naming convention — proto3 style guide requires snake_case
# https://protobuf.dev/programming-guides/style/#message-and-field-names
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "slot_name,expected_field",
    [
        ("phenotypic features", "phenotypic_features"),
        ("has news events", "has_news_events"),
        ("first name", "first_name"),
        ("birth_date", "birth_date"),  # already snake — leave alone
        ("id", "id"),
    ],
)
def test_slot_names_emitted_as_snake_case(slot_name, expected_field, tmp_path):
    """Slot names must be emitted in proto3-style snake_case, not lcamelcase.

    Pre-fix ``gen-proto`` used ``lcamelcase`` (e.g. ``phenotypicFeatures``),
    which violates the proto3 style guide.
    """
    yaml_text = _schema(
        name="snake_schema",
        body=textwrap.dedent(
            f"""
            classes:
              Holder:
                attributes:
                  "{slot_name}":
                    range: string
            """
        ).strip(),
    )
    out = _gen(yaml_text, tmp_path)
    assert f"string {expected_field} =" in out, out
    # And the lcamelcase form must NOT appear.
    if "_" in expected_field:
        from linkml_runtime.utils.formatutils import lcamelcase

        assert f" {lcamelcase(slot_name)} =" not in out


def test_slot_with_digit_segment_sanitised(tmp_path):
    """A slot name like ``slot with space 1`` produces ``slot_with_space1`` —
    ``_to_proto_ident`` drops the underscore-before-digit per the proto3 style
    guide (no ``_<digit>``)."""
    yaml_text = _schema(
        name="digit_schema",
        body=textwrap.dedent(
            """
            classes:
              ClassWithSpaces:
                attributes:
                  "slot with space 1":
                    range: string
            """
        ).strip(),
    )
    out = _gen(yaml_text, tmp_path)
    assert "string slot_with_space1 =" in out


# ---------------------------------------------------------------------------
# Slot-level descriptions emitted as `//` comments
# ---------------------------------------------------------------------------


def test_slot_description_emitted_as_comment(tmp_path):
    """``slot.description`` must be emitted as a ``//`` comment above the
    field, mirroring how ``cls.description`` is emitted above the message."""
    yaml_text = _schema(
        name="desc_schema",
        body=textwrap.dedent(
            """
            classes:
              Person:
                attributes:
                  name:
                    description: the person's full name
                    range: string
            """
        ).strip(),
    )
    out = _gen(yaml_text, tmp_path)
    assert "  // the person's full name\n  string name =" in out


def test_multiline_slot_description_emits_one_comment_per_line(tmp_path):
    """A multi-line ``slot.description`` becomes one ``//`` per line."""
    yaml_text = _schema(
        name="multi_desc_schema",
        body=textwrap.dedent(
            """
            classes:
              Person:
                attributes:
                  bio:
                    description: |-
                      first line
                      second line
                    range: string
            """
        ).strip(),
    )
    out = _gen(yaml_text, tmp_path)
    assert "  // first line\n  // second line\n  string bio =" in out


def test_slot_without_description_emits_no_comment(tmp_path):
    """When ``slot.description`` is unset the generator must NOT emit a stray
    ``//`` line — only annotated slots get a leading comment."""
    yaml_text = _schema(
        name="no_desc_schema",
        body=textwrap.dedent(
            """
            classes:
              Person:
                attributes:
                  name:
                    range: string
            """
        ).strip(),
    )
    out = _gen(yaml_text, tmp_path)
    # The Person message body should be exactly the one field line, no `//`.
    body = re.search(r"message Person \{(.*?)\}", out, re.DOTALL).group(1)
    assert "//" not in body


# ---------------------------------------------------------------------------
# Defect #11: protoc compilation
# ---------------------------------------------------------------------------


def test_kitchen_sink_proto_compiles_with_protoc(tmp_path):
    """The generated kitchen_sink proto must compile cleanly with ``protoc``.

    Uses ``grpc_tools.protoc`` (the same Python wrapper as ``uvx --from
    grpcio-tools``) so no system ``protoc`` binary is required. Skipped if
    ``grpc_tools`` isn't installed in the test environment.
    """
    pytest.importorskip("grpc_tools")

    result = CliRunner().invoke(cli, [KITCHEN_SINK_PATH])
    assert result.exit_code == 0

    proto_path = tmp_path / "kitchen_sink.proto"
    proto_path.write_text(result.output)
    desc_path = tmp_path / "kitchen_sink.desc"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "grpc_tools.protoc",
            f"--proto_path={tmp_path}",
            f"--descriptor_set_out={desc_path}",
            str(proto_path),
        ],
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert desc_path.exists() and desc_path.stat().st_size > 0
