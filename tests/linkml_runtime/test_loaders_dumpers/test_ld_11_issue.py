import json
import unittest
from typing import Union, Dict, List

import pyld
from rdflib import Namespace, Graph, SKOS

OBO = Namespace("http://purl.obolibrary.org/obo/")
NCIT = Namespace("http://purl.obolibrary.org/obo/NCI_")
TERMCI = Namespace("https://hotecosystem.org/termci/")

# Conversion to json-ld: https://tinyurl.com/yyw2ktyf
# Reverse conversion: https://tinyurl.com/y6fo3clj

input_json = {
    "@type": "Package",
    "system": [
        {
            "namespace": "http://purl.obolibrary.org/obo/",
            "contents": [
                {
                    "uri": "ncit:C147557",
                    "label": "Stuff"
                }
            ]
        }
    ]
}

context = {
    "@context": {
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "obo": "https://purl.obolibrary.org/obo/",
        "termci": "https://hotecosystem.org/termci/",
        "ncit": {
            "@id": "http://purl.obolibrary.org/obo/NCI_",
            "@prefix": True
        },
        "system": {
            "@type": "@id",
            "@id": "termci:system",
            "@container": "@set",
            "@context": {
                "@id": "skos:ConceptScheme",
                "@context": {
                    "namespace": "@id",
                    "contents": {
                        "@type": "@id",
                        "@id": "skos:hasConcept",
                        "@container": "@set",
                        "@context": {
                            "uri": "@id",
                            "label": "skos:label"
                        }
                    }
                }
            }
        }
    },
    "@type": "https://hotecosystem.org/termci/Package"
}


class PYLDTestCase(unittest.TestCase):

    def _as_json_str(self, json_obj: Union[str, Dict, List]) -> str:
        """ Convert json_obj to a string with all ld stuff removed"""
        def strip_cruft(entry: Dict) -> Dict:
            for k, v in list(entry.items()):
                if k.startswith('@'):
                    del(entry[k])
                elif isinstance(v, dict):
                    strip_cruft(v)
                elif isinstance(v, list):
                    entry[k] = [strip_cruft(e) for e in v]
            return entry

        if isinstance(json_obj, str):
            json_obj = json.loads(json_obj)

        if isinstance(json_obj, list):
            json_obj = [strip_cruft(e) for e in json_obj]
        else:
            json_obj = strip_cruft(json_obj)
        return json.dumps(json_obj, indent='  ')


    @unittest.skipIf(True, "uri will load as namespace until JSONLD 1.1 is working")
    def test_rdf_frame(self):
        options = dict(expandContext=context, base=str(TERMCI))

        # Start with system 'namespace' and contents 'uri'
        self.assertTrue('namespace' in input_json['system'][0])
        self.assertTrue('uri' in input_json['system'][0]['contents'][0])

        # Take the vanilla JSON and convert it to RDF
        expanded = pyld.jsonld.expand(input_json, options=options)
        g = Graph()
        g.bind('skos', SKOS)
        g.bind('termci', TERMCI)
        g.bind('obo', OBO)
        g.bind('ncit', NCIT)
        g.parse(data=json.dumps(expanded), format='json-ld')
        # Converting JSON to RDF works correctly
        #   In particular, "namespace" maps to "obo:" and "uri" maps to "ncit:C147557"
        print('=' * 40)
        print(g.serialize(format='ttl').decode())
        print()
        print('-' * 40)

        # Convert the RDF back into vanilla JSON
        output_json = pyld.jsonld.frame(expanded, context, options=options)
        print(self._as_json_str(output_json))

        # Observe that system.contents.uri has changed to system.contents.namespace
        self.assertTrue('namespace' in output_json['system'][0])
        self.assertTrue('uri' in output_json['system'][0]['contents'][0])


if __name__ == '__main__':
    unittest.main()
