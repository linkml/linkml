
import unittest

from linkml.generators.rdfgen import RDFGenerator
from tests.test_issues.environment import env
from tests.utils.compare_rdf import compare_rdf
from tests.utils.test_environment import TestEnvironmentTestCase


class NamespaceIssueTestCase(TestEnvironmentTestCase):
    env = env

    # TODO: Find out why test_issue_namespace is emitting generation_date in the TYPE namespace
    def test_namespace(self):
        context = "https://biolink.github.io/biolink-model/context.jsonld"
        env.generate_single_file('issue_namespace.ttl',
                                 lambda: RDFGenerator(env.input_path('issue_namespace.yaml')).serialize(context=context),
                                 comparator=compare_rdf, value_is_returned=True)


if __name__ == '__main__':
    unittest.main()
