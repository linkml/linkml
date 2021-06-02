import unittest

from rdflib import Graph, Namespace

from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml_runtime.linkml_model.meta import LINKML
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env

NS = Namespace('https://example.org/test/')

schema = f'''id: {NS}
enums:
  test_enum:
    permissible_values:
      a b:
'''


class Issue381TestCase(TestEnvironmentTestCase):
    """ Test URL generation w/ non-mangled values """
    env = env

    def test_non_url_pv(self):
        g = Graph()
        g.parse(data=RDFGenerator(schema).serialize(), format="ttl")
        self.assertEqual('https://example.org/test/a%20b', str(g.value(NS.test_enum, LINKML.permissible_values)))


if __name__ == '__main__':
    unittest.main()
