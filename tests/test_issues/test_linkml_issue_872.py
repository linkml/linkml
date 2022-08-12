import json
import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition

from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.yamlgen import YAMLGenerator
from linkml.utils.schema_builder import SchemaBuilder
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue872Case(TestEnvironmentTestCase):
    """
    Tests https://github.com/linkml/linkml/issues/872
    """

    env = env

    def test_monotonic(self):
        """
        Ensure that a schema which uses attributes can be successfully translated to JSONLD.

        Currently this requires a second pass of the schema through schema loader, after mangled
        names are already introduced
        """
        sb = SchemaBuilder()
        sb.add_class(
            "C",
            [SlotDefinition("s1", description="d1")],
            use_attributes=True,
            from_schema="http://x.org",
        )
        sb.add_defaults()
        schema = sb.schema
        s = JSONLDGenerator(schema).serialize()
        self.assertIsNotNone(s)


if __name__ == "__main__":
    unittest.main()
