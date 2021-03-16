import os
import re
import unittest
# This has to occur post ClickTestCase
from functools import reduce
from typing import List, Tuple
from urllib.parse import urljoin

import click

from linkml import LOCAL_METAMODEL_LDCONTEXT_FILE
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators import rdfgen
from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase
from tests.utils.filters import ldcontext_metadata_filter

repl1: List[Tuple[str, str]] = [
    (r'(\s*):generation_date\s*".*"\^\^xsd:dateTime', r'\1:generation_date "2019-01-25 12:34"^^xsd:dateTime'),
    (r'(\s*):source_file_date\s*".*"\^\^xsd:dateTime', r'\1:source_file_date "2019-01-25 12:34"^^xsd:dateTime'),
    (r'(\s*):source_file_size\s*[0-9]+', r'\1:source_file_size 10000'),
]


def filtr(txt: str) -> str:
    return reduce(lambda s, expr: re.sub(expr[0], expr[1], s, flags=re.MULTILINE), repl1, txt)


class GenRDFTestCase(ClickTestCase):
    testdir = "genrdf"
    click_ep = rdfgen.cli
    prog_name = "gen-rdf"
    env = env

    def test_help(self):
        self.do_test("--help", 'help')

    def _gen_context_file(self, fname: str, metauris: bool = False) -> str:
        cntxt_txt = ldcontext_metadata_filter(ContextGenerator(env.meta_yaml, useuris=not metauris,
                                                               importmap=env.import_map).serialize())
        cntxt_file_path = self.expected_file_path(fname)
        if os.path.exists(cntxt_file_path):
            with open(cntxt_file_path) as f:
                expected = ldcontext_metadata_filter(f.read())
        else:
            expected = ''
        if expected != cntxt_txt:
            with open(cntxt_file_path, 'w') as f:
                f.write(cntxt_txt)
        return urljoin('file:', cntxt_file_path)

    def test_meta(self):
        """ Test the RDF generator on the metamodel """

        # Build the input contexts
        meta_context_path = self._gen_context_file('meta_context_rdf.jsonld')
        meta_contextn_path = self._gen_context_file('meta_contextn_rdf.jsonld')

        self.do_test(f"--context {meta_context_path}", 'meta.ttl', filtr=filtr,
                     comparator=ClickTestCase.rdf_comparator)
        self.do_test(f"--context {meta_contextn_path} --metauris", 'metan.ttl', filtr=filtr,
                     comparator=ClickTestCase.rdf_comparator)
        self.do_test(f'-f n3  --context {meta_context_path}', 'meta.n3', filtr=filtr,
                     comparator=ClickTestCase.rdf_comparator)
        self.do_test(f'-f xsv  --context {meta_context_path}', 'meta_error',
                     expected_error=click.exceptions.BadParameter)

    def test_make_script(self):
        """ Test a relative file path in JSON """
        self.do_test(f"--context {LOCAL_METAMODEL_LDCONTEXT_FILE}",
                     'make_output.ttl', filtr=filtr, comparator=ClickTestCase.rdf_comparator)


if __name__ == '__main__':
    unittest.main()
