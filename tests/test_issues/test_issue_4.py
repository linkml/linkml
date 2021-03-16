import unittest

from jsonasobj import loads

from linkml.generators.shexgen import ShExGenerator
from includes.types import METATYPE
from tests.test_issues.environment import env


class UriTypeTestCase(unittest.TestCase):
    def test_uri_type(self):
        """ URI datatype should map to ShEx URI instead of NONLITERAL """
        shex = loads(ShExGenerator(env.types_yaml, format='json').serialize())
        uri_shape = [s for s in shex.shapes if s.id == str(METATYPE.Uri)]
        self.assertEqual(1, len(uri_shape))
        self.assertEqual('iri', uri_shape[0].nodeKind)


if __name__ == '__main__':
    unittest.main()
