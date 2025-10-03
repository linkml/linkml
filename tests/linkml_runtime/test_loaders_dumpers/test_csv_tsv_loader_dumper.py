import json
import logging
import os

import pytest
from jsonasobj2 import as_json_obj

from linkml_runtime.dumpers import csv_dumper, json_dumper, tsv_dumper, yaml_dumper
from linkml_runtime.loaders import csv_loader, tsv_loader, yaml_loader
from linkml_runtime.utils.formatutils import remove_empty_items
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import as_json_object
from tests.test_loaders_dumpers.models.books_normalized import Author, Book, BookSeries, Review, Shop

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


def _json(obj) -> str:
    return json.dumps(obj, indent=" ", sort_keys=True)


@pytest.fixture
def schema_view():
    """SchemaView instance for books normalized schema."""
    return SchemaView(SCHEMA)


@pytest.fixture
def test_data(schema_view):
    """Load test data from books_normalized_01.yaml."""
    return yaml_loader.load(DATA, target_class=Shop)


@pytest.fixture
def test_data2(schema_view):
    """Load test data from books_normalized_02.yaml."""
    return yaml_loader.load(DATA2, target_class=Shop)


def test_object_model(schema_view):
    """Test basic object model and enum handling."""
    book = Book(id="B1", genres=["fantasy"], creator={})
    logger.debug(as_json_obj(book.genres[0]))
    assert str(book.genres[0]) == "fantasy"
    assert book.genres[0].code.text == "fantasy"
    processed = remove_empty_items(book.genres)
    assert processed[0] == "fantasy"

    # Create series and shop
    series = BookSeries(id="S1", creator=Author(name="Q. Writer"), reviews=[Review(rating=5)])
    series.books.append(book)
    shop = Shop()
    shop.all_book_series.append(series)

    # Test CSV dumping
    csvstr = csv_dumper.dumps(shop, index_slot="all_book_series", schemaview=schema_view)
    assert "," in csvstr
    assert "\t" not in csvstr

    # Test TSV dumping
    tsvstr = tsv_dumper.dumps(shop, index_slot="all_book_series", schemaview=schema_view)
    assert "\t" in tsvstr


def test_csvgen_roundtrip(schema_view, test_data, tmp_path):
    """Test CSV round-trip conversion (dump and load)."""
    output_file = tmp_path / "books_flattened.tsv"

    csv_dumper.dump(test_data, to_file=str(output_file), index_slot="all_book_series", schemaview=schema_view)
    roundtrip = csv_loader.load(
        str(output_file), target_class=Shop, index_slot="all_book_series", schemaview=schema_view
    )

    logger.debug(json_dumper.dumps(roundtrip))
    logger.debug(f"COMPARE 1: {roundtrip}")
    logger.debug(f"COMPARE 2: {test_data}")
    assert roundtrip == test_data


def test_csvgen_roundtrip_to_dict(schema_view, test_data, tmp_path):
    """Test CSV round-trip conversion to dictionary."""
    output_file = tmp_path / "books_flattened.tsv"

    csv_dumper.dump(test_data, to_file=str(output_file), index_slot="all_book_series", schemaview=schema_view)
    roundtrip = csv_loader.load_as_dict(str(output_file), index_slot="all_book_series", schemaview=schema_view)
    assert roundtrip == json_dumper.to_dict(test_data)


def test_tsvgen_roundtrip(schema_view, test_data, tmp_path):
    """Test TSV round-trip conversion (dump and load)."""
    output_file = tmp_path / "books_flattened.tsv"

    tsv_dumper.dump(test_data, to_file=str(output_file), index_slot="all_book_series", schemaview=schema_view)
    roundtrip = tsv_loader.load(
        str(output_file), target_class=Shop, index_slot="all_book_series", schemaview=schema_view
    )
    assert roundtrip == test_data


def test_tsvgen_roundtrip_to_dict(schema_view, test_data, tmp_path):
    """Test TSV round-trip conversion to dictionary."""
    output_file = tmp_path / "books_flattened.tsv"

    tsv_dumper.dump(test_data, to_file=str(output_file), index_slot="all_book_series", schemaview=schema_view)
    roundtrip = tsv_loader.load_as_dict(str(output_file), index_slot="all_book_series", schemaview=schema_view)
    assert roundtrip == json_dumper.to_dict(test_data)


def test_csvgen_unroundtrippable(schema_view, test_data2, tmp_path):
    """Test CSV handling of complex/unroundtrippable data."""
    output_file = tmp_path / "books_flattened_02.tsv"

    # Test initial data structure
    logger.debug(test_data2.all_book_series[0])
    logger.debug(test_data2.all_book_series[0].genres[0])
    assert str(test_data2.all_book_series[0].genres[0]) == "fantasy"
    logger.debug(yaml_dumper.dumps(test_data2))
    logger.debug(json_dumper.dumps(test_data2))

    # Test data processing
    processed = remove_empty_items(test_data2)
    logger.debug(f"PROC {processed['all_book_series']}")
    asj = as_json_object(processed, None)
    logger.debug(f"ASJ {asj['all_book_series']}")

    reconstituted_json = json.loads(json_dumper.dumps(test_data2))
    s0 = reconstituted_json["all_book_series"][0]
    logger.debug(s0)
    logger.debug(json_dumper.dumps(test_data2))

    # Test CSV dump and load
    csv_dumper.dump(test_data2, to_file=str(output_file), index_slot="all_book_series", schemaview=schema_view)
    roundtrip = csv_loader.load(
        str(output_file), target_class=Shop, index_slot="all_book_series", schemaview=schema_view
    )
    logger.debug(json_dumper.dumps(roundtrip))
    assert roundtrip == test_data2


def test_tsvgen_unroundtrippable(schema_view, test_data2, tmp_path):
    """Test TSV handling of complex/unroundtrippable data."""
    output_file = tmp_path / "books_flattened_02.tsv"

    assert str(test_data2.all_book_series[0].genres[0]) == "fantasy"

    tsv_dumper.dump(test_data2, to_file=str(output_file), index_slot="all_book_series", schemaview=schema_view)
    roundtrip = tsv_loader.load(
        str(output_file), target_class=Shop, index_slot="all_book_series", schemaview=schema_view
    )
    assert roundtrip == test_data2
