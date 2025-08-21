import logging
import os
from dataclasses import dataclass
from typing import Optional, Union
from urllib.parse import urljoin

import pytest
import requests
from linkml_runtime.linkml_model.linkml_files import GITHUB_IO_BASE, LINKML_URL_BASE
from rdflib import Namespace, URIRef

from tests import SKIP_REWRITE_RULES, SKIP_REWRITE_RULES_REASON

logger = logging.getLogger(__name__)


# see README.md
W3ID_SERVER = urljoin(LINKML_URL_BASE, "/")
DEFAULT_SERVER = W3ID_SERVER
# DEFAULT_SERVER = "http://localhost:8091/"
# SKIP_REWRITE_RULES = False

# Taken from Firefox network.http.accept.default
default_header = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"


@dataclass
class TestEntry:
    __test__ = False
    input_url: Union[str, URIRef, Namespace]
    expected_url: str
    accept_header: Optional[str] = None


def build_test_entry_set(input_url: Namespace, model: str) -> list[TestEntry]:
    return [
        TestEntry(input_url, f"docs/{model}"),
        TestEntry(input_url, f"linkml_model/model/schema/{model}.yaml", "text/yaml"),
        TestEntry(input_url, f"linkml_model/rdf/{model}.ttl", "text/turtle"),
        TestEntry(input_url, f"linkml_model/json/{model}.json", "application/json"),
        TestEntry(input_url, f"linkml_model/shex/{model}.shex", "text/shex"),
        TestEntry(input_url[".context.jsonld"], f"linkml_model/jsonld/{model}.context.jsonld"),
        TestEntry(input_url[".owl"], f"linkml_model/owl/{model}.owl.ttl"),
        TestEntry(input_url["/"], f"{model}/"),
    ]


def generate_fixture_lists():
    server = os.environ.get("SERVER", DEFAULT_SERVER)
    if not server.endswith(("#", "/")):
        server += "/"
    linkml = server + "linkml/"
    types = Namespace(linkml + "types")
    mappings = Namespace(linkml + "mappings")
    extensions = Namespace(linkml + "extensions")
    annotations = Namespace(linkml + "annotations")
    metas = Namespace(linkml + "meta")
    type_ = Namespace(linkml + "type/")
    mapping = Namespace(linkml + "mapping/")
    meta = Namespace(linkml + "meta/")

    meta_entries: list[TestEntry] = []
    meta_entries += build_test_entry_set(types, "types")
    meta_entries += build_test_entry_set(mappings, "mappings")
    meta_entries += build_test_entry_set(extensions, "extensions")
    meta_entries += build_test_entry_set(annotations, "annotations")

    vocab_entries: list[TestEntry] = [
        TestEntry(type_["index"], "docs/type/index"),
        TestEntry(type_.Element, "linkml_model/model/schema/type/Element.yaml/Element.yaml", "text/yaml"),
        TestEntry(type_.Element, "linkml_model/rdf/type/Element.ttl/Element.ttl", "text/turtle"),
        TestEntry(type_.slots, "linkml_model/json/type/slots.json/slots.json", "application/json"),
        TestEntry(mapping["index"], "docs/mapping/index"),
    ]

    meta_model_entries: list[TestEntry] = [
        TestEntry(metas, "docs/meta"),
        TestEntry(metas, "linkml_model/model/schema/meta.yaml", "text/yaml"),
        TestEntry(metas, "linkml_model/rdf/meta.ttl", "text/turtle"),
        TestEntry(metas, "linkml_model/json/meta.json", "application/json"),
        TestEntry(metas, "linkml_model/shex/meta.shex", "text/shex"),
        TestEntry(metas[".owl"], "linkml_model/owl/meta.owl.ttl"),
        TestEntry(metas[".foo"], "meta.foo"),
        TestEntry(linkml + "context.jsonld", "linkml_model/jsonld/context.jsonld"),
        TestEntry(linkml + "contextn.jsonld", "contextn.jsonld"),
    ]
    meta_vocab_entries: list[TestEntry] = [
        TestEntry(meta.Element, "docs/meta/Element"),
        TestEntry(meta.slot, "docs/meta/slot"),
        TestEntry(meta.Element, "linkml_model/model/schema/meta/Element.yaml/Element.yaml", "text/yaml"),
        TestEntry(meta.Element, "linkml_model/rdf/meta/Element.ttl/Element.ttl", "text/turtle"),
        TestEntry(meta.Element, "linkml_model/json/meta/Element.json/Element.json", "application/json"),
        TestEntry(meta.Element, "linkml_model/shex/meta/Element.shex/Element.shex", "text/shex"),
        TestEntry(meta.Element, "meta/Element", "text/foo"),
    ]

    return {
        "meta_entries": meta_entries,
        "vocab_entries": vocab_entries,
        "meta_model_entries": meta_model_entries,
        "meta_vocab_entries": meta_vocab_entries,
    }


@pytest.fixture
def fail_on_error():
    return os.environ.get("FAIL_ON_ERROR", "False") == "True"


@pytest.fixture(scope="class")
def results() -> set[tuple[str, str, str]]:
    return set()  # from, to, format


def record_results(results, from_url: str, accept_header, to_url: str) -> None:
    results.add((from_url, to_url, accept_header.split(",")[0]))


fixture_lists = generate_fixture_lists()


@pytest.mark.network
@pytest.mark.skipif(SKIP_REWRITE_RULES, reason=SKIP_REWRITE_RULES_REASON)
@pytest.mark.parametrize(
    "entries",
    [
        pytest.param(fixture_lists["meta_entries"], id="meta_entries"),
        pytest.param(fixture_lists["vocab_entries"], id="vocab_entries"),
        pytest.param(fixture_lists["meta_model_entries"], id="meta_model_entries"),
        pytest.param(fixture_lists["meta_vocab_entries"], id="meta_vocab_entries"),
    ],
)
def test_rewrite_rules(entries: list[TestEntry], results, fail_on_error) -> None:
    def test_it(e: TestEntry, accept_header: str) -> bool:
        expected = urljoin(GITHUB_IO_BASE, e.expected_url)
        resp = requests.head(e.input_url, headers={"accept": accept_header}, verify=False)

        # w3id.org uses a 301 to go from http: to https:
        if resp.status_code == 301 and "location" in resp.headers:
            resp = requests.head(
                resp.headers["location"],
                headers={"accept": accept_header},
                verify=False,
            )
        actual = (
            resp.headers["location"]
            if resp.status_code == 302 and "location" in resp.headers
            else f"Error: {resp.status_code}"
        )
        if fail_on_error:
            assert expected == actual, f"redirect for: {resp.url}"
            record_results(results, e.input_url, accept_header, actual)
            return True
        elif expected != actual:
            logger.info(f"{e.input_url} ({accept_header}):\n expected {expected} - got {actual}")
            return False
        record_results(results, e.input_url, accept_header, actual)
        return True

    def ev_al(entry: TestEntry) -> bool:
        if not entry.accept_header:
            return test_it(entry, default_header)
        else:
            r1 = test_it(entry, entry.accept_header)
            return test_it(entry, entry.accept_header + "," + default_header) and r1

    assert all([ev_al(entry) for entry in entries])
