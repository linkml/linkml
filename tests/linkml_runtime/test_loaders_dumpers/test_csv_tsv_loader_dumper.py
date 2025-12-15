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


def test_bracket_free_multivalued_primitives():
    """Test that multivalued primitives are dumped without brackets.

    See https://github.com/linkml/linkml/issues/3041
    CSV/TSV output should use pipe-delimited format without brackets,
    aligning with schemasheets conventions and common spreadsheet patterns.
    """
    schemaview = SchemaView(SCHEMA)
    data = yaml_loader.load(DATA, target_class=Shop)

    # Dump to CSV
    csv_output = csv_dumper.dumps(data, index_slot="all_book_series", schemaview=schemaview)

    # Split into lines and check header and data
    lines = csv_output.strip().split("\n")
    header = lines[0]
    data_lines = lines[1:]

    # Header should have 'genres' column
    assert "genres" in header

    # Find genres column index
    headers = header.split(",")
    genres_idx = headers.index("genres")

    # Check each row's genres value - should NOT have brackets
    for line in data_lines:
        # Handle CSV parsing (fields may contain commas in JSON)
        import csv
        import io

        reader = csv.reader(io.StringIO(line))
        row = next(reader)
        genres_value = row[genres_idx]

        # Should not start/end with brackets (unless empty)
        if genres_value:
            assert not genres_value.startswith("["), f"Genres should not have brackets: {genres_value}"
            assert not genres_value.endswith("]"), f"Genres should not have brackets: {genres_value}"


def test_load_bracket_free_csv():
    """Test loading CSV with bracket-free pipe-delimited values.

    Users commonly enter data like "apple|banana|cherry" in spreadsheets,
    not "[apple|banana|cherry]". This should be properly parsed as a list.
    """
    import tempfile

    schemaview = SchemaView(SCHEMA)

    # Create a CSV with bracket-free pipe-delimited genres
    csv_content = """id,name,genres,creator_json
S001,Test Series,scifi|fantasy,{"name": "Test Author"}
S002,Another Series,romance,{"name": "Another Author"}
S003,No Genre,,{"name": "Third Author"}
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        csv_file = f.name

    try:
        # Load the CSV
        result = csv_loader.load_as_dict(csv_file, index_slot="all_book_series", schemaview=schemaview)

        items = result.get("all_book_series", [])
        assert len(items) == 3

        # First item should have genres as a list
        assert items[0]["genres"] == ["scifi", "fantasy"]

        # Second item should have single-item list
        assert items[1]["genres"] == ["romance"]

        # Third item should have no genres (empty)
        assert "genres" not in items[2] or items[2].get("genres") is None
    finally:
        import os

        os.unlink(csv_file)


def test_multivalued_primitive_roundtrip():
    """Test that multivalued primitives round-trip correctly with bracket-free format."""
    schemaview = SchemaView(SCHEMA)

    # Create test data with multiple genres
    series = BookSeries(
        id="TEST001",
        name="Test Book Series",
        genres=[GenreEnum.scifi, GenreEnum.fantasy, GenreEnum.romance],
        creator=Author(name="Test Author"),
    )
    shop = Shop(all_book_series=[series])

    # Dump to CSV
    csv_output = csv_dumper.dumps(shop, index_slot="all_book_series", schemaview=schemaview)

    # Verify output format
    assert "scifi|fantasy|romance" in csv_output
    assert "[scifi|fantasy|romance]" not in csv_output

    # Load back
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_output)
        csv_file = f.name

    try:
        roundtrip = csv_loader.load(csv_file, target_class=Shop, index_slot="all_book_series", schemaview=schemaview)

        # Verify genres came back correctly
        assert len(roundtrip.all_book_series) == 1
        roundtrip_genres = [str(g) for g in roundtrip.all_book_series[0].genres]
        assert roundtrip_genres == ["scifi", "fantasy", "romance"]
    finally:
        import os

        os.unlink(csv_file)


if __name__ == "__main__":
    unittest.main()
