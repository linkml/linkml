import unittest

from rdflib import Graph

from linkml.generators.rdfgen import RDFGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path("kitchen_sink.yaml")
RDF_OUTPUT = env.expected_path("kitchen_sink.ttl")

JSONLD = """
{
  "slots": [
    {
      "name": "type",
      "slot_uri": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    }
  ],
  "@context": [
  {
      "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
      "@vocab": "https://w3id.org/linkml/",
      "slot_uri": {
         "@type": "@id"
      }
    }
  ]
}"""


class RdfGeneratorTestCase(unittest.TestCase):
    @unittest.skip("TODO")
    def test_rdfgen(self):
        """rdf"""
        s = RDFGenerator(SCHEMA, mergeimports=False).serialize()
        with open(RDF_OUTPUT, "w") as stream:
            stream.write(s)
        g = Graph()
        g.parse(RDF_OUTPUT, format="turtle")

    @unittest.skip("TODO")
    def test_rdf_type_in_jsonld(self):
        graph = Graph()
        graph.parse(data=JSONLD, format="json-ld", prefix=True)
        ttl_str = graph.serialize(format="turtle").decode()
        graph.parse(data=ttl_str, format="turtle")


if __name__ == "__main__":
    unittest.main()
