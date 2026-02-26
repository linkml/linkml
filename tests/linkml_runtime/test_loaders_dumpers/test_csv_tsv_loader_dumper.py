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


# Boolean handling tests for CSV/TSV (issue #2580)

BOOLEAN_TEST_SCHEMA = """
id: https://example.org/boolean_test
name: boolean_test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

classes:
  Container:
    tree_root: true
    slots:
      - items
  Item:
    slots:
      - id
      - is_active
      - name

slots:
  items:
    range: Item
    multivalued: true
    inlined_as_list: true
  id:
    identifier: true
  is_active:
    range: boolean
  name:
    range: string
"""

BOOLEAN_OVERRIDE_SCHEMA = """
id: https://example.org/boolean_override_test
name: boolean_override_test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
annotations:
  boolean_truthy: "yes,on,1"
  boolean_falsy: "no,off,0"

classes:
  Container:
    tree_root: true
    slots:
      - items
  Item:
    slots:
      - id
      - is_active
      - name

slots:
  items:
    range: Item
    multivalued: true
    inlined_as_list: true
  id:
    identifier: true
  is_active:
    range: boolean
  name:
    range: string
"""

BOOLEAN_OUTPUT_SCHEMA = """
id: https://example.org/boolean_output_test
name: boolean_output_test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
annotations:
  boolean_output: "yes"

classes:
  Container:
    tree_root: true
    slots:
      - items
  Item:
    slots:
      - id
      - is_active

slots:
  items:
    range: Item
    multivalued: true
    inlined_as_list: true
  id:
    identifier: true
  is_active:
    range: boolean
"""


@pytest.fixture
def boolean_schemaview(tmp_path):
    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text(BOOLEAN_TEST_SCHEMA)
    return SchemaView(str(schema_file))


@pytest.fixture
def boolean_override_schemaview(tmp_path):
    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text(BOOLEAN_OVERRIDE_SCHEMA)
    return SchemaView(str(schema_file))


@pytest.fixture
def boolean_output_schemaview(tmp_path):
    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text(BOOLEAN_OUTPUT_SCHEMA)
    return SchemaView(str(schema_file))


# --- Loading: default truthy/falsy values ---


@pytest.mark.parametrize("truthy_value", ["true", "True", "TRUE", "t", "T"])
def test_load_default_truthy_values(boolean_schemaview, tmp_path, truthy_value):
    tsv_file = tmp_path / "data.tsv"
    tsv_file.write_text(f"id\tis_active\tname\n1\t{truthy_value}\ttest\n")
    result = tsv_loader.load_as_dict(str(tsv_file), index_slot="items", schemaview=boolean_schemaview)
    assert result["items"][0]["is_active"] is True


@pytest.mark.parametrize("falsy_value", ["false", "False", "FALSE", "f", "F"])
def test_load_default_falsy_values(boolean_schemaview, tmp_path, falsy_value):
    tsv_file = tmp_path / "data.tsv"
    tsv_file.write_text(f"id\tis_active\tname\n1\t{falsy_value}\ttest\n")
    result = tsv_loader.load_as_dict(str(tsv_file), index_slot="items", schemaview=boolean_schemaview)
    assert result["items"][0]["is_active"] is False


@pytest.mark.parametrize("non_default_value", ["yes", "Yes", "YES", "no", "No", "NO", "on", "off"])
def test_non_default_values_not_coerced(boolean_schemaview, tmp_path, non_default_value):
    tsv_file = tmp_path / "data.tsv"
    tsv_file.write_text(f"id\tis_active\tname\n1\t{non_default_value}\ttest\n")
    result = tsv_loader.load_as_dict(str(tsv_file), index_slot="items", schemaview=boolean_schemaview)
    assert isinstance(result["items"][0]["is_active"], str)


@pytest.mark.parametrize("numeric_value", ["1", "0"])
def test_numeric_values_not_coerced(boolean_schemaview, tmp_path, numeric_value):
    """Numeric 1/0 should not become True/False without explicit override."""
    tsv_file = tmp_path / "data.tsv"
    tsv_file.write_text(f"id\tis_active\tname\n1\t{numeric_value}\ttest\n")
    result = tsv_loader.load_as_dict(str(tsv_file), index_slot="items", schemaview=boolean_schemaview)
    assert not isinstance(result["items"][0]["is_active"], bool)


def test_string_yes_not_coerced_in_string_slot(boolean_schemaview, tmp_path):
    """Coercion is schema-aware: 'yes' in a string slot stays as string."""
    tsv_file = tmp_path / "data.tsv"
    tsv_file.write_text("id\tis_active\tname\n1\ttrue\tyes\n")
    result = tsv_loader.load_as_dict(str(tsv_file), index_slot="items", schemaview=boolean_schemaview)
    assert result["items"][0]["is_active"] is True
    assert result["items"][0]["name"] == "yes"


# --- Loading: multivalued boolean slots ---


def test_multivalued_boolean_coercion():
    from linkml_runtime.utils.boolean_utils import coerce_boolean_values

    obj = {"is_active": ["true", "false", "T", "F"], "name": "test"}
    result = coerce_boolean_values(obj, {"is_active"})
    assert result["is_active"] == [True, False, True, False]
    assert result["name"] == "test"


def test_multivalued_boolean_coercion_with_custom_values():
    from linkml_runtime.utils.boolean_utils import coerce_boolean_values

    truthy = frozenset({"true", "t", "yes", "on"})
    falsy = frozenset({"false", "f", "no", "off"})
    obj = {"is_active": ["yes", "no", "ON", "off"], "name": "test"}
    result = coerce_boolean_values(obj, {"is_active"}, truthy, falsy)
    assert result["is_active"] == [True, False, True, False]
    assert result["name"] == "test"


# --- Loading: schema annotation extends defaults ---


@pytest.mark.parametrize("truthy_value", ["true", "T", "yes", "Yes", "YES", "on", "On", "ON", "1"])
def test_annotation_truthy_values(boolean_override_schemaview, tmp_path, truthy_value):
    tsv_file = tmp_path / "data.tsv"
    tsv_file.write_text(f"id\tis_active\tname\n1\t{truthy_value}\ttest\n")
    result = tsv_loader.load_as_dict(str(tsv_file), index_slot="items", schemaview=boolean_override_schemaview)
    assert result["items"][0]["is_active"] is True


@pytest.mark.parametrize("falsy_value", ["false", "F", "no", "No", "NO", "off", "Off", "OFF", "0"])
def test_annotation_falsy_values(boolean_override_schemaview, tmp_path, falsy_value):
    tsv_file = tmp_path / "data.tsv"
    tsv_file.write_text(f"id\tis_active\tname\n1\t{falsy_value}\ttest\n")
    result = tsv_loader.load_as_dict(str(tsv_file), index_slot="items", schemaview=boolean_override_schemaview)
    assert result["items"][0]["is_active"] is False


# --- Loading: empty string to null ---


def test_empty_csv_cell_is_absent(boolean_schemaview, tmp_path):
    """json-flattener drops empty CSV cells entirely."""
    tsv_file = tmp_path / "data.tsv"
    tsv_file.write_text("id\tis_active\tname\n1\ttrue\t\n")
    result = tsv_loader.load_as_dict(str(tsv_file), index_slot="items", schemaview=boolean_schemaview)
    assert "name" not in result["items"][0]


def test_empty_boolean_cell_is_absent(boolean_schemaview, tmp_path):
    """Empty boolean CSV cell is dropped, not coerced to bool."""
    tsv_file = tmp_path / "data.tsv"
    tsv_file.write_text("id\tis_active\tname\n1\t\ttest\n")
    result = tsv_loader.load_as_dict(str(tsv_file), index_slot="items", schemaview=boolean_schemaview)
    assert "is_active" not in result["items"][0]


def test_coerce_empty_to_none_function():
    from linkml_runtime.loaders.delimited_file_loader import _coerce_empty_to_none

    obj = {"name": "", "id": "1", "tags": ["a", "", "c"]}
    result = _coerce_empty_to_none(obj)
    assert result == {"name": None, "id": "1", "tags": ["a", None, "c"]}


# --- Dumping: configurable boolean output format ---


def test_dump_boolean_default_format(boolean_schemaview, tmp_path):
    data = {"items": [{"id": "1", "is_active": True, "name": "test"}]}
    output_file = tmp_path / "output.tsv"
    tsv_dumper.dump(data, to_file=str(output_file), index_slot="items", schemaview=boolean_schemaview)
    content = output_file.read_text()
    assert "true" in content.lower()


def test_dump_boolean_yes_no_format(boolean_output_schemaview, tmp_path):
    data = {"items": [{"id": "1", "is_active": True}]}
    output_file = tmp_path / "output.tsv"
    tsv_dumper.dump(data, to_file=str(output_file), index_slot="items", schemaview=boolean_output_schemaview)
    content = output_file.read_text()
    assert "yes" in content.lower()
    assert "true" not in content.lower()


def test_dump_boolean_cli_override(boolean_schemaview, tmp_path):
    data = {"items": [{"id": "1", "is_active": True}]}
    output_file = tmp_path / "output.tsv"
    tsv_dumper.dump(
        data, to_file=str(output_file), index_slot="items", schemaview=boolean_schemaview, boolean_output="1"
    )
    content = output_file.read_text()
    assert "\t1\n" in content or "\t1\t" in content
