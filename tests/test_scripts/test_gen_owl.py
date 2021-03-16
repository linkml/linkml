import re
import unittest

# This has to occur post ClickTestCase
from functools import reduce
from typing import List, Tuple

import click

from linkml.generators import owlgen
from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase

repl: List[Tuple[str, str]] = [
    (r'\s*meta:generation_date ".*" ;', 'meta:generation_date "Fri Jan 25 14:22:29 2019" ;'),
    (r'\s*meta:source_file_date ".*" ;', 'meta:source_file_date "Fri Jan 25 14:22:29 2019" ;')
]


def filtr(txt: str) -> str:
    return reduce(lambda s, expr: re.sub(expr[0], expr[1], s, flags=re.MULTILINE), repl, txt)


class GenOWLTestCase(ClickTestCase):
    testdir = "genowl"
    click_ep = owlgen.cli
    prog_name = "gen-owl"
    env = env

    def test_help(self):
        self.do_test("--help", 'help')

    def test_meta(self):
        self.do_test([], 'meta_owl.ttl', filtr=filtr, comparator=ClickTestCase.rdf_comparator)
        self.do_test('-f json-ld', 'meta_owl.jsonld', comparator=ClickTestCase.jsonld_comparator)
        self.do_test('-f n3', 'meta_owl.n3', filtr=filtr, comparator=ClickTestCase.n3_comparator)
        self.do_test('-f xsv', 'meta_error', expected_error=click.exceptions.BadParameter)


if __name__ == '__main__':
    unittest.main()
