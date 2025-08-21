from jsonasobj2 import loads

from linkml.generators.jsonldcontextgen import ContextGenerator

without_default = """
id: http://example.org/sssom/schema/
name: sssom
imports:
- linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  sssom: https://w3id.org/sssom/
  dcterms: http://purl.org/dc/terms/
default_curi_maps:
- semweb_context

slots:
  name:
    range: string
"""

with_default = """
id: http://example.org/sssom/schema/
name: sssom
imports:
- linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  sssom: https://w3id.org/sssom/
  dcterms: http://purl.org/dc/terms/
default_curi_maps:
- semweb_context
default_prefix: sssom

slots:
  name:
    range: string
"""


def test_default_vocab():
    """This test case should (eventually) be used to address some of the questions raised in issue #378.  At the
    moment it just confirms the existing behavior."""
    json_ld_text = ContextGenerator(without_default).serialize()
    json_ld = loads(json_ld_text)
    assert json_ld["@context"]["@vocab"] == "http://example.org/sssom/schema/"
    assert json_ld["@context"]["name"]["@id"] == "name"
    json_ld_text2 = ContextGenerator(with_default).serialize()
    json_ld2 = loads(json_ld_text2)
    assert json_ld2["@context"]["@vocab"] == "https://w3id.org/sssom/"
    assert "name" not in json_ld2["@context"]["@vocab"]
