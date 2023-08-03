# MetadataProfile
from collections import namedtuple

import pytest
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.loaders import yaml_loader

import tests.test_issues.model.issue_1104_classes
from linkml.generators.linkmlgen import LinkmlGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.utils.sqlutils import SQLStore
from tests.test_issues.model.issue_1104_classes import Database


@pytest.fixture
def paths(input_path, tmp_path):
    Paths = namedtuple("Paths", ["SCHEMA", "DATA", "DB"])
    return Paths(
        SCHEMA=input_path("issue_1104_schema.yaml"),
        DATA=input_path("issue_1104_data.yaml"),
        DB=str(tmp_path / "issue_1104_data.db"),
    )


def test_view(paths):
    schemaview = SchemaView(paths.SCHEMA)
    assert schemaview.schema.name == "was_associated_with"


def test_generated(paths):
    generator = LinkmlGenerator(paths.SCHEMA, format="yaml")
    generated = generator.serialize()
    assert generated


def test_schema_owl(paths):
    generated = OwlSchemaGenerator(
        paths.SCHEMA,
        mergeimports=False,
        metaclasses=False,
        type_objects=False,
        ontology_uri_suffix=".owl.ttl",
    ).serialize()
    assert generated


def test_load_yaml(paths):
    ly = yaml_loader.load(paths.DATA, Database)  # instantiates Database
    assert ly


def test_dump_json(paths):
    # log = logging.getLogger("TestActivityAgent.test_schema_ttl")
    ly = yaml_loader.load(paths.DATA, Database)
    json_dumper.dumps(ly)  # creates a JSON string
    # log.warning(jd)


def test_prepare_dump_sqlite(paths):
    endpoint = SQLStore(paths.SCHEMA, database_path=paths.DB, include_schema_in_database=False)
    endpoint.native_module = tests.test_issues.model.issue_1104_classes
    endpoint.db_exists(force=True)
    endpoint.compile()
    yaml_loader.load(paths.DATA, target_class=Database)
    endpoint.engine.dispose()


def test_do_dump_sqlite(paths):
    endpoint = SQLStore(paths.SCHEMA, database_path=paths.DB, include_schema_in_database=False)
    endpoint.native_module = tests.test_issues.model.issue_1104_classes
    endpoint.db_exists(force=True)
    endpoint.compile()
    database: Database = yaml_loader.load(paths.DATA, target_class=Database)
    endpoint.dump(database)
    endpoint.engine.dispose()
