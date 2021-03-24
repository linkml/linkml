import os
import sys
import unittest
from dataclasses import dataclass
from typing import List, Optional, Union, Tuple, Set

import requests

from rdflib import Namespace, URIRef

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    print(sys.path)

from tests import SKIP_REWRITE_RULES, SKIP_REWRITE_RULES_REASON

W3ID_SERVER = "https://w3id.org/"
DEFAULT_SERVER = W3ID_SERVER
# DEFAULT_SERVER = "http://localhost:8091/"
# SKIP_REWRITE_RULES = False

# Taken from Firefox network.http.accept.default
default_header = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
github_io = "https://linkml.github.io/"


@dataclass
class TestEntry:
    input_url: Union[str, URIRef, Namespace]
    expected_url: str
    accept_header: Optional[str] = None


def build_test_entry_set(input_url: Namespace, model: str) -> List[TestEntry]:
    return [
        TestEntry(input_url, f'includes/{model}'),
        TestEntry(input_url, f'includes/{model}.yaml', 'text/yaml'),
        TestEntry(input_url, f'includes/{model}.ttl', 'text/turtle'),
        TestEntry(input_url, f'includes/{model}.jsonld', 'application/json'),
        TestEntry(input_url, f'includes/{model}.shex', 'text/shex'),
        TestEntry(input_url['.context.jsonld'], f'includes/{model}.context.jsonld'),
        TestEntry(input_url['.owl'], f'includes/{model}.owl'),
        TestEntry(input_url['/'], f'includes/{model}/')
    ]


class TestLists:
    def __init__(self, server: str) -> None:
        if not server.endswith(('#', '/')):
            server += '/'
        self.linkml = server + 'linkml/'
        self.types = Namespace(self.linkml + 'types')
        self.mappings = Namespace(self.linkml + 'mappings')
        self.extensions = Namespace(self.linkml + 'extensions')
        self.annotations = Namespace(self.linkml + 'annotations')
        self.metas = Namespace(self.linkml + 'meta')
        self.type = Namespace(self.linkml + 'type/')
        self.mapping = Namespace(self.linkml + 'mapping/')
        self.meta = Namespace(self.linkml + 'meta/')

        self.meta_entries: List[TestEntry] = []

        self.meta_entries += build_test_entry_set(self.types, 'types')
        self.meta_entries += build_test_entry_set(self.mappings, 'mappings')
        self.meta_entries += build_test_entry_set(self.extensions, 'extensions')
        self.meta_entries += build_test_entry_set(self.annotations, 'annotations')

        self.vocab_entries: List[TestEntry] = [
            TestEntry(self.type['index'], 'docs/types/index'),
            TestEntry(self.type.Element, 'docs/types/Element.yaml', 'text/yaml'),
            TestEntry(self.type.Element, 'docs/types/Element.ttl', 'text/turtle'),
            TestEntry(self.type.slots, 'docs/types/slots.jsonld', 'application/json'),
            TestEntry(self.mapping['index'], 'docs/mappings/index')
        ]

        self.meta_model_entries: List[TestEntry] = [
            TestEntry(self.metas, 'meta'),
            TestEntry(self.metas, 'meta.yaml', 'text/yaml'),
            TestEntry(self.metas, 'meta.ttl', 'text/turtle'),
            TestEntry(self.metas, 'meta.jsonld', 'application/json'),
            TestEntry(self.metas, 'meta.shex', 'text/shex'),
            TestEntry(self.metas['.owl'], 'meta.owl'),
            TestEntry(self.metas['.foo'], 'meta.foo'),
            TestEntry(self.linkml + 'context.jsonld', 'context.jsonld'),
            TestEntry(self.linkml + 'contextn.jsonld', 'contextn.jsonld')
        ]
        self.meta_vocab_entries: List[TestEntry] = [
            TestEntry(self.meta.Element, 'docs/Element'),
            TestEntry(self.meta.slot, 'docs/slot'),
            TestEntry(self.meta.Element, 'docs/Element.yaml', 'text/yaml'),
            TestEntry(self.meta.Element, 'docs/Element.ttl', 'text/turtle'),
            TestEntry(self.meta.Element, 'docs/Element.jsonld', 'application/json'),
            TestEntry(self.meta.Element, 'docs/Element.shex', 'text/shex'),
            TestEntry(self.meta.Element, 'docs/Element', 'text/foo'),
        ]


FAIL_ON_ERROR = True


@unittest.skipIf(SKIP_REWRITE_RULES, SKIP_REWRITE_RULES_REASON)
class RewriteRuleTestCase(unittest.TestCase):
    SERVER = DEFAULT_SERVER         # Can be overwritten with a startup parameter
    results: Set[Tuple[str, str, str]] = None

    @classmethod
    def setUpClass(cls):
        cls.tests = TestLists(cls.SERVER)
        print(f"Server: {cls.SERVER}")
        cls.results = set()   # from, to, format

    @classmethod
    def tearDownClass(cls):
        print()
        for from_url, to_url, hdr in sorted(list(cls.results)):
            fmt = '' if hdr == 'text/html' else f" ({hdr})"
            if DEFAULT_SERVER != W3ID_SERVER:
                from_url = from_url.replace(DEFAULT_SERVER, W3ID_SERVER)
            print(f"{from_url}{fmt} - {to_url}")

    def record_results(self, from_url: str, accept_header, to_url: str) -> None:
        self.results.add((from_url, to_url, accept_header.split(',')[0]))

    def rule_test(self, entries: List[TestEntry]) -> None:

        def test_it(e: TestEntry, accept_header: str) -> bool:
            expected = github_io + e.expected_url
            resp = requests.head(e.input_url, headers={'accept': accept_header}, verify=False)

            # w3id.org uses a 301 to go from http: to https:
            if resp.status_code == 301 and 'location' in resp.headers:
                resp = requests.head(resp.headers['location'], headers={'accept': accept_header}, verify=False)
            actual = resp.headers['location'] \
                if resp.status_code == 302 and 'location' in resp.headers \
                else f"Error: {resp.status_code}"
            if FAIL_ON_ERROR:
                self.assertEqual(expected, actual, f"redirect for: {resp.url}")
                self.record_results(e.input_url, accept_header, actual)
                return True
            elif expected != actual:
                print(f"{e.input_url} ({accept_header}):\n expected {expected} - got {actual}")
                return False
            self.record_results(e.input_url, accept_header, actual)
            return True

        def ev_al(entry: TestEntry) -> bool:
            if not entry.accept_header:
                return test_it(entry, default_header)
            else:
                r1 = test_it(entry, entry.accept_header)
                return test_it(entry, entry.accept_header + ',' + default_header) and r1

        self.assertTrue(all([ev_al(entry) for entry in entries]))

    def test_type_meta(self):
        self.rule_test(self.tests.meta_entries)

    def test_type_entry(self):
        self.rule_test(self.tests.vocab_entries)

    def test_meta_meta(self):
        self.rule_test(self.tests.meta_model_entries)

    def test_meta_entry(self):
        self.rule_test(self.tests.meta_vocab_entries)


if __name__ == '__main__':
    RewriteRuleTestCase.SERVER = os.environ.get('SERVER', RewriteRuleTestCase.SERVER)
    unittest.main()
