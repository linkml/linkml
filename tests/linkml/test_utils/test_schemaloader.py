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
        "child/index",
        "child/grandchild/index",
        "child/grandchild/greatgrandchild/index",
    ]


@pytest.mark.parametrize(
    ("file", "error"),
    [
        (
            "loadererror1.yaml",
            r'loadererror1.yaml", line 11, col 13 slot: s1 - unrecognized domain \(foo\)',
        ),
        ("loadererror2.yaml", 'type "string" does not declare a URI'),
        (
            "loadererror2a.yaml",
            "slot: s1 - key and identifier slots cannot be optional",
        ),
        (
            "loadererror4.yaml",
            'loadererror4.yaml", line 6, col 17 Default prefix: foo is not defined',
        ),
        (
            "loadererror5.yaml",
            r'type "phenotype" must declare a type base or parent \(typeof\)',
        ),
        ("loadererror6.yaml", "multiple keys/identifiers not allowed"),
        ("loadererror7.yaml", "multiple keys/identifiers not allowed"),
        (
            "loadererror8.yaml",
            "A slot cannot be both a key and identifier at the same time",
        ),
        (
            "loadererror9.yaml",
            "A slot cannot be both a key and identifier at the same time",
        ),
        ("loadererror10.yaml", 'type "string" does not declare a URI'),
        (
            "loadererror11.yaml",
            'loadererror11.yaml", line 22, col 16 Subset: sss1 is not defined',
        ),
    ],
)
def test_error_paths(input_path, file: str, error: str) -> None:
    """Test various loader error situations."""
    with pytest.raises(ValueError, match=error):
        SchemaLoader(input_path(file)).resolve()


def test_infer_slot_range_from_default(input_path):
    fn = input_path("loadertest1.yaml")
    schema = SchemaLoader(fn).resolve()
    assert "string" == schema.slots["s1"].range


def test_type_definition_ok(input_path):
    """A type with either a typeof or uri is OK."""
    fn = input_path("loaderpass11.yaml")
    schema = SchemaLoader(fn).resolve()
    assert set(schema.types) == {"string", "bstring"}
    assert schema.types["bstring"].base == schema.types["string"].base
    assert schema.types["bstring"].uri == schema.types["string"].uri
    assert schema.types["bstring"].typeof == "string"
    assert schema.types["string"].typeof is None


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
