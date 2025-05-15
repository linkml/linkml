import os
import pytest

from jsonasobj2 import JsonObj, loads
from rdflib import URIRef

from linkml_runtime.linkml_model.meta import ClassDefinition, Prefix, SchemaDefinition
from linkml_runtime.utils.context_utils import map_import, merge_contexts
from linkml_runtime.utils.namespaces import Namespaces

from tests.test_utils import METAMODEL_CONTEXT_URI, META_BASE_URI

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


def test_merge_contexts():
    assert merge_contexts() is None
    assert "file://local.jsonld" == merge_contexts("local.jsonld")["@context"]
    assert "file://local.jsonld" == merge_contexts(["local.jsonld"])["@context"]
    assert METAMODEL_CONTEXT_URI == merge_contexts(METAMODEL_CONTEXT_URI)["@context"]
    assert METAMODEL_CONTEXT_URI == merge_contexts([METAMODEL_CONTEXT_URI])["@context"]
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
        f"file://local.jsonld",
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
    assert "file://local.jsonld", merge_contexts("local.jsonld")["@context"]


def test_merge_contexts_base():
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
        ("ex_file", "/tmp/example/schema"),
        ("_types", "https://w3id.org/linkml/types"),
    ],
)
def test_map_import(imp, result):
    importmap = {
        "linkml:": "C:\\temp\\linkml_model\\model\\schema",
        "ex_file": "/tmp/example/schema",
        "_types": "linkml:types",
    }

    def namespaces():
        ns = Namespaces()
        ns["linkml"] = URIRef("https://w3id.org/linkml/")
        ns["ex_file"] = URIRef("https://example.org/file/")
        ns["_types"] = URIRef("https://w3id.org/linkml/types/")
        return ns

    assert map_import(importmap, namespaces, imp) == result
