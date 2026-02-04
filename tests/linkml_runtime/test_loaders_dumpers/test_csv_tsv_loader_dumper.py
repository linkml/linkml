import json
import logging
import os

import pytest
import unittest
from jsonasobj2 import as_json_obj

from linkml_runtime.dumpers import csv_dumper, json_dumper, tsv_dumper, yaml_dumper
from linkml_runtime.loaders import csv_loader, tsv_loader, yaml_loader
from linkml_runtime.utils.formatutils import remove_empty_items
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import as_json_object
from tests.linkml_runtime.test_loaders_dumpers.models.books_normalized import (
    Author,
    Review,
    Shop,
    Book,
    GenreEnum,
    BookSeries,
)
from tests.linkml_runtime.test_loaders_dumpers.models.table import Table, Row

logger = logging.getLogger(__name__)


ROOT = os.path.abspath(os.path.dirname(__file__))
INPUT_DIR = os.path.join(ROOT, "input")
OUTPUT_DIR = os.path.join(ROOT, "output")
MODEL_DIR = os.path.join(ROOT, "models")

SCHEMA = os.path.join(MODEL_DIR, "books_normalized.yaml")
DATA = os.path.join(INPUT_DIR, "books_normalized_01.yaml")
DATA2 = os.path.join(INPUT_DIR, "books_normalized_02.yaml")
OUTPUT = os.path.join(OUTPUT_DIR, "books_flattened.tsv")
OUTPUT2 = os.path.join(OUTPUT_DIR, "books_flattened_02.tsv")


TABLE_SCHEMA = os.path.join(MODEL_DIR, "table.yaml")
TABLE_DATA_JSON = os.path.join(INPUT_DIR, "table-json.tsv")
TABLE_DATA_INLINED = os.path.join(INPUT_DIR, "table-inlined.tsv")


def _json(obj) -> str:
    return json.dumps(obj, indent=" ", sort_keys=True)


class CsvAndTsvGenTestCase(unittest.TestCase):
    def test_object_model(self):
        book = Book(id="B1", genres=["fantasy"], creator={})
        logger.debug(as_json_obj(book.genres[0]))
        assert str(book.genres[0]) == "fantasy"
        assert book.genres[0].code.text == "fantasy"
        processed = remove_empty_items(book.genres)
        assert processed[0] == "fantasy"
        series = BookSeries(id="S1", creator=Author(name="Q. Writer"), reviews=[Review(rating=5)])
        series.books.append(book)
        schemaview = SchemaView(SCHEMA)
        shop = Shop()
        shop.all_book_series.append(series)

        csvstr = csv_dumper.dumps(shop, index_slot="all_book_series", schemaview=schemaview)
        assert "," in csvstr
        assert "\t" not in csvstr

        tsvstr = tsv_dumper.dumps(shop, index_slot="all_book_series", schemaview=schemaview)
        assert "\t" in tsvstr

    def test_csvgen_roundtrip(self):
        schemaview = SchemaView(SCHEMA)
        data = yaml_loader.load(DATA, target_class=Shop)
        csv_dumper.dump(data, to_file=OUTPUT, index_slot="all_book_series", schemaview=schemaview)
        roundtrip = csv_loader.load(OUTPUT, target_class=Shop, index_slot="all_book_series", schemaview=schemaview)
        logger.debug(json_dumper.dumps(roundtrip))
        logger.debug(f"COMPARE 1: {roundtrip}")
        logger.debug(f"COMPARE 2: {data}")
        assert roundtrip == data

    def test_csvgen_roundtrip_to_dict(self):
        schemaview = SchemaView(SCHEMA)
        data = yaml_loader.load(DATA, target_class=Shop)
        csv_dumper.dump(data, to_file=OUTPUT, index_slot="all_book_series", schemaview=schemaview)
        roundtrip = csv_loader.load_as_dict(OUTPUT, index_slot="all_book_series", schemaview=schemaview)
        assert roundtrip == json_dumper.to_dict(data)

    def test_tsvgen_roundtrip(self):
        schemaview = SchemaView(SCHEMA)
        data = yaml_loader.load(DATA, target_class=Shop)
        tsv_dumper.dump(data, to_file=OUTPUT, index_slot="all_book_series", schemaview=schemaview)
        roundtrip = tsv_loader.load(OUTPUT, target_class=Shop, index_slot="all_book_series", schemaview=schemaview)
        assert roundtrip == data

    def test_tsvgen_roundtrip_to_dict(self):
        schemaview = SchemaView(SCHEMA)
        data = yaml_loader.load(DATA, target_class=Shop)
        tsv_dumper.dump(data, to_file=OUTPUT, index_slot="all_book_series", schemaview=schemaview)
        roundtrip = tsv_loader.load_as_dict(OUTPUT, index_slot="all_book_series", schemaview=schemaview)
        assert roundtrip == json_dumper.to_dict(data)

    def test_csvgen_unroundtrippable(self):
        schemaview = SchemaView(SCHEMA)
        # schema = YAMLGenerator(SCHEMA).schema
        data = yaml_loader.load(DATA2, target_class=Shop)
        logger.debug(data.all_book_series[0])
        logger.debug(data.all_book_series[0].genres[0])
        assert str(data.all_book_series[0].genres[0]) == "fantasy"
        logger.debug(yaml_dumper.dumps(data))
        logger.debug(json_dumper.dumps(data))
        processed = remove_empty_items(data)
        logger.debug(f"PROC {processed['all_book_series']}")
        asj = as_json_object(processed, None)
        logger.debug(f"ASJ {asj['all_book_series']}")
        reconstituted_json = json.loads(json_dumper.dumps(data))
        s0 = reconstituted_json["all_book_series"][0]
        logger.debug(s0)
        logger.debug(json_dumper.dumps(data))
        # logger.debug(csv_dumper.dumps(data, index_slot='all_book_series', schema=schema))
        csv_dumper.dump(data, to_file=OUTPUT2, index_slot="all_book_series", schemaview=schemaview)
        # assert False
        roundtrip = csv_loader.load(OUTPUT2, target_class=Shop, index_slot="all_book_series", schemaview=schemaview)
        logger.debug(json_dumper.dumps(roundtrip))
        assert roundtrip == data

    @pytest.mark.skip(reason="json_flattener list bug in unflatten_from_csv()")
    def test_table_model(self):
        schemaview = SchemaView(SCHEMA)
        table_json = csv_loader.load(TABLE_DATA_JSON, target_class=Table, index_slot="rows", schemaview=schemaview)
        for row in table_json.rows:
            assert len(row["columnB"]) == 2

    def test_tsvgen_unroundtrippable(self):
        schemaview = SchemaView(SCHEMA)
        data = yaml_loader.load(DATA2, target_class=Shop)
        assert str(data.all_book_series[0].genres[0]) == "fantasy"
        tsv_dumper.dump(data, to_file=OUTPUT2, index_slot="all_book_series", schemaview=schemaview)
        roundtrip = tsv_loader.load(OUTPUT2, target_class=Shop, index_slot="all_book_series", schemaview=schemaview)
        assert roundtrip == data


if __name__ == "__main__":
    unittest.main()


# =============================================================================
# Integration tests for multivalued primitive CSV/TSV handling (issue #3041)
#
# Tests use inline schemas with list_syntax/list_delimiter annotations to
# verify configurable delimiter behavior for multivalued fields.
#
# Related issues:
# - https://github.com/linkml/linkml/issues/3041 (main issue)
# - https://github.com/linkml/linkml/issues/2581 (configurable syntax)
# =============================================================================

SCHEMA_WITH_PLAINTEXT_ANNOTATIONS = """
id: https://example.org/test
name: test_plaintext_annotations
description: >-
  Schema with list_syntax=plaintext annotation for testing bracket-free
  multivalued primitive serialization. This is the format users naturally
  type in spreadsheets: a|b|c instead of [a|b|c].
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

annotations:
  list_syntax: plaintext
  list_delimiter: "|"

classes:
  Container:
    tree_root: true
    slots:
      - persons
  Person:
    slots:
      - id
      - name
      - aliases

slots:
  persons:
    range: Person
    multivalued: true
    inlined_as_list: true
  id:
    identifier: true
  name:
    range: string
  aliases:
    range: string
    multivalued: true
"""


@pytest.fixture
def plaintext_schemaview():
    """Schema with list_syntax=plaintext annotation for bracket-free format."""
    return SchemaView(SCHEMA_WITH_PLAINTEXT_ANNOTATIONS)


class TestAnnotationBasedDelimiters:
    """
    Integration tests for annotation-based delimiter configuration.

    Tests that list_syntax and list_delimiter annotations control how
    multivalued fields are serialized/deserialized in CSV/TSV.
    """

    def test_plaintext_annotation_produces_no_brackets(self, plaintext_schemaview, tmp_path):
        """With list_syntax=plaintext, output should have no brackets."""
        data = {
            "persons": [
                {"id": "1", "name": "Test Person", "aliases": ["Alias One", "Alias Two"]},
            ]
        }
        output_file = tmp_path / "plaintext_test.tsv"

        tsv_dumper.dump(
            data,
            to_file=str(output_file),
            index_slot="persons",
            schemaview=plaintext_schemaview,
        )
        content = output_file.read_text()

        # Should be: Alias One|Alias Two (no brackets)
        assert "Alias One|Alias Two" in content
        assert "[Alias One|Alias Two]" not in content

    def test_plaintext_roundtrip(self, plaintext_schemaview, tmp_path):
        """Round-trip with plaintext annotations should preserve data."""
        original_aliases = ["First Alias", "Second Alias", "Third Alias"]
        data = {"persons": [{"id": "1", "name": "Test", "aliases": original_aliases}]}
        output_file = tmp_path / "plaintext_roundtrip.tsv"

        tsv_dumper.dump(
            data,
            to_file=str(output_file),
            index_slot="persons",
            schemaview=plaintext_schemaview,
        )
        roundtrip = tsv_loader.load_as_dict(str(output_file), index_slot="persons", schemaview=plaintext_schemaview)

        assert roundtrip["persons"][0]["aliases"] == original_aliases


@pytest.mark.parametrize(
    "delimiter,test_values",
    [
        ("|", ["a", "b", "c"]),
        (";", ["x", "y", "z"]),
        (",", ["one", "two", "three"]),
    ],
)
def test_custom_delimiter_roundtrip(delimiter, test_values, tmp_path):
    """
    Different delimiters should work for round-trip.

    Tests that the list_delimiter annotation correctly configures
    the delimiter used for joining/splitting multivalued fields.
    """
    # Create a valid schema name (delimiters have special chars, use ordinal)
    schema_name = f"test_delimiter_ord{ord(delimiter)}"
    schema_yaml = f"""
id: https://example.org/test
name: {schema_name}
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

annotations:
  list_syntax: plaintext
  list_delimiter: "{delimiter}"

classes:
  Container:
    tree_root: true
    slots:
      - items
  Item:
    slots:
      - id
      - tags

slots:
  items:
    range: Item
    multivalued: true
    inlined_as_list: true
  id:
    identifier: true
  tags:
    range: string
    multivalued: true
"""
    schemaview = SchemaView(schema_yaml)
    data = {"items": [{"id": "1", "tags": test_values}]}
    # Use ordinal for filename to avoid Windows reserved characters (|, etc.)
    output_file = tmp_path / f"delimiter_ord{ord(delimiter)}_test.tsv"

    tsv_dumper.dump(data, to_file=str(output_file), index_slot="items", schemaview=schemaview)
    content = output_file.read_text()
    expected = delimiter.join(test_values)
    assert expected in content

    roundtrip = tsv_loader.load_as_dict(str(output_file), index_slot="items", schemaview=schemaview)
    assert roundtrip["items"][0]["tags"] == test_values


# -----------------------------------------------------------------------------
# Edge case tests
# -----------------------------------------------------------------------------


class TestMultivaluedEdgeCases:
    """Tests for edge cases in multivalued primitive handling."""

    def test_empty_aliases_list(self, plaintext_schemaview, tmp_path):
        """Empty aliases list should round-trip correctly (not become [None])."""
        # Note: Empty lists cause issues in json_clean with None values.
        # This is a known edge case that needs separate handling.
        pytest.skip("Empty list handling has json_clean bug - needs separate fix")

    def test_single_alias(self, plaintext_schemaview, tmp_path):
        """Single alias (no delimiter needed) should round-trip correctly."""
        data = {"persons": [{"id": "1", "name": "Test Person", "aliases": ["Only One Alias"]}]}

        output_file = tmp_path / "single_alias.tsv"
        tsv_dumper.dump(
            data,
            to_file=str(output_file),
            index_slot="persons",
            schemaview=plaintext_schemaview,
        )
        roundtrip = tsv_loader.load_as_dict(str(output_file), index_slot="persons", schemaview=plaintext_schemaview)

        assert roundtrip["persons"][0]["aliases"] == ["Only One Alias"]

    def test_alias_containing_delimiter(self, plaintext_schemaview, tmp_path):
        """Alias containing the delimiter character needs proper escaping."""
        # This is a tricky edge case - what if someone's alias contains a pipe?
        data = {
            "persons": [
                {"id": "1", "name": "Test", "aliases": ["Name|With|Pipes", "Normal"]},
            ]
        }
        output_file = tmp_path / "delimiter_in_value.tsv"

        # This test documents expected behavior - may need escaping strategy
        # tsv_dumper.dump(data, to_file=str(output_file), index_slot="persons",
        #                 schemaview=plaintext_schemaview)
        # roundtrip = tsv_loader.load_as_dict(str(output_file), index_slot="persons",
        #                                      schemaview=plaintext_schemaview)

        # Exact behavior TBD - might need escaping or different delimiter
        pytest.skip("Delimiter-in-value escaping not yet implemented")
