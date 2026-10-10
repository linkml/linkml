"""Tests for gen-sssom: its output is a SSSOM 1.x mapping set written as SSSOM/TSV."""

import re
from pathlib import Path

import pytest
import yaml

from linkml.generators.sssomgen import (
    DEFAULT_MAPPING_JUSTIFICATION,
    MAPPING_JUSTIFICATIONS,
    SSSOM_PREFIXES,
    UNSPECIFIED_LICENSE,
    SSSOMGenerator,
)

SCHEMA_ID = "https://w3id.org/linkml/tests/kitchen_sink"

# Columns SSSOM 1.x requires in every mapping (sssom_schema: required slots of ``mapping``),
# plus the recommended subject_label.
REQUIRED_COLUMNS = {"subject_id", "subject_label", "predicate_id", "object_id", "mapping_justification"}


def read_sssom(path: str) -> tuple[dict, list[str], list[dict[str, str]]]:
    """Split an SSSOM/TSV file into its YAML header, its column names and its rows as dicts."""
    header_lines = []
    table_lines = []
    for line in Path(path).read_text().splitlines():
        if line.startswith("#"):
            header_lines.append(line[1:])
        else:
            table_lines.append(line)
    metadata = yaml.safe_load("\n".join(header_lines))
    columns = table_lines[0].split("\t")
    rows = [dict(zip(columns, line.split("\t"))) for line in table_lines[1:]]
    return metadata, columns, rows


def generate(schema_path: str, tmp_path: Path, **kwargs) -> tuple[dict, list[str], list[dict[str, str]]]:
    output_path = str(tmp_path / "test_sssom.tsv")
    SSSOMGenerator(schema_path, output=output_path, **kwargs).serialize()
    return read_sssom(output_path)


def triples(rows: list[dict[str, str]]) -> set[tuple[str, str, str]]:
    return {(row["subject_id"], row["predicate_id"], row["object_id"]) for row in rows}


@pytest.fixture
def schema_path(input_path) -> str:
    return str(input_path("kitchen_sink_sssom.yaml"))


@pytest.fixture
def sssom(schema_path, tmp_path) -> tuple[dict, list[str], list[dict[str, str]]]:
    return generate(schema_path, tmp_path)


def test_header_identifies_the_set(schema_path, sssom):
    metadata, _, _ = sssom
    with open(schema_path) as input_yaml:
        schema = yaml.safe_load(input_yaml)

    assert metadata["mapping_set_id"] == SCHEMA_ID + "/mappings"
    assert metadata["license"] == schema["license"]
    assert metadata["mapping_provider"] == SCHEMA_ID
    # Off by default, like every generator's generation_date, so output is byte-stable.
    assert "mapping_date" not in metadata
    # Pre-1.0 header keys the generator used to invent.
    assert "creator_id" not in metadata
    assert "mapping_tool" not in metadata


def test_curie_map_covers_every_prefix_used(schema_path, sssom):
    metadata, _, rows = sssom
    with open(schema_path) as input_yaml:
        schema = yaml.safe_load(input_yaml)
    curie_map = metadata["curie_map"]

    for prefix, expansion in schema["prefixes"].items():
        assert curie_map[prefix] == expansion
    for prefix, expansion in SSSOM_PREFIXES.items():
        assert curie_map[prefix] == expansion
    used = set()
    for row in rows:
        for column in ("subject_id", "predicate_id", "object_id", "mapping_justification"):
            value = row[column]
            if "://" not in value:
                used.add(value.split(":", 1)[0])
    assert used <= set(curie_map)
    # prov and core come from the imported core schema, not from the main schema's prefixes.
    assert {"prov", "core"} <= set(curie_map)


def test_columns_are_sssom_1(sssom):
    _, columns, rows = sssom
    assert "match_type" not in columns
    assert REQUIRED_COLUMNS <= set(columns)
    assert len(columns) == len(set(columns))
    assert rows
    assert {row["mapping_justification"] for row in rows} == {DEFAULT_MAPPING_JUSTIFICATION}
    for row in rows:
        for column in REQUIRED_COLUMNS:
            assert row[column]
        assert " " not in row["subject_id"]
        assert " " not in row["object_id"]


def test_class_uri_is_a_mapping_not_a_self_row(sssom):
    _, _, rows = sssom
    found = triples(rows)
    for subject, _, obj in found:
        assert subject != obj
    # Person declares class_uri: schema:Person; the mapping runs from its own URI to it.
    assert ("ks:Person", "skos:exactMatch", "schema:Person") in found
    assert ("ks:Person", "skos:exactMatch", "wd:Q215627") in found
    # agent, imported from core, declares class_uri: prov:Agent.
    assert ("core:Agent", "skos:exactMatch", "prov:Agent") in found
    subjects = {subject for subject, _, _ in found}
    assert "schema:Person" not in subjects
    assert "prov:Agent" not in subjects


def test_slot_uri_is_a_mapping_not_a_self_row(sssom):
    _, _, rows = sssom
    found = triples(rows)
    # The attribute ceo of Company declares slot_uri: schema:ceo.
    assert ("ks:ceo", "skos:exactMatch", "schema:ceo") in found
    assert ("schema:ceo", "skos:exactMatch", "schema:ceo") not in found
    # Slots without an explicit slot_uri map from their own URI only.
    assert ("ks:has_medical_history", "skos:broadMatch", "wd:Q309") in found
    assert ("ks:has_medical_history", "skos:exactMatch", "wd:Q15762873") in found


def test_labels(sssom):
    _, _, rows = sssom
    labels = {(row["subject_id"], row["object_id"]): row["subject_label"] for row in rows}
    # A slot's label is its alias (the attribute name), not the loader's mangled slot name.
    assert labels[("ks:ceo", "schema:ceo")] == "ceo"
    assert labels[("ks:Person", "schema:Person")] == "Person"
    assert labels[("ks:has_medical_history", "wd:Q309")] == "has medical history"


def test_permissible_values(sssom):
    _, _, rows = sssom
    found = triples(rows)
    by_object = {row["object_id"]: row for row in rows}
    # Every value is named under its enum, as gen-owl names a value without a meaning,
    # and labelled with its text.
    hire = by_object["CODE:hire"]
    assert hire["subject_id"] == "ks:EmploymentEventType#HIRE"
    assert hire["subject_label"] == "HIRE"
    assert hire["predicate_id"] == "skos:exactMatch"
    assert hire["subject_category"] == "EmploymentEventType"
    # A meaning is an exact mapping of the value, also when the value has nothing else.
    assert ("ks:EmploymentEventType#HIRE", "skos:exactMatch", "bizcodes:001") in found
    assert ("ks:EmploymentEventType#FIRE", "skos:exactMatch", "bizcodes:002") in found
    assert not {subject for subject, _, _ in found} & {"bizcodes:001", "bizcodes:002"}
    # A title wins over the text as the label.
    assert by_object["CODE:promotion"]["subject_label"] == "Promotion"
    assert by_object["bizcodes:003"]["subject_label"] == "Promotion"
    sibling = by_object["CODE:sibling"]
    assert sibling["subject_id"] == "ks:FamilialRelationshipType#SIBLING_OF"
    assert sibling["subject_label"] == "SIBLING_OF"
    assert sibling["predicate_id"] == "skos:closeMatch"


@pytest.mark.parametrize("justification", ["semapv:LexicalMatching", "semapv:MappingReview"])
def test_mapping_justification_option(schema_path, tmp_path, justification):
    _, _, rows = generate(schema_path, tmp_path, mapping_justification=justification)
    assert {row["mapping_justification"] for row in rows} == {justification}


def test_mapping_justification_must_be_admitted(schema_path, tmp_path):
    assert "semapv:AutomatedStringMatch" not in MAPPING_JUSTIFICATIONS
    with pytest.raises(ValueError, match="mapping_justification"):
        SSSOMGenerator(schema_path, output=str(tmp_path / "x.tsv"), mapping_justification="semapv:AutomatedStringMatch")


def test_mapping_set_id_option(schema_path, tmp_path):
    metadata, _, _ = generate(schema_path, tmp_path, mapping_set_id="https://example.org/sets/ks")
    assert metadata["mapping_set_id"] == "https://example.org/sets/ks"


def test_mapping_date_follows_generation_date_option(schema_path, tmp_path):
    metadata, _, _ = generate(schema_path, tmp_path, include_generation_date=True)
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(metadata["mapping_date"]))


MINIMAL_SCHEMA = """
id: https://example.org/minimal
name: minimal
{license_line}
prefixes:
  ex: https://example.org/minimal/
  schema: http://schema.org/
default_prefix: ex
classes:
  Person:
    exact_mappings:
      - schema:Person
"""


@pytest.mark.parametrize(
    "license_line,expected_license,comment_expected",
    [
        (
            "license: https://creativecommons.org/licenses/by/4.0/",
            "https://creativecommons.org/licenses/by/4.0/",
            False,
        ),
        ("license: CC0-1.0", "https://creativecommons.org/publicdomain/zero/1.0/", False),
        ("license: MIT", "https://spdx.org/licenses/MIT.html", False),
        ("license: Proprietary", UNSPECIFIED_LICENSE, True),
        ("", UNSPECIFIED_LICENSE, True),
    ],
)
def test_license_is_a_uri(tmp_path, license_line, expected_license, comment_expected):
    schema_path = tmp_path / "minimal.yaml"
    schema_path.write_text(MINIMAL_SCHEMA.format(license_line=license_line))
    metadata, _, rows = generate(str(schema_path), tmp_path)
    assert metadata["license"] == expected_license
    assert ("comment" in metadata) == comment_expected
    if comment_expected:
        assert "license" in metadata["comment"]
    assert triples(rows) == {("ex:Person", "skos:exactMatch", "schema:Person")}
