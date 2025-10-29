"""Tests of the functions from context_utils.py."""

import os

import pytest
from jsonasobj2 import JsonObj, loads
from rdflib import URIRef

from linkml_runtime.utils.context_utils import map_import, merge_contexts, parse_import_map
from linkml_runtime.utils.namespaces import Namespaces
from tests.test_utils import META_BASE_URI, METAMODEL_CONTEXT_URI

json_1 = '{ "ex": "http://example.org/test/", "ex2": "http://example.org/test2/" }'
json_2 = '{ "foo": 17, "@context": { "ex": "http://example.org/test3/", "ex2": {"@id": "http://example.org/test4/" }}}'

context_output = """{
   "@context": [
      "file://local.jsonld",
      "https://w3id.org/linkml/meta.context.jsonld",
      {
         "ex": "http://example.org/test/",
         "ex2": "http://example.org/test2/"
      },
      {
         "ex": "http://example.org/test3/",
         "ex2": {
            "@id": "http://example.org/test4/"
         }
      }
   ]
}"""


def test_merge_contexts() -> None:
    """Test the merge_contexts function."""
    assert merge_contexts() is None
    assert merge_contexts("local.jsonld")["@context"] == "file://local.jsonld"
    assert merge_contexts(["local.jsonld"])["@context"] == "file://local.jsonld"
    assert merge_contexts(METAMODEL_CONTEXT_URI)["@context"] == METAMODEL_CONTEXT_URI
    assert merge_contexts([METAMODEL_CONTEXT_URI])["@context"] == METAMODEL_CONTEXT_URI
    assert JsonObj(ex="http://example.org/test/", ex2="http://example.org/test2/") == merge_contexts(json_1)["@context"]
    assert (
        JsonObj(ex="http://example.org/test/", ex2="http://example.org/test2/") == merge_contexts([json_1])["@context"]
    )
    assert (
        JsonObj(ex="http://example.org/test3/", ex2=JsonObj(**{"@id": "http://example.org/test4/"}))
        == merge_contexts(json_2)["@context"]
    )
    assert (
        JsonObj(ex="http://example.org/test3/", ex2=JsonObj(**{"@id": "http://example.org/test4/"}))
        == merge_contexts([json_2])["@context"]
    )
    assert [
        "file://local.jsonld",
        "https://w3id.org/linkml/meta.context.jsonld",
        JsonObj(ex="http://example.org/test/", ex2="http://example.org/test2/"),
        JsonObj(ex="http://example.org/test3/", ex2=JsonObj(**{"@id": "http://example.org/test4/"})),
    ] == merge_contexts(["local.jsonld", METAMODEL_CONTEXT_URI, json_1, json_2])["@context"]
    assert loads(context_output) == merge_contexts(["local.jsonld", METAMODEL_CONTEXT_URI, json_1, json_2])
    # Dups are not removed
    assert JsonObj(
        **{
            "@context": [
                JsonObj(ex="http://example.org/test/", ex2="http://example.org/test2/"),
                JsonObj(ex="http://example.org/test/", ex2="http://example.org/test2/"),
            ]
        }
    ) == merge_contexts([json_1, json_1])


def test_merge_contexts_base() -> None:
    assert JsonObj(**{"@context": JsonObj(**{"@base": "file://relloc"})}) == merge_contexts(base="file://relloc")
    assert loads(f'{{"@context": {{"@base": "{META_BASE_URI}"}}}}') == merge_contexts(base=META_BASE_URI)
    assert loads("""
{"@context": [
      "https://w3id.org/linkml/meta.context.jsonld",
      {
         "ex": "http://example.org/test/",
         "ex2": "http://example.org/test2/"
      },
      {
         "ex": "http://example.org/test3/",
         "ex2": {
            "@id": "http://example.org/test4/"
         }
      },
      {
         "@base": "https://w3id.org/linkml/"
      }
   ]
}""") == merge_contexts([METAMODEL_CONTEXT_URI, json_1, json_2], base=META_BASE_URI)


@pytest.mark.parametrize(
    ("imp", "result"),
    [
        ("linkml:types", f"C:\\temp\\linkml_model\\model\\schema{os.sep}types"),
        ("ex_file", "/tmp/example/schema"),  # noqa: S108
        ("_types", "https://w3id.org/linkml/types"),
    ],
)
def test_map_import(imp: str, result: str) -> None:
    importmap = {
        "linkml:": "C:\\temp\\linkml_model\\model\\schema",
        "ex_file": "/tmp/example/schema",  # noqa: S108
        "_types": "linkml:types",
    }

    def namespaces() -> Namespaces:
        ns = Namespaces()
        ns["linkml"] = URIRef("https://w3id.org/linkml/")
        ns["ex_file"] = URIRef("https://example.org/file/")
        ns["_types"] = URIRef("https://w3id.org/linkml/types/")
        return ns

    assert map_import(importmap, namespaces, imp) == result


def test_parse_import_map_trailing_sep() -> None:
    """Test the importmap namespace.

    See https://github.com/linkml/linkml-runtime/issues/163.
    """
    importmap = parse_import_map('{ "base:": "base/" }', os.path.dirname(__file__))
    # TODO: see how this works in a windows environment
    assert importmap["base:"].endswith("/")
