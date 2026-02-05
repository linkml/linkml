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
# pytest-style tests for boolean handling in CSV/TSV (issue #2580)
#
# Tests verify that:
# - YAML 1.1 boolean values plus numeric 0/1 are accepted on load
# - Boolean output format is configurable via annotation or CLI
# - Coercion is schema-aware (only for boolean slots)
# =============================================================================

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


class TestBooleanLoading:
    """Test loading boolean values from CSV/TSV.

    YAML 1.1 booleans plus numeric 0/1 should be accepted:
    - Truthy: true, True, TRUE, yes, Yes, YES, on, On, ON, 1
    - Falsy: false, False, FALSE, no, No, NO, off, Off, OFF, 0
    """

    @pytest.fixture
    def schemaview(self, tmp_path):
        schema_file = tmp_path / "schema.yaml"
        schema_file.write_text(BOOLEAN_TEST_SCHEMA)
        return SchemaView(str(schema_file))

    @pytest.mark.parametrize(
        "truthy_value",
        ["true", "True", "TRUE", "yes", "Yes", "YES", "on", "On", "ON", "1"],
    )
    def test_load_truthy_values(self, schemaview, tmp_path, truthy_value):
        """All YAML 1.1 truthy values plus '1' should load as True."""
        tsv_file = tmp_path / "data.tsv"
        tsv_file.write_text(f"id\tis_active\tname\n1\t{truthy_value}\ttest\n")

        result = tsv_loader.load_as_dict(
            str(tsv_file),
            index_slot="items",
            schemaview=schemaview,
        )
        assert result["items"][0]["is_active"] is True

    @pytest.mark.parametrize(
        "falsy_value",
        ["false", "False", "FALSE", "no", "No", "NO", "off", "Off", "OFF", "0"],
    )
    def test_load_falsy_values(self, schemaview, tmp_path, falsy_value):
        """All YAML 1.1 falsy values plus '0' should load as False."""
        tsv_file = tmp_path / "data.tsv"
        tsv_file.write_text(f"id\tis_active\tname\n1\t{falsy_value}\ttest\n")

        result = tsv_loader.load_as_dict(
            str(tsv_file),
            index_slot="items",
            schemaview=schemaview,
        )
        assert result["items"][0]["is_active"] is False

    def test_multivalued_boolean_coercion(self):
        """Boolean coercion handles list values in boolean slots."""
        from linkml_runtime.loaders.delimited_file_loader import _coerce_boolean_values

        obj = {"is_active": ["yes", "no", "ON", "0"], "name": "test"}
        result = _coerce_boolean_values(obj, {"is_active"})
        assert result["is_active"] == [True, False, True, False]
        assert result["name"] == "test"

    def test_string_yes_not_coerced_in_string_slot(self, schemaview, tmp_path):
        """String 'yes' in a string slot should NOT be coerced to boolean."""
        tsv_file = tmp_path / "data.tsv"
        tsv_file.write_text("id\tis_active\tname\n1\ttrue\tyes\n")

        result = tsv_loader.load_as_dict(
            str(tsv_file),
            index_slot="items",
            schemaview=schemaview,
        )
        # is_active (boolean slot) should be True
        assert result["items"][0]["is_active"] is True
        # name (string slot) should remain "yes" not be coerced
        assert result["items"][0]["name"] == "yes"


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


class TestBooleanDumping:
    """Test dumping boolean values to CSV/TSV with configurable output format."""

    @pytest.fixture
    def schemaview_default(self, tmp_path):
        """Schema with default boolean output (true/false)."""
        schema_file = tmp_path / "schema.yaml"
        schema_file.write_text(BOOLEAN_TEST_SCHEMA)
        return SchemaView(str(schema_file))

    @pytest.fixture
    def schemaview_yes_no(self, tmp_path):
        """Schema with boolean_output: yes annotation."""
        schema_file = tmp_path / "schema.yaml"
        schema_file.write_text(BOOLEAN_OUTPUT_SCHEMA)
        return SchemaView(str(schema_file))

    def test_dump_boolean_default_format(self, schemaview_default, tmp_path):
        """Default boolean output should be 'true'/'false'."""
        data = {"items": [{"id": "1", "is_active": True, "name": "test"}]}
        output_file = tmp_path / "output.tsv"

        tsv_dumper.dump(
            data,
            to_file=str(output_file),
            index_slot="items",
            schemaview=schemaview_default,
        )

        content = output_file.read_text()
        assert "true" in content.lower()

    def test_dump_boolean_yes_no_format(self, schemaview_yes_no, tmp_path):
        """With boolean_output: yes, output should be 'yes'/'no'."""
        data = {"items": [{"id": "1", "is_active": True}]}
        output_file = tmp_path / "output.tsv"

        tsv_dumper.dump(
            data,
            to_file=str(output_file),
            index_slot="items",
            schemaview=schemaview_yes_no,
        )

        content = output_file.read_text()
        # Should contain 'yes' not 'true'
        assert "yes" in content.lower()
        assert "true" not in content.lower()

    def test_dump_boolean_cli_override(self, schemaview_default, tmp_path):
        """CLI option should override schema annotation."""
        data = {"items": [{"id": "1", "is_active": True}]}
        output_file = tmp_path / "output.tsv"

        tsv_dumper.dump(
            data,
            to_file=str(output_file),
            index_slot="items",
            schemaview=schemaview_default,
            boolean_output="1",  # CLI override
        )

        content = output_file.read_text()
        # Should contain '1' not 'true'
        assert "\t1\n" in content or "\t1\t" in content
