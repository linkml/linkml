import os
import unittest
from contextlib import redirect_stdout


from linkml.generators.sparqlgen import SparqlGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path('kitchen_sink.yaml')
DIR = env.expected_path('kitchen_sink_sparql')
SPARQL = env.expected_path('kitchen_sink.rq')


class SparqlGeneratorTestCase(unittest.TestCase):

    def test_sparqlgen(self):
        """ Generate java classes  """
        gen = SparqlGenerator(SCHEMA)
        sparql = gen.serialize(directory=DIR)
        print(sparql)




if __name__ == '__main__':
    unittest.main()
