import unittest

from rdflib import URIRef
from rdflib.namespace import SKOS

from linkml_runtime.utils.namespaces import Namespaces


class NamespacesTestCase(unittest.TestCase):
    def test_namespaces(self):
        ns = Namespaces()
        ns['meta'] = "https://w3id.org/biolink/metamodel/"
        ns.skos = SKOS
        self.assertEqual(str(ns.skos), str(SKOS))
        self.assertEqual(ns.skos.note, SKOS.note)
        ns.OIO = URIRef("http://www.geneontology.org/formats/oboInOwl")
        ns['dc'] = "http://example.org/dc/"  # Overrides 'dc' in semweb_context
        ns['l1'] = "http://example.org/subset/"
        ns['l2'] = "http://example.org/subset/test/"
        ns['l3'] = "http://example.org/subset/t"
        ns['u1'] = "urn:example:"
        # This is now a warning instead of a value error
        # with self.assertRaises(ValueError):
        #     ns['OIO'] = URIRef("http://www.geneontology.org/formats/another")
        # try:
        #     ns.OIO = URIRef("http://www.geneontology.org/formats/another")
        # except ValueError as e:
        #     self.assertEqual("Namespace OIO is already mapped to http://www.geneontology.org/formats/oboInOwl", str(e))
        with self.assertRaises(ValueError):
            ns["123"] = "http://example.org/foo/"

        with self.assertRaises(KeyError) as e:
            ns.FOO
        self.assertEqual("'foo'", str(e.exception), "Unknown namespace should raise a KeyError with a lower case entry")

        ns._default = ns['meta']
        ns._default = ns['meta']
        with self.assertRaises(ValueError):
            ns._default = "http://example.org/wrong/"
        del ns._default
        with self.assertRaises(KeyError):
            del ns._default
        self.assertIsNone(ns._default)
        ns._default = ns['meta']

        ns._base = "http://example.org/base/"
        ns._base = "http://example.org/base/"
        with self.assertRaises(ValueError):
            ns._base = "http://example.org/wrong/"
        del ns._base
        with self.assertRaises(KeyError):
            del ns._base
        ns._base = "http://example.org/wrong/"
        del ns._default
        ns.add_prefixmap('semweb_context')
        ns.add_prefixmap('monarch_context')
        self.assertEqual('https://monarchinitiative.org/', str(ns._default))
        del ns._default
        ns._default = ns['meta']
        self.assertEqual('l1:foo', ns.curie_for("http://example.org/subset/foo"))
        self.assertEqual('l2:foo', ns.curie_for("http://example.org/subset/test/foo"))
        self.assertEqual('l3:able/foo', ns.curie_for("http://example.org/subset/table/foo"))
        self.assertEqual('u1:foo', ns.curie_for("urn:example:foo"))
        with self.assertRaises(ValueError):
            ns.curie_for("1abc\junk")
        # no comment in skos?
        # self.assertEqual(SKOS.comment, ns.uri_for("skos:comment"))
        self.assertEqual(URIRef('http://example.org/dc/table'), ns.uri_for("dc:table"))
        self.assertEqual(ns.uri_for("http://something.org"), URIRef("http://something.org"))
        self.assertEqual('https://w3id.org/biolink/metamodel/Schema', str(ns.uri_for(":Schema")))
        self.assertEqual(URIRef('http://example.org/wrong/Base'), ns.uri_for("Base"))
        del ns._base
        with self.assertRaises(ValueError):
            ns.uri_for("Base")
        try:
            ns.uri_for("Base")
        except ValueError as e:
            self.assertEqual('Unknown CURIE prefix: @base', str(e))

        self.assertIsNone(ns.curie_for("http://google.com/test"))
        with self.assertRaises(ValueError):
            ns.uri_for("1abc:junk")

    def test_prefixmaps_integration(self):

        prefixmap_merged = Namespaces()
        prefixmap_merged.add_prefixmap('merged')
        self.assertGreater(len(prefixmap_merged), 3780)

        prefixmap_merged.add_prefixmap('monarch_context')
        self.assertGreater(len(prefixmap_merged), 3850)

        self.assertRaises(ValueError, prefixmap_merged.add_prefixmap, 'nonexistent_context')

        prefixmap_merged.add_prefixmap('bioregistry')
        self.assertGreater(len(prefixmap_merged), 3860)

        test_NCIT_curie = 'NCIT:C25300'
        test_NCIT_uri = URIRef('http://purl.obolibrary.org/obo/NCIT_C25300')
        self.assertEqual(prefixmap_merged.curie_for(test_NCIT_uri), test_NCIT_curie)
        self.assertEqual(prefixmap_merged.uri_for(test_NCIT_curie), test_NCIT_uri)

    def test_prefix_suffix(self):
        ns = Namespaces()
        ns['farm'] = 'https://example.org/farm'
        ns['farm_slash'] = 'https://slash.org/farm/'

        self.assertEqual(('farm', 'cow'), ns.prefix_suffix('farm:cow'))
        self.assertEqual(('farm', '/cow'), ns.prefix_suffix('https://example.org/farm/cow'))
        self.assertEqual(('farm_slash', 'cow'), ns.prefix_suffix('https://slash.org/farm/cow'))
        self.assertEqual(('farm_slash', 'cow/horns'), ns.prefix_suffix('farm_slash:cow/horns'))
        self.assertEqual(('farm', '/cow/horns'), ns.prefix_suffix('farm:/cow/horns'))
        self.assertEqual(('farm', '#cow/horns'), ns.prefix_suffix('farm:#cow/horns'))
        self.assertEqual(('farm', ''), ns.prefix_suffix('farm:'))
        self.assertEqual(('', 'cow'), ns.prefix_suffix(':cow'))
        self.assertEqual((None, None), ns.prefix_suffix('https://missing-prefix.org/farm/cow'))


if __name__ == '__main__':
    unittest.main()
