import logging
from io import StringIO
from pathlib import Path

import pytest
from jsonasobj2 import as_json

from linkml.utils.schemaloader import SchemaLoader


@pytest.mark.skip(reason="Disabled until we get SchemaDefinitionList implemented")
def test_basic_merge(input_path, snapshot):
    """Test the basic merge paths"""
    logstream = StringIO()
    logging.basicConfig()
    logger = logging.getLogger()
    for handler in logger.handlers:
        logger.removeHandler(handler)
    logger.addHandler(logging.StreamHandler(logstream))
    logger.setLevel(logging.INFO)

    loader = SchemaLoader(input_path("merge1.yaml"), logger=logger)
    assert as_json(loader.resolve()) == snapshot("merge1.json")
    assert loader.synopsis.errors() == []
    assert "Overlapping subset and slot names: s1, s2" in logstream.getvalue().strip()


@pytest.mark.skip(reason="Disabled until we get SchemaDefinitionList implemented")
def test_mergeerror1(input_path):
    """Test conflicting definitions path"""
    fn = input_path("mergeerror1.yaml")
    message = "Conflicting URIs (http://example.org/schema2, http://example.org/schema1) for item: c1"
    with pytest.raises(ValueError, match=message):
        SchemaLoader(fn)


def test_imports(input_path, snapshot):
    loader = SchemaLoader(input_path("base.yaml"))
    assert as_json(loader.resolve()) == snapshot("base.json")
    assert loader.synopsis.errors() == []


def test_imports_relative(input_path):
    loader = SchemaLoader(input_path("relative_import_test/main.yaml"))
    loader.resolve()
    normalized_imports = [Path(p).as_posix() for p in loader.schema.imports]
    assert normalized_imports == [
        "./child/index",
        "child/grandchild/index",
        "child/grandchild/greatgrandchild/index",
    ]


@pytest.mark.skip(reason="Re-enable this once we get fully migrated")
def test_error_paths(input_path):
    """Test various loader error situations"""

    fn = input_path("loadererror1.yaml")
    with pytest.raises(ValueError, match="Unknown slot domain should fail") as e:
        SchemaLoader(fn).resolve()
    assert 'loadererror1.yaml", line 11, col 13' in str(e.value)

    fn = input_path("loadererror2.yaml")
    with pytest.raises(ValueError, match='type "string" does not declare a URI'):
        SchemaLoader(fn).resolve()

    fn = input_path("loadererror2a.yaml")
    with pytest.raises(ValueError, match="slot: s1 - key and identifier slots cannot be optional"):
        SchemaLoader(fn).resolve()

    fn = input_path("loadertest1.yaml")
    schema = SchemaLoader(fn).resolve()
    assert "string" == schema.slots["s1"].range

    fn = input_path("loadererror4.yaml")
    with pytest.raises(ValueError, match='loadererror4.yaml", line 6, col 17'):
        SchemaLoader(fn).resolve()


@pytest.mark.skip(reason="Re-enable this once we get fully migrated")
def test_empty_range(input_path):
    """A type must have either a base or a parent"""
    fn = input_path("loadererror5.yaml")
    with pytest.raises(ValueError, match='loadererror5.yaml", line 9, col 3'):
        SchemaLoader(fn).resolve()


def test_multi_key(input_path):
    """Multiple keys are not supported"""
    fn = input_path("loadererror6.yaml")
    with pytest.raises(ValueError, match="multiple keys/identifiers not allowed"):
        SchemaLoader(fn).resolve()

    fn = input_path("loadererror7.yaml")
    with pytest.raises(ValueError, match="multiple keys/identifiers not allowed"):
        SchemaLoader(fn).resolve()


def test_key_and_id(input_path):
    """A slot cannot be both a key and an identifier"""
    fn = input_path("loadererror8.yaml")
    with pytest.raises(ValueError, match="A slot cannot be both a key and identifier at the same time"):
        SchemaLoader(fn).resolve()

    fn = input_path("loadererror9.yaml")
    with pytest.raises(ValueError, match="A slot cannot be both a key and identifier at the same time"):
        SchemaLoader(fn).resolve()


@pytest.mark.skip(reason="Re-enable this once we get fully migrated")
def test_missing_type_uri(input_path):
    """A type with neither a typeof or uri is an error"""
    fn = input_path("loadererror10.yaml")
    with pytest.raises(ValueError, match='loadererror10.yaml", line 12, col 3'):
        SchemaLoader(fn).resolve()

    fn = input_path("loaderpass11.yaml")
    SchemaLoader(fn).resolve()


@pytest.mark.skip(reason="Re-enable this once we get fully migrated")
def test_undefined_subset(input_path):
    """Throw an error on an undefined subset reference"""
    fn = input_path("loadererror11.yaml")
    with pytest.raises(ValueError, match='loadererror11.yaml", line 22, col 16'):
        SchemaLoader(fn).resolve()


@pytest.mark.network
def test_importmap(input_path, snapshot):
    """Test the importmap parameter"""
    fn = input_path("import_test_1.yaml")
    importmap = {
        "http://example.org/import_test_2": "import_test_2",
        "loc/imp3": "import_test_3",
        "base:import_test_4": "http://example.org/import_test_4",
        "http://example.org/import_test_4": "import_test_4",
        "types": "http://w3id.org/linkml/types",
    }
    output = as_json(SchemaLoader(fn, importmap=importmap).resolve())
    assert output == snapshot("import_test_1.json")
