import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml.validators.sparqlvalidator import SparqlDataValidator
from tests.test_validation.environment import env
from tests import SKIP_REMOTE_SPARQL_TESTS


SCHEMA = env.input_path('omo.yaml')
REPORT = env.expected_path('omo-report.yaml')

NGS = [
    '<http://purl.obolibrary.org/obo/merged/OBI>',
    '<http://purl.obolibrary.org/obo/merged/GO>'
]
class RemoteSparqlValidatorTestCase(unittest.TestCase):

    def test_remote_sparql_validation(self):
        """ Validate a schema  """
        sv = SparqlDataValidator()
        sv.load_schema(SCHEMA)
        if SKIP_REMOTE_SPARQL_TESTS:
            print(f'Skipping ontobee test')
        else:
            results = sv.validate_endpoint('http://sparql.hegroup.org/sparql', named_graphs=NGS)
            print(results)
            yaml_dumper.dump(results, to_file=REPORT)








if __name__ == '__main__':
    unittest.main()
