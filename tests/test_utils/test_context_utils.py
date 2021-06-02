import unittest

from jsonasobj2 import JsonObj, loads

from linkml import METAMODEL_CONTEXT_URI, META_BASE_URI
from linkml_runtime.utils.context_utils import merge_contexts

json_1 = '{ "ex": "http://example.org/test/", "ex2": "http://example.org/test2/" }'
json_2 = '{ "foo": 17, "@context": { "ex": "http://example.org/test3/", "ex2": {"@id": "http://example.org/test4/" }}}'

context_output = """{
   "@context": [
      "file://local.jsonld",
      "https://w3id.org/linkml/meta.context.jsonld",
      {
         "ex": "http://example.org/test/",
         "ex2": "http://example.org/test2/"
      },
      {
         "ex": "http://example.org/test3/",
         "ex2": {
            "@id": "http://example.org/test4/"
         }
      }
   ]
}"""


class ContextUtilsTestCase(unittest.TestCase):
    def test_merge_contexts(self):
        self.assertIsNone(merge_contexts())
        self.assertEqual('file://local.jsonld', merge_contexts("local.jsonld")['@context'])
        self.assertEqual('file://local.jsonld', merge_contexts(["local.jsonld"])['@context'])
        self.assertEqual(METAMODEL_CONTEXT_URI, merge_contexts(METAMODEL_CONTEXT_URI)['@context'])
        self.assertEqual(METAMODEL_CONTEXT_URI, merge_contexts([METAMODEL_CONTEXT_URI])['@context'])
        self.assertEqual(JsonObj(ex='http://example.org/test/', ex2='http://example.org/test2/'),
                         merge_contexts(json_1)['@context'])
        self.assertEqual(JsonObj(ex='http://example.org/test/', ex2='http://example.org/test2/'),
                         merge_contexts([json_1])['@context'])
        self.assertEqual(JsonObj(ex='http://example.org/test3/', ex2=JsonObj(**{'@id': 'http://example.org/test4/'})),
                         merge_contexts(json_2)['@context'])
        self.assertEqual(JsonObj(ex='http://example.org/test3/', ex2=JsonObj(**{'@id': 'http://example.org/test4/'})),
                         merge_contexts([json_2])['@context'])
        self.assertEqual([f'file://local.jsonld',
                          'https://w3id.org/linkml/meta.context.jsonld',
                          JsonObj(ex='http://example.org/test/', ex2='http://example.org/test2/'),
                          JsonObj(ex='http://example.org/test3/', ex2=JsonObj(**{'@id': 'http://example.org/test4/'}))],
                         merge_contexts(["local.jsonld", METAMODEL_CONTEXT_URI, json_1, json_2])['@context'])
        self.assertEqual(loads(context_output),
                         merge_contexts(["local.jsonld", METAMODEL_CONTEXT_URI, json_1, json_2]))

        # Dups are not removed
        self.assertEqual(
            JsonObj(**{'@context': [JsonObj(ex='http://example.org/test/', ex2='http://example.org/test2/'),
                                    JsonObj(ex='http://example.org/test/', ex2='http://example.org/test2/')]}),
            merge_contexts([json_1, json_1]))
        self.assertEqual('file://local.jsonld', merge_contexts("local.jsonld")['@context'])

    def test_merge_contexts_base(self):
        self.assertEqual(
            JsonObj(**{'@context':
                           JsonObj(**{'@base': 'file://relloc'})}),
            merge_contexts(base='file://relloc'))
        self.assertEqual(loads(f'{{"@context": {{"@base": "{META_BASE_URI}"}}}}'), merge_contexts(base=META_BASE_URI))
        self.assertEqual(loads("""
{"@context": [
      "https://w3id.org/linkml/meta.context.jsonld",
      {
         "ex": "http://example.org/test/",
         "ex2": "http://example.org/test2/"
      },
      {
         "ex": "http://example.org/test3/",
         "ex2": {
            "@id": "http://example.org/test4/"
         }
      },
      {
         "@base": "https://w3id.org/linkml/"
      }
   ]
}"""), merge_contexts([METAMODEL_CONTEXT_URI, json_1, json_2], base=META_BASE_URI))


if __name__ == '__main__':
    unittest.main()
