import unittest

from linkml_runtime.utils.yamlutils import as_yaml

from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.markdowngen import MarkdownGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.utils.schemaloader import SchemaLoader
from tests.test_issues.environment import env
from tests.utils.compare_rdf import compare_rdf
from tests.utils.filters import json_metadata_filter, yaml_filter
from tests.utils.python_comparator import compare_python
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue167TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_167(self):
        """Test extensions to the four basic types"""
        env.generate_single_file(
            "issue_167.yaml",
            lambda: as_yaml(SchemaLoader(env.input_path("issue_167.yaml")).resolve()),
            value_is_returned=True,
            filtr=yaml_filter,
        )

    def test_issue_167b_yaml(self):
        """Annotations yaml example"""
        env.generate_single_file(
            "issue_167b.yaml",
            lambda: as_yaml(
                SchemaLoader(
                    env.input_path("issue_167b.yaml"), importmap=env.import_map
                ).resolve()
            ),
            value_is_returned=True,
            filtr=yaml_filter,
        )

    def test_issue_167b_python(self):
        """Annotations python example"""
        env.generate_single_file(
            "issue_167b.py",
            lambda: PythonGenerator(
                env.input_path("issue_167b.yaml"),
                importmap=env.import_map,
                emit_metadata=False,
            ).serialize(),
            comparator=lambda exp, act: compare_python(
                exp, act, self.env.expected_path("issue_167b.py")
            ),
            value_is_returned=True,
        )
        env.generate_single_file(
            "issue_167b2.py",
            lambda: PythonGenerator(
                env.input_path("issue_167b.yaml"),
                importmap=env.import_map,
                mergeimports=False,
                emit_metadata=False,
            ).serialize(),
            comparator=lambda exp, act: compare_python(
                exp, act, self.env.expected_path("issue_167b_nomerged.py")
            ),
            value_is_returned=True,
        )

    @unittest.skip("skipped during refactor: https://github.com/linkml/linkml/pull/924")
    def test_issue_167b_json(self):
        env.generate_single_file(
            "issue_167b.json",
            lambda: JSONLDGenerator(
                env.input_path("issue_167b.yaml"),
            ).serialize(),
            filtr=json_metadata_filter,
            value_is_returned=True,
        )

    @unittest.skip("Stopped working during refactor -- to hard to debug")
    def test_issue_167b_rdf(self):
        env.generate_single_file(
            "issue_167b.ttl",
            lambda: RDFGenerator(
                env.input_path("issue_167b.yaml"), importmap=env.import_map
            ).serialize(),
            comparator=compare_rdf,
            value_is_returned=True,
        )


if __name__ == "__main__":
    unittest.main()
