import json
import logging
import os

import pytest
from jsonasobj2 import as_json_obj

from linkml_runtime.dumpers import csv_dumper, json_dumper, tsv_dumper, yaml_dumper
from linkml_runtime.loaders import csv_loader, tsv_loader, yaml_loader
from linkml_runtime.loaders.delimited_file_loader import (
    check_data_for_delimiter,
    get_list_config_from_annotations,
    enhance_configmap_for_multivalued_primitives,
)
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


def test_object_model():
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


def test_csvgen_roundtrip():
    schemaview = SchemaView(SCHEMA)
    data = yaml_loader.load(DATA, target_class=Shop)
    csv_dumper.dump(data, to_file=OUTPUT, index_slot="all_book_series", schemaview=schemaview)
    roundtrip = csv_loader.load(OUTPUT, target_class=Shop, index_slot="all_book_series", schemaview=schemaview)
    logger.debug(json_dumper.dumps(roundtrip))
    logger.debug(f"COMPARE 1: {roundtrip}")
    logger.debug(f"COMPARE 2: {data}")
    assert roundtrip == data


def test_csvgen_roundtrip_to_dict():
    schemaview = SchemaView(SCHEMA)
    data = yaml_loader.load(DATA, target_class=Shop)
    csv_dumper.dump(data, to_file=OUTPUT, index_slot="all_book_series", schemaview=schemaview)
    roundtrip = csv_loader.load_as_dict(OUTPUT, index_slot="all_book_series", schemaview=schemaview)
    assert roundtrip == json_dumper.to_dict(data)


def test_tsvgen_roundtrip():
    schemaview = SchemaView(SCHEMA)
    data = yaml_loader.load(DATA, target_class=Shop)
    tsv_dumper.dump(data, to_file=OUTPUT, index_slot="all_book_series", schemaview=schemaview)
    roundtrip = tsv_loader.load(OUTPUT, target_class=Shop, index_slot="all_book_series", schemaview=schemaview)
    assert roundtrip == data


def test_tsvgen_roundtrip_to_dict():
    schemaview = SchemaView(SCHEMA)
    data = yaml_loader.load(DATA, target_class=Shop)
    tsv_dumper.dump(data, to_file=OUTPUT, index_slot="all_book_series", schemaview=schemaview)
    roundtrip = tsv_loader.load_as_dict(OUTPUT, index_slot="all_book_series", schemaview=schemaview)
    assert roundtrip == json_dumper.to_dict(data)


def test_csvgen_unroundtrippable():
    schemaview = SchemaView(SCHEMA)
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
    csv_dumper.dump(data, to_file=OUTPUT2, index_slot="all_book_series", schemaview=schemaview)
    roundtrip = csv_loader.load(OUTPUT2, target_class=Shop, index_slot="all_book_series", schemaview=schemaview)
    logger.debug(json_dumper.dumps(roundtrip))
    assert roundtrip == data


@pytest.mark.skip(reason="json_flattener list bug in unflatten_from_csv()")
def test_table_model():
    schemaview = SchemaView(SCHEMA)
    table_json = csv_loader.load(TABLE_DATA_JSON, target_class=Table, index_slot="rows", schemaview=schemaview)
    for row in table_json.rows:
        assert len(row["columnB"]) == 2


def test_tsvgen_unroundtrippable():
    schemaview = SchemaView(SCHEMA)
    data = yaml_loader.load(DATA2, target_class=Shop)
    assert str(data.all_book_series[0].genres[0]) == "fantasy"
    tsv_dumper.dump(data, to_file=OUTPUT2, index_slot="all_book_series", schemaview=schemaview)
    roundtrip = tsv_loader.load(OUTPUT2, target_class=Shop, index_slot="all_book_series", schemaview=schemaview)
    assert roundtrip == data


SCHEMA_WITH_PLAINTEXT_ANNOTATIONS = """
id: https://example.org/test
name: test_plaintext_annotations
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

SCHEMA_WITHOUT_ANNOTATIONS = """
id: https://example.org/test
name: no_annotations
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

classes:
  Item:
    slots:
      - id
slots:
  id:
    identifier: true
"""

SCHEMA_WHITESPACE_STRIP = """
id: https://example.org/whitespace
name: whitespace_test
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

SCHEMA_WHITESPACE_PRESERVE = """
id: https://example.org/preserve
name: preserve_whitespace
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

annotations:
  list_syntax: plaintext
  list_delimiter: "|"
  list_strip_whitespace: "false"

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


def make_delimiter_schema(delimiter: str) -> str:
    """Factory for creating schemas with custom delimiters."""
    schema_name = f"test_delimiter_ord{ord(delimiter)}"
    return f"""
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


@pytest.fixture
def plaintext_schemaview():
    """Schema with list_syntax=plaintext annotation."""
    return SchemaView(SCHEMA_WITH_PLAINTEXT_ANNOTATIONS)


@pytest.fixture
def whitespace_schemaview():
    """Schema with plaintext list syntax (strip enabled by default)."""
    return SchemaView(SCHEMA_WHITESPACE_STRIP)


@pytest.fixture
def whitespace_preserve_schemaview():
    """Schema with list_strip_whitespace=false."""
    return SchemaView(SCHEMA_WHITESPACE_PRESERVE)


# Helper function defaults


def test_get_list_config_with_none_schemaview():
    """When schemaview is None, should return defaults."""
    list_markers, inner_delimiter, strip_whitespace, refuse = get_list_config_from_annotations(None, None)
    assert list_markers == ("[", "]")
    assert inner_delimiter == "|"
    assert strip_whitespace is True
    assert refuse is False


def test_get_list_config_without_annotations():
    """Schema without annotations should return defaults."""
    sv = SchemaView(SCHEMA_WITHOUT_ANNOTATIONS)
    list_markers, inner_delimiter, strip_whitespace, refuse = get_list_config_from_annotations(sv, "id")
    assert list_markers == ("[", "]")
    assert inner_delimiter == "|"
    assert strip_whitespace is True
    assert refuse is False


def test_enhance_configmap_with_none_schemaview():
    """When schemaview is None, should return original configmap."""
    original = {"some": "config"}
    result = enhance_configmap_for_multivalued_primitives(None, "slot", original, plaintext_mode=True)
    assert result is original


def test_enhance_configmap_not_plaintext_mode():
    """When plaintext_mode is False, should return original configmap."""
    original = {"some": "config"}
    sv = SchemaView(SCHEMA_WITH_PLAINTEXT_ANNOTATIONS)
    result = enhance_configmap_for_multivalued_primitives(sv, "persons", original, plaintext_mode=False)
    assert result is original


# Annotation-based delimiters


def test_plaintext_annotation_produces_no_brackets(plaintext_schemaview, tmp_path):
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

    assert "Alias One|Alias Two" in content
    assert "[Alias One|Alias Two]" not in content


def test_plaintext_roundtrip(plaintext_schemaview, tmp_path):
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
    """Different delimiters should round-trip correctly."""
    schemaview = SchemaView(make_delimiter_schema(delimiter))
    data = {"items": [{"id": "1", "tags": test_values}]}
    output_file = tmp_path / f"delimiter_ord{ord(delimiter)}_test.tsv"

    tsv_dumper.dump(data, to_file=str(output_file), index_slot="items", schemaview=schemaview)
    content = output_file.read_text()
    expected = delimiter.join(test_values)
    assert expected in content

    roundtrip = tsv_loader.load_as_dict(str(output_file), index_slot="items", schemaview=schemaview)
    assert roundtrip["items"][0]["tags"] == test_values


# Edge cases


@pytest.mark.skip(reason="Empty list handling has json_clean bug - needs separate fix")
def test_empty_aliases_list(plaintext_schemaview, tmp_path):
    """Empty aliases list should round-trip correctly."""
    pass


def test_single_alias(plaintext_schemaview, tmp_path):
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


@pytest.mark.skip(reason="Delimiter-in-value escaping not yet implemented")
def test_alias_containing_delimiter(plaintext_schemaview, tmp_path):
    """Alias containing the delimiter character needs escaping."""
    pass


# Whitespace stripping


def test_whitespace_stripped_by_default(whitespace_schemaview, tmp_path):
    """Whitespace around delimiters should be stripped by default."""
    tsv_content = "id\ttags\n1\tred | green | blue\n"
    tsv_file = tmp_path / "whitespace.tsv"
    tsv_file.write_text(tsv_content)

    result = tsv_loader.load_as_dict(str(tsv_file), index_slot="items", schemaview=whitespace_schemaview)
    assert result["items"][0]["tags"] == ["red", "green", "blue"]


def test_whitespace_preserved_with_annotation(whitespace_preserve_schemaview, tmp_path):
    """With list_strip_whitespace=false, whitespace should be preserved."""
    tsv_content = "id\ttags\n1\tred | green | blue\n"
    tsv_file = tmp_path / "preserve_whitespace.tsv"
    tsv_file.write_text(tsv_content)

    result = tsv_loader.load_as_dict(str(tsv_file), index_slot="items", schemaview=whitespace_preserve_schemaview)
    assert result["items"][0]["tags"] == ["red ", " green ", " blue"]


@pytest.mark.parametrize("true_value", ["true", "True", "TRUE"])
def test_strip_whitespace_true_values(true_value):
    """Case-insensitive 'true' annotation values should enable stripping."""
    schema_yaml = f"""
id: https://example.org/test
name: test
annotations:
  list_strip_whitespace: "{true_value}"
"""
    sv = SchemaView(schema_yaml)
    _, _, strip, _ = get_list_config_from_annotations(sv, None)
    assert strip is True, f"Expected True for '{true_value}'"


@pytest.mark.parametrize("false_value", ["false", "False", "FALSE"])
def test_strip_whitespace_false_values(false_value):
    """Case-insensitive 'false' annotation values should disable stripping."""
    schema_yaml = f"""
id: https://example.org/test
name: test
annotations:
  list_strip_whitespace: "{false_value}"
"""
    sv = SchemaView(schema_yaml)
    _, _, strip, _ = get_list_config_from_annotations(sv, None)
    assert strip is False, f"Expected False for '{false_value}'"


@pytest.mark.parametrize("invalid_value", ["yes", "no", "1", "0", "on", "off"])
def test_strip_whitespace_invalid_values_default_to_true(invalid_value, caplog):
    """Invalid annotation values should warn and default to true (stripping enabled)."""
    schema_yaml = f"""
id: https://example.org/test
name: test
annotations:
  list_strip_whitespace: "{invalid_value}"
"""
    sv = SchemaView(schema_yaml)
    with caplog.at_level(logging.WARNING):
        _, _, strip, _ = get_list_config_from_annotations(sv, None)
    assert strip is True, f"Expected True (default) for invalid value '{invalid_value}'"
    assert "Invalid list_strip_whitespace value" in caplog.text


def test_output_whitespace_stripped_by_default(whitespace_schemaview, tmp_path):
    """Whitespace in values should be stripped when dumping."""
    data = {"items": [{"id": "1", "tags": ["dog   ", "cat  ", "bird"]}]}
    output_file = tmp_path / "output_strip.tsv"

    tsv_dumper.dump(data, to_file=str(output_file), index_slot="items", schemaview=whitespace_schemaview)
    content = output_file.read_text()

    assert "dog|cat|bird" in content
    assert "dog   " not in content


def test_output_whitespace_preserved_with_annotation(whitespace_preserve_schemaview, tmp_path):
    """With list_strip_whitespace=false, output whitespace should be preserved."""
    data = {"items": [{"id": "1", "tags": ["dog   ", "cat  ", "bird"]}]}
    output_file = tmp_path / "output_preserve.tsv"

    tsv_dumper.dump(data, to_file=str(output_file), index_slot="items", schemaview=whitespace_preserve_schemaview)
    content = output_file.read_text()

    assert "dog   |cat  |bird" in content


# refuse_delimiter_in_data tests


SCHEMA_REFUSE_DELIMITER = """
id: https://example.org/refuse
name: refuse_delimiter_test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

annotations:
  list_syntax: plaintext
  list_delimiter: "|"
  refuse_delimiter_in_data: "true"

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

SCHEMA_REFUSE_DELIMITER_BRACKET = """
id: https://example.org/refuse_bracket
name: refuse_delimiter_bracket_test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

annotations:
  list_syntax: python
  list_delimiter: "|"
  refuse_delimiter_in_data: "true"

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

SCHEMA_REFUSE_DELIMITER_SEMICOLON = """
id: https://example.org/refuse_semi
name: refuse_delimiter_semicolon_test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

annotations:
  list_syntax: plaintext
  list_delimiter: ";"
  refuse_delimiter_in_data: "true"

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


def test_refuse_delimiter_in_data_raises_on_conflict(tmp_path):
    """Plaintext mode: value containing pipe should raise ValueError when refuse_delimiter_in_data is true."""
    sv = SchemaView(SCHEMA_REFUSE_DELIMITER)
    data = {"items": [{"id": "1", "tags": ["safe", "has|pipe"]}]}

    with pytest.raises(ValueError, match="list delimiter"):
        tsv_dumper.dumps(data, index_slot="items", schemaview=sv)


def test_refuse_delimiter_in_data_raises_bracket_mode(tmp_path):
    """Bracket mode: value containing pipe should raise ValueError when refuse_delimiter_in_data is true."""
    sv = SchemaView(SCHEMA_REFUSE_DELIMITER_BRACKET)
    data = {"items": [{"id": "1", "tags": ["safe", "has|pipe"]}]}

    with pytest.raises(ValueError, match="list delimiter"):
        tsv_dumper.dumps(data, index_slot="items", schemaview=sv)


def test_refuse_delimiter_in_data_false_allows_conflict():
    """Default (false): value containing pipe should NOT raise an error."""
    sv = SchemaView(SCHEMA_WITH_PLAINTEXT_ANNOTATIONS)
    data = {"persons": [{"id": "1", "name": "Test", "aliases": ["has|pipe"]}]}

    # Should not raise - refuse_delimiter_in_data defaults to false
    result = tsv_dumper.dumps(data, index_slot="persons", schemaview=sv)
    assert result is not None


def test_refuse_delimiter_in_data_custom_delimiter():
    """Semicolon delimiter: value containing semicolon should raise ValueError."""
    sv = SchemaView(SCHEMA_REFUSE_DELIMITER_SEMICOLON)
    data = {"items": [{"id": "1", "tags": ["safe", "has;semi"]}]}

    with pytest.raises(ValueError, match="list delimiter"):
        tsv_dumper.dumps(data, index_slot="items", schemaview=sv)


def test_refuse_delimiter_in_data_cli_override(tmp_path):
    """CLI override: refuse_delimiter_in_data=True passed to dumps should raise even without annotation."""
    sv = SchemaView(SCHEMA_WITH_PLAINTEXT_ANNOTATIONS)
    data = {"persons": [{"id": "1", "name": "Test", "aliases": ["has|pipe"]}]}

    with pytest.raises(ValueError, match="list delimiter"):
        tsv_dumper.dumps(data, index_slot="persons", schemaview=sv, refuse_delimiter_in_data=True)


def test_refuse_delimiter_in_data_cli_override_false():
    """CLI override: refuse_delimiter_in_data=False should suppress the annotation."""
    sv = SchemaView(SCHEMA_REFUSE_DELIMITER)
    data = {"items": [{"id": "1", "tags": ["has|pipe"]}]}

    # Annotation says true, but CLI override says false
    result = tsv_dumper.dumps(data, index_slot="items", schemaview=sv, refuse_delimiter_in_data=False)
    assert result is not None


def test_get_list_config_refuse_delimiter_annotation():
    """get_list_config_from_annotations should read refuse_delimiter_in_data."""
    sv = SchemaView(SCHEMA_REFUSE_DELIMITER)
    _, _, _, refuse = get_list_config_from_annotations(sv, "items")
    assert refuse is True


def test_get_list_config_refuse_delimiter_default():
    """Default refuse_delimiter_in_data should be False."""
    sv = SchemaView(SCHEMA_WITH_PLAINTEXT_ANNOTATIONS)
    _, _, _, refuse = get_list_config_from_annotations(sv, "persons")
    assert refuse is False


def test_check_data_for_delimiter_raises():
    """check_data_for_delimiter should raise ValueError for conflicts."""
    sv = SchemaView(SCHEMA_REFUSE_DELIMITER)
    objs = [{"id": "1", "tags": ["good", "bad|value"]}]

    with pytest.raises(ValueError, match="bad\\|value"):
        check_data_for_delimiter(objs, "|", sv, "items")


def test_check_data_for_delimiter_no_conflict():
    """check_data_for_delimiter should pass silently when no conflict exists."""
    sv = SchemaView(SCHEMA_REFUSE_DELIMITER)
    objs = [{"id": "1", "tags": ["good", "also_good"]}]

    # Should not raise
    check_data_for_delimiter(objs, "|", sv, "items")
