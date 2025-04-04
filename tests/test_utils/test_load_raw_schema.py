import os
import re
from typing import Callable

import pytest
from jsonasobj2 import as_dict, as_json, loads
from linkml_runtime.linkml_model.meta import SchemaDefinition

from linkml.utils.rawloader import load_raw_schema
from linkml.utils.schemaloader import SchemaLoader


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
