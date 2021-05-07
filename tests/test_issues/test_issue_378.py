import unittest

from jsonasobj2 import loads

from linkml.generators.jsonldcontextgen import ContextGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase

without_default = """
id: http://example.org/sssom/schema/
name: sssom
imports:
- linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  sssom: https://w3id.org/sssom/
  dcterms: http://purl.org/dc/terms/
default_curi_maps:
- semweb_context

slots:
  name:
    range: string
"""

with_default = """
id: http://example.org/sssom/schema/
name: sssom
imports:
- linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  sssom: https://w3id.org/sssom/
  dcterms: http://purl.org/dc/terms/
default_curi_maps:
- semweb_context
default_prefix: sssom

slots:
  name:
    range: string
"""


class Issue378TestCase(TestEnvironmentTestCase):
    """ This test case should (eventually) be used to address some of the questions raised in issue #378.  At the
    moment it just confirms the existing behavior. """
    env = env

    def test_default_vocab(self):
        json_ld_text = ContextGenerator(without_default).serialize()
        json_ld = loads(json_ld_text)
        self.assertEqual('http://example.org/sssom/schema/', json_ld['@context']['@vocab'])
        self.assertEqual('http://example.org/sssom/schema/name', json_ld['@context']['name']['@id'])
        json_ld_text2 = ContextGenerator(with_default).serialize()
        json_ld2 = loads(json_ld_text2)
        self.assertEqual('https://w3id.org/sssom/', json_ld2['@context']['@vocab'])
        self.assertNotIn('name', json_ld2['@context']['@vocab'])


if __name__ == '__main__':
    unittest.main()
