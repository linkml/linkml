import pytest
from rdflib import URIRef
from rdflib.namespace import SKOS

from linkml_runtime.utils.namespaces import Namespaces


def test_namespaces():
    ns = Namespaces()
    ns["meta"] = "https://w3id.org/biolink/metamodel/"
    ns.skos = SKOS
    assert str(ns.skos) == str(SKOS)
    assert ns.skos.note == SKOS.note
    ns.OIO = URIRef("http://www.geneontology.org/formats/oboInOwl")
    ns["dc"] = "http://example.org/dc/"  # Overrides 'dc' in semweb_context
    ns["l1"] = "http://example.org/subset/"
    ns["l2"] = "http://example.org/subset/test/"
    ns["l3"] = "http://example.org/subset/t"
    ns["u1"] = "urn:example:"
    with pytest.raises(ValueError):
        ns["123"] = "http://example.org/foo/"

    with pytest.raises(KeyError) as exc_info:
        ns.FOO
    assert "'foo'" == str(exc_info.value), "Unknown namespace should raise a KeyError with a lower case entry"

    ns._default = ns["meta"]
    ns._default = ns["meta"]
    with pytest.raises(ValueError):
        ns._default = "http://example.org/wrong/"
    del ns._default
    with pytest.raises(KeyError):
        del ns._default
    assert ns._default is None
    ns._default = ns["meta"]

    ns._base = "http://example.org/base/"
    ns._base = "http://example.org/base/"
    with pytest.raises(ValueError):
        ns._base = "http://example.org/wrong/"
    del ns._base
    with pytest.raises(KeyError):
        del ns._base
    ns._base = "http://example.org/wrong/"
    del ns._default
    ns.add_prefixmap("semweb_context")
    ns.add_prefixmap("monarch_context")
    assert "https://monarchinitiative.org/" == str(ns._default)
    del ns._default
    ns._default = ns["meta"]
    assert "l1:foo" == ns.curie_for("http://example.org/subset/foo")
    assert "l2:foo" == ns.curie_for("http://example.org/subset/test/foo")
    assert "l3:able/foo" == ns.curie_for("http://example.org/subset/table/foo")
    assert "u1:foo" == ns.curie_for("urn:example:foo")
    with pytest.raises(ValueError):
        ns.curie_for(r"1abc\junk")
    assert URIRef("http://example.org/dc/table") == ns.uri_for("dc:table")
    assert ns.uri_for("http://something.org") == URIRef("http://something.org")
    assert "https://w3id.org/biolink/metamodel/Schema" == str(ns.uri_for(":Schema"))
    assert URIRef("http://example.org/wrong/Base") == ns.uri_for("Base")
    del ns._base
    with pytest.raises(ValueError, match="no base IRI is registered"):
        ns.uri_for("Base")

    assert ns.curie_for("http://google.com/test") is None
    with pytest.raises(ValueError):
        ns.uri_for("1abc:junk")


def test_uri_for_plain_identifier_without_base():
    """A plain (non-URI, non-CURIE) identifier with no base IRI raises an actionable error.

    The error must name the offending identifier and explain how to register a base, not
    leaking the internal ``@base`` as if it were a CURIE prefix or useful info (its not).
    """
    ns = Namespaces()
    ns["ex"] = "http://example.org/"

    with pytest.raises(ValueError) as exc_info:
        ns.uri_for("CVE-2023-12345")

    message = str(exc_info.value)
    assert "no base IRI is registered" in message
    assert "CVE-2023-12345" in message

    # Must not expose the internal sentinel as if it were a missing CURIE prefix.
    assert "Unknown CURIE prefix" not in message
    assert "@base" in message  # only as part of the remediation hint

    # Once a base is registered the same identifier resolves cleanly.
    ns._base = "http://example.org/base/"
    assert ns.uri_for("CVE-2023-12345") == URIRef("http://example.org/base/CVE-2023-12345")


def test_uri_for_unknown_curie_prefix():
    """A genuine unknown CURIE prefix still raises the CURIE-specific message."""
    ns = Namespaces()
    ns["ex"] = "http://example.org/"

    with pytest.raises(ValueError, match="Unknown CURIE prefix: nope"):
        ns.uri_for("nope:foo")


def test_prefixmaps_integration():
    prefixmap_merged = Namespaces()
    prefixmap_merged.add_prefixmap("merged")
    assert len(prefixmap_merged) > 3780

    prefixmap_merged.add_prefixmap("monarch_context")
    assert len(prefixmap_merged) > 3850

    with pytest.raises(ValueError):
        prefixmap_merged.add_prefixmap("nonexistent_context")

    prefixmap_merged.add_prefixmap("bioregistry")
    assert len(prefixmap_merged) > 3860

    test_NCIT_curie = "NCIT:C25300"
    test_NCIT_uri = URIRef("http://purl.obolibrary.org/obo/NCIT_C25300")
    assert prefixmap_merged.curie_for(test_NCIT_uri) == test_NCIT_curie
    assert prefixmap_merged.uri_for(test_NCIT_curie) == test_NCIT_uri


def test_prefix_suffix():
    ns = Namespaces()
    ns["farm"] = "https://example.org/farm"
    ns["farm_slash"] = "https://slash.org/farm/"

    assert ("farm", "cow") == ns.prefix_suffix("farm:cow")
    assert ("farm", "/cow") == ns.prefix_suffix("https://example.org/farm/cow")
    assert ("farm_slash", "cow") == ns.prefix_suffix("https://slash.org/farm/cow")
    assert ("farm_slash", "cow/horns") == ns.prefix_suffix("farm_slash:cow/horns")
    assert ("farm", "/cow/horns") == ns.prefix_suffix("farm:/cow/horns")
    assert ("farm", "#cow/horns") == ns.prefix_suffix("farm:#cow/horns")
    assert ("farm", "") == ns.prefix_suffix("farm:")
    assert ("", "cow") == ns.prefix_suffix(":cow")
    assert (None, None) == ns.prefix_suffix("https://missing-prefix.org/farm/cow")
