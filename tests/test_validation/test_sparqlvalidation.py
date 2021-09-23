import unittest

from linkml.generators.sparqlgen import SparqlGenerator
from linkml.validators.sparqlvalidator import SparqlDataValidator
from tests.test_validation.environment import env

SCHEMA = env.input_path('kitchen_sink.yaml')
DATA = env.input_path('kitchen_sink_inst_01.ttl')




class SparqlValidatorTestCase(unittest.TestCase):

    # rdflib bug on parsing sparql queries
    @unittest.skip
    def test_sparql_validation(self):
        """ Validate using in-memory sparql  """
        print(f'TEST: Loading {SCHEMA}')
        sg = SparqlGenerator(SCHEMA)
        print(sg.queries)
        print(f'Making validator {SCHEMA}')
        sv = SparqlDataValidator()
        sv.load_schema(SCHEMA)
        results = sv.validate_file(DATA)
        print(results)

if __name__ == '__main__':
    unittest.main()
