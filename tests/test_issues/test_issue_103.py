import unittest

from rdflib import Graph


class Issue103TestCase(unittest.TestCase):

    @unittest.skipIf(True, "JSON-LD 1.1 Prefix Issue is still not resolved")
    def test_jsonld_prefix(self):
        test_json = '''
        {
            "@context": {
                "CHEBI": "http://purl.obolibrary.org/obo/CHEBI_",
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "@vocab": "http://example.org"
            },
            "CHEBI:33709": {
                "rdf:label": "Amino Acid"
            }
        }
        '''

        g = Graph().parse(data=test_json, format="json-ld", prefix=True)
        rdfstr = g.serialize(format="turtle").decode()
        assert '@prefix CHEBI: <http://purl.obolibrary.org/obo/CHEBI_>' in rdfstr

        g = Graph().parse(data=test_json, format="json-ld", prefix=False)
        rdfstr = g.serialize(format="turtle").decode()
        assert '@prefix CHEBI: <http://purl.obolibrary.org/obo/CHEBI_>' not in rdfstr


if __name__ == '__main__':
    unittest.main()
