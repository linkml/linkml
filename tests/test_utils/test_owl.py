import re
import unittest

from functools import reduce
from typing import List, Tuple

from rdflib import Graph

from linkml.generators.owlgen import OwlSchemaGenerator
from tests.test_utils.environment import env
from tests.utils.compare_rdf import compare_rdf
from tests.utils.test_environment import TestEnvironmentTestCase

repl: List[Tuple[str, str]] = [
    (r'\s*meta:generation_date ".*" ;', 'meta:generation_date "Fri Jan 25 14:22:29 2019" ;'),
    (r'\s*meta:source_file_date ".*" ;', 'meta:source_file_date "Fri Jan 25 14:22:29 2019" ;')
]


def filtr(txt: str) -> str:
    return reduce(lambda s, expr: re.sub(expr[0], expr[1], s, flags=re.MULTILINE), repl, txt)


class OWLTestCase(TestEnvironmentTestCase):
    env = env

    def test_cardinalities(self):
        self.env.generate_single_file('owl1.owl',
                                      lambda: OwlSchemaGenerator(env.input_path('owl1.yaml'),
                                                                 importmap=env.import_map).serialize(),
                                      filtr=filtr, comparator=compare_rdf, value_is_returned=True)

    def test_pred_types(self):
        self.env.generate_single_file('owl2.owl',
                                      lambda: OwlSchemaGenerator(env.input_path('owl2.yaml'),
                                                                 importmap=env.import_map).serialize(),
                                      filtr=filtr, comparator=compare_rdf, value_is_returned=True)


if __name__ == '__main__':
    unittest.main()
