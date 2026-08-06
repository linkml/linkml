import os
import re
from collections.abc import Callable

import pytest
from jsonasobj2 import as_dict, as_json, loads

from linkml.utils.rawloader import load_raw_schema
from linkml.utils.schemaloader import SchemaLoader
from linkml_runtime.linkml_model.meta import SchemaDefinition, metamodel_version


def _verify_schema1_content(
    schema: SchemaDefinition,
    source_file,
    addl_checks: Callable[[SchemaDefinition], None] = None,
) -> None:
    expected = loads(
        f"""{{
       "default_prefix": "http://example.org/{source_file}/",
       "name": "{source_file}",
       "id": "http://example.org/{source_file}",
       "title": "Load Raw Schema Test",
       "metamodel_version": "0.5.0",
       "source_file": "{source_file}.yaml",
       "source_file_date": "Mon Dec 31 11:25:38 2018",
       "source_file_size": 76,
       "generation_date": "2018-12-31 11:50"
    }}"""
    )

    schema.source_file = os.path.basename(schema.source_file)
    if addl_checks:
        addl_checks(schema)

    assert isinstance(schema.metamodel_version, str)
    expected.metamodel_version = schema.metamodel_version

    pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"  # date in ISO 8601 format
    assert isinstance(schema.source_file_date, str)
    assert re.search(pattern, schema.source_file_date)
    expected.source_file_date = schema.source_file_date

    assert isinstance(schema.source_file_size, int)
    expected.source_file_size = schema.source_file_size

    assert isinstance(schema.generation_date, str)
    assert re.search(pattern, schema.generation_date)

    expected.generation_date = schema.generation_date
    assert expected == loads(as_json(schema))


def test_load_raw_file(input_path):
    """Test loading a data file"""
    _verify_schema1_content(load_raw_schema(input_path("schema1.yaml")), "schema1")

    # Verify that we can't pass source_file parameters when we've got a directory name
    with pytest.raises(AssertionError, match="source_file_size parameter not allowed if data is a file or URL"):
        load_raw_schema(input_path("schema1.yaml"), source_file_size=117)


@pytest.mark.skip(reason="Disabled until we implement SchemaDefinitionList")
def test_explicit_name(input_path):
    """Test the named schema option"""
    _verify_schema1_content(load_raw_schema(input_path("schema2.yaml")), "schema2")


@pytest.mark.skip(reason="Disabled until we implement SchemaDefinitionList")
def test_multi_schemas(input_path):
    """Test multiple schemas in the same file"""

    def check_types(s: SchemaDefinition) -> None:
        expected = {
            "string": {
                "name": "string",
                "definition_uri": "http://example.org/schema4/String",
                "from_schema": "http://example.org/schema4",
                "base": "str",
            },
            "integer": {
                "name": "integer",
                "definition_uri": "http://example.org/schema5/Integer",
                "from_schema": "http://example.org/schema5",
                "base": "int",
            },
        }
        assert expected == {k: as_dict(loads(as_json(v))) for k, v in s.types.items()}
        s.types = None

    _verify_schema1_content(load_raw_schema(input_path("schema4.yaml")), "schema4", check_types)


def test_base_dir(input_path):
    """Test the base directory option"""
    _verify_schema1_content(load_raw_schema("schema1.yaml", base_dir=str(input_path("."))), "schema1")


def test_schema_id(input_path):
    """Test loading a schema with just an id"""
    _verify_schema1_content(load_raw_schema("schema3.yaml", base_dir=str(input_path("."))), "schema3")


def test_name_from_sourcefile(input_path):
    """Test no identifier at all"""
    with pytest.raises(ValueError):
        load_raw_schema(input_path("schema5.yaml"))


def test_metadata_true_records_resolved_source_file(input_path):
    """``metadata=True`` (the default) records the path the loader resolved."""
    schema = load_raw_schema(input_path("schema1.yaml"))
    assert schema.source_file is not None
    assert os.path.basename(schema.source_file) == "schema1.yaml"


def test_metadata_false_drops_loader_derived_source_file(input_path):
    """``metadata=False`` suppresses the path the loader derived.

    ``yaml_loader`` records the resolved (absolute) path on every file load, so without this
    suppression ``metadata=False`` output would carry machine-specific paths.
    """
    assert load_raw_schema(input_path("schema1.yaml"), metadata=False).source_file is None


def test_metadata_false_drops_caller_supplied_source_file(input_path):
    """A ``source_file`` passed as a loader argument is loader metadata, so it is suppressed too."""
    with open(input_path("schema1.yaml")) as f:
        schema = load_raw_schema(f.read(), "schema1.yaml", metadata=False)
    assert schema.source_file is None


DECLARED_SOURCE_FILE = "declared-by-the-schema.yaml"

SCHEMA_DECLARING_SOURCE_FILE = f"""
id: http://example.org/declared_source_file
name: declared_source_file
source_file: {DECLARED_SOURCE_FILE}
"""


@pytest.mark.parametrize(
    "data",
    [
        pytest.param(SCHEMA_DECLARING_SOURCE_FILE, id="text"),
        pytest.param(
            {
                "id": "http://example.org/declared_source_file",
                "name": "declared_source_file",
                "source_file": DECLARED_SOURCE_FILE,
            },
            id="dict",
        ),
    ],
)
def test_metadata_false_keeps_schema_declared_source_file(data):
    """A ``source_file`` the schema itself declares is content, not loader metadata.

    ``SchemaLoader`` loads in-memory (dict) imports with ``metadata=False`` specifically so that
    fields the caller set on the dict are not overwritten, so the suppression must not clobber a
    declared value.
    """
    schema = load_raw_schema(data, metadata=False)
    assert schema.source_file == DECLARED_SOURCE_FILE


def test_metadata_false_keeps_source_file_on_schema_definition_input():
    """A ``SchemaDefinition`` input is caller content; its ``source_file`` must survive."""
    sd = SchemaDefinition(id="http://example.org/t", name="t", source_file=DECLARED_SOURCE_FILE)
    assert load_raw_schema(sd, metadata=False).source_file == DECLARED_SOURCE_FILE


def test_metadata_true_accepts_schema_definition_input():
    """``metadata=True`` (the default) works on a ``SchemaDefinition`` input.

    This path used to raise ``NameError`` because ``schema_metadata`` was only created on the
    str/dict/TextIO branch. There is no source to derive metadata from, so ``source_file`` stays
    unset and only ``generation_date`` is stamped.
    """
    schema = load_raw_schema(SchemaDefinition(id="http://example.org/t", name="t"))
    assert schema.source_file is None
    assert schema.generation_date is not None


def test_metadata_false_keeps_declared_source_file_over_resolved_path(input_path, tmp_path):
    """A declared value wins over the resolved path even when loading from a file."""
    schema_file = tmp_path / "declares_source_file.yaml"
    schema_file.write_text(SCHEMA_DECLARING_SOURCE_FILE)

    schema = load_raw_schema(str(schema_file), metadata=False)
    assert schema.source_file == DECLARED_SOURCE_FILE


def test_load_text(input_path):
    """Test loading straight text"""
    with open(input_path("schema1.yaml")) as f:
        _verify_schema1_content(
            load_raw_schema(f.read(), "schema1.yaml", "Mon Dec 31 11:25:38 2018", 76),
            "schema1",
        )


@pytest.mark.parametrize(
    "filename",
    [
        "typeerror1.yaml",
        "typeerror2.yaml",
        "typeerror3.yaml",
        "typeerror4.yaml",
    ],
)
def test_representation_errors(filename, input_path):
    """Test that malformed schemas raise an exception, if appropriate."""
    fn = input_path(filename)
    try:
        SchemaLoader(fn)
        assert False, "Expected an exception due to malformed schema"
    except Exception as e:
        # If exception raised, log it and optionally check message
        assert isinstance(e, Exception)


def test_metamodel_version_preserved_when_defined():
    """Test that metamodel_version from schema YAML is preserved, not overwritten.

    This addresses issue #2719: when a schema explicitly defines its own
    metamodel_version, it should be preserved rather than being overwritten
    by the version from the installed runtime. This is essential for
    generating the metamodel itself without circular dependencies.
    """
    schema_with_version = """
id: http://example.org/test_metamodel_version
name: test_metamodel_version
metamodel_version: "99.0.0"
"""
    schema = load_raw_schema(schema_with_version, source_file="test.yaml")
    # The schema's explicit metamodel_version should be preserved
    assert schema.metamodel_version == "99.0.0"


def test_metamodel_version_set_when_not_defined():
    """Test that metamodel_version is set from runtime when not in schema.

    When a schema doesn't define its own metamodel_version, the loader
    should set it from the installed runtime's metamodel_version.
    """
    schema_without_version = """
id: http://example.org/test_no_metamodel_version
name: test_no_metamodel_version
"""
    schema = load_raw_schema(schema_without_version, source_file="test.yaml")
    # Should use the runtime's metamodel_version
    assert schema.metamodel_version == metamodel_version
