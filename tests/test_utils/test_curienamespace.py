import unittest

from rdflib import URIRef

from linkml_runtime.utils.curienamespace import CurieNamespace


class CurieNamespaceTestCase(unittest.TestCase):
    def test_basics(self):
        BFO = CurieNamespace('bfo', "http://purl.obolibrary.org/obo/BFO_")
        self.assertEqual(URIRef("http://purl.obolibrary.org/obo/BFO_test"), BFO.test)
        self.assertEqual("http://purl.obolibrary.org/obo/BFO_", BFO)
        self.assertEqual("bfo:test", BFO.curie('test'))
        self.assertEqual("bfo:", BFO.curie())

    @unittest.expectedFailure
    def test_curie_as_curie(self):
        """ "curie can't be a local name at the moment" """
        BFO = CurieNamespace('bfo', "http://purl.obolibrary.org/obo/BFO_")
        self.assertEqual("bfo:curie", BFO.curie)

if __name__ == '__main__':
    unittest.main()
