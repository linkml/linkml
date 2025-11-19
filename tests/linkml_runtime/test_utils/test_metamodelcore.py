import datetime
from dataclasses import dataclass

import pytest
from jsonasobj2 import as_json
from rdflib import RDF, XSD, Graph, Literal, Namespace

from linkml_runtime.utils.metamodelcore import (
    URI,
    Bool,
    Curie,
    NCName,
    NodeIdentifier,
    URIorCURIE,
    XSDDate,
    XSDDateTime,
    XSDTime,
)
from linkml_runtime.utils.namespaces import Namespaces
from linkml_runtime.utils.strictness import lax, strict
from linkml_runtime.utils.yamlutils import YAMLRoot, as_rdf


@pytest.fixture(autouse=True)
def reset_strictness():
    yield
    strict()


def test_ncname():
    assert "A123" == NCName("A123")
    x = NCName("A1.B_C-")
    assert "A1.B_C-" == x
    assert isinstance(x, str)
    assert isinstance(x, NCName)
    assert x == NCName(x)
    x = str(x)
    assert isinstance(x, str)
    assert not isinstance(x, NCName)
    with pytest.raises(ValueError):
        NCName("1")
    with pytest.raises(ValueError):
        NCName("A12!")


def test_uriorcuries():
    """Test the URI and URIorCURIE types"""
    str1 = "https://google.com/test#file?abc=1&def=4"
    assert str1 == URIorCURIE(str1)
    str2 = "abc:123"
    assert str2 == URIorCURIE(str2)
    str3 = ":123"
    assert str3 == URIorCURIE(str3)
    with pytest.raises(ValueError):
        URIorCURIE("abc:[def]")
    with pytest.raises(ValueError):
        URIorCURIE("1abc:def")
    with pytest.raises(ValueError):
        URIorCURIE("1:def")
    with pytest.raises(ValueError):
        URIorCURIE(" ")
    with pytest.raises(ValueError):
        URIorCURIE("[")
    assert URIorCURIE.is_valid("NCIT:C176962")
    lax()
    URIorCURIE("1abc:def")
    URIorCURIE("1:def")
    assert not URIorCURIE.is_valid(123)
    URIorCURIE.is_curie("abc:123")
    assert not URIorCURIE.is_curie("http://example.org/path")


def test_curie():
    """Test the CURIE type"""
    assert "rdf:type" == Curie("rdf:type")
    with pytest.raises(ValueError):
        Curie("type")
    assert not Curie.is_valid("type")
    assert ":type" == Curie(":type")
    assert Curie.is_valid(":type")
    assert Curie.is_valid("WIKIDATA_PROPERTY:P854")
    assert Curie.is_valid("WIKIDATA.PROPERTY:P854")
    assert Curie.is_valid("CL:0000001")
    with pytest.raises(ValueError):
        Curie("1df:type")
    assert not Curie.is_valid("1df:type")
    assert Curie.is_valid("rdf:17")
    nsm = Namespaces(Graph())
    assert RDF.type == Curie("rdf:type").as_uri(nsm)
    assert Curie("ex:foo").as_uri(nsm) is None
    assert Curie(":bar").as_uri(nsm) is None
    nsm._default = "http://example.org/test#"
    assert nsm._default["bear"] == Curie(":bear").as_uri(nsm)


def test_uri():
    """Test the URI data type"""
    str1 = "https://google.com/test#file?abc=1&def=4"
    assert str1 == URI(str1)
    assert "http://foo.org/bargles" == URI("http://foo.org/bargles")
    with pytest.raises(ValueError):
        URI(":")
    with pytest.raises(ValueError):
        URI(":123")
    # imports range is uriorcurie, so we allow file paths
    # URI("1")
    assert URI.is_valid("foo.bar")
    assert URI.is_valid("../a/b")
    assert URI.is_valid("abc:123")
    # with pytest.raises(ValueError):
    #    URI("x1")
    # an empty URI is a valid same-document URI reference
    assert URI.is_valid("")
    x = URI("rdf:type")
    assert URI.is_valid(x)
    assert URI.is_valid("urn:abc:123")
    assert URI.is_valid("https://john.doe@www.example.com:123/forum/questions/?tag=networking&order=newest#top")
    assert URI.is_valid("ldap://[2001:db8::7]/c=GB?objectClass?one")
    assert URI.is_valid("ldap://[2001:db8::7]/c=GB?objectClass?one")
    assert URI.is_valid("mailto:John.Doe@example.com")
    assert URI.is_valid("news:comp.infosystems.www.servers.unix")
    assert URI.is_valid("tel:+1-816-555-1212")
    assert URI.is_valid("telnet://192.0.2.16:80/")
    assert URI.is_valid("urn:oasis:names:specification:docbook:dtd:xml:4.1.2")
    assert URI.is_valid("file:///home/user/")


def test_bool():
    assert Bool(True)
    assert Bool("True")
    assert Bool("true")
    assert Bool(1)
    assert Bool("1")
    assert Bool(Bool(True))
    assert not Bool(False)
    assert not Bool("False")
    assert not Bool("false")
    assert not Bool(0)
    assert not Bool("0")
    assert not Bool(Bool(0))
    # Strict mode
    with pytest.raises(ValueError):
        x = Bool(17)
    with pytest.raises(ValueError):
        x = Bool("a")
    lax()
    x = Bool(17)
    assert not Bool.is_valid(17)
    x = Bool("a")
    assert not Bool.is_valid("a")
    assert Bool.is_valid(True)
    assert Bool.is_valid(Bool(True))


def test_time():
    v = datetime.time(13, 17, 43, 279000)
    assert "13:17:43.279000" == XSDTime(v)  # A date can be a datetime
    assert "13:17:43.279000" == XSDTime(Literal(v, datatype=XSD.time))  # An RDFLIB Literal
    assert "13:17:43.279000" == v.isoformat()  # A string
    assert "13:17:43.279000" == XSDTime(XSDTime(v))  # An existing date
    strict()
    with pytest.raises(ValueError):
        XSDTime("Jan 12, 2019")
    with pytest.raises(ValueError):
        XSDTime(datetime.datetime.now())
    lax()
    assert "Jan 12, 2019" == XSDTime("Jan 12, 2019")
    XSDDate(datetime.datetime.now())
    assert not XSDTime.is_valid("Jan 12, 2019")
    assert not XSDTime.is_valid(datetime.datetime.now())
    assert not XSDTime.is_valid("2019-07-06T17:22:39Z")
    assert XSDTime.is_valid(v)


def test_date():
    v = datetime.date(2019, 7, 6)
    assert "2019-07-06" == XSDDate(v)  # A date can be a datetime
    assert "2019-07-06" == XSDDate(Literal(v, datatype=XSD.date))  # An RDFLIB Literal
    assert "2019-07-06" == v.isoformat()  # A string
    assert "2019-07-06" == XSDDate(XSDDate(v))  # An existing date
    strict()
    with pytest.raises(ValueError):
        XSDDate("20190706")
    with pytest.raises(ValueError):
        XSDDate("Jan 12, 2019")
    with pytest.raises(ValueError):
        XSDDate(datetime.datetime.now())
    with pytest.raises(ValueError):
        XSDDate("2019-07-06T17:22:39Z")

    lax()
    bv = XSDDate("Jan 12, 2019")
    assert "Jan 12, 2019" == bv
    assert not XSDDate.is_valid(bv)
    XSDDate(datetime.datetime.now())
    assert not XSDDate.is_valid("Jan 12, 2019")
    assert not XSDDate.is_valid(datetime.datetime.now())
    assert XSDDate.is_valid(XSDDate(datetime.datetime.now().date()))
    assert XSDDate.is_valid(v)


def test_datetime():
    v = datetime.datetime(2019, 7, 6, 17, 22, 39, 7300)
    assert "2019-07-06T17:22:39.007300" == XSDDateTime(v)
    assert "2019-07-06T17:22:39.007300" == XSDDateTime(Literal(v, datatype=XSD.dateTime))
    assert "2019-07-06T17:22:39.007300" == XSDDateTime(Literal(v).value)
    assert "2019-07-06T17:22:39.007300" == v.isoformat()
    assert "2019-07-06T17:22:39.007300" == XSDDateTime(XSDDateTime(v))
    vstr = str(Literal(v).value)
    assert "2019-07-06 17:22:39.007300" == vstr  # Note that this has no 'T'
    assert "2019-07-06T17:22:39.007300" == XSDDateTime(vstr)
    assert "2019-07-06T17:22:39+00:00" == XSDDateTime("2019-07-06T17:22:39Z")
    assert "2019-07-06T00:00:00" == XSDDateTime("2019-07-06")  # Date as datetime
    with pytest.raises(ValueError):
        XSDDateTime("Jan 12, 2019")

    lax()
    assert "penguins" == XSDDateTime("penguins")
    XSDDateTime(datetime.datetime.now())
    assert not XSDDateTime.is_valid("Jan 12, 2019")
    assert XSDDateTime.is_valid(datetime.datetime.now())
    assert XSDDateTime.is_valid(XSDDate(datetime.datetime.now().date()))
    assert XSDDateTime.is_valid(v)


@pytest.mark.skip(reason="Finish implementing this")
def test_nodeidentifier():
    context = """{
        "@context": {
            "type": "@type",
            "OIO": "http://www.geneontology.org/formats/oboInOwl#",
            "dcterms": "http://purl.org/dc/terms/",
            "metatype": "https://w3id.org/linkml/type/",
            "owl": "http://www.w3.org/2002/07/owl#",
            "pav": "http://purl.org/pav/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "skos": "http://www.w3.org/2004/02/skos/core#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "s": {
                "@id": "rdfs:subject"
            },
            "t": {
                "@id": "rdfs:object"
            }
        }
    }"""
    EX = Namespace("http://example.org/tests/")

    class Root(NodeIdentifier):
        pass

    class Child1(Root):
        pass

    class Child2(Root):
        pass

    class Desc1(Child1):
        pass

    class Unassoc(NodeIdentifier):
        pass

    @dataclass
    class Pair(YAMLRoot):
        s: Child1 = None
        t: Child2 = None

        def __post_init__(self):
            if not isinstance(self.s, Child1):
                self.s = Child1(self.s)
            if not isinstance(self.t, Child2):
                self.t = Child2(self.t)
                super().__post_init__()

    s = Desc1(EX.descendant1)
    t = Child2(EX.child2)
    y = Pair(s, t)
    assert """{
   "s": "http://example.org/tests/descendant1",
   "t": "http://example.org/tests/child2"
}""" == as_json(y)
    assert """@prefix OIO: <http://www.geneontology.org/formats/oboInOwl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix metatype: <https://w3id.org/linkml/type/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix pav: <http://purl.org/pav/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] a <linkml/tests/Pair> ;
    rdfs:object "http://example.org/tests/child2" ;
    rdfs:subject "http://example.org/tests/descendant1" .

""" == as_rdf(y, context).serialize(format="turtle")
    with pytest.raises(ValueError):
        y = Pair(s, s)


def test_issue_1355_invalid_url_message() -> None:
    """Check that quotes are used when referencing invalid urls to improve troubleshooting UX.

    See https://github.com/linkml/linkml/issues/1355, improve invalid URL message
    """
    #  note the trailing blank
    url = "https://ceur-ws.org/Vol-2931/ICBO_2019_paper_20.pdf "
    with pytest.raises(
        ValueError,
        match="'https://ceur-ws.org/Vol-2931/ICBO_2019_paper_20.pdf ': is not a valid URI",
    ):
        URI(url)
