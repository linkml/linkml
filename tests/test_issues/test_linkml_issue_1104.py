import logging
import unittest

from linkml.generators.linkmlgen import LinkmlGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
# MetadataProfile
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.loaders import yaml_loader

import tests.test_issues.model.issue_1104_classes
from tests.test_issues.model.issue_1104_classes import Database
from tests.test_issues.environment import env
from linkml.utils.sqlutils import SQLStore

SCHEMA = env.input_path("issue_1104_schema.yaml")
DATA = env.input_path("issue_1104_data.yaml")
DB = env.expected_path("issue_1104_data.db")


class TestActivityAgent(unittest.TestCase):
    def test_view(self):
        schemaview = SchemaView(SCHEMA)
        assert schemaview.schema.name == "was_associated_with"

    def test_generated(self):
        generator = LinkmlGenerator(SCHEMA, format='yaml')
        generated = generator.serialize()
        assert generated

    def test_schema_owl(self):
        generated = OwlSchemaGenerator(
            SCHEMA,
            mergeimports=False,
            metaclasses=False,
            type_objects=False,
            ontology_uri_suffix=".owl.ttl",
        ).serialize()
        assert generated

    def test_load_yaml(self):
        ly = yaml_loader.load(DATA, Database)  # instantiates Database
        assert ly

    def test_dump_json(self):
        # log = logging.getLogger("TestActivityAgent.test_schema_ttl")
        ly = yaml_loader.load(DATA, Database)
        jd = json_dumper.dumps(ly)  # creates a JSON string
        # log.warning(jd)

    def test_prepare_dump_sqlite(self):
        endpoint = SQLStore(SCHEMA, database_path=DB, include_schema_in_database=False)
        endpoint.native_module = tests.test_issues.model.issue_1104_classes
        endpoint.db_exists(force=True)
        endpoint.compile()
        database: Database = yaml_loader.load(DATA, target_class=Database)

    def test_do_dump_sqlite(self):
        endpoint = SQLStore(SCHEMA, database_path=DB, include_schema_in_database=False)
        endpoint.native_module = tests.test_issues.model.issue_1104_classes
        endpoint.db_exists(force=True)
        endpoint.compile()
        database: Database = yaml_loader.load(DATA, target_class=Database)
        endpoint.dump(database)
