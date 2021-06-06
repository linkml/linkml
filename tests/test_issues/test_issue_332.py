import unittest

from jsonasobj2 import loads, JsonObj, as_json

from linkml.generators.jsonldgen import JSONLDGenerator
from tests.test_issues.environment import env


class JSONContextTestCase(unittest.TestCase):
    def test_context(self):
        """ Test no context in the argument"""
        json_ld = JSONLDGenerator(env.input_path('issue_332.yaml')).serialize()
        json_ld_obj = loads(json_ld)
        expected = JsonObj([
            "https://w3id.org/linkml/meta.context.jsonld",
            {
              "meta": "https://w3id.org/linkml/",
              "test14": "https://example.com/test14/",
              "@vocab": "https://example.com/test14/"
            },
            {
              "@base": "https://example.com/test14/"
            }
          ]
        )
        self.assertEqual(as_json(expected), as_json(json_ld_obj['@context']))

    def test_context_2(self):
        """ Test a single context argument """
        json_ld = JSONLDGenerator(env.input_path('issue_332.yaml')).\
            serialize(context="http://some.org/nice/meta.context.jsonld")
        json_ld_obj = loads(json_ld)
        expected = JsonObj([
               "http://some.org/nice/meta.context.jsonld",
               {
                  "@base": "https://example.com/test14/"
               }
            ]
        )
        self.assertEqual(as_json(expected), as_json(json_ld_obj['@context']))

    def test_context_3(self):
        """ Test multi context arguments """
        json_ld = JSONLDGenerator(env.input_path('issue_332.yaml')).\
            serialize(context=["http://some.org/nice/meta.context.jsonld", "http://that.org/meta.context.jsonld"])
        json_ld_obj = loads(json_ld)
        expected = JsonObj([
               "http://some.org/nice/meta.context.jsonld",
               "http://that.org/meta.context.jsonld",
               {
                  "@base": "https://example.com/test14/"
               }
            ]
        )
        self.assertEqual(as_json(expected), as_json(json_ld_obj['@context']))


if __name__ == '__main__':
    unittest.main()
